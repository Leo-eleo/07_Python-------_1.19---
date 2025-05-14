#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
import JCL_info_setup
import COBOL_info_setup
import create_level_layout
import layout_analysis_main
import process_UTL_Step_IO
import DD_joint
import Identity_Resolution
import multi_layout_check
import Identity_dsn_set
import shutil
import re
import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

today = str(datetime.date.today())


def main(out_path,base_db_path,jcl_db_path,cobol_db_path,cobol_base_folder,layout_setting_file_path):
    out_folder = out_path
    new_db_path = os.path.join(out_folder,f"�f�[�^���Y_{today}.accdb")

    new_cobol_folder = cobol_base_folder
    new_schema_folder = os.path.join(out_path,"SCHEMA")

    new_single_layout_check_folder = os.path.join(out_path,"�P�̃}���`���C�A�E�gCHECK")
    new_some_layout_check_folder = os.path.join(out_path,"�����}���`���C�A�E�gCHECK")

    if os.path.exists(out_folder) == False:
        os.makedirs(out_folder)
        
    if os.path.exists(new_cobol_folder) == False:
        os.makedirs(new_cobol_folder)

    if os.path.exists(new_schema_folder) == False:
        os.makedirs(new_schema_folder)

    if os.path.exists(new_single_layout_check_folder) == False:
        os.makedirs(new_single_layout_check_folder)

    if os.path.exists(new_some_layout_check_folder) == False:
        os.makedirs(new_some_layout_check_folder)

    if os.path.exists(new_db_path) == False:
        shutil.copy(base_db_path,new_db_path)

    ### �����͌��ʂ̐ݒ�
    COBOL_info_setup.main(new_db_path,cobol_db_path)
    JCL_info_setup.main(new_db_path,jcl_db_path)
    
    ### �X�L�[�}�t�@�C���쐬
    create_level_layout.main(new_db_path,new_cobol_folder,new_schema_folder)
    
    ### �X�L�[�}�t�@�C���̃��C�A�E�g���
    layout_analysis_main.main(new_db_path,new_schema_folder,layout_setting_file_path,True,True,new_single_layout_check_folder)
    
    ### �e��DSN���񂹏���
    process_UTL_Step_IO.process_UTL_Step_IO_main(new_db_path,out_folder)
    DD_joint.DD_joint_main(new_db_path,out_folder)

    utl_step_excel_path = os.path.join(out_folder,f"UTL_STEP��_IO���(���H).xlsx")
    dd_joint_excel_path = os.path.join(out_folder,f"QRY_DD�A�����.xlsx")

    Identity_dsn_set.main(new_db_path,dd_joint_excel_path,utl_step_excel_path)
    Identity_Resolution.identity_resolution_main(new_db_path,out_folder)

    ### ���񂹏����� �����}���`���C�A�E�g���
    multi_layout_check.muiti_layout_main(new_db_path,out_folder,"�@�f�[�^�Z�b�g�O���[�v",new_some_layout_check_folder)
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])