#!/usr/bin/env python
# -*- coding: cp932 -*-

import numpy as np

from make_JCL_relations import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

def main(db_path,excel_path,title):
    
    print("start analysis")
    if os.path.isdir(title) == False:
        os.makedirs(title)

    
    df_sheet_all = pd.read_excel(excel_path, sheet_name=None)
    df_sheet_list = df_sheet_all.keys()
 
    ### get the list of members
    sheet_members = df_sheet_all["settings"]["メンバ一覧"]
    for sheet in sheet_members:
        if sheet not in df_sheet_list:
            continue
        
        df_member = df_sheet_all[sheet]
        update_member_list(df_member)

    # for sheet in df_sheet_list:
    #     if "資産分類不足情報" not in sheet:
    #         continue
    #     df = df_sheet_all[sheet]

    #     update_member_list2(df)
        
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    df_sheet_list = []
    # データベースに含まれるテーブルを取得します
    for table_info in cursor.tables(tableType='TABLE'):
        df_sheet_list.append(table_info.table_name)

    

    ### get the list of which source is proc_parm
    sheet_proc_parm = df_sheet_all["settings"]["PROC_PARM"]
    for sheet in sheet_proc_parm:
        if sheet not in df_sheet_list:
            continue
        
        sql = "SELECT * FROM "+sheet
        df = pd.read_sql(sql,conn)
        df.replace("", np.nan,inplace=True)
        update_proc_parm_dic(df)            
            
         
    ### get the list of which source is internal proc
    sheet_basic_info = df_sheet_all["settings"]["JCL_基本情報"]
    for sheet in sheet_basic_info:
        if sheet not in df_sheet_list:
            continue

        sql = "SELECT * FROM "+sheet
        df = pd.read_sql(sql,conn)
        df.replace("", np.nan,inplace=True)
        
        update_internal_proc_list(df[df.JCL分類 == "内部PROC"])
        
    
    ### get the list of which source is jcl cmd info
    sheet_cmd_info = df_sheet_all["settings"]["JCL_CMD情報"]
    for sheet in sheet_cmd_info:
        if sheet not in df_sheet_list:
            continue

        sql = "SELECT * FROM "+sheet
        df = pd.read_sql(sql,conn)
        df.replace("", np.nan,inplace=True)
        update_jobproc_list(df[df.DD_NAME == "JOBPROC"])

    has_relation_proc_set = set()
    
    ### get the list of jcl step info
    sheet_step = df_sheet_all["settings"]["JCL_STEP情報"]
    for sheet in sheet_step:
        if sheet not in df_sheet_list:
            continue
        
        sql = "SELECT * FROM "+sheet
        df = pd.read_sql(sql,conn)
        df.replace("", np.nan,inplace=True)
        has_relation_proc_set = update_step_info(df,has_relation_proc_set)
        
    conn.close()

    ActSheet = [[proc_name,""] for proc_name in sorted(has_relation_proc_set)]
    write_excel_multi_sheet("JCL呼出ありカタプロ一覧.xlsx",ActSheet,"JCL呼出ありカタプロ一覧",title,["カタプロ名","備考"])

    print("finish analysis")
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3])