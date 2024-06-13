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
    
    condition_df = pd.read_excel(COBOL_setting_path,sheet_name="���Y���")
    for cond,val in zip(condition_df["����"],condition_df["�ݒ�"]):
        if cond == "�ݒ����HIT�֘A���o�́i��ID�j":
            �ݒ����HIT���o�� = val == "�o�͂���"
            
        if cond == "�ݒ����HIT�֘A���o�́i����ID�j":
            ���͏���HIT���o�� = val == "�o�͂���"
            
        if cond == "�ݒ����HIT�֘A���o�́i�݌vID�j":
            �݌v����HIT���o�� = val == "�o�͂���"
            
        if cond == "�ݒ����HIT-NG���o��":
            �ݒ����HIT_NG���o�� = val == "�o�͂���"
            
        if cond == "COBOL���o�͊֘A���o��":
            COBOL���o�͏��o�� = val == "�o�͂���"
            
        if cond == "DB�X�V����":
            IsDelete = val == "���s�O�Ɋ֘ATABLE�N���A����"
            
            
        if cond == "���ʏo�̓t�H���_1":
            ������_path = val
            
        if cond == "���ʏo�̓t�H���_1":
            ������_path = val
        
        if cond == "���ʏo�̓t�H���_1":
            �g�[�N�����_path = val
            
        if cond == "���ʃt�@�C���o�͐���i�\�[�X�R�[�h�j":
            ������_out = val == "�o�͂���"
            
        if cond == "���ʃt�@�C���o�͐���i�����͗p�j":
            ������_out = val == "�o�͂���"
            
        if cond == "���ʃt�@�C���o�͐���iİ�ݍč\���p�j":
            �g�[�N�����_out = val == "�o�͂���"
            
            
    if os.path.isdir(title) == False:
        os.makedirs(title)

    COBOLSheet = pd.read_excel(COBOL_setting_path,sheet_name="COBOL�ݒ�V�[�g")
    COBOLSheet.fillna("",inplace=True)
    COBOLSheet = COBOLSheet.values.tolist()
    COBOLSheet = [[""]+sheet for sheet in COBOLSheet]
    COBOLSheet = setting_re_pattern_sheet(COBOLSheet)
    

    ### ���s�O��DB���폜�����I�������ꍇ�ɍ폜����
    if IsDelete == True:
        print("you chose to clear db, so clear the remaining data.")
        
        conn = connect_accdb(db_base_path)

        cursor = conn.cursor()
        
        sql = "DELETE FROM �ACOBOL_���o�͏��1"
        cursor.execute(sql)
        sql = "DELETE FROM �ACOBOL_���o�͏��2"
        cursor.execute(sql)
        sql = "DELETE FROM �ACOBOL_���o�͏��3"
        cursor.execute(sql)
        sql = "DELETE FROM �ACOBOL_�֘A���Y"
        cursor.execute(sql)
        sql = "DELETE FROM �ACOBOL_CMD���"
        cursor.execute(sql)
        sql = "DELETE FROM �ACOBOL_��{���"
        cursor.execute(sql)
        sql = "DELETE FROM ����_PGM_IO���"
        cursor.execute(sql)

        # 'HIT���֘A���폜
        sql = "DELETE FROM ����_���Y���_�֘A���"
        cursor.execute(sql)
        # 'HIT-NG���֘A���폜
        sql = "DELETE FROM ����_���Y���_NG���"
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
        
        
        db_path = title+"\\������DB_"+Folder_name + "_" + str(file_num)+".accdb"
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
                db_path = title+"\\������DB_"+Folder_name+str(file_num)+".accdb"
                command = "copy "+db_base_path + " " + db_path
                subprocess.call(command,shell=True)
                print("create the new accdb file ",db_path)
                
                conn = connect_accdb(db_path)
                cursor =conn.cursor()
                
                
            �t�@�C���� = get_filename(COBOL_File)
            �t�@�C����2 = take_extensions(�t�@�C����)
            print("\r","analysis finished",i,"/",ld,�t�@�C����,end="")
        
            
            
            TmpSheet = analysis1_2_read_text_COBOL(COBOL_File)

            if ������_out == True:
                ActSheet_all,output_header = make_output_list_val_length(TmpSheet,["�s���","�W��","�̈�A����","�̈�B�̂�","���ݽ��","73-80","�����Y�s�ԍ�","�����Y�s���"])

                # output_header = ["�s���","�W��","�̈�A����","�̈�B�̂�","���ݽ��","73-80","�����Y�s�ԍ�","�����Y�s���"]
                write_excel_multi_sheet("�����͌���_"+�t�@�C����2.replace("%","_") + ".xlsx",ActSheet_all,"������",������_path,output_header)
        
        
            
            TokenSheet = analysis1_3_lexical_COBOL(TmpSheet)

            if ������_out == True:
                ActSheet_all,output_header = make_output_list_val_length(TokenSheet,["�s�ԍ����","�s���","�L�q�̈�","�K�w���","TOKEN���"])
 
                # output_header = ["�s�ԍ����","�s���","�L�q�̈�","�K�w���","TOKEN���"]
                write_excel_multi_sheet("�����͌���_"+�t�@�C����2.replace("%","_") + ".xlsx",ActSheet_all,"������",������_path,output_header)
     

            TokenSheet2 = analysis1_4_rebuild_Token_COBOL(TokenSheet)

            if �g�[�N�����_out == True:
                ActSheet_all,output_header = make_output_list_val_length(TokenSheet2,["�s�ԍ����","�s���","�L�q�̈�","�K�w���","������"])
 
                # output_header = ["�s�ԍ����","�s���","�L�q�̈�","�K�w���","������"]
                write_excel_multi_sheet("�g�[�N����͌���_"+�t�@�C����2.replace("%","_") + ".xlsx",ActSheet_all,"�g�[�N�����",�g�[�N�����_path,output_header)
            
     
            analysis1_5_structure_COBOL(TokenSheet2,COBOLSheet,�t�@�C����,db_path, �ݒ����HIT���o��,���͏���HIT���o��,�݌v����HIT���o��,�ݒ����HIT_NG���o��,conn,cursor)
            
            
            if COBOL���o�͏��o��:
                COBOL_IO_Info(TokenSheet2,�t�@�C����,db_path,conn,cursor)
        conn.close()
if __name__ == "__main__":     

    main_all_folder(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])