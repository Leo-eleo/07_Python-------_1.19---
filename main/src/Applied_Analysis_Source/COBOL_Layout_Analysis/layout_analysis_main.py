#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

from read_text_Scm import read_text_Scm
from lexical_Scm import lexical_Scm
from rebuild_Token_Scm import rebuild_Token_Scm
from structure_Scm import structure_Scm
from schema_detail_insert import schema_insert_main
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

def main(db_path, Folder_Scm_path, Scm_setting_path,detail_insert=False,IsDelete=True,multicheck_folder=None):

    print("start preparation for analysis.")

    ScmSheet = pd.read_excel(Scm_setting_path,sheet_name="COPY��ݒ�V�[�g�C��")
    ScmSheet.fillna("",inplace=True)
    ScmSheet = ScmSheet.values.tolist()
    ScmSheet = [[""]+sheet for sheet in ScmSheet]

    Scm_Files = glob_files(Folder_Scm_path)

    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    if IsDelete:
        print("you chose to clear db, so clear the remaining data.")
        
        sql = "DELETE FROM �X�L�[�}_��{���"
        cursor.execute(sql)
        sql = "DELETE FROM �X�L�[�}_�ڍ׏��"
        cursor.execute(sql)
        sql = "DELETE FROM ����_���Y���_�֘A���"
        cursor.execute(sql)
        sql = "DELETE FROM ����_���Y���_NG���"
        cursor.execute(sql)
        sql = "DELETE FROM ���C�A�E�g��͏��"
        cursor.execute(sql)
        conn.commit()
  
    
    print("finish preparation and start analysis.")
    ld = len(Scm_Files)
    for i,Scm_File in enumerate(Scm_Files):
        if "desktop" in Scm_File:
            continue
        try:
            �t�@�C���� = get_filename(Scm_File)
            �t�@�C����2 = take_extensions(�t�@�C����)
            print("\r","analysis finished",i,"/",ld,�t�@�C����,end="")
            

            TmpSheet = read_text_Scm(Scm_File)
            TmpSheet_edit = [[i] for i in TmpSheet]
            # m = 0
            # for i in TmpSheet_edit:
            #     m = max(m,len(i))
            # ActSheet_all = []
            # for i in TmpSheet_edit:
            #     ActSheet_all.append(i+[""]*(m-len(i)))
            
            # output_header = [""]*m
            # write_excel_multi_sheet("������1.xlsx",ActSheet_all,"������",title,output_header)
            TokenSheet = lexical_Scm(TmpSheet)

            # m = 0
            # for i in TokenSheet:
            #     m = max(m,len(i))
            # ActSheet_all = []
            # for i in TokenSheet:
            #     ActSheet_all.append(i+[""]*(m-len(i)))
            
            # output_header = [""]*m
            # write_excel_multi_sheet("������2.xlsx",ActSheet_all,"������",title,output_header)
            TokenSheet2 = rebuild_Token_Scm(TokenSheet,�t�@�C����)

            # m = 0
            # for i in TokenSheet2:
            #     m = max(m,len(i))
            # ActSheet_all = []
            # for i in TokenSheet2:
            #     ActSheet_all.append(i+[""]*(m-len(i)))
            
            
            # output_header = [""]*m
            # write_excel_multi_sheet("������.xlsx",ActSheet_all,"������",title,output_header)
            
            ���C�A�E�g�s�� = len(TmpSheet)
            AnalyzeSheet = structure_Scm(TokenSheet2,ScmSheet,�t�@�C����,True,conn,cursor,���C�A�E�g�s��,multicheck_folder)
            
            # m = 0
            # for i in AnalyzeSheet:
            #     m = max(m,len(i))
            # ActSheet_all = []
            # for i in AnalyzeSheet:
            #     ActSheet_all.append(i+[""]*(m-len(i)))
            
            
            # output_header = [""]*m
            # write_excel_multi_sheet("�\�����.xlsx",ActSheet_all,"�\�����",title,output_header)
            
            if detail_insert:
                schema_insert_main(AnalyzeSheet,conn,cursor)
                
        except:
            print("Error at :",�t�@�C����)
    conn.close()
    
if __name__ == "__main__":
    if len(sys.argv) >= 5:
        detail_insert = sys.argv[4]
    else:
        detail_insert = False
    main(sys.argv[1],sys.argv[2],sys.argv[3],detail_insert)