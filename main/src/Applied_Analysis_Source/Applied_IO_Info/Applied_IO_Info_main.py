#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
sys.path.append(os.path.dirname(__file__))
import time
from analysis0 import analysis0
from analysis1 import analysis1
from analysis3 import analysis3
from analysis4 import analysis4

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

def main(db_path,title):
    
    start = time.time()

    if os.path.isdir(title) == False:
        os.makedirs(title)
        
        
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    output_header = analysis0()[1:]
    
#'20250202 UPD qian.e.wang ���쌧�M�e�X�gIO�o�͑Ή�
    # TEST_�e�X�g���{�P�ʃe�[�u������f�[�^���擾
    sql = "SELECT * FROM TEST_�e�X�g���{�P��"
    df_test_units = pd.read_sql(sql, conn)
    df_test_units.fillna("", inplace=True)
    
    # �ŏ��ɋ󃊃X�g�Ƃ��Đ錾
    ActSheet_testid = []
    ActSheet_all = []
    # ���������p�ϐ��錾
    i = 1
    chunk_size = 500000  # �K�؂ȃ`�����N�T�C�Y�ɒ������Ă�������[EXCEL�ő�l1000000]
    
    # TEST_ID���Ƃɏ��������s
    for test_id in df_test_units["TEST_ID"].unique():
        print(f"Processing TEST_ID: {test_id}")
        
        # ���sJOB�̃��X�g�𒊏o
        job_list = df_test_units[df_test_units["TEST_ID"] == test_id]["���sJOB"].tolist()
        
        # analysis1�̃��R�[�h���o������WHERE������ǉ�
        # ActSheet_all = analysis1(conn,cursor)
        ActSheet_testid = analysis1(conn, cursor, test_id, job_list)
        
        # �f�o�b�O�p�F�e�X�e�b�v��̃T�C�Y�m�F
        # print("Initial data size:", len(ActSheet_all))
        print("Initial data size:", len(ActSheet_testid))
        
        # �d���r������
        unique_ActSheet = [list(t) for t in set(tuple(item) for item in ActSheet_testid)]
        
        # �\�[�g����
        # ActSheet_all.sort(key=lambda x: (x[1],x[2],x[5],x[7],x[8],x[22]))
        unique_ActSheet.sort(key=lambda x: (x[1], x[2], x[5], x[7], x[8], x[22]))
        
        print(f"Unique  data size: {len(unique_ActSheet)}")
        print(test_id, "���1����", time.time()-start)
        
        ### ���p_���o�͏��o��_2
        # ActSheet_all = analysis3(ActSheet_all,conn,cursor)
        unique_ActSheet = analysis3(unique_ActSheet,conn,cursor)
        print(test_id, "���3����", time.time()-start)
        
        ### TEST_���o�͏��e�[�u���֔��f
        # analysis4(ActSheet_all,conn,cursor)
        # �ꎞ�I�ɓ��o�͏��DB�o�͂�}�~
        # analysis4(unique_ActSheet,conn,cursor)
        # print(test_id, "���4����", time.time()-start)
        
        # unique_ActSheet �� ActSheet_all �ɒǉ�
        ActSheet_all.extend(unique_ActSheet)
        
        # ActSheet_testid ��������
        ActSheet_testid = []
        
        # �f�o�b�O�p�F�e�`�����N���Ƃ̌����m�F
        print(f"Chunk {i}: Number of Records: {len(ActSheet_all)}")
        if len(ActSheet_all) >= chunk_size:
            # �f�o�b�O�p�F�e�`�����N���Ƃ̃J�������m�F
            print(f"Chunk {i}: Number of columns in ActSheet_all: {len(ActSheet_all[0])}")
            print(f"Chunk {i}: Number of columns in output_header: {len(output_header)}")
                
            df_chunk = pd.DataFrame(ActSheet_all, columns=output_header)
            # �`�����N���Ƃ̏o�̓t�@�C�����𐶐�
            output_file = os.path.join(title, f"���p���o�͉��_{i}.xlsx")
            
            # �t�@�C�������ɑ��݂���΍폜
            if os.path.exists(output_file):
                os.remove(output_file)
            
            # Excel�t�@�C���ւ̏�������
            with pd.ExcelWriter(output_file, mode='w', engine='openpyxl') as writer:
                df_chunk.to_excel(writer, sheet_name=f'���p���o��', index=False)
            
            ActSheet_all = []  # �󃊃X�g�ɏ�����
            df_chunk = None  # df_chunk ��������
            i += 1
    
    # �f�o�b�O�p�F�ŏI�`�����N�̌����m�F
    print(f"Chunk {i}: Number of Records: {len(ActSheet_all)}")
    if len(ActSheet_all) > 0:
        # �f�o�b�O�p�F�ŏI�`�����N�̃J�������m�F
        print(f"Chunk {i}: Number of columns in ActSheet_all: {len(ActSheet_all[0])}")
        print(f"Chunk {i}: Number of columns in output_header: {len(output_header)}")
        
        df_chunk = pd.DataFrame(ActSheet_all, columns=output_header)
        # �`�����N���Ƃ̏o�̓t�@�C�����𐶐�
        output_file = os.path.join(title, f"���p���o�͉��_{i}.xlsx")
        
        # �t�@�C�������ɑ��݂���΍폜
        if os.path.exists(output_file):
            os.remove(output_file)
        
        # Excel�t�@�C���ւ̏�������
        with pd.ExcelWriter(output_file, mode='w', engine='openpyxl') as writer:
            df_chunk.to_excel(writer, sheet_name=f'���p���o��', index=False)
        
        df_chunk = None  # df_chunk ��������
    
    print("Data processing completed")
# UPD END
    
    conn.close()
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])