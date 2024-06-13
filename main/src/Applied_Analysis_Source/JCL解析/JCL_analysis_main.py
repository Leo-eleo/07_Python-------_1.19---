#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import sys

from analysis1_2_read_text_JCL import analysis1_2_read_text_JCL
from analysis1_3_lexical_JCL import analysis1_3_lexical_JCL
from analysis1_4_rebuild_Token_JCL import analysis1_4_rebuild_Token_JCL
from analysis1_5_structure_JCL import analysis1_5_structure_JCL

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

def main(db_path, Folder_JCL_path, JCL_setting_path):

    print("start preparation for analysis.")

    condition_df = pd.read_excel(JCL_setting_path,sheet_name="資産解析")
    for cond,val in zip(condition_df["項目"],condition_df["設定"]):
        if cond == "設定条件HIT関連情報出力（ｷｰID）":
            設定条件HIT情報出力 = val == "出力する"
            
        if cond == "設定条件HIT関連情報出力（分析ID）":
            分析条件HIT情報出力 = val == "出力する"
            
        if cond == "設定条件HIT関連情報出力（設計ID）":
            設計条件HIT情報出力 = val == "出力する"
            
        if cond == "設定条件HIT-NG情報出力":
            設定条件HIT_NG情報出力 = val == "出力する"
            
        if cond == "DB更新制御":
            IsDelete = val == "実行前に関連TABLEクリアする"
            
        if cond == "PROC解析対象制御":
            IsPROCLimit = val == "JCLからの呼出があるPROCのみ解析する"
            
        if cond == "A-AUTO世代情報管理":
            a_auto = val
            
        
        if cond == "結果出力フォルダ1":
            言語解析_path = val
            
        if cond == "結果出力フォルダ1":
            字句解析_path = val
        
        if cond == "結果出力フォルダ1":
            トークン解析_path = val
            
        if cond == "結果ファイル出力制御（ソースコード）":
            言語解析_out = val == "出力する"
            
        if cond == "結果ファイル出力制御（字句解析用）":
            字句解析_out = val == "出力する"
            
        if cond == "結果ファイル出力制御（ﾄｰｸﾝ再構成用）":
            トークン解析_out = val == "出力する"
            
            
    JCLSheet = pd.read_excel(JCL_setting_path,sheet_name="JCL設定シート")
    JCLSheet.fillna("",inplace=True)
    JCLSheet = JCLSheet.values.tolist()
    JCLSheet = [[""]+sheet for sheet in JCLSheet]
    JCLtoPROCSheet = pd.read_excel(JCL_setting_path,sheet_name="JCL呼出ありカタプロ一覧")
    JCLtoPROCSheet = JCLtoPROCSheet["カタプロ名"]
    JCLtoPROCset = set(JCLtoPROCSheet.values.tolist())
    JCL_Files = glob_files(Folder_JCL_path)

    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    if IsDelete:
        print("you chose to clear db, so clear the remaining data.")
        
        sql = "DELETE FROM ①JCL_基本情報"
        cursor.execute(sql)
        sql = "DELETE FROM ①JCL_STEP_SYSIN"
        cursor.execute(sql)
        sql = "DELETE FROM ①JCL_STEP情報"
        cursor.execute(sql)
        sql = "DELETE FROM ①JCL_PGM_DSN"
        cursor.execute(sql)
        sql = "DELETE FROM ①JCL_CMD情報"
        cursor.execute(sql)
        sql = "DELETE FROM ①PROC_PARM"
        cursor.execute(sql)
        # 'HIT時関連情報削除
        sql = "DELETE FROM 共通_資産解析_関連情報"
        cursor.execute(sql)
        # 'HIT-NG時関連情報削除
        sql = "DELETE FROM 共通_資産解析_NG情報"
        cursor.execute(sql)
        conn.commit()
  
    
    print("finish preparation and start analysis.")
    ld = len(JCL_Files)
    for i,JCL_File in enumerate(JCL_Files):
        ファイル名 = get_filename(JCL_File)
        ファイル名2 = take_extensions(ファイル名)
        print("\r","analysis finished",i,"/",ld,ファイル名,end="")
        
        if IsPROCLimit and ファイル名2 not in JCLtoPROCset:
            print(ファイル名2+"はJCLからの呼出がないため解析をスキップします。")
            continue

        TmpSheet = analysis1_2_read_text_JCL(JCL_File,a_auto)
        
        if 言語解析_out == True:
            ActSheet_all,output_header = make_output_list_val_length(TmpSheet,["行情報","NAME","CMD","PARM","COMMENT","PARM継続","継続","制御情報","元資産行番号","元資産行情報","A-AUTO世代情報"])
   
            # output_header = ["行情報","NAME","CMD","PARM","COMMENT","PARM継続","継続","制御情報","元資産行番号","元資産行情報","A-AUTO世代情報"]
            write_excel_multi_sheet("言語解析結果_"+ファイル名2.replace("%","_") + ".xlsx",ActSheet_all,"言語解析",言語解析_path,output_header)
        

        TokenSheet = analysis1_3_lexical_JCL(TmpSheet)
        
        if 字句解析_out == True:
            ActSheet_all,output_header = make_output_list_val_length(TokenSheet,["元資産行","ID行","NAME行","CMD行","P制御","AAUTO世代","PARM行"])
            
            # output_header = ["元資産行","ID行","NAME行","CMD行","P制御","AAUTO世代","PARM行"]
            write_excel_multi_sheet("字句解析結果_"+ファイル名2.replace("%","_") + ".xlsx",ActSheet_all,"字句解析",字句解析_path,output_header)
     
        TokenSheet2 = analysis1_4_rebuild_Token_JCL(TokenSheet)

        if トークン解析_out == True:
            ActSheet_all,output_header = make_output_list_val_length(TokenSheet2,["元資産行番号","行分類","AAUTO世代","NAME","CMD","PARM"])
     
            # output_header = ["元資産行番号","行分類","AAUTO世代","NAME","CMD","PARM"]
            write_excel_multi_sheet("トークン解析結果_"+ファイル名2.replace("%","_") + ".xlsx",ActSheet_all,"トークン解析",トークン解析_path,output_header)
            
        
        analysis1_5_structure_JCL(TokenSheet2,JCLSheet,ファイル名,conn,cursor, 設定条件HIT情報出力,分析条件HIT情報出力,設計条件HIT情報出力,設定条件HIT_NG情報出力)

    conn.close()
    
if __name__ == "__main__":     
    main(sys.argv[1],sys.argv[2],sys.argv[3])