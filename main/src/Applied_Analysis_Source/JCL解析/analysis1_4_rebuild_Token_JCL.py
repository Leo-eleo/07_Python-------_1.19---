#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

def analysis1_4_rebuild_Token_JCL(TokenSheet):
    
    ��� = 7          #  'TokenSheet    2020/4/14 6��7
    ���2 = 6         #  'TokenSheet2   2020/4/14 5��6
    �����s = 0          # 'TokenSheet�@�s�|�C���^
   
    TokenSheet2 = []
    TokenSheet_last = ["@@@@@@@"]*10
    
    while �����s < len(TokenSheet):
  
        TokenSheet_GYO = TokenSheet[�����s]
        TokenSheet2_GYO = [""]*6
    #    '���R�ʉ^�Ή��@�I���s�̒��オJOB���łȂ���Έȍ~�̉�͍͂s��Ȃ�
    #    'if TokenSheet_GYO[2] = "�I���s":
    #    '   �ŏI�s_flg = True
    #    '   '�����s = �����s + 1
    #    'else:
    #    '
    #    '   if �ŏI�s_flg:
    #    '     if TokenSheet_GYO[2] = "�ʏ�s" and TokenSheet_GYO[4] = "JOB":
    #    '         �ŏI�s_flg = False
    #    '     elif TokenSheet_GYO[2] = "�ʏ�s" and TokenSheet_GYO[4] != "JOB":
    #    '         ��͒��~_flg = True
    #    '     elif TokenSheet_GYO[2] = "SYSIN�s":
    #    '         ��͒��~_flg = True
    #    '     End If
    #    '   End If
    #    'End If
       
    #    'if Not (��͒��~_flg):
       
        TokenSheet2_GYO[1] = TokenSheet_GYO[1]   #'�����Y�s�ԍ�
        TokenSheet2_GYO[2] = TokenSheet_GYO[2]   #'�s����
        TokenSheet2_GYO[3] = TokenSheet_GYO[6]   #'A-AUTO����  2020/4/14 ADD
        TokenSheet2_GYO[4] = TokenSheet_GYO[3]   #'NAME
        TokenSheet2_GYO[5] = TokenSheet_GYO[4]   #'CMD

        #'�o�͗� = 4
        �o�͗� = ���2
        while True:
            
            # '������ = 5
            ������ = ���
            while ������ < len(TokenSheet_GYO):
                
                # 'if ������ = 5 and TokenSheet_last[4] = "A�p��":
                if ������ == ��� and TokenSheet_last[5] == "A�p��":
                    �o�͗� = �o�͗� - 1
                    TokenSheet2_GYO[�o�͗�] = TokenSheet2_GYO[�o�͗�] + TokenSheet_GYO[������]
                    ������ = ������ + 1
                    �o�͗� = �o�͗� + 1
                elif ������ == ��� and TokenSheet_GYO[2] == "NET�s" and TokenSheet_last[2] == "NET�s":
                    # '�x�m�ʑΉ�
                    # 'NET�s���p������ꍇ��1�s�ɂ܂Ƃ߂�
                    �o�͗� = �o�͗� - 1
                    TokenSheet2_GYO[�o�͗�] = TokenSheet2_GYO[�o�͗�] + TokenSheet_GYO[������]
                    ������ = ������ + 1
                    �o�͗� = �o�͗� + 1
                else:
                    if TokenSheet_GYO[������] != "'":
                        TokenSheet2_GYO.append("")
                        TokenSheet2_GYO[�o�͗�] = TokenSheet_GYO[������]
                        �o�͗� = �o�͗� + 1
                    ������ = ������ + 1
                    
            
               
            TokenSheet_last = TokenSheet_GYO[:]
          
            �����s = �����s + 1
            
            if �����s >= len(TokenSheet):
                break
            
            TokenSheet_GYO = TokenSheet[�����s]
          
            # '�p������
            # 'if TokenSheet_last[4] = "":
            if TokenSheet_last[5] == "":
                �p������ = True
            else:
                �p������ = False

            # '�s���u���C�N
            # 'if TokenSheet_GYO[1] != TokenSheet_last[1]:
            if TokenSheet_GYO[2] != TokenSheet_last[2]:
                ID�u���C�N = True
            else:
                ID�u���C�N = False

           
            # 'NAME���u���C�N
            # 'if TokenSheet_GYO[2] != TokenSheet_last[2]:
            if TokenSheet_GYO[3] != TokenSheet_last[3]:
                Name�u���C�N = True
            else:
                Name�u���C�N = False

           
            # 'CMD���u���C�N
            # 'if TokenSheet_GYO[3] != TokenSheet_last[3] Or
            if TokenSheet_GYO[4] != TokenSheet_last[4] or \
                TokenSheet_GYO[4] == "EXEC" or \
                TokenSheet_GYO[4] == "DD":
                CMD�u���C�N = True
            else:
                CMD�u���C�N = False
            
            # '�������[�v�Ή� V1.27.01�Œǉ�
            if TokenSheet_GYO[1] == "" and TokenSheet_GYO[2] == "" and TokenSheet_GYO[3] == "" and TokenSheet_GYO[4] == "":
                break
                
            if �p������ and (ID�u���C�N or Name�u���C�N or CMD�u���C�N):
                break

        TokenSheet2.append(TokenSheet2_GYO)
 
        
    return TokenSheet2