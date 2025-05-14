#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from PED_DAM import PED_DAM_main_all_folder
from Applied_UTL import Applied_UTL_main
from BMCP import BMCP_main
from JFE_DB import JFE_DB_main

def main(db_path,title,is_skip_jfe_db):
    
    if os.path.isdir(title) == False:
        os.makedirs(title)
        
    # PED_DAM_main_all_folder.main(db_path,title,folder_Schema_path,ped_file_path)
    Applied_UTL_main.main(db_path,title)
    BMCP_main.main(db_path,title)
    
    if is_skip_jfe_db == True:
        print("JFE_DB利用箇所特定解析をスキップします。")
    else:
        JFE_DB_main.main(db_path,title)
   
    
if __name__ == "__main__":
    arg_list = sys.argv
    db_path = arg_list[1]
    title = arg_list[2]
    if len(arg_list) == 4:
        is_skip_jfe_db = arg_list[3]
    else:
        is_skip_jfe_db = False
        
    if type(is_skip_jfe_db) == str:
        is_skip_jfe_db = is_skip_jfe_db == "True"
        
    main(db_path, title, is_skip_jfe_db)