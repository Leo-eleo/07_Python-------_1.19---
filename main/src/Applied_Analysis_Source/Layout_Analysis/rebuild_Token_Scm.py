#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *



def ���s����_COBOL():
    global  ���O�g�[�N��,���O�g�[�N��2,���s����FLG,����������
    # '���s����t���O
    # 'EXEC SQL �` END-EXEC �Ȃǂ̓r���ɉ��s�L�[���[�h�����Ă����s�����Ȃ��悤�ɐ��䂷��
    if ���s����FLG:
        if ���������� == "END-EXEC":
            ���s����FLG = False
            return True  #'���ۂɉ��s�ɂȂ�̂͌��������񂪗\�������𖞂����ꍇ
    else:

        if ���O�g�[�N��2 == "EXEC" and ���O�g�[�N�� == "SQL":
            ���s����FLG = True
            return False
            
# '        elif ���O�g�[�N��2 = "CURSOR" and ���O�g�[�N�� = "FOR": # '���s����t���O�̒ǉ��ɂ�肱�̏ꍇ�͋N���Ȃ�
# '            return False
        elif ���O�g�[�N��2 == "EXEC" and ���O�g�[�N�� == "CICS":
            return False
        else:
            return True
    return False
            
def �g�[�N���o��_COBOL(P_STR):
    global ���O�g�[�N��,���O�g�[�N��2

    ���O�g�[�N��2 = ���O�g�[�N��    #'���̃g�[�N���̉��s����ɗ��p
    ���O�g�[�N�� = P_STR            #'���̃g�[�N���̉��s����ɗ��p
      
            
def rebuild_Token_Scm(TokenSheet,layout_name):
    
   
    TokenSheet2 = []
    
    �����s = 0
    while �����s < len(TokenSheet):
        hit_flg = False
        TokenSheet2_GYO = [layout_name]
        while �����s < len(TokenSheet) and hit_flg == False:
            
            ������ = 1
            TokenSheet_GYO = TokenSheet[�����s]
            while ������ < len(TokenSheet_GYO):
                TokenSheet2_GYO.append(TokenSheet_GYO[������])
                if TokenSheet_GYO[������] == ".":
                    hit_flg = True
                    
                ������ += 1
                
                if hit_flg:
                    break
            
            �����s += 1
            if hit_flg:
                break
        TokenSheet2.append(TokenSheet2_GYO)
    
    return TokenSheet2
            