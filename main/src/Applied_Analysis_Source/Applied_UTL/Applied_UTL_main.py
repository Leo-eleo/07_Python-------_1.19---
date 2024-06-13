#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import sys

sys.path.append(os.path.dirname(__file__))
import time

from analysis1_UTL_analysis import analysis1_UTL_analysis
from analysis2_DFSRRC00 import analysis2_DFSRRC00
from analysis4_EASY_analysis import analysis4_EASY_analysis
from analysis5_JCL_PGM_SYSIN_SEPARATE import analysis5_JCL_PGM_SYSIN_SEPARATE

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


DB�����o�^��PARM = "�����ݒ�iUTL��́j"
def main(db_path,title):
    
    start = time.time()
    if os.path.isdir(title) == False:
        os.makedirs(title)
    
    ### ����DB�폜
    
    
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    
    
    # sql,values = make_delete_sql("�ڋq��_���Y�֘A�����",[DB�����o�^��PARM],["�o�^����"])
    # cursor.execute(sql,values)
    
    #sql = "SELECT * FROM �ڋq��_���Y�֘A����� WHERE �o�^���� = '�����ݒ�iUTL��́j'"
    #df = pd.read_sql(sql,conn)
    #keys = df.columns.tolist()
    #for i in range(len(df)):
    #    data = df.iloc[i]
    #    values = [data[key] for key in keys]
    #    
    #    sql,values = make_delete_sql("�ڋq��_���Y�֘A�����",values,keys)
    #    cursor.execute(sql,values)
 
    # sql,values = make_delete_sql("�ڋq��_JCL_PGM_DSN",["",DB�����o�^��PARM],["�蓮�X�VFLG","�����X�VFLG"])
    # cursor.execute(sql,values)

    sql = "SELECT * FROM �ڋq��_JCL_PGM_DSN WHERE �蓮�X�VFLG = '' AND �����X�VFLG = '�����ݒ�iUTL��́j'"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("�ڋq��_JCL_PGM_DSN",values,keys)
        cursor.execute(sql,values)
    
    # sql,values = make_delete_sql("UTL_STEP��_IO���",[DB�����o�^��PARM],["�⑫"])
    # cursor.execute(sql,values)
    
    sql = "SELECT * FROM UTL_STEP��_IO��� WHERE �⑫ = '�����ݒ�iUTL��́j'"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("UTL_STEP��_IO���",values,keys)
        cursor.execute(sql,values)
        
    print("DB�폜����", time.time()-start)
    
    ActSheet_all = []
 
    ActSheet,conn,cursor = analysis1_UTL_analysis(db_path,conn,cursor)
    ActSheet_all += ActSheet
    
    print("���1����", time.time()-start)
    ActSheet_all += analysis2_DFSRRC00(conn,cursor)
    print("���2����", time.time()-start)
    
    ActSheet_all += analysis4_EASY_analysis(conn,cursor)
    print("���4����", time.time()-start)
    analysis5_JCL_PGM_SYSIN_SEPARATE(conn,cursor)
    print("���5����", time.time()-start)
    ActSheet_all = [ActSheet[1:] for ActSheet in ActSheet_all]
    print(len(ActSheet_all))
    output_header = ["LIBRARY_ID","JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP_ID","PGM_NAME","PROC_NAME","SYSIN_PGM","SYSIN_SEQ","SYSIN","��͎����b�Z�[�W","���Y�֘A��","DSN�ǉ�","DSN�X�V","STEP_IO�ǉ�/�X�V","�֘A�L�[���","","STEP_SYSIN�X�V"]
    write_excel_multi_sheet("���pUTL.xlsx",ActSheet_all,"���p_UTL���",title,output_header)
    
    
if __name__ == "__main__":
    # Debug
    # db_path = (
    #     r"C:\WORK\tmp\���Y�Č�\���C�A�E�g��͗p\������DB_202310��̎��Y_�e�X�gIO�o�͗p.accdb"
    # )
    # title = r"C:\WORK\tmp\���Y�Č�\���C�A�E�g��͗p"
    # main(db_path,title)
    # Release
    main(sys.argv[1],sys.argv[2])