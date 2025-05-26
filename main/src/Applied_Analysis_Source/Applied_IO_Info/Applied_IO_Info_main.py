#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
sys.path.append(os.path.dirname(__file__))
import time
from analysis0 import analysis0
from analysis1 import analysis1
from analysis3 import analysis3
from analysis4 import analysis4

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

def main(db_path,title):
    
    start = time.time()

    if os.path.isdir(title) == False:
        os.makedirs(title)
        
        
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    output_header = analysis0()[1:]
    
#'20250202 UPD qian.e.wang 長野県信テストIO出力対応
    # TEST_テスト実施単位テーブルからデータを取得
    sql = "SELECT * FROM TEST_テスト実施単位"
    df_test_units = pd.read_sql(sql, conn)
    df_test_units.fillna("", inplace=True)
    
    # 最初に空リストとして宣言
    ActSheet_testid = []
    ActSheet_all = []
    # 分割処理用変数宣言
    i = 1
    chunk_size = 500000  # 適切なチャンクサイズに調整してください[EXCEL最大値1000000]
    
    # TEST_IDごとに処理を実行
    for test_id in df_test_units["TEST_ID"].unique():
        print(f"Processing TEST_ID: {test_id}")
        
        # 実行JOBのリストを抽出
        job_list = df_test_units[df_test_units["TEST_ID"] == test_id]["実行JOB"].tolist()
        
        # analysis1のレコード抽出処理にWHERE条件を追加
        # ActSheet_all = analysis1(conn,cursor)
        ActSheet_testid = analysis1(conn, cursor, test_id, job_list)
        
        # デバッグ用：各ステップ後のサイズ確認
        # print("Initial data size:", len(ActSheet_all))
        print("Initial data size:", len(ActSheet_testid))
        
        # 重複排除処理
        unique_ActSheet = [list(t) for t in set(tuple(item) for item in ActSheet_testid)]
        
        # ソート処理
        # ActSheet_all.sort(key=lambda x: (x[1],x[2],x[5],x[7],x[8],x[22]))
        unique_ActSheet.sort(key=lambda x: (x[1], x[2], x[5], x[7], x[8], x[22]))
        
        print(f"Unique  data size: {len(unique_ActSheet)}")
        print(test_id, "解析1完了", time.time()-start)
        
        ### 応用_入出力情報出力_2
        # ActSheet_all = analysis3(ActSheet_all,conn,cursor)
        unique_ActSheet = analysis3(unique_ActSheet,conn,cursor)
        print(test_id, "解析3完了", time.time()-start)
        
        ### TEST_入出力情報テーブルへ反映
        # analysis4(ActSheet_all,conn,cursor)
        # 一時的に入出力情報DB出力を抑止
        # analysis4(unique_ActSheet,conn,cursor)
        # print(test_id, "解析4完了", time.time()-start)
        
        # unique_ActSheet を ActSheet_all に追加
        ActSheet_all.extend(unique_ActSheet)
        
        # ActSheet_testid を初期化
        ActSheet_testid = []
        
        # デバッグ用：各チャンクごとの件数確認
        print(f"Chunk {i}: Number of Records: {len(ActSheet_all)}")
        if len(ActSheet_all) >= chunk_size:
            # デバッグ用：各チャンクごとのカラム数確認
            print(f"Chunk {i}: Number of columns in ActSheet_all: {len(ActSheet_all[0])}")
            print(f"Chunk {i}: Number of columns in output_header: {len(output_header)}")
                
            df_chunk = pd.DataFrame(ActSheet_all, columns=output_header)
            # チャンクごとの出力ファイル名を生成
            output_file = os.path.join(title, f"応用入出力解析_{i}.xlsx")
            
            # ファイルが既に存在すれば削除
            if os.path.exists(output_file):
                os.remove(output_file)
            
            # Excelファイルへの書き込み
            with pd.ExcelWriter(output_file, mode='w', engine='openpyxl') as writer:
                df_chunk.to_excel(writer, sheet_name=f'応用入出力', index=False)
            
            ActSheet_all = []  # 空リストに初期化
            df_chunk = None  # df_chunk を初期化
            i += 1
    
    # デバッグ用：最終チャンクの件数確認
    print(f"Chunk {i}: Number of Records: {len(ActSheet_all)}")
    if len(ActSheet_all) > 0:
        # デバッグ用：最終チャンクのカラム数確認
        print(f"Chunk {i}: Number of columns in ActSheet_all: {len(ActSheet_all[0])}")
        print(f"Chunk {i}: Number of columns in output_header: {len(output_header)}")
        
        df_chunk = pd.DataFrame(ActSheet_all, columns=output_header)
        # チャンクごとの出力ファイル名を生成
        output_file = os.path.join(title, f"応用入出力解析_{i}.xlsx")
        
        # ファイルが既に存在すれば削除
        if os.path.exists(output_file):
            os.remove(output_file)
        
        # Excelファイルへの書き込み
        with pd.ExcelWriter(output_file, mode='w', engine='openpyxl') as writer:
            df_chunk.to_excel(writer, sheet_name=f'応用入出力', index=False)
        
        df_chunk = None  # df_chunk を初期化
    
    print("Data processing completed")
# UPD END
    
    conn.close()
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])