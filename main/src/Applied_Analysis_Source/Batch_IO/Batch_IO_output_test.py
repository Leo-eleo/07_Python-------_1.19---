#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *
from Applied_IO_Info import Applied_IO_Info_main
from Test_Step_Import import test_step_import

dsn_dic = {}
io_header = ["TEST_ID","DSN","日本語名称(DSN)","データ種別","受領入力","受領照合"]
test_io_info_all = []
def make_output_file(io_list,title,test_id,keys):
    if io_list == []:
        return
    
    global dsn_dic
    global test_io_info_all
    assert "受領判定" in keys
    assert "DSN" in keys
    assert "データ種別" in keys
    
    receive_idx = keys.index("受領判定")
    dsn_idx = keys.index("DSN")
    data_idx = keys.index("データ種別")
    test_io_info = []
    for list_now in io_list:
        if "入力" in list_now[receive_idx] or "照合" in list_now[receive_idx]:
            dsn = list_now[dsn_idx]
            data = list_now[data_idx]
            dsn_japanese = dsn_dic.get(dsn,"")
            receive_input = ""
            receive_collation = ""
            if "入力" in list_now[receive_idx]:
                receive_input = "●"
            if "照合" in list_now[receive_idx]:
                receive_collation = "●"
                
            io_info = [test_id,dsn,dsn_japanese,data,receive_input,receive_collation]
            test_io_info.append(io_info)
            test_io_info_all.append(io_info)

    write_excel_multi_sheet3(test_id + ".xlsx",[io_list,test_io_info],["応用_入出力情報出力","テストIO情報"],title,[keys,io_header])
    
    return 

def main(db_path,excel_path,title):
    global dsn_dic
    global test_io_info_all
    if os.path.isdir(title) == False:
        os.makedirs(title)
        
        
    test_step_import.analysis1_main(db_path,title)
    Applied_IO_Info_main.main(db_path,title)
    
    conn = connect_accdb(db_path)
    sql = "SELECT * FROM TEST_テスト実施単位"
    df_starting_point = pd.read_sql(sql,conn)
    df_starting_point.fillna("",inplace=True)
    starting_point_to_out_folder_dic = {}
    for test_id,out_folder in zip(df_starting_point["TEST_ID"],df_starting_point["出力フォルダ"]):
        if test_id not in starting_point_to_out_folder_dic:
            starting_point_to_out_folder_dic[test_id] = []
        starting_point_to_out_folder_dic[test_id].append(out_folder)
        
        
    dsn_df = pd.read_excel(excel_path,sheet_name="DSN名称")
    dsn_df.fillna("",inplace=True)
    dsn_dic = {dsn:name for dsn,name in zip(dsn_df["データセット名"],dsn_df["日本語名称"])}
    
    io_out_path = os.path.join(title,"応用入出力解析.xlsx")
    io_df = pd.read_excel(io_out_path,sheet_name="応用入出力")
    io_df.fillna("",inplace=True)
    keys = io_df.columns.tolist()
    
    if "JCL_MBR" in keys:
        keys = keys[:keys.index("JCL_MBR")]
    else:
        print("データが想定された形式ではありません。")
    io_list = []
    last = ""
    for i in range(len(io_df)):
        data = io_df.iloc[i]
        test_id_now = data["TEST_ID"]
        list_now = [data[key] for key in keys]
        if test_id_now != last:
            
            if last not in starting_point_to_out_folder_dic:
                starting_point_to_out_folder_dic[last] = [""]
                
                
            for out_folder in starting_point_to_out_folder_dic[last]:
                if out_folder == "":
                    out_title = title
                else:
                    out_title = os.path.join(title,out_folder)
                
                if os.path.isdir(out_title) == False:
                    os.makedirs(out_title)
                    
                make_output_file(io_list,out_title,last,keys)
                    
            
            io_list = []
        io_list.append(list_now)
        last = test_id_now
    
    if last not in starting_point_to_out_folder_dic:
        starting_point_to_out_folder_dic[last] = [""]
            
    for out_folder in starting_point_to_out_folder_dic[last]:
        if out_folder == "":
            out_title = title
        else:
            out_title = os.path.join(title,out_folder)
        
        if os.path.isdir(out_title) == False:
            os.makedirs(out_title)
            
        make_output_file(io_list,out_title,last,keys)
        
    write_excel_multi_sheet3("テストIO情報_マージ.xlsx",[test_io_info_all],["テストIO情報"],title,[io_header])
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3])
    