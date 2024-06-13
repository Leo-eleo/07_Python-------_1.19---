#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


def main(Folder_JCL_path,title,rem_extentions=True):
    
    print("start to merge JCL db")
    if os.path.isdir(title) == False:
        os.makedirs(title)

    JCL_Files = glob_files(Folder_JCL_path)
    JCL_CMD = []
    JCL_basic_info = []
    JCL_step_info = []
    JCL_step_sysin1 = []
    JCL_step_sysin2 = []
    JCL_PGM_DSN = []
    PROC_PARM = []


    JCL_CMD_header = []
    JCL_basic_info_header = []
    JCL_step_info_header = []
    JCL_step_sysin1_header = []
    JCL_step_sysin2_header = []
    JCL_PGM_DSN_header = []
    PROC_PARM_header = []
        
    
    
    for JCL_File in JCL_Files:
        conn = connect_accdb(JCL_File)
        
        sql =   """\
                SELECT * FROM ①JCL_CMD情報
                """
    
        df = pd.read_sql(sql,conn)
        df.fillna("",inplace=True)
        JCL_CMD += df.values.tolist()
        JCL_CMD_header = df.columns.tolist()

        
        sql =   """\
                SELECT * FROM ①JCL_基本情報
                """
    
        df = pd.read_sql(sql,conn)
        df.fillna("",inplace=True)
        JCL_basic_info += df.values.tolist()
        JCL_basic_info_header = df.columns.tolist()
        
        sql =   """\
                SELECT * FROM ①JCL_STEP情報
                """
    
        df = pd.read_sql(sql,conn)
        df.fillna("",inplace=True)
        JCL_step_info += df.values.tolist()
        JCL_step_info_header = df.columns.tolist()
        
        
        sql =   """\
                SELECT * FROM ①JCL_STEP_SYSIN
                """
    
        df = pd.read_sql(sql,conn)
        df.fillna("",inplace=True)
        JCL_step_sysin1 += df.values.tolist()
        JCL_step_sysin1_header = df.columns.tolist()
        
        sql =   """\
                SELECT * FROM ①JCL_STEP_SYSIN2
                """
    
        df = pd.read_sql(sql,conn)
        df.fillna("",inplace=True)
        JCL_step_sysin2 += df.values.tolist()
        JCL_step_sysin2_header = df.columns.tolist()
        
        sql =   """\
                SELECT * FROM ①JCL_PGM_DSN
                """
    
        df = pd.read_sql(sql,conn)
        df.fillna("",inplace=True)
        JCL_PGM_DSN += df.values.tolist()
        JCL_PGM_DSN_header = df.columns.tolist()

        sql =   """\
                SELECT * FROM ①PROC_PARM
                """
    
        df = pd.read_sql(sql,conn)
        df.fillna("",inplace=True)
        PROC_PARM += df.values.tolist()
        PROC_PARM_header = df.columns.tolist()
        

    if rem_extentions:
        JCL_CMD = take_all_extensions(JCL_CMD)
        JCL_basic_info = take_all_extensions(JCL_basic_info)
        JCL_step_info = take_all_extensions(JCL_step_info)
        JCL_step_sysin1 = take_all_extensions(JCL_step_sysin1)
        JCL_step_sysin2 = take_all_extensions(JCL_step_sysin2)
        JCL_PGM_DSN = take_all_extensions(JCL_PGM_DSN)
        PROC_PARM = take_all_extensions(PROC_PARM)
        
    write_excel_multi_sheet2("JCL解析結果_merge.xlsx",[JCL_CMD,JCL_basic_info,JCL_step_info,JCL_step_sysin1,JCL_step_sysin2,JCL_PGM_DSN,PROC_PARM],\
                                                ["JCL_CMD情報","JCL_基本情報","JCL_STEP情報","JCL_STEP_SYSIN1","JCL_STEP_SYSIN2","JCL_PGM_DSN","PROC_PARM"],title, \
                                                [JCL_CMD_header,JCL_basic_info_header,JCL_step_info_header,JCL_step_sysin1_header,JCL_step_sysin2_header,JCL_PGM_DSN_header,PROC_PARM_header]    )
    
    print("finish to merge JCL db")
    
      
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])
        
    ### 引数1 JCL解析済DBの格納フォルダ 引数2 出力フォルダ