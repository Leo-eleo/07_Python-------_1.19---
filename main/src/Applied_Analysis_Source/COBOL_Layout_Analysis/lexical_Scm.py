#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

KEY_STR = ""
def ������������(STR, str2, str3):
      
    if STR == " ":
        return True
    elif STR == ".":
        if str2 == " " or str2 == "":
           return True
        else:
           return False
    
    elif STR == ",":
        # 'if KEY_STR <> "�f�[�^��":   '�f�[�^���� ZZZ,ZZ9 �̗l�ȏꍇ�͕��������Ȃ�
        # '   return True
        # 'else:
        return False
        
    elif STR == ";":
        if str2 == " ":
           return True
        else:
           return False
    
    elif STR == ":":
        return True
    elif STR == "'":
        if str2 == " ":
           return True
        else:
           return False
    
    elif STR == "\"":
        if str2 == " ":
           return True
        else:
           return False
    
    elif STR == "(":
        return True
    elif STR == ")":
        return True
    # '���F"=="�͋^��÷�Ă�\����؂蕶���ł��邪���ّΉ����K�v�Ȉ׏�ʃ��W���[���ŏ�������
    elif STR == "=":
            return True
    elif STR == "X":
        if str2 == "\"" or str2 == "\'":
           return True
        else:
           return False
    
    elif STR == "Z":
        if str2 == "\"" or str2 == "'":
           return True
        else:
           return False
    
    elif STR == "N":
        if str2 == "\"" or str2 == "'":
           return True
        elif str2 == "X" and \
           (str3 == "\"" or str3 == "'"):
           return True
    # '2013/9/19 ADD �x�m��COBOL�H�Ή�
        elif str2 == "C" and \
           (str3 == "\"" or str3 == "'"):
           return True
        elif str2 == "A" and \
           (str3 == "\"" or str3 == "'"):
           return True
        elif str2 == "K" and \
           (str3 == "\"" or str3 == "'"):
           return True
        elif str2 == "H" and \
           (str3 == "\"" or str3 == "'"):
           return True
        elif str2 == "N" and \
           (str3 == "\"" or str3 == "'"):
           return True
        else:
           return False
    
    elif STR == "G":
        if str2 == "\"" or str2 == "'":
           return True
        else:
           return False
    
    # '2013/9/19 ADD �x�m��COBOL�H�Ή�
    elif STR == "B":
        if str2 == "\"" or str2 == "'":
           return True
        else:
           return False
    
    else:
        return False


def lexical_Scm(TmpSheet):
    global KEY_STR
     
   
    ��� = 5
    �����s = 2      #'TempSheet�@�s�|�C���^
    �o�͍s = 1
    �o�͗� = 5
    KEY_STR = "�w�b�_�["
    TokenSheet_GYO = [""]*5
    TokenSheet = []
    �����s = 1    #  'TempSheet�@�s�|�C���^
   
    for �����s in range(len(TmpSheet)):
        CMD_fld = TmpSheet[�����s]
        �o�͍s = �o�͍s + 1 # '�o�͎��J�E���g�A�b�v
        TokenSheet_GYO = []
        TokenSheet_GYO.append(�����s+1)
        �o�͗� = 1
        
        # '�R�}���h��񕪉�
        i = 0
        while i < len(CMD_fld):
            ����Ώە��� = Mid(CMD_fld, i, 1)
            ����Ώە���2 = Mid(CMD_fld, i + 1, 1)
            ����Ώە���3 = Mid(CMD_fld, i + 2, 1)
            ����Ώە���_from = i
            ����Ώە���_to = i

        #   '�ォ��D�悵�Ĕ��肷��
            if ����Ώە��� == "'":
                apost_cnt = 1
                apost_start = True
                apost_end = False

                while True:
                    ����Ώە���_to = ����Ώە���_to + 1
                    if Mid(CMD_fld, ����Ώە���_to, 1) == "'":
                        apost_cnt = apost_cnt + 1       #   '�J�n���ɃA�|�X�g���t�B�������ꍇ�̍l��
                    else:
                        apost_start = False  # '��U�A�|�X�g���t�B�[���r�؂��
                        apost_cnt = 0      #�r���œr�؂ꂽ��J�E���g�����Z�b�g
                           
                    temp_num = apost_cnt %2 #  '�A���A�|�X�g���t�B����������炨���
                           
                    if apost_start:
                        if apost_cnt > 3 and temp_num == 0: #'�ŏ�����A�|�X�g���t�B��4�ȏ�����A������ꍇ�͏I��
                            apost_end = True
                        else:
                            apost_end = False
                    else:
                        if temp_num == 1: # '��U�r�؂ꂽ�A�|�X�g���t�B�̏ꍇ�͊�̃A�|�X�g���t�B��1�ȏ�̏ꍇ�I��
                            apost_end = True
                        else:
                            apost_end = False

                    if (Mid(CMD_fld, ����Ώە���_to, 1) == "'" and Mid(CMD_fld, ����Ώە���_to + 1, 1) != "'" and apost_end) or \
                        ����Ώە���_to >= 72:
                        break

                #   '[����Ώە���_to]�@�̌��ʂ� [����Ώە���_from]�̕��������w�������ꂽ���ʂɂȂ�
                �Ώە����� = ����Ώە���_to - ����Ώە���_from + 1
                i = i + �Ώە�����                                  #  '
                �o�͗� = �o�͗� + 1
                # '���ӁFEXCEL�V�[�g�ɍďo�͂���ہu'�v�����������̂ŗ]���Ɂu''�v��t�^����
             
                TokenSheet_GYO.append("'" + Mid(CMD_fld, ����Ώە���_from, �Ώە�����))
                #    '�u"�v����؂Ŏg�����ǂ����v�m�F�i�g��Ȃ��̂ł���΁��͍폜�j
            elif ����Ώە��� == "\"":
                ����Ώە���_to = Mid(CMD_fld, ����Ώە���_from + 1, 80).find("\"")
                # '[����Ώە���_to]�@�̌��ʂ� [����Ώە���_from]�̕��������w�������ꂽ���ʂɂȂ�
                �Ώە����� = ����Ώە���_to + 2 
                i = i + �Ώە�����                                    
                �o�͗� = �o�͗� + 1
   
            elif ������������(����Ώە���, ����Ώە���2,����Ώە���3) == True:
                 
                if ����Ώە��� == " ":
                    i = i + 1
                    #  '���������i�o�͂���j
                elif ����Ώە��� == "=" and ����Ώە���2 == "=":
                    ����Ώە���_to = Mid(CMD_fld, ����Ώە���_from + 1, 80).find("==")
                    # '[����Ώە���_to]�@�̌��ʂ� [����Ώە���_from]�̕��������w�������ꂽ���ʂɂȂ�
                    �Ώە����� = ����Ώە���_to + 3
                    i = i + �Ώە�����                                    
                    �o�͗� = �o�͗� + 1
                    # '���ӁFEXCEL�ɏo�͂���ɂ́u==�v�̓G���[�ɂȂ�̂Ő擪�Ɂu'�v��t�^����
                    TokenSheet_GYO.append("'" + Mid(CMD_fld, ����Ώە���_from, �Ώە�����))
                
                elif ����Ώە��� in ("X","Z","N","G"):
                            
                    if ����Ώە���2 == "'":
                        ����Ώە���_to = Mid(CMD_fld, ����Ώە���_from + 2, 80).find(����Ώە���2)
                        �Ώە����� = ����Ώە���_to + 2 + 1
                    elif ����Ώە���2 == "\"":
                        ����Ώە���_to = Mid(CMD_fld, ����Ώە���_from + 2, 80).find(����Ώە���2)
                        �Ώە����� = ����Ώە���_to + 2 + 1
                    elif ����Ώە���2 == "X":
                        ����Ώە���_to = Mid(CMD_fld, ����Ώە���_from + 3, 80).find(����Ώە���3)
                        �Ώە����� = ����Ώە���_to + 3 +1
                    elif ����Ώە���2 == "C":
                        ����Ώە���_to = Mid(CMD_fld, ����Ώە���_from + 3, 80).find(����Ώە���3)
                        �Ώە����� = ����Ώە���_to + 3 + 1
                    elif ����Ώە���2 == "A":
                        ����Ώە���_to = Mid(CMD_fld, ����Ώە���_from + 3, 80).find(����Ώە���3)
                        �Ώە����� = ����Ώە���_to + 3 + 1
                    elif ����Ώە���2 == "K":
                        ����Ώە���_to = Mid(CMD_fld, ����Ώە���_from + 3, 80).find(����Ώە���3)
                        �Ώە����� = ����Ώە���_to + 3 + 1
                    elif ����Ώە���2 == "H":
                        ����Ώە���_to = Mid(CMD_fld, ����Ώە���_from + 3, 80).find(����Ώە���3)
                        �Ώە����� = ����Ώە���_to + 3 + 1
                    elif ����Ώە���2 == "N":
                        ����Ώە���_to = Mid(CMD_fld, ����Ώە���_from + 3, 80).find(����Ώە���3)
                        �Ώە����� = ����Ώە���_to + 3 + 1
                    else:
                        MSG = "�z��O�̏���"
                            
                    i = i + �Ώە�����                                    
                    �o�͗� = �o�͗� + 1
                    TokenSheet_GYO.append(Mid(CMD_fld, ����Ώە���_from, �Ώە�����))
                            
                else:
                    i = i + 1
                    �o�͗� = �o�͗� + 1
                    TokenSheet_GYO.append(����Ώە���)
   
            else:
            # '�擪�����������ł͂Ȃ��ꍇ
                i2 = i
                while True:
                    i2 = i2 + 1
                    if i2 >= len(CMD_fld) or ������������(Mid(CMD_fld, i2, 1), Mid(CMD_fld, i2 + 1, 1), Mid(CMD_fld, i2 + 2, 1)) == True:
                        break
              
                if i2 >= 80:
                    ����Ώە���_to = 80
                    i = 80 #'�㑱�����I��
                    �Ώە����� = ����Ώە���_to - ����Ώە���_from + 1
                    �o�͗� = �o�͗� + 1
                    TokenSheet_GYO.append(Mid(CMD_fld, ����Ώە���_from, �Ώە�����))

                else:
                    ����Ώە���_to = i2 - 1
                    �Ώە����� = ����Ώە���_to - ����Ώە���_from + 1
                    i = i + �Ώە�����                                    
                    �o�͗� = �o�͗� + 1
                    TokenSheet_GYO.append(Mid(CMD_fld, ����Ώە���_from, �Ώە�����))

        TokenSheet.append(TokenSheet_GYO)        
    
    return TokenSheet