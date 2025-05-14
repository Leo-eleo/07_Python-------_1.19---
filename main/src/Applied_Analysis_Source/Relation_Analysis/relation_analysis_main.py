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
output_header = ["�ďo�����Y�i�����j","�ďo�����Y�i�����o�̂݁j","�Ăяo�����@","�Ăяo���掑�Y","���l"]

output_header2 = ["MCP��`","�ďo�����Y�i�����j","�ďo�����Y�i�����o�̂݁j","�Ăяo�����@","�Ăяo���掑�Y","���l"]


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
    
    source_df = pd.read_excel(setting_path,sheet_name="�ʊ֘A�����_�i�[�t�H���_")
    source_df.fillna("",inplace=True)
    for source,source_path in zip(source_df["�\�[�X���"],source_df["�i�[�t�H���_"]):
        if source == "JCL�A�J�^�v����͍ς�DB":
            db_path = source_path
        
        if source == "JCL":
            jcl_path = source_path
        
        if source == "�J�^�v��":
            proc_path = source_path
        
        if source == "COBOL":
            cobol_path = source_path
    
        if source == "Fortran":
            fortran_path = source_path
    
        if source == "MCP��`":
            mcp_path = source_path
    
        if source == "PSAM��`":
            screen_path = source_path
    
        if source == "DAM":
            damschema_path = source_path
            
        if source == "PED":
            ped_path = source_path
            
        if source == "DB�X�L�[�}":
            dbschema_path = source_path
            
        if source == "DB�T�u�X�L�[�}":
            dbsubschema_path = source_path
            
        if source == "MQN":
            mqn_path = source_path
            
        if source == "�A�Z���u��":
            asm_path = source_path
            
        if source == "EASY":
            easy_path = source_path
            
        if source == "EASY�p�����^":
            easy_parm_path = source_path
   
            
    if db_path != "" :
        
    
        print("JCL��͌��ʂ̊֘A���������J�n���܂��B")
        stime = time.time()
        df_sheet_all = pd.read_excel(excel_path, sheet_name=None)
        df_sheet_list = df_sheet_all.keys()


        ## get the list of members
        sheet_members = df_sheet_all["settings"]["�����o�ꗗ"]
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
            df.replace("\\","$",inplace=True)
            update_proc_parm_dic(df)            
                
                
                
        ### get the list of which source is internal proc
        sheet_basic_info = df_sheet_all["settings"]["JCL_��{���"]
        for sheet in sheet_basic_info:
            if sheet not in df_sheet_list:
                continue
    
            sql = "SELECT * FROM "+sheet
            df = pd.read_sql(sql,conn)
            df.replace("", np.nan,inplace=True)
            df.replace("\\","$",inplace=True)
            
            update_internal_proc_list(df[df.JCL���� == "����PROC"])
            
        
        ### get the list of which source is jcl cmd info
        sheet_cmd_info = df_sheet_all["settings"]["JCL_CMD���"]
        for sheet in sheet_cmd_info:
            if sheet not in df_sheet_list:
                continue

            sql = "SELECT * FROM "+sheet
            df = pd.read_sql(sql,conn)
            df.replace("", np.nan,inplace=True)
            df.replace("\\","$",inplace=True)
            df.sort_values(["�����Y�s���"],inplace=True)
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
        sheet_step = df_sheet_all["settings"]["JCL_STEP���"]
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

        print("JCL��͌��ʂ̊֘A���������������܂����B",time.time()-stime,"�b�Ŋ������܂����B")
  
           
    if jcl_path != "" or proc_path != "":
        print("JCL-INCLUDE-EXPAND�̊֘A���������J�n���܂��B")
        stime = time.time()
        jcl_files = glob_files(jcl_path)
        proc_files = glob_files(proc_path)
        print(len(jcl_files)+len(proc_files))
        
        include_expand_list,include_proc_list = make_include_expand_list(jcl_files=jcl_files,proc_files=proc_files)
        include_proc_list = make_member_with_library_list(include_proc_list)
        write_excel_multi_sheet4(join_file_name_xlsx(today,"JCL_INCLUDE_EXPAND���Y�֘A��"),[list(include_expand_list)+include_proc_list],["INCLUDE_EXPAND"],path,output_header)
        
        print("JCL-INCLUDE-EXPAND�̊֘A���������������܂����B",time.time()-stime,"�b�Ŋ������܂����B")
        
    # if proc_path != "":
    #     proc_files = glob_files(proc_path)
        
    #     proc_pgm_list,proc_proc_list = update_proc_list(proc_files=proc_files, proc_pgm_list=proc_pgm_list, proc_proc_list=proc_proc_list)
        
        
    if fortran_path != "":
        print("FORTRAN�̊֘A���������J�n���܂��B")
        stime = time.time()
        fortran_files = glob_files(fortran_path)
        
        fortran_list = make_fortran_list(fortran_files)
        print(len(fortran_list))
        write_excel_multi_sheet4(join_file_name_xlsx(today,"FORTRAN���Y�֘A��"),[fortran_list],["FORTRAN"],path,output_header)
        print("FORTRAN�̊֘A���������������܂����B",time.time()-stime,"�b�Ŋ������܂����B")
        
        
    if mcp_path != "" or screen_path != "":
        print("��ʒ�`�̊֘A���������J�n���܂��B")
        stime = time.time()
        mcp_files = glob_files(mcp_path)
        screen_files = glob_files(screen_path)
        print(len(mcp_files),len(screen_files))
        screen_definition_list = make_screen_definition_list(mcp_files,screen_files)
        write_excel_multi_sheet4(join_file_name_xlsx(today,"��ʒ�`���Y�֘A��"),[screen_definition_list],["��ʒ�`"],path, output_header=output_header2)
        print("��ʒ�`�̊֘A���������������܂����B",time.time()-stime,"�b�Ŋ������܂����B")
        
    if damschema_path != "" or mcp_path != "" or ped_path != "" or dbschema_path != "" or dbsubschema_path != "" or jcl_path != "" or proc_path != "":
        print("�f�[�^��`�̊֘A���������J�n���܂��B")
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
        write_excel_multi_sheet4(join_file_name_xlsx(today,"�f�[�^��`���Y�֘A��"),[data_definition_list],["�f�[�^��`"],path,output_header)
        print("�f�[�^��`�̊֘A���������������܂����B",time.time()-stime,"�b�Ŋ������܂����B")
    
    if asm_path != "":
        print("ASSEMBLY�̊֘A���������J�n���܂��B")
        stime = time.time()
        asm_files = glob_files(asm_path)
        assembly_list = make_assembly_list(asm_files)

        write_excel_multi_sheet4(join_file_name_xlsx(today,"ASM���Y�֘A��"),[assembly_list],["ASM"],path,output_header)
        print("ASSEMBLY�̊֘A���������������܂����B",time.time()-stime,"�b�Ŋ������܂����B")
        
    if easy_path != "" or easy_parm_path != "":
        print("EASY�̊֘A���������J�n���܂��B")
        stime = time.time()
        easy_files = glob_files(easy_path)
        easy_parm_files = glob_files(easy_parm_path)
        jcl_easy_list, easy_call_list = update_easy_list(easy_files,easy_parm_files,jcl_easy_list,easy_call_list)
        

        write_excel_multi_sheet4(join_file_name_xlsx(today,"JCL-EASY���Y�֘A��"),[jcl_easy_list],["JCL_EASY"],path,output_header)
        write_excel_multi_sheet4(join_file_name_xlsx(today,"EASY-CALL���Y�֘A��"),[easy_call_list],["EASY_CALL"],path,output_header)
        print("EASY�̊֘A���������������܂����B",time.time()-stime,"�b�Ŋ������܂����B")
        
        
        
    if cobol_path != "" or ped_path != "" or mqn_path != "":
        print("ACSAPI�̊֘A���������J�n���܂��B")
        stime = time.time()
        cobol_files = glob_files(cobol_path)
        ped_files = glob_files(ped_path)
        mqn_files = glob_files(mqn_path)
        print(len(cobol_files),len(ped_files),len(mqn_files))
        acsapi_acsext_list,acsapi_switch_list = make_acsapi_acsext_list(cobol_files,ped_files,mqn_files)
        
        write_excel_multi_sheet4(join_file_name_xlsx(today,"CALL_ACSAPI_USING_ACSEXT���Y�֘A��"),[acsapi_acsext_list],["ACSAPI_ACSEXT"],path,output_header)
        write_excel_multi_sheet4(join_file_name_xlsx(today,"ACSAPI_SWITCH���Y�֘A��"),[acsapi_switch_list],["ACSAPI_SWITCH"],path,output_header)
        print("ACSAPI�̊֘A���������������܂����B",time.time()-stime,"�b�Ŋ������܂����B")
        
            
    if cobol_path != "":
        print("COBOL�̊֘A���������J�n���܂��B")
        stime = time.time()
        cobol_files = glob_files(cobol_path)    
        
        obj_xpbkic_file_list,obj_xpobapi_list,obj_xpobapi_variable_list = make_obj_list(cobol_files=cobol_files)
                
        pgm_screen_move_list, pgm_screen_value_list = make_pgm_screen_list(cobol_files=cobol_files)
        write_excel_multi_sheet4(join_file_name_xlsx(today,"PGM-��ʎ��Y�֘A��"),[pgm_screen_value_list,pgm_screen_move_list],["PGM_VALUE","PGM_MOVE"],path,output_header)

            
        cobol_call_list,cobol_call_variable_list,cobol_entry_list,cobol_subschema_list,owft_cobol_list = make_cobol_list(cobol_files)
        write_excel_multi_sheet4(join_file_name_xlsx(today,"COBOL_SUB���Y�֘A��"),[cobol_subschema_list],["COBOL_SUB"],path,output_header)
        write_excel_multi_sheet4(join_file_name_xlsx(today,"COBOL_CALL���Y�֘A��"),[cobol_call_list],["COBOL_CALL"],path,output_header)
        write_excel_multi_sheet4(join_file_name_xlsx(today,"COBOL_CALL�ϐ����Y�֘A��"),[cobol_call_variable_list],["COBOL_CALL�ϐ�"],path,output_header)
        write_excel_multi_sheet4(join_file_name_xlsx(today,"COBOL_ENTRY���Y�֘A��"),[cobol_entry_list],["COBOL_ENTRY"],path,output_header)
            
        print("COBOL�̊֘A���������������܂����B",time.time()-stime,"�b�Ŋ������܂����B")
            
    
        
        
    jcl_proc_list_with_library = make_member_with_library_list(base_list=jcl_proc_list)
    proc_proc_list_with_library = make_member_with_library_list(base_list=proc_proc_list)
    
    obj_uxcmdclr_list_with_library = make_member_with_library_list_onbatch(base_list=obj_uxcmdclr_list)
    obj_ujobkic_list_with_library = make_member_with_library_list_onbatch(base_list=obj_ujobkic_list)
    obj_upjobkic_list_with_library = make_member_with_library_list_onbatch(base_list=obj_upjobkic_list)
    obj_upbkic_list_with_library = make_member_with_library_list_onbatch(base_list=obj_upbkic_list)

    
    write_excel_multi_sheet4(join_file_name_xlsx(today,"JCL-PGM���Y�֘A��"),[jcl_pgm_list,jcl_proc_list_with_library],["JCL_PGM","JCL_PROC"],path,output_header)
    write_excel_multi_sheet4(join_file_name_xlsx(today,"PROC-PGM���Y�֘A��"),[proc_pgm_list,proc_proc_list_with_library],["PROC_PGM","PROC_PROC"],path,output_header)
    bmcp_list = list(bmcp_list)
    bmcp_variable_list = list(bmcp_variable_list)
    write_excel_multi_sheet4(join_file_name_xlsx(today,"PROC-�ϐ����Y�֘A��"),[proc_pgm_variable_list],["PROC_�ϐ�"],path,output_header)
    write_excel_multi_sheet4(join_file_name_xlsx(today,"BMCP���Y�֘A��"),[bmcp_list+bmcp_variable_list],["BMCP"],path,output_header)
    write_excel_multi_sheet4(join_file_name_xlsx(today,"UTACH���Y�֘A��"),[utach_list],["UTACH"],path,output_header)
    write_excel_multi_sheet4(join_file_name_xlsx(today,"FOCUS_EX���Y�֘A��"),[focus_ex_list],["FOCUS_EX"],path,output_header)
    
  
    if cobol_path != "":
        obj_xpobapi_list_with_library = make_member_with_library_list_onbatch(base_list=obj_xpobapi_list)
        write_excel_multi_sheet4(join_file_name_xlsx(today,"�I���o�b�`�A�g���Y�֘A��"),[obj_ujobkic_list_with_library,obj_upjobkic_list_with_library,obj_upbkic_list_with_library,obj_xpbkic_file_list,\
                                                                                            obj_xpobapi_list_with_library,obj_xpobapi_variable_list,obj_uxcmdclr_list_with_library],\
                                                                                                ["UJOBKIC","UPJOBKIC","UPBKIC","XPBKIC","XPOBAPI","XPOBAPI_�ϐ�","UXCMDCLR"],path,output_header)
        
        write_excel_multi_sheet4(join_file_name_xlsx(today,"OWFT���Y�֘A��"),[owft_jcl_list,owft_jcl_proc_list,owft_jcl_utach_list,owft_dxliftin_list,\
                                                                                            owft_uftpques_list,owft_uftpendc_list,owft_cobol_list],\
                                                                                                ["OWFT_JCL","OWFT_JCL_PROC","OWFT_JCL_UTACH","OWFT_DXLIFTIN","OWFT_UFTPQUES","OWFT_UFTPENDC","OWFT_COBOL"],path,output_header)
    
       
  
    write_excel_multi_sheet4(join_file_name_xlsx(today,"�ʒ����Ώۈꗗ"),[need_search_and_check_list],["�ʒ����Ώ�"],path,output_header)
    write_excel_multi_sheet4(join_file_name_xlsx(today,"����̔���"),[check_list],["�ʒ����Ώ�"],path,["�ďo�����Y�i�����j","�ďo�����Y�i�����o�̂݁j","�Ăяo�����@","�Ăяo���掑�Y","JOBPROC����","��̍ςݎ��Y"])
    print("�֘A���������ʂ̏o�͂��������܂����B")
    print(time.time()-start,"�b�Ŋ������܂����B")
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])