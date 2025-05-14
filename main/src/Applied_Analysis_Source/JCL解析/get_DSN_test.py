#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import sys

sys.path.append(os.path.abspath("."))

from Common_analysis import *
from make_JCL_relations import *
def main(db_path,excel_path,title,excel_path2):
    
    
    print("start preparation for analysis.")

    if os.path.isdir(title) == False:
        os.makedirs(title)
    
    df_sheet_all = pd.read_excel(excel_path, sheet_name=None)
    df_sheet_list = df_sheet_all.keys()

    ### get the list of members
    sheet_members = df_sheet_all["settings"]["�����o�ꗗ"]
    for sheet in sheet_members:
        if sheet not in df_sheet_list:
            continue
        
        df_member = df_sheet_all[sheet]
        update_member_list(df_member)

    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    df_sheet_list = []
    # �f�[�^�x�[�X�Ɋ܂܂��e�[�u�����擾���܂�
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
    sheet_basic_info = df_sheet_all["settings"]["JCL_��{���"]
    for sheet in sheet_basic_info:
        if sheet not in df_sheet_list:
            continue

        sql = "SELECT * FROM "+sheet
        df = pd.read_sql(sql,conn)
        df.replace("", np.nan,inplace=True)
        update_internal_proc_list(df[df.JCL���� == "����PROC"])
        
    
    ### get the list of which source is jcl cmd info
    sheet_cmd_info = df_sheet_all["settings"]["JCL_CMD���"]
    for sheet in sheet_cmd_info:
        if sheet not in df_sheet_list:
            continue

        sql = "SELECT * FROM "+sheet
        df = pd.read_sql(sql,conn)
        df.replace("", np.nan,inplace=True)
        df.sort_values(["�����Y�s���"],inplace=True)
        update_jobproc_list(df[df.DD_NAME == "JOBPROC"])

    
    has_relation_proc_set = set()
    ### get the list of jcl step info
    sheet_step = df_sheet_all["settings"]["JCL_STEP���"]
    for sheet in sheet_step:
        if sheet not in df_sheet_list:
            continue
        
        sql = "SELECT * FROM "+sheet
        df = pd.read_sql(sql,conn)
        df.replace("", np.nan,inplace=True)
        has_relation_proc_set = update_step_info(df,has_relation_proc_set)

    conn.close()
    
    
    print("finish preparation and start analysis.")
    
    df = pd.read_excel(excel_path2,sheet_name="�ϐ�DSN�����Ώے��o")
    keys = df.columns.tolist()
    ActSheet = []
    ld = len(df)
    for i in range(len(df)):
        print("\r","analysis finished",i,"/",ld,end="")
        data = df.iloc[i]
        SYSINSheet_GYO = [""] + [data[key] for key in keys]
 
        JCL_NAME = data["JCL_NAME"]

        dsn = data["DSN"]
        
        dsn_list = get_variable2(JCL_NAME,dsn)
        

        for dsn,dsn_source in dsn_list:
                
            SYSINSheet_GYO_TEMP = SYSINSheet_GYO[:]
            SYSINSheet_GYO_TEMP.append(dsn_source)
            if "�����Ώ�" in dsn_source:
                continue
            if dsn_source.split("%")[1] != data["���@"]:
                SYSINSheet_GYO_TEMP[-1] += " ���@�Ⴂ"
                
            SYSINSheet_GYO_TEMP.append(dsn)
            ActSheet.append(SYSINSheet_GYO_TEMP) 
            
            
    ActSheet_all = [actSheet[1:] for actSheet in ActSheet]
    output_header = keys + ["�ďo��","�ϊ���DSN��"]
    write_excel_multi_sheet("DSN���茋��.xlsx",ActSheet_all,"DSN���茋��",title,output_header)


if __name__ == "__main__":    
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])