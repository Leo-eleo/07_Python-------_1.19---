#!/usr/bin/env python
# -*- coding: shift-jis -*-

import sys
import os
import time
import datetime
from relation_analysis_functions import *
import pandas as pd
import numpy as np


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


### header of output excel files
output_header = ["呼出元資産（元情報）","呼出元資産（メンバのみ）","呼び出し方法","呼び出し先資産","備考"]

output_header2 = ["MCP定義","呼出元資産（元情報）","呼出元資産（メンバのみ）","呼び出し方法","呼び出し先資産","備考"]


def main(setting_path,title):
    start = time.time()
    today = str(datetime.date.today())
    jcl_pgm_list = set()
    jcl_pgm_search_list = set()
    jcl_proc_list = set()
    jcl_easy_list = set()
    easy_call_list = set()
    
    proc_pgm_list = set()
    proc_proc_list = set()
    proc_pgm_search_list = set()
    proc_pgm_variable_list = set()
    
    utach_list = set()
    bmcp_list = set()
    bmcp_variable_list = set()
    bmcp_search_list = set()
    focus_ex_list = set()
    
    obj_uxcmdclr_list = set()
    obj_upjobkic_list = set()
    obj_ujobkic_list = set()
    obj_upbkic_list = set()
    
    obj_xpobapi_list = set()
    obj_xpobapi_variable_list = set()
    obj_xpbkic_file_list = set()
    
    owft_jcl_list = set()
    owft_jcl_proc_list = set()
    owft_jcl_proc_cand_list = set()
    owft_jcl_utach_list = set()
    owft_dxliftin_list = set()
    owft_uftpques_list = set()
    owft_uftpendc_list = set()

    owft_cobol_list = set()
    
    include_expand_list = set()
    
    pgm_screen_move_list = set()
    pgm_screen_value_list = set()
    
    fortran_list = set()
    
    screen_definition_list = set()
    
    data_definition_list = set()
    
    cobol_call_list = set()
    cobol_call_variable_list = set()
    cobol_entry_list = set()
    cobol_subschema_list = set()
    
    path = title
    if os.path.isdir(path) == False:
        os.makedirs(path)
    
    excel_path = setting_path

    db_path = ""
    jcl_path = ""
    proc_path = ""
    cobol_path = ""
    fortran_path = ""
    mcp_path = ""
    screen_path = ""
    damschema_path = ""
    ped_path = ""
    dbschema_path = ""
    dbsubschema_path = ""
    mqn_path = ""
    asm_path = ""
    easy_path = ""
    easy_parm_path = ""
    
    source_df = pd.read_excel(setting_path,sheet_name="個別関連性解析_格納フォルダ")
    source_df.fillna("",inplace=True)
    for source,source_path in zip(source_df["ソース種別"],source_df["格納フォルダ"]):
        if source == "JCL、カタプロ解析済みDB":
            db_path = source_path
        
        if source == "JCL":
            jcl_path = source_path
        
        if source == "カタプロ":
            proc_path = source_path
        
        if source == "COBOL":
            cobol_path = source_path
    
        if source == "Fortran":
            fortran_path = source_path
    
        if source == "MCP定義":
            mcp_path = source_path
    
        if source == "PSAM定義":
            screen_path = source_path
    
        if source == "DAM":
            damschema_path = source_path
            
        if source == "PED":
            ped_path = source_path
            
        if source == "DBスキーマ":
            dbschema_path = source_path
            
        if source == "DBサブスキーマ":
            dbsubschema_path = source_path
            
        if source == "MQN":
            mqn_path = source_path
            
        if source == "アセンブラ":
            asm_path = source_path
            
        if source == "EASY":
            easy_path = source_path
            
        if source == "EASYパラメタ":
            easy_parm_path = source_path
   
            
    if db_path != "" :
        
    
        print("JCL解析結果の関連性調査を開始します。")
        stime = time.time()
        df_sheet_all = pd.read_excel(excel_path, sheet_name=None)
        df_sheet_list = df_sheet_all.keys()


        ## get the list of members
        sheet_members = df_sheet_all["settings"]["メンバ一覧"]
        for sheet in sheet_members:
            if sheet not in df_sheet_list:
                continue
            
            df_member = df_sheet_all[sheet]
            update_member_list(df_member)

        # df = pd.read_excel(excel_path2)
        # update_member_list2(df)
        
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
            df.replace("\\","$",inplace=True)
            update_proc_parm_dic(df)            
                
                
                
        ### get the list of which source is internal proc
        sheet_basic_info = df_sheet_all["settings"]["JCL_基本情報"]
        for sheet in sheet_basic_info:
            if sheet not in df_sheet_list:
                continue
    
            sql = "SELECT * FROM "+sheet
            df = pd.read_sql(sql,conn)
            df.replace("", np.nan,inplace=True)
            df.replace("\\","$",inplace=True)
            
            update_internal_proc_list(df[df.JCL分類 == "内部PROC"])
            
        
        ### get the list of which source is jcl cmd info
        sheet_cmd_info = df_sheet_all["settings"]["JCL_CMD情報"]
        for sheet in sheet_cmd_info:
            if sheet not in df_sheet_list:
                continue

            sql = "SELECT * FROM "+sheet
            df = pd.read_sql(sql,conn)
            df.replace("", np.nan,inplace=True)
            df.replace("\\","$",inplace=True)
            df.sort_values(["元資産行情報"],inplace=True)
            update_jobproc_list(df[df.DD_NAME == "JOBPROC"])

        ### get the list of jcl step sysin 
        sheet_step_sysin = df_sheet_all["settings"]["JCL_STEP_SYSIN"]
        for sheet in sheet_step_sysin:
            if sheet not in df_sheet_list:
                continue
            
            sql = "SELECT * FROM "+sheet
            df = pd.read_sql(sql,conn)
            df.replace("", np.nan,inplace=True)
            df.replace("\\","$",inplace=True)
            
            focus_ex_list,utach_list,owft_jcl_utach_list,bmcp_list,owft_dxliftin_list = update_step_sysin(df_step_sysin=df,\
                                                                                        focus_ex_list=focus_ex_list, utach_list=utach_list, owft_jcl_utach_list=owft_jcl_utach_list, bmcp_list=bmcp_list, owft_dxliftin_list=owft_dxliftin_list)
            
        
        ### get the list of jcl step info
        sheet_step = df_sheet_all["settings"]["JCL_STEP情報"]
        for sheet in sheet_step:
            if sheet not in df_sheet_list:
                continue
            
            sql = "SELECT * FROM "+sheet
            df = pd.read_sql(sql,conn)
            df.replace("", np.nan,inplace=True)
            df.replace("\\","$",inplace=True)
            
            jcl_pgm_list, proc_pgm_list, jcl_proc_list, proc_proc_list, bmcp_list, \
            obj_ujobkic_list, obj_upjobkic_list, obj_upbkic_list, obj_uxcmdclr_list, \
            owft_jcl_list, owft_jcl_proc_cand_list, owft_uftpendc_list, owft_uftpques_list,jcl_pgm_search_list,proc_pgm_search_list,bmcp_search_list = update_step_info(df,jcl_pgm_list, proc_pgm_list, jcl_proc_list, proc_proc_list, bmcp_list, \
                                                                                                                            obj_ujobkic_list, obj_upjobkic_list, obj_upbkic_list, obj_uxcmdclr_list, \
                                                                                                                            owft_jcl_list, owft_jcl_proc_cand_list, owft_uftpendc_list, owft_uftpques_list,jcl_pgm_search_list,proc_pgm_search_list, bmcp_search_list)
            
        ### get the list of jcl pgm dsn info
        sheet_pgm_dsn = df_sheet_all["settings"]["JCL_PGM_DSN"]
        for sheet in sheet_pgm_dsn:
            if sheet not in df_sheet_list:
                continue
            
            sql = "SELECT * FROM "+sheet
            df = pd.read_sql(sql,conn)
            df.replace("", np.nan,inplace=True)
            df.replace("\\","$",inplace=True)
            
            jcl_easy_list = update_pgm_dsn(df,jcl_easy_list)
                
        jcl_pgm_list = update_jcl_pgm_variable_list(jcl_pgm_list, jcl_pgm_search_list)
        proc_pgm_variable_list = make_proc_pgm_variable_list(proc_pgm_search_list)
        bmcp_variable_list = make_bmcp_variable_list(bmcp_search_list)
        owft_jcl_proc_list = make_owft_jcl_proc_list(owft_jcl_proc_cand_list)

        print("JCL解析結果の関連性調査を完了しました。",time.time()-stime,"秒で完了しました。")
  
           
    if jcl_path != "" or proc_path != "":
        print("JCL-INCLUDE-EXPANDの関連性調査を開始します。")
        stime = time.time()
        jcl_files = glob_files(jcl_path)
        proc_files = glob_files(proc_path)
        print(len(jcl_files)+len(proc_files))
        
        include_expand_list,include_proc_list = make_include_expand_list(jcl_files=jcl_files,proc_files=proc_files)
        include_proc_list = make_member_with_library_list(include_proc_list)
        write_excel_multi_sheet4(join_file_name_xlsx(today,"JCL_INCLUDE_EXPAND資産関連性"),[list(include_expand_list)+include_proc_list],["INCLUDE_EXPAND"],path,output_header)
        
        print("JCL-INCLUDE-EXPANDの関連性調査を完了しました。",time.time()-stime,"秒で完了しました。")
        
    # if proc_path != "":
    #     proc_files = glob_files(proc_path)
        
    #     proc_pgm_list,proc_proc_list = update_proc_list(proc_files=proc_files, proc_pgm_list=proc_pgm_list, proc_proc_list=proc_proc_list)
        
        
    if fortran_path != "":
        print("FORTRANの関連性調査を開始します。")
        stime = time.time()
        fortran_files = glob_files(fortran_path)
        
        fortran_list = make_fortran_list(fortran_files)
        print(len(fortran_list))
        write_excel_multi_sheet4(join_file_name_xlsx(today,"FORTRAN資産関連性"),[fortran_list],["FORTRAN"],path,output_header)
        print("FORTRANの関連性調査を完了しました。",time.time()-stime,"秒で完了しました。")
        
        
    if mcp_path != "" or screen_path != "":
        print("画面定義の関連性調査を開始します。")
        stime = time.time()
        mcp_files = glob_files(mcp_path)
        screen_files = glob_files(screen_path)
        print(len(mcp_files),len(screen_files))
        screen_definition_list = make_screen_definition_list(mcp_files,screen_files)
        write_excel_multi_sheet4(join_file_name_xlsx(today,"画面定義資産関連性"),[screen_definition_list],["画面定義"],path, output_header=output_header2)
        print("画面定義の関連性調査を完了しました。",time.time()-stime,"秒で完了しました。")
        
    if damschema_path != "" or mcp_path != "" or ped_path != "" or dbschema_path != "" or dbsubschema_path != "" or jcl_path != "" or proc_path != "":
        print("データ定義の関連性調査を開始します。")
        stime = time.time()
        damschema_files = glob_files(damschema_path)
        mcp_files = glob_files(mcp_path)
        ped_files = glob_files(ped_path)
        dbschema_files = glob_files(dbschema_path)
        dbsubschema_files = glob_files(dbsubschema_path)
        jcl_files = glob_files(jcl_path)
        proc_files = glob_files(proc_path)
        
        data_definition_list = make_data_definition_list(damschema_files=damschema_files, mcp_files=mcp_files, ped_files=ped_files,\
                                                        dbschema_files=dbschema_files, dbsubschema_files=dbsubschema_files, jcl_files=jcl_files, proc_files=proc_files)
        write_excel_multi_sheet4(join_file_name_xlsx(today,"データ定義資産関連性"),[data_definition_list],["データ定義"],path,output_header)
        print("データ定義の関連性調査を完了しました。",time.time()-stime,"秒で完了しました。")
    
    if asm_path != "":
        print("ASSEMBLYの関連性調査を開始します。")
        stime = time.time()
        asm_files = glob_files(asm_path)
        assembly_list = make_assembly_list(asm_files)

        write_excel_multi_sheet4(join_file_name_xlsx(today,"ASM資産関連性"),[assembly_list],["ASM"],path,output_header)
        print("ASSEMBLYの関連性調査を完了しました。",time.time()-stime,"秒で完了しました。")
        
    if easy_path != "" or easy_parm_path != "":
        print("EASYの関連性調査を開始します。")
        stime = time.time()
        easy_files = glob_files(easy_path)
        easy_parm_files = glob_files(easy_parm_path)
        jcl_easy_list, easy_call_list = update_easy_list(easy_files,easy_parm_files,jcl_easy_list,easy_call_list)
        

        write_excel_multi_sheet4(join_file_name_xlsx(today,"JCL-EASY資産関連性"),[jcl_easy_list],["JCL_EASY"],path,output_header)
        write_excel_multi_sheet4(join_file_name_xlsx(today,"EASY-CALL資産関連性"),[easy_call_list],["EASY_CALL"],path,output_header)
        print("EASYの関連性調査を完了しました。",time.time()-stime,"秒で完了しました。")
        
        
        
    if cobol_path != "" or ped_path != "" or mqn_path != "":
        print("ACSAPIの関連性調査を開始します。")
        stime = time.time()
        cobol_files = glob_files(cobol_path)
        ped_files = glob_files(ped_path)
        mqn_files = glob_files(mqn_path)
        print(len(cobol_files),len(ped_files),len(mqn_files))
        acsapi_acsext_list,acsapi_switch_list = make_acsapi_acsext_list(cobol_files,ped_files,mqn_files)
        
        write_excel_multi_sheet4(join_file_name_xlsx(today,"CALL_ACSAPI_USING_ACSEXT資産関連性"),[acsapi_acsext_list],["ACSAPI_ACSEXT"],path,output_header)
        write_excel_multi_sheet4(join_file_name_xlsx(today,"ACSAPI_SWITCH資産関連性"),[acsapi_switch_list],["ACSAPI_SWITCH"],path,output_header)
        print("ACSAPIの関連性調査を完了しました。",time.time()-stime,"秒で完了しました。")
        
            
    if cobol_path != "":
        print("COBOLの関連性調査を開始します。")
        stime = time.time()
        cobol_files = glob_files(cobol_path)    
        
        obj_xpbkic_file_list,obj_xpobapi_list,obj_xpobapi_variable_list = make_obj_list(cobol_files=cobol_files)
                
        pgm_screen_move_list, pgm_screen_value_list = make_pgm_screen_list(cobol_files=cobol_files)
        write_excel_multi_sheet4(join_file_name_xlsx(today,"PGM-画面資産関連性"),[pgm_screen_value_list,pgm_screen_move_list],["PGM_VALUE","PGM_MOVE"],path,output_header)

            
        cobol_call_list,cobol_call_variable_list,cobol_entry_list,cobol_subschema_list,owft_cobol_list = make_cobol_list(cobol_files)
        write_excel_multi_sheet4(join_file_name_xlsx(today,"COBOL_SUB資産関連性"),[cobol_subschema_list],["COBOL_SUB"],path,output_header)
        write_excel_multi_sheet4(join_file_name_xlsx(today,"COBOL_CALL資産関連性"),[cobol_call_list],["COBOL_CALL"],path,output_header)
        write_excel_multi_sheet4(join_file_name_xlsx(today,"COBOL_CALL変数資産関連性"),[cobol_call_variable_list],["COBOL_CALL変数"],path,output_header)
        write_excel_multi_sheet4(join_file_name_xlsx(today,"COBOL_ENTRY資産関連性"),[cobol_entry_list],["COBOL_ENTRY"],path,output_header)
            
        print("COBOLの関連性調査を完了しました。",time.time()-stime,"秒で完了しました。")
            
    
        
        
    jcl_proc_list_with_library = make_member_with_library_list(base_list=jcl_proc_list)
    proc_proc_list_with_library = make_member_with_library_list(base_list=proc_proc_list)
    
    obj_uxcmdclr_list_with_library = make_member_with_library_list_onbatch(base_list=obj_uxcmdclr_list)
    obj_ujobkic_list_with_library = make_member_with_library_list_onbatch(base_list=obj_ujobkic_list)
    obj_upjobkic_list_with_library = make_member_with_library_list_onbatch(base_list=obj_upjobkic_list)
    obj_upbkic_list_with_library = make_member_with_library_list_onbatch(base_list=obj_upbkic_list)

    
    write_excel_multi_sheet4(join_file_name_xlsx(today,"JCL-PGM資産関連性"),[jcl_pgm_list,jcl_proc_list_with_library],["JCL_PGM","JCL_PROC"],path,output_header)
    write_excel_multi_sheet4(join_file_name_xlsx(today,"PROC-PGM資産関連性"),[proc_pgm_list,proc_proc_list_with_library],["PROC_PGM","PROC_PROC"],path,output_header)
    bmcp_list = list(bmcp_list)
    bmcp_variable_list = list(bmcp_variable_list)
    write_excel_multi_sheet4(join_file_name_xlsx(today,"PROC-変数資産関連性"),[proc_pgm_variable_list],["PROC_変数"],path,output_header)
    write_excel_multi_sheet4(join_file_name_xlsx(today,"BMCP資産関連性"),[bmcp_list+bmcp_variable_list],["BMCP"],path,output_header)
    write_excel_multi_sheet4(join_file_name_xlsx(today,"UTACH資産関連性"),[utach_list],["UTACH"],path,output_header)
    write_excel_multi_sheet4(join_file_name_xlsx(today,"FOCUS_EX資産関連性"),[focus_ex_list],["FOCUS_EX"],path,output_header)
    
  
    if cobol_path != "":
        obj_xpobapi_list_with_library = make_member_with_library_list_onbatch(base_list=obj_xpobapi_list)
        write_excel_multi_sheet4(join_file_name_xlsx(today,"オンバッチ連携資産関連性"),[obj_ujobkic_list_with_library,obj_upjobkic_list_with_library,obj_upbkic_list_with_library,obj_xpbkic_file_list,\
                                                                                            obj_xpobapi_list_with_library,obj_xpobapi_variable_list,obj_uxcmdclr_list_with_library],\
                                                                                                ["UJOBKIC","UPJOBKIC","UPBKIC","XPBKIC","XPOBAPI","XPOBAPI_変数","UXCMDCLR"],path,output_header)
        
        write_excel_multi_sheet4(join_file_name_xlsx(today,"OWFT資産関連性"),[owft_jcl_list,owft_jcl_proc_list,owft_jcl_utach_list,owft_dxliftin_list,\
                                                                                            owft_uftpques_list,owft_uftpendc_list,owft_cobol_list],\
                                                                                                ["OWFT_JCL","OWFT_JCL_PROC","OWFT_JCL_UTACH","OWFT_DXLIFTIN","OWFT_UFTPQUES","OWFT_UFTPENDC","OWFT_COBOL"],path,output_header)
    
       
  
    write_excel_multi_sheet4(join_file_name_xlsx(today,"個別調査対象一覧"),[need_search_and_check_list],["個別調査対象"],path,output_header)
    write_excel_multi_sheet4(join_file_name_xlsx(today,"未受領判定"),[check_list],["個別調査対象"],path,["呼出元資産（元情報）","呼出元資産（メンバのみ）","呼び出し方法","呼び出し先資産","JOBPROC命令","受領済み資産"])
    print("関連性調査結果の出力が完了しました。")
    print(time.time()-start,"秒で完了しました。")
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])