#!/usr/bin/env python
# -*- coding: shift-jis -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


def asm_split_line(line):
    split_list = []
    
    if line == "":
        return split_list
    
    if line[0] != " ":
        label = line[:line.index(" ")]
        line = line[line.index(" "):]
    else:
        label = ""
        
    split_list.append(label)
    
    literal = []
    now_word = ""
    for s in line:
        
        if s == " ":
            if literal:
                now_word += s
            elif now_word:
                split_list.append(now_word)
                now_word = ""
            
            continue
        
        now_word += s
        if s == "'":
            if literal and literal[-1] == s:
                literal.pop()
            else:
                literal.append(s)
        
        elif s == '"':
            if literal and literal[-1] == s:
                literal.pop()
            else:
                literal.append(s)
                
    
    if now_word:
        split_list.append(now_word)
        
    return split_list

def asm_split_text(asm_file,output_list):
    
    asm_file_name = os.path.split(asm_file)[-1]
    
    with open(asm_file,"r",errors="ignore") as f:
        for line_num,line in enumerate(f,1):
            line = line.replace("\n","")
            line_list = ["",asm_file_name,line_num,line] + asm_split_line(line)
            output_list.append(line_list)
    
    return output_list

def main(asm_file_path,title):
    
    asm_files = glob_files(asm_file_path)
    
    output_list = []
    
    for asm_file in asm_files:
        output_list = asm_split_text(asm_file,output_list)
        
        
    output_list,output_header = make_output_list_val_length(output_list,["ファイル名","行番号","行情報","ラベル","オペランド1","オペランド2","オペランド3","オペランド4"])
    
    write_excel_multi_sheet("ASM解析結果.xlsx",output_list,"ASM解析",title,output_header)

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])