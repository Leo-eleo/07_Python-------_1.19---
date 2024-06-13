#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


def output_by_process(out_list,process,output_name,output_keys,update_keys,update_values,output_conn,output_cursor):
    
    if process == "追加":
        sql,value = make_insert_sql(output_name,out_list,output_keys)
    elif process == "更新":
        sql,value = make_update_sql(output_name,out_list,output_keys,update_values,update_keys)
    elif process == "削除":
        sql,value = make_delete_sql(output_name,out_list,output_keys)
        
    else:
        print("処理区分に 追加,更新,削除 以外が指定されています。追加として処理を続行します。")
        sql,value = make_insert_sql(output_name,out_list,output_keys)
    output_cursor.execute(sql,value)
    output_conn.commit()
    
    return 
    
    
def main(input_path, output_path, setting_path,IsDelete):
    

    print("start preparation for analysis.")

    if type(IsDelete) != bool:
        IsDelete = IsDelete == "True"
        
    title,output_file_name = os.path.split(output_path)
    # ### create folder to save excel data
    if os.path.isdir(title) == False:
        os.makedirs(title)
    # ######################
    
    if str(input_path).endswith("accdb"):
        input_format = "accdb"
    else:
        input_format = "excel"
    
    if str(output_path).endswith("accdb"):
        output_format = "accdb"
    else:
        output_format = "excel"
    
    ### setup and check setting information
    setting_sheet = pd.read_excel(setting_path,sheet_name="解析結果整理")
    setting_sheet.fillna("", inplace=True)
    input_name = ""
    output_name = ""
    for in_name,out_name in zip(setting_sheet["入力側テーブル・シート名 ※必須項目"],setting_sheet["出力側テーブル・シート名 ※必須項目"]):
        if in_name != "":
            if input_name == "":
                input_name = in_name
            else:
                print("Error: 入力側テーブル・シート名は１つのみ設定して下さい")
                exit()
                
        if out_name != "":
            if output_name == "":
                output_name = out_name
            else:
                print("Error: 出力側テーブル・シート名は１つのみ設定して下さい")
                exit()
    
    input_keys = []
    output_keys = []
    for in_key,out_key in zip(setting_sheet["入力側キー"],setting_sheet["出力側キー"]):
        if in_key == "" and out_key == "":
            continue
        
        if in_key != "" and out_key != "":
            input_keys.append(in_key)
            output_keys.append(out_key)
            
        else:
            print("Error: 入力側・出力側のキーは1対1で対応させて下さい")
            exit()
            
    update_keys = []
    if input_format == "excel":
        for upd_key in setting_sheet["更新用キー"]:
            if upd_key != "":
                update_keys.append(upd_key)
    
    ######################
                
    ### setup and check input data
    if input_format == "excel":
        input_df = pd.read_excel(input_path,sheet_name=input_name)
        input_df.fillna("",inplace=True)
        
    elif input_format == "accdb":
        input_conn = connect_accdb(input_path)
        input_cursor = input_conn.cursor()
        
        input_sheet_list = [row[2] for row in input_cursor.tables()]

        if input_name not in input_sheet_list:
            print("Error: 入力側テーブル・シート名が存在しません")
            exit()
     
            
        sql = "SELECT * FROM " + input_name
        input_df = pd.read_sql(sql,input_conn)
        input_df.fillna("",inplace=True)
    
    input_df_columns = input_df.columns.tolist()
    
    for key in input_keys:
        if key not in input_df_columns:
            print("Error: 入力側キー",key,"が入力側のデータに存在しません")
            exit()
            
    for key in update_keys:
        if key not in input_df_columns:
            print("Error: 更新用キー",key,"が入力側のデータに存在しません")
            exit()
    ####################
    
    ### setup and check output data
    if output_format == "excel":
        output_df = []
        
    elif output_format == "accdb":
        output_conn = connect_accdb(output_path)
        output_cursor = output_conn.cursor()
        
        output_sheet_list = [row[2] for row in output_cursor.tables()]

        if output_name not in output_sheet_list:
            print("Error: 出力側テーブル・シート名が存在しません")
            exit()
        
        sql =   "SELECT * FROM " + output_name
        output_df = pd.read_sql(sql,output_conn)

        output_df_columns = output_df.columns.tolist()
    
        for key in output_keys:
            if key not in output_df_columns:
                print("Error: 出力側キー",key,"が出力側のデータに存在しません")
                exit()
                
        for key in update_keys:
            if key not in output_df_columns:
                print("Error: 更新用キー",key,"が出力側のデータに存在しません")
                exit()
    ####################
    
    
    if IsDelete and output_format == "accdb":
        print("you chose to clear db, so clear the remaining data.")
        
        sql = "DELETE FROM " + output_name
        output_cursor.execute(sql)
        output_conn.commit()
    
    
    print("finish preparation and start to organize data.")
    
    for i in range(len(input_df)):
        data = input_df.iloc[i]
        out_list = [data[key] for key in input_keys]
        
        if output_format == "excel":
            
            output_df.append(out_list)
            
        elif output_format == "accdb":
            if input_format == "excel" and "処理区分" in input_df_columns:
                process = data["処理区分"]
            else:
                process = "追加"

            update_values = [data[key] for key in update_keys]
            output_by_process(out_list,process,output_name,output_keys,update_keys,update_values,output_conn,output_cursor)
        
        
    if output_format == "excel":
        write_excel_multi_sheet(output_file_name,output_df,output_name,title,output_keys)        

    
    
if __name__ == "__main__":     
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])