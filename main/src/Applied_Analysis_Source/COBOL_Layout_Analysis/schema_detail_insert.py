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
        sql,values = make_insert_sql("�X�L�[�}_�ڍ׏��",AnalyzeSheet[i][1:],["���C�A�E�g��","�Ώۍs","���x��","�ϐ���","�T�C��","�^�C�v","�^�C�v2","����","G�o�C�g��","�o�C�g��","REDIFINE","OCCURS","���Έʒu","����1","����2","����3","����4"])
        cursor.execute(sql,values)
    conn.commit()
    
    return 