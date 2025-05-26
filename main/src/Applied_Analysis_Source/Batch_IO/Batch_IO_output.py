#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *
from Applied_IO_Info import Applied_IO_Info_main
from Test_Step_Import import test_step_import

import warnings

dsn_dic = {}
io_header = ["TEST_ID","DSN","���{�ꖼ��(DSN)","�f�[�^���","��̓���","��̏ƍ�"]
test_io_info_all = []
def make_output_file(io_list,title,test_id,keys):
    if io_list == []:
        return
    
    global dsn_dic
    global test_io_info_all
    assert "��̔���" in keys
    assert "DSN" in keys
#'20240604 UPD qian.e.wang ���쌧�M�e�X�gIO�o�͑Ή�
#    assert "�f�[�^���" in keys
    assert "�f�[�^���2" in keys
#'UPD END
    
    receive_idx = keys.index("��̔���")
    dsn_idx = keys.index("DSN")
#'20240604 UPD qian.e.wang ���쌧�M�e�X�gIO�o�͑Ή�
#    data_idx = keys.index("�f�[�^���")
    data_idx = keys.index("�f�[�^���2")
#'UPD END
    test_io_info = []
    
#'20250202 UPD qian.e.wang ���쌧�M�e�X�gIO�o�͑Ή�
#    for list_now in io_list:
    
    # ���j�[�N�������̒ǉ�
    unique_io_list = [list(t) for t in set(tuple(item) for item in io_list)]
    
    for list_now in unique_io_list:
# UPD END
        if "����" in list_now[receive_idx] or "�ƍ�" in list_now[receive_idx]:
            dsn = list_now[dsn_idx]
            data = list_now[data_idx]
            dsn_japanese = dsn_dic.get(dsn,"")
            receive_input = ""
            receive_collation = ""
            
            if "����" in list_now[receive_idx]:
                receive_input = "��"
            
            if "�ƍ�" in list_now[receive_idx]:
                receive_collation = "��"
            
            io_info = [test_id,dsn,dsn_japanese,data,receive_input,receive_collation]
            test_io_info.append(io_info)
            test_io_info_all.append(io_info)

#'20250202 UPD qian.e.wang ���쌧�M�e�X�gIO�o�͑Ή�
#    write_excel_multi_sheet3(test_id + ".xlsx",[io_list,test_io_info],["���p_���o�͏��o��","�e�X�gIO���"],title,[keys,io_header])
    write_excel_multi_sheet3(test_id + ".xlsx",[unique_io_list,test_io_info],["���p_���o�͏��o��","�e�X�gIO���"],title,[keys,io_header])
# UPD END
    
    return 

def main(db_path,excel_path,title):
    global dsn_dic
    global test_io_info_all
    if os.path.isdir(title) == False:
        os.makedirs(title)
    
#'20250202 ADD qian.e.wang ���쌧�M�e�X�gIO�o�͑Ή�
    # ����̌x�����b�Z�[�W�𖳎�
    warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy connectable")
    warnings.filterwarnings("ignore", message="Setting an item of incompatible dtype is deprecated and will raise an error in a future version of pandas.")
# ADD END
    
    test_step_import.analysis1_main(db_path,title)
    Applied_IO_Info_main.main(db_path,title)
    
    conn = connect_accdb(db_path)
    sql = "SELECT * FROM TEST_�e�X�g���{�P��"
    df_starting_point = pd.read_sql(sql,conn)
    df_starting_point.fillna("",inplace=True)
    starting_point_to_out_folder_dic = {}
    for test_id,out_folder in zip(df_starting_point["TEST_ID"],df_starting_point["�o�̓t�H���_"]):
        if test_id not in starting_point_to_out_folder_dic:
            starting_point_to_out_folder_dic[test_id] = []
        starting_point_to_out_folder_dic[test_id].append(out_folder)
        
        
    dsn_df = pd.read_excel(excel_path,sheet_name="DSN����")
    dsn_df.fillna("",inplace=True)
    dsn_dic = {dsn:name for dsn,name in zip(dsn_df["�f�[�^�Z�b�g��"],dsn_df["���{�ꖼ��"])}
    
#'20250129 UPD qian.e.wang ���쌧�M�e�X�gIO�o�͑Ή�
    # io_out_path = os.path.join(title,"���p���o�͉��.xlsx")
    
    # io_df = pd.read_excel(io_out_path,sheet_name="���p���o��")
    # �`�����N���ƂɈقȂ�V�[�g���œǂݍ���
    all_chunks = []
    i=0
    
    while True:
        try:
            # �`�����N���Ƃ̏o�̓t�@�C�����𐶐�
            io_out_path = os.path.join(title, f'���p���o�͉��_{i+1}.xlsx')
            
            # �t�@�C�������݂���ꍇ�̂ݓǂݍ���
            if os.path.exists(io_out_path):
                chunk=pd.read_excel(io_out_path,sheet_name=f'���p���o��')
                all_chunks.append(chunk)
                i+=1
            else:
                break
        
        except ValueError:
            break
    
    # �󃊃X�g�̃`�F�b�N
    if not all_chunks:
        print("No data to concatenate for all_chunks")
        return
    
    io_df=pd.concat(all_chunks) 
# UPD END
    
    io_df.fillna("",inplace=True)
    keys = io_df.columns.tolist()
    
    if "JCL_MBR" in keys:
        keys = keys[:keys.index("JCL_MBR")]
    else:
        print("�f�[�^���z�肳�ꂽ�`���ł͂���܂���B")
    
#'20250202 ADD qian.e.wang ���쌧�M�e�X�gIO�o�͑Ή�
    unique_io_set = set()
# ADD END
    
    io_list = []
    last = ""
    for i in range(len(io_df)):
        data = io_df.iloc[i]
        test_id_now = data["TEST_ID"]
        list_now = [data[key] for key in keys]
        
        if test_id_now != last:
            
            if last not in starting_point_to_out_folder_dic:
                starting_point_to_out_folder_dic[last] = [""]
                
                
            for out_folder in starting_point_to_out_folder_dic[last]:
                if out_folder == "":
                    out_title = title
                else:
                    out_title = os.path.join(title,out_folder)
                
                if os.path.isdir(out_title) == False:
                    os.makedirs(out_title)
                    
                make_output_file(io_list,out_title,last,keys)
                    
            
            io_list = []
            
        io_list.append(list_now)
        last = test_id_now
    
    if last not in starting_point_to_out_folder_dic:
        starting_point_to_out_folder_dic[last] = [""]
            
    for out_folder in starting_point_to_out_folder_dic[last]:
        if out_folder == "":
            out_title = title
        else:
            out_title = os.path.join(title,out_folder)
        
        if os.path.isdir(out_title) == False:
            os.makedirs(out_title)
            
        make_output_file(io_list,out_title,last,keys)
    
#'20250202 UPD qian.e.wang ���쌧�M�e�X�gIO�o�͑Ή�
    # ���j�[�N�������̒ǉ�
    unique_io_info_all = [list(t) for t in set(tuple(item) for item in test_io_info_all)]
    
#    write_excel_multi_sheet3("�e�X�gIO���_�}�[�W.xlsx",[test_io_info_all],["�e�X�gIO���"],title,[io_header])
    write_excel_multi_sheet3("�e�X�gIO���_�}�[�W.xlsx",[unique_io_info_all],["�e�X�gIO���"],title,[io_header])
# UPD END
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3])
    