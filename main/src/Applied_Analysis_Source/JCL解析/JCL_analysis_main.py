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

    condition_df = pd.read_excel(JCL_setting_path,sheet_name="���Y���")
    for cond,val in zip(condition_df["����"],condition_df["�ݒ�"]):
        if cond == "�ݒ����HIT�֘A���o�́i��ID�j":
            �ݒ����HIT���o�� = val == "�o�͂���"
            
        if cond == "�ݒ����HIT�֘A���o�́i����ID�j":
            ���͏���HIT���o�� = val == "�o�͂���"
            
        if cond == "�ݒ����HIT�֘A���o�́i�݌vID�j":
            �݌v����HIT���o�� = val == "�o�͂���"
            
        if cond == "�ݒ����HIT-NG���o��":
            �ݒ����HIT_NG���o�� = val == "�o�͂���"
            
        if cond == "DB�X�V����":
            IsDelete = val == "���s�O�Ɋ֘ATABLE�N���A����"
            
        if cond == "PROC��͑Ώې���":
            IsPROCLimit = val == "JCL����̌ďo������PROC�̂݉�͂���"
            
        if cond == "A-AUTO������Ǘ�":
            a_auto = val
            
        
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
            
            
    JCLSheet = pd.read_excel(JCL_setting_path,sheet_name="JCL�ݒ�V�[�g")
    JCLSheet.fillna("",inplace=True)
    JCLSheet = JCLSheet.values.tolist()
    JCLSheet = [[""]+sheet for sheet in JCLSheet]
    JCLtoPROCSheet = pd.read_excel(JCL_setting_path,sheet_name="JCL�ďo����J�^�v���ꗗ")
    JCLtoPROCSheet = JCLtoPROCSheet["�J�^�v����"]
    JCLtoPROCset = set(JCLtoPROCSheet.values.tolist())
    JCL_Files = glob_files(Folder_JCL_path)

    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    if IsDelete:
        print("you chose to clear db, so clear the remaining data.")
        
        sql = "DELETE FROM �@JCL_��{���"
        cursor.execute(sql)
        sql = "DELETE FROM �@JCL_STEP_SYSIN"
        cursor.execute(sql)
        sql = "DELETE FROM �@JCL_STEP���"
        cursor.execute(sql)
        sql = "DELETE FROM �@JCL_PGM_DSN"
        cursor.execute(sql)
        sql = "DELETE FROM �@JCL_CMD���"
        cursor.execute(sql)
        sql = "DELETE FROM �@PROC_PARM"
        cursor.execute(sql)
        # 'HIT���֘A���폜
        sql = "DELETE FROM ����_���Y���_�֘A���"
        cursor.execute(sql)
        # 'HIT-NG���֘A���폜
        sql = "DELETE FROM ����_���Y���_NG���"
        cursor.execute(sql)
        conn.commit()
  
    
    print("finish preparation and start analysis.")
    ld = len(JCL_Files)
    for i,JCL_File in enumerate(JCL_Files):
        �t�@�C���� = get_filename(JCL_File)
        �t�@�C����2 = take_extensions(�t�@�C����)
        print("\r","analysis finished",i,"/",ld,�t�@�C����,end="")
        
        if IsPROCLimit and �t�@�C����2 not in JCLtoPROCset:
            print(�t�@�C����2+"��JCL����̌ďo���Ȃ����߉�͂��X�L�b�v���܂��B")
            continue

        TmpSheet = analysis1_2_read_text_JCL(JCL_File,a_auto)
        
        if ������_out == True:
            ActSheet_all,output_header = make_output_list_val_length(TmpSheet,["�s���","NAME","CMD","PARM","COMMENT","PARM�p��","�p��","������","�����Y�s�ԍ�","�����Y�s���","A-AUTO������"])
   
            # output_header = ["�s���","NAME","CMD","PARM","COMMENT","PARM�p��","�p��","������","�����Y�s�ԍ�","�����Y�s���","A-AUTO������"]
            write_excel_multi_sheet("�����͌���_"+�t�@�C����2.replace("%","_") + ".xlsx",ActSheet_all,"������",������_path,output_header)
        

        TokenSheet = analysis1_3_lexical_JCL(TmpSheet)
        
        if ������_out == True:
            ActSheet_all,output_header = make_output_list_val_length(TokenSheet,["�����Y�s","ID�s","NAME�s","CMD�s","P����","AAUTO����","PARM�s"])
            
            # output_header = ["�����Y�s","ID�s","NAME�s","CMD�s","P����","AAUTO����","PARM�s"]
            write_excel_multi_sheet("�����͌���_"+�t�@�C����2.replace("%","_") + ".xlsx",ActSheet_all,"������",������_path,output_header)
     
        TokenSheet2 = analysis1_4_rebuild_Token_JCL(TokenSheet)

        if �g�[�N�����_out == True:
            ActSheet_all,output_header = make_output_list_val_length(TokenSheet2,["�����Y�s�ԍ�","�s����","AAUTO����","NAME","CMD","PARM"])
     
            # output_header = ["�����Y�s�ԍ�","�s����","AAUTO����","NAME","CMD","PARM"]
            write_excel_multi_sheet("�g�[�N����͌���_"+�t�@�C����2.replace("%","_") + ".xlsx",ActSheet_all,"�g�[�N�����",�g�[�N�����_path,output_header)
            
        
        analysis1_5_structure_JCL(TokenSheet2,JCLSheet,�t�@�C����,conn,cursor, �ݒ����HIT���o��,���͏���HIT���o��,�݌v����HIT���o��,�ݒ����HIT_NG���o��)

    conn.close()
    
if __name__ == "__main__":     
    main(sys.argv[1],sys.argv[2],sys.argv[3])