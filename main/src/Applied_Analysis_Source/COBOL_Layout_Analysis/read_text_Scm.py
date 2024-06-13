#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

import unicodedata

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *



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

def read_text_Scm(Filename):
    
    global レイアウト行数
    
    TmpSheet = []
  
    GYO = 1

    chk_end = False
    
    with open(Filename) as TS:
        for strREC in TS:

            strREC = strREC.replace("\n","")
            # tmpstr = StrConv(strREC, vbFromUnicode, 1041)
            tmpstrOutstr = get_ZENKAKU_str(strREC,7,65)
            
            if Trim(tmpstrOutstr) != "": 
                if "PROCEDURE" in tmpstrOutstr and "DIVISION" in tmpstrOutstr:
                    chk_end = True
                else:
                    if get_ZENKAKU_str(strREC,6,1) != "*":
                        TmpSheet.append(tmpstrOutstr)
                        GYO = GYO + 1
  
            if chk_end:
                break

    レイアウト行数 = GYO
        
    return TmpSheet