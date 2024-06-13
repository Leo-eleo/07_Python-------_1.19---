#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
import re
import unicodedata
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


reg = "INIT\(\'(?P<tran_name>[0-9]{5})\'\)"
reg = re.compile(reg)
        
        
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

def get_transaction_from_pl1(pl1_file,file_name,transaction_list):
    # print(file_name)
    with open(pl1_file,encoding="shift-jis",errors="ignore") as f:
        
        lines = []
        for line in f:
            if "/*" in line:
                continue
            lines.append(get_ZENKAKU_str(line,0,72))
            # print(lines[-1])

        
        data1 = re.split(';|\\.\s|,', ' '.join(lines))
        
        for line in data1:
            if "INIT(" not in line:
                continue
            
            search = reg.search(line)
            if search:
                if "CHAR" not in line:
                    print("CHAR構文がありません。想定外のパターンのため。確認が必要です。")
                    print("file name = {}".format(file_name))
                    print("error source = {}".format(line))
                    
                tran_name = search.group("tran_name")
                lines = ArrayEmptyDelete(line.split(" "))
                val_name = ""
                for s in lines:
                    if s == "STATIC":
                        continue
                    
                    if s == "CHAR(5)" or s == "CHAR(05)":
                        transaction_list.add((file_name,val_name,tran_name))
                        break
                    val_name = s
                
                
            # reg = "\s+?(?P<name>\S*)\s+?CHAR\((5|05)\)\s*\S*\s*INIT\(\'(?P<tran_name>[0-9]{5})\'\)"
            # reg = re.compile(reg)
            # search = reg.search(line)
            # if search:
            #     # print("find match")
            #     lines = ArrayEmptyDelete(line.split(" "))
            #     lines = " ".join(lines)
            #     print(lines)
            #     # print(line,search.group("tran_name"),"tran_name",search.group("name"))

    return transaction_list
def main(pl1_path,title):
    
    today = str(datetime.date.today())
    pl1_files = glob_files(pl1_path)
    
    transaction_list = set()
    
    finish_file_set = set()
    ld = len(pl1_files)
    
    for i,pl1_file in enumerate(pl1_files):
        file_name = os.path.split(pl1_file)[-1]
        file_name = take_extensions(file_name)
        print("\r","analysis finished",i,"/",ld,file_name,end="")
        if file_name.endswith("N") and file_name[:-1] in finish_file_set:
            continue
        
        finish_file_set.add(file_name)
        
        transaction_list = get_transaction_from_pl1(pl1_file,file_name,transaction_list)
        
    write_excel_multi_sheet3(join_file_name_xlsx(today,"PGM⇒取引コード関連性"),[sorted(transaction_list)],["PGM_取引コード関連性"],title,[["資産名","変数名","取引コード"]])
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])