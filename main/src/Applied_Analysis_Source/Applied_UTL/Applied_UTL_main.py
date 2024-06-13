#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import sys

sys.path.append(os.path.dirname(__file__))
import time

from analysis1_UTL_analysis import analysis1_UTL_analysis
from analysis2_DFSRRC00 import analysis2_DFSRRC00
from analysis4_EASY_analysis import analysis4_EASY_analysis
from analysis5_JCL_PGM_SYSIN_SEPARATE import analysis5_JCL_PGM_SYSIN_SEPARATE

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


DB自動登録時PARM = "自動設定（UTL解析）"
def main(db_path,title):
    
    start = time.time()
    if os.path.isdir(title) == False:
        os.makedirs(title)
    
    ### 既存DB削除
    
    
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    
    
    # sql,values = make_delete_sql("顧客別_資産関連性情報",[DB自動登録時PARM],["登録分類"])
    # cursor.execute(sql,values)
    
    #sql = "SELECT * FROM 顧客別_資産関連性情報 WHERE 登録分類 = '自動設定（UTL解析）'"
    #df = pd.read_sql(sql,conn)
    #keys = df.columns.tolist()
    #for i in range(len(df)):
    #    data = df.iloc[i]
    #    values = [data[key] for key in keys]
    #    
    #    sql,values = make_delete_sql("顧客別_資産関連性情報",values,keys)
    #    cursor.execute(sql,values)
 
    # sql,values = make_delete_sql("顧客別_JCL_PGM_DSN",["",DB自動登録時PARM],["手動更新FLG","自動更新FLG"])
    # cursor.execute(sql,values)

    sql = "SELECT * FROM 顧客別_JCL_PGM_DSN WHERE 手動更新FLG = '' AND 自動更新FLG = '自動設定（UTL解析）'"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("顧客別_JCL_PGM_DSN",values,keys)
        cursor.execute(sql,values)
    
    # sql,values = make_delete_sql("UTL_STEP別_IO情報",[DB自動登録時PARM],["補足"])
    # cursor.execute(sql,values)
    
    sql = "SELECT * FROM UTL_STEP別_IO情報 WHERE 補足 = '自動設定（UTL解析）'"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("UTL_STEP別_IO情報",values,keys)
        cursor.execute(sql,values)
        
    print("DB削除完了", time.time()-start)
    
    ActSheet_all = []
 
    ActSheet,conn,cursor = analysis1_UTL_analysis(db_path,conn,cursor)
    ActSheet_all += ActSheet
    
    print("解析1完了", time.time()-start)
    ActSheet_all += analysis2_DFSRRC00(conn,cursor)
    print("解析2完了", time.time()-start)
    
    ActSheet_all += analysis4_EASY_analysis(conn,cursor)
    print("解析4完了", time.time()-start)
    analysis5_JCL_PGM_SYSIN_SEPARATE(conn,cursor)
    print("解析5完了", time.time()-start)
    ActSheet_all = [ActSheet[1:] for ActSheet in ActSheet_all]
    print(len(ActSheet_all))
    output_header = ["LIBRARY_ID","JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP_ID","PGM_NAME","PROC_NAME","SYSIN_PGM","SYSIN_SEQ","SYSIN","解析時メッセージ","資産関連性","DSN追加","DSN更新","STEP_IO追加/更新","関連キー情報","","STEP_SYSIN更新"]
    write_excel_multi_sheet("応用UTL.xlsx",ActSheet_all,"応用_UTL解析",title,output_header)
    
    
if __name__ == "__main__":
    # Debug
    # db_path = (
    #     r"C:\WORK\tmp\日産案件\レイアウト解析用\言語解析DB_202310受領資産_テストIO出力用.accdb"
    # )
    # title = r"C:\WORK\tmp\日産案件\レイアウト解析用"
    # main(db_path,title)
    # Release
    main(sys.argv[1],sys.argv[2])