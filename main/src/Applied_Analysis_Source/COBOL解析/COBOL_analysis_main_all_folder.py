#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

import subprocess

from analysis1_2_read_text_COBOL import analysis1_2_read_text_COBOL
from analysis1_3_lexical_COBOL import analysis1_3_lexical_COBOL
from analysis1_4_rebuild_Token_COBOL import analysis1_4_rebuild_Token_COBOL
from analysis1_5_structure_COBOL import analysis1_5_structure_COBOL
from COBOL_IO_Info import COBOL_IO_Info
from common_Regular_Expression import setting_re_pattern_sheet

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


def main_all_folder(db_base_path, Folder_COBOL_path, COBOL_setting_path,title):
    
    
    print("start preparation for analysis.")
    
    condition_df = pd.read_excel(COBOL_setting_path,sheet_name="資産解析")
    for cond,val in zip(condition_df["項目"],condition_df["設定"]):
        if cond == "設定条件HIT関連情報出力（ｷｰID）":
            設定条件HIT情報出力 = val == "出力する"
            
        if cond == "設定条件HIT関連情報出力（分析ID）":
            分析条件HIT情報出力 = val == "出力する"
            
        if cond == "設定条件HIT関連情報出力（設計ID）":
            設計条件HIT情報出力 = val == "出力する"
            
        if cond == "設定条件HIT-NG情報出力":
            設定条件HIT_NG情報出力 = val == "出力する"
            
        if cond == "COBOL入出力関連情報出力":
            COBOL入出力情報出力 = val == "出力する"
            
        if cond == "DB更新制御":
            IsDelete = val == "実行前に関連TABLEクリアする"
            
            
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
            
            
    if os.path.isdir(title) == False:
        os.makedirs(title)

    COBOLSheet = pd.read_excel(COBOL_setting_path,sheet_name="COBOL設定シート")
    COBOLSheet.fillna("",inplace=True)
    COBOLSheet = COBOLSheet.values.tolist()
    COBOLSheet = [[""]+sheet for sheet in COBOLSheet]
    COBOLSheet = setting_re_pattern_sheet(COBOLSheet)
    

    ### 実行前にDBを削除するを選択した場合に削除する
    if IsDelete == True:
        print("you chose to clear db, so clear the remaining data.")
        
        conn = connect_accdb(db_base_path)

        cursor = conn.cursor()
        
        sql = "DELETE FROM ②COBOL_入出力情報1"
        cursor.execute(sql)
        sql = "DELETE FROM ②COBOL_入出力情報2"
        cursor.execute(sql)
        sql = "DELETE FROM ②COBOL_入出力情報3"
        cursor.execute(sql)
        sql = "DELETE FROM ②COBOL_関連資産"
        cursor.execute(sql)
        sql = "DELETE FROM ②COBOL_CMD情報"
        cursor.execute(sql)
        sql = "DELETE FROM ②COBOL_基本情報"
        cursor.execute(sql)
        sql = "DELETE FROM 共通_PGM_IO情報"
        cursor.execute(sql)

        # 'HIT時関連情報削除
        sql = "DELETE FROM 共通_資産解析_関連情報"
        cursor.execute(sql)
        # 'HIT-NG時関連情報削除
        sql = "DELETE FROM 共通_資産解析_NG情報"
        cursor.execute(sql)
        conn.commit()
        conn.close()

    
    print("finish preparation and start analysis.")
    COBOL_Folders = glob_files(Folder_COBOL_path,recursive=False,type="folder")
    COBOL_Folders.append(Folder_COBOL_path)
    # COBOL_Files = glob_files(Folder_COBOL_path)
    
    for COBOL_Folder in COBOL_Folders:
        if COBOL_Folder == Folder_COBOL_path:
            COBOL_Files = glob_files(COBOL_Folder,recursive=False,type="file")
            
            if len(COBOL_Files) == 0:
                continue
            
            
        Folder_name = os.path.split(COBOL_Folder)[-1]
        
        file_num = 1
        print("start analysis the folder of ",Folder_name)
        
        
        db_path = title+"\\言語解析DB_"+Folder_name + "_" + str(file_num)+".accdb"
        command = "copy "+db_base_path + " " + db_path
        subprocess.call(command,shell=True)
        print("create the new accdb file ",db_path)
        
        if COBOL_Folder != Folder_COBOL_path:
            COBOL_Files = glob_files(COBOL_Folder)
        else:
            COBOL_Files = glob_files(COBOL_Folder,recursive=False,type="file")
        
        
        ld = len(COBOL_Files)
        conn = connect_accdb(db_path)
        cursor =conn.cursor()
    
        for i,COBOL_File in enumerate(COBOL_Files):
            
            if os.path.getsize(db_path) >= 1500000000:
                conn.close()
                
                file_num += 1
                db_path = title+"\\言語解析DB_"+Folder_name+str(file_num)+".accdb"
                command = "copy "+db_base_path + " " + db_path
                subprocess.call(command,shell=True)
                print("create the new accdb file ",db_path)
                
                conn = connect_accdb(db_path)
                cursor =conn.cursor()
                
                
            ファイル名 = get_filename(COBOL_File)
            ファイル名2 = take_extensions(ファイル名)
            print("\r","analysis finished",i,"/",ld,ファイル名,end="")
        
            
            
            TmpSheet = analysis1_2_read_text_COBOL(COBOL_File)

            if 言語解析_out == True:
                ActSheet_all,output_header = make_output_list_val_length(TmpSheet,["行情報","標識","領域Aあり","領域Bのみ","ｼｰｹﾝｽ域","73-80","元資産行番号","元資産行情報"])

                # output_header = ["行情報","標識","領域Aあり","領域Bのみ","ｼｰｹﾝｽ域","73-80","元資産行番号","元資産行情報"]
                write_excel_multi_sheet("言語解析結果_"+ファイル名2.replace("%","_") + ".xlsx",ActSheet_all,"言語解析",言語解析_path,output_header)
        
        
            
            TokenSheet = analysis1_3_lexical_COBOL(TmpSheet)

            if 字句解析_out == True:
                ActSheet_all,output_header = make_output_list_val_length(TokenSheet,["行番号情報","行情報","記述領域","階層情報","TOKEN情報"])
 
                # output_header = ["行番号情報","行情報","記述領域","階層情報","TOKEN情報"]
                write_excel_multi_sheet("字句解析結果_"+ファイル名2.replace("%","_") + ".xlsx",ActSheet_all,"字句解析",字句解析_path,output_header)
     

            TokenSheet2 = analysis1_4_rebuild_Token_COBOL(TokenSheet)

            if トークン解析_out == True:
                ActSheet_all,output_header = make_output_list_val_length(TokenSheet2,["行番号情報","行情報","記述領域","階層情報","制御情報"])
 
                # output_header = ["行番号情報","行情報","記述領域","階層情報","制御情報"]
                write_excel_multi_sheet("トークン解析結果_"+ファイル名2.replace("%","_") + ".xlsx",ActSheet_all,"トークン解析",トークン解析_path,output_header)
            
     
            analysis1_5_structure_COBOL(TokenSheet2,COBOLSheet,ファイル名,db_path, 設定条件HIT情報出力,分析条件HIT情報出力,設計条件HIT情報出力,設定条件HIT_NG情報出力,conn,cursor)
            
            
            if COBOL入出力情報出力:
                COBOL_IO_Info(TokenSheet2,ファイル名,db_path,conn,cursor)
        conn.close()
if __name__ == "__main__":     

    main_all_folder(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])