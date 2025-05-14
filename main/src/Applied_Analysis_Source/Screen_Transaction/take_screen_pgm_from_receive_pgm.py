#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
import re
import unicodedata
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


reg_when = "WHEN\(\(\'(?P<screen_name>[0-9]+?)\'\)\)"
reg_when = re.compile(reg_when)
        
reg_mod = "MOD\((?P<pgm_id>\S+?)\)"
reg_mod = re.compile(reg_mod)
        
def get_ZENKAKU_str(string,HANKAKU_start,HANKAKU_len):
    num = 0
    for i,s in enumerate(string):
        if unicodedata.east_asian_width(s) in "FWA":
            num += 2
        else:
            num += 1
        if num == HANKAKU_start:
            string = string[i+1:]
            break
    if num < HANKAKU_start:
        return ""
    num = 0
    for i,s in enumerate(string):
        if unicodedata.east_asian_width(s) in "FWA":
            num += 2
        else:
            num += 1
        if num == HANKAKU_len:
            return string[:i+1]
    
    return string

def get_transaction_from_receive_pgm(receive_file,file_name,transaction_list):
    
    with open(receive_file,encoding="shift-jis",errors="ignore") as f:
        
        lines = []
        for line in f:
            if "/*" in line:
                continue
            lines.append(get_ZENKAKU_str(line,0,72))
        
        data1 = re.split(';|\\.\s|,', ' '.join(lines))
        
        for line in data1:
            if "WHEN" not in line:
                continue
            
            if "CCALL" not in line:
                continue
            if "MOD" not in line:
                continue
            lines = ArrayEmptyDelete(line.split(" "))
            
            when_cand = ""
            mod_cand = ""
            for cand in lines:
                if "WHEN" in cand:
                    search = re.search(reg_when,cand)
                    if search:
                        when_cand = search.group("screen_name")
            
                if "MOD" in cand:
                    search = re.search(reg_mod,cand)
                    if search:
                        mod_cand = search.group("pgm_id")
                        transaction_list.add((file_name,when_cand,mod_cand))
            

    return transaction_list
def main(receive_path,title):
    
    today = str(datetime.date.today())
    receive_files = glob_files(receive_path)
    
    transaction_list = set()
    
    ld = len(receive_files)
    
    for i,receive_file in enumerate(receive_files):
        file_name = os.path.split(receive_file)[-1]
        file_name = take_extensions(file_name)
        print("\r","analysis finished",i,"/",ld,file_name,end="")
        
        transaction_list = get_transaction_from_receive_pgm(receive_file,file_name,transaction_list)
        
    write_excel_multi_sheet3(join_file_name_xlsx(today,"受信振分⇒画面関連性"),[sorted(transaction_list)],["受信振分_画面関連性"],title,[["資産名","画面コード","PGM-ID"]])
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])