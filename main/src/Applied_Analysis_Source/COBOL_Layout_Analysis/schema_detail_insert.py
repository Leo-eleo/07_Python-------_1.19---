#!/usr/bin/env python
# -*- coding: cp932 -*-
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


def schema_insert_main(AnalyzeSheet,conn,cursor):
    
    
    for i in range(len(AnalyzeSheet)):
        if type(AnalyzeSheet[i][2]) == int:
            AnalyzeSheet[i][2] += 1
        sql,values = make_insert_sql("スキーマ_詳細情報",AnalyzeSheet[i][1:],["レイアウト名","対象行","レベル","変数名","サイン","タイプ","タイプ2","桁数","Gバイト数","バイト数","REDIFINE","OCCURS","相対位置","属性1","属性2","属性3","属性4"])
        cursor.execute(sql,values)
    conn.commit()
    
    return 