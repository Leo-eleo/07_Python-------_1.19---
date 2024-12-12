#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import sys
import os
import unicodedata

import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


EndLineString = " "*69 ### JCL,PROC �ɂ�����I���s
AAUTO������Ǘ� = "�@A-AUTO����̂܂܏o��"
strREC = ""
# ADD 20240619 yi.a.qian
IN_LINE_COMMENT_STR = ["<<-", "<-"]
# ADD END

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

def SUB_PC����_JCL():
    global A�p��,C�p��,P�p��,IF�p��,strREC,PC����,PARM_�J�n��,PARM_�I����,COM_�J�n��,COMMENT������,MSG,PARM������
    # ADD 20240613 yi.a.qian
    global next_rec
    # ADD END

    PARM_�I���� = 71
    for i in range(PARM_�J�n��,min(72,len(strREC))):

        ����Ώە��� = strREC[i]

        if ����Ώە��� ==  "'":
            if PC���� == "PARM":
                if A�p��:
                    A�p�� = False
                else:
                    A�p�� = True
# '20111209 ADD
            elif PC���� == "������":
                    PC���� = "PARM"
                    PARM_�J�n�� = i
                    A�p�� = True
# 'ADD END
        elif ����Ώە��� ==  " ":
            if A�p��:
                pass
            else:
                if PC���� == "PARM":

                    PARM_�I���� = i - 1
                    PC���� = ""
# '20111209 ADD
        elif ����Ώە��� ==  "":    # '�ڍs�㎑�Y�Ȃǂœr���ŉ��s�������Ă���ꍇ�z��
            if A�p��:
                pass
            else:
                if PC���� == "PARM":

                    PARM_�I���� = i - 1
                    PC���� = ""
# 'ADD END

        else:
            if PC���� == "":
                PC���� = "COMMENT"
                COM_�J�n�� = i
            elif PC���� == "������":
                PC���� = "PARM"
                PARM_�J�n�� = i


    # 'PARM��
    if A�p��:
#'20240205 UPD qian.e.wang
        #PARM������ = Mid(strREC, PARM_�J�n��, 72 - PARM_�J�n��)#+1)
        PARM������ = Mid(strREC, PARM_�J�n��, 72 - PARM_�J�n��)
#'UPD END

    else:
        # 'if PARM_�J�n�� = PARM_�I����:
        # '    PARM������ = ""
        # 'else:
        PARM������ = Mid(strREC, PARM_�J�n��, PARM_�I���� - PARM_�J�n�� + 1)

    MSG = PARM������[-1]
    if MSG == ",":
        # UPD 20240613 yi.a.qian
        if not next_rec == "" and len(next_rec) > 3:
            third_char = next_rec[2]
            if third_char == " " or next_rec.startswith("//*") or next_rec.startswith("//-"):
                P�p�� = True
            else:
                P�p�� = False
        else:
            P�p�� = True
        # UPD END
    else:
        P�p�� = False

    # 'COMEENT��
    if PC���� == "������" or PC���� == "PARM" or PC���� == "":
        COMMENT������ = ""
    else:
        COMMENT������ = Mid(strREC, COM_�J�n��, 72 - COM_�J�n��+1)

# ADD 20240619 yi.a.qian
def remove_inline_comment(s: str) -> str:
    for comment_str in IN_LINE_COMMENT_STR:
        if comment_str in s:
            return s[:s.index(comment_str)]
    return s
# ADD END

def analysis1_2_read_text_JCL(Filename,AAUTO������Ǘ�):

    global DLM_flg,�ŏI�s_flg,��͒��~_flg, NET�s�p��,A�p��,C�p��,P�p��,IF�p��,strREC
    global PC����,PARM_�J�n��,PARM_�I����,COM_�J�n��,COMMENT������,MSG,PARM������
    # ADD 20240613 yi.a.qian
    global next_rec
    # ADD END
    TmpSheet = []

    DLM_flg = False
    �ŏI�s_flg = False
    ��͒��~_flg = False
    NET�s�p�� = False
    A�p�� = False
    C�p�� = False
    P�p�� = False
    IF�p�� = False
    PARM������ = ""
    COMMENT������ = ""

    CMD���� = ""
    GYO = 2

    with open(Filename,errors="ignore") as TS:

        # UPD 20240613 yi.a.qian
        lines = TS.readlines()
        for rec_index, strREC in enumerate(lines):
        # UPD END

            # UPD 20240619 yi.a.qian
            # strREC = strREC.replace("\n","")
            strREC = remove_inline_comment(strREC.replace("\n",""))
            # UPD END
            TmpSheet_GYO = [""]*12

            # ADD 20240613 yi.a.qian
            if not rec_index + 1 >= len(lines):
                next_rec = lines[rec_index + 1]
            else:
                next_rec = ""
            # ADD END
#         'ADD 20111202 takei
            # '        if strREC.startswith(//*":
            # '           if �R�����g�s���� = "�o�͂���":
            # '              GYO = GYO + 1
            # '              TmpSheet_GYO[1] = "*"
            # '              TmpSheet_GYO[2] = strREC
            # '           End if
            # '        else
            # '            GYO = GYO + 1
            # '            TmpSheet_GYO[2] = strREC
            # '        End if

            # '�s��񔻒�
            if ��͒��~_flg:
                JCL�s���� = "�I���s"

                #    '�ēx�uJOB���v��������ĉ�͊J�n 20140724 H.Takei
                # UPD 20240613 yi.a.qian
                if strREC.startswith("//") and strREC[2] != "*" and " JOB " in strREC:
                # if (strREC.startswith("//") or strREC.startswith("/\\")) and strREC[2] != "*" and " JOB " in strREC:
                # UPD END
                    ��͒��~_flg = False
                    �ŏI�s_flg = False
                    JCL�s���� = "�ʏ�s"

            elif NET�s�p��:
                JCL�s���� = "NET�s"
                if Trim(Mid(strREC, 3, 68)).endswith(","):
                    pass
                else:
                    NET�s�p�� = False

            # 'elif �ŏI�s_flg:
            elif strREC.startswith("//*NET "):   #'�x�m�� DLM�Ή�
                JCL�s���� = "NET�s"
                #'MSG = Right(Trim(Mid(strREC, 8, 64)), 1)
                if Trim(Mid(strREC, 7, 64)).endswith(","):
                    NET�s�p�� = True

            # UPD 20240613 yi.a.qian
            elif strREC.startswith("/\\"):
                continue
                # JCL�s���� = "/\�s"   #'JFE�q�~�Œǉ�
            # UPD END
            elif strREC.startswith("//*") or strREC.startswith("//-"):  #'"//-"�͕��R�ʉ^�p�b��Ή��i�I���s�̌�ɂ���ꍇ������j
                JCL�s���� = "���čs"

            # UPD 20240613 yi.a.qian
            elif strREC.startswith("//"):
            # elif strREC.startswith("//") or strREC.startswith("/\\"):
            # UPD END
                if �ŏI�s_flg:
                    if " JOB " in strREC:
                        �ŏI�s_flg = False
                        JCL�s���� = "�ʏ�s"
                    elif Mid(strREC, 2, 69) == EndLineString:
                        JCL�s���� = "�I���s"
                        #'��͒��~�ɂ͂��Ȃ�
                    else:
                        ��͒��~_flg = True
                        JCL�s���� = "�I���s"
                elif Mid(strREC, 2, 69) == EndLineString:
                    JCL�s���� = "�I���s"                              #'���R�ʉ^���Y�Ή��i�I���s�̒����JOB���ȊO�Ȃ��͏I���j
                    �ŏI�s_flg = True
                else:
                    JCL�s���� = "�ʏ�s"
            elif DLM_flg == False and strREC.startswith("/*"):
                if �ŏI�s_flg:
                    ��͒��~_flg = True
                    JCL�s���� = "�I���s"
                else:
                    JCL�s���� = "��؍s"

            elif DLM_flg and strREC.startswith(DLM����): #'DLM�Ŏw�肵����؍s
                JCL�s���� = "��؍s"
                DLM_flg = False                              #    'DLM�w�����
            else:
                if �ŏI�s_flg:
                    ��͒��~_flg = True
                    JCL�s���� = "�I���s"
                else:
                    JCL�s���� = "SYSIN�s"


            TmpSheet_GYO[1] = JCL�s����

            #'��ؕ�������
            if JCL�s���� == "�ʏ�s" and  "DLM='" in strREC:
                DLM_flg = True
                DLM���� = Mid(strREC, strREC.find("DLM='") + 5, 2)
            elif JCL�s���� == "�ʏ�s" and "DLM=" in strREC:
                DLM_flg = True
                DLM���� = Mid(strREC, strREC.find("DLM=") + 4, 2)
            #'���F�A�|�X�g���t�B�[���̂܂��̓A���p�T���h�͖��Ή�

            #'�X�e�[�g�����g���ޏ�񔻒�
            �p���s_flg = True      # '�X�e�[�g�����g���ނ̎��ʏ��(JOB EXEC DD�Ȃ�)����������Ȃ��ꍇ

            #'20111209 ADD
            strREC_���茅 = strREC.find("'") + 1
            if strREC_���茅 > 0:
                strREC_����p = strREC[:strREC_���茅]
            else:
                #strREC_����p = strREC.startswith
                strREC_����p = strREC[:30]  # '�E���R�����g�̈�Ɂu JOB �v���̃L�[���[�h������ꍇ�����茟���͈͂�����

#'ADD END

            if JCL�s���� == "�ʏ�s":
                # �X�e�[�g�����g:JOB
                # �t�B�[���h    ://jobname   JOB   [parameter   [comments]]
                #                //jobname   JOB
                if " JOB " in strREC_����p:
                    CMD����_�J�n�� = strREC.find(" JOB ")
                    CMD���� = "JOB"
                    PARM_�J�n�� = CMD����_�J�n�� + 5
                    �p���s_flg = False
                # �X�e�[�g�����g:DD
                # �t�B�[���h    ://[ddname]   DD  [parameter   [comments]]
                #                //[ddname]   DD
                elif  " DD " in strREC_����p:
                    CMD����_�J�n�� = strREC.find(" DD ")
                    CMD���� = "DD"
                    PARM_�J�n�� = CMD����_�J�n�� + 4
                    �p���s_flg = False
                # �X�e�[�g�����g:EXEC
                # �t�B�[���h    ://[stepname]   EXEC   parameter   [comments]
                elif " EXEC " in strREC_����p:
                    CMD����_�J�n�� = strREC.find(" EXEC ")
                    CMD���� = "EXEC"
                    PARM_�J�n�� = CMD����_�J�n�� + 6
                    �p���s_flg = False
                # �X�e�[�g�����g:PROC (cataloged)
                # �t�B�[���h    ://[name]   PROC   [parameter   [comments]]
                #                //[name]   PROC
                # �X�e�[�g�����g:PROC (in-stream)
                # �t�B�[���h    ://name   PROC   [parameter   [comments]]
                #                //name   PROC
                elif " PROC " in strREC_����p:
                    CMD����_�J�n�� = strREC.find(" PROC ")
                    CMD���� = "PROC"
                    PARM_�J�n�� = CMD����_�J�n�� + 6
                    �p���s_flg = False
                # �X�e�[�g�����g:PEND
                # �t�B�[���h    ://[name]   PEND   [comments]
                elif " PEND " in strREC_����p:
                    CMD����_�J�n�� = strREC.find(" PEND ")
                    CMD���� = "PEND"
                    PARM_�J�n�� = CMD����_�J�n�� + 6
                    �p���s_flg = False
                # �X�e�[�g�����g:JCLLIB
                # �t�B�[���h    ://[name]  JCLLIB   parameter   [comments]
                elif " JCLLIB " in strREC_����p:
                    CMD����_�J�n�� = strREC.find(" JCLLIB ")
                    CMD���� = "JCLLIB"
                    PARM_�J�n�� = CMD����_�J�n�� + 8
                    �p���s_flg = False
#'20240131 ADD qian.e.wang
                # �X�e�[�g�����g:INCLUDE
                # �t�B�[���h    ://[name]  INCLUDE  parameter   [comments]
                elif " INCLUDE " in strREC_����p:
                    CMD����_�J�n�� = strREC.find(" INCLUDE ")
                    CMD���� = "INCLUDE"
                    PARM_�J�n�� = CMD����_�J�n�� + 9
                    PARM������ = Mid(strREC, PARM_�J�n��, 72 - PARM_�J�n��)
                    �p���s_flg = False
#'ADD END

#'20111215 ADD takei
                # �X�e�[�g�����g:IF/THEN/ELSE/ENDIF
                # �t�B�[���h    ://name IF [relational expression] THEN  [comments]
                #                //name ELSE  [comments]
                #                //name ENDIF  [comments]
                elif " IF " in strREC_����p:
                    CMD����_�J�n�� = strREC.find(" IF ")
                    CMD���� = "IF"
                    PARM_�J�n�� = CMD����_�J�n�� + 4
                    #'�p���s_flg = False                                      '"IF"���͒ʏ��PC����͍s��Ȃ�
                    #'if ":") > 0:
                    if " THEN" in strREC:                   #    'THEN�̏ꍇ�ustrREC_����p�v�ł͂Ȃ��ustrREC�v�Ō���
                        IF�p�� = False
                        #'PARM_�I���� = ":")
                        PARM_�I���� = strREC.find(" THEN")
                        PARM������ = "'" + Mid(strREC, PARM_�J�n��, PARM_�I���� - PARM_�J�n�� - 1) + "'THEN"  #'�K���ɱ�߽��̨�ǉ�
                        COMMENT������ = strREC[PARM_�I���� + 5:72]   # '�����͎��M�Ȃ��B�B
                    else:
                        IF�p�� = True
                        PARM������ = "'" + strREC[PARM_�J�n��:72]  # '�����͎��M�Ȃ��B�B
                        COMMENT������ = ""

                elif " ELSE " in strREC:
                    CMD����_�J�n�� = strREC.find(" ELSE ")
                    CMD���� = "ELSE"
                    PARM_�J�n�� = CMD����_�J�n�� + 6
                    �p���s_flg = False
                elif " ENDIF " in strREC:
                    CMD����_�J�n�� = strREC.find(" ENDIF ")
                    CMD���� = "ENDIF"
                    PARM_�J�n�� = CMD����_�J�n�� + 7
                    �p���s_flg = False
                elif IF�p�� and " THEN " in strREC:  #'THEN�̏ꍇ�ustrREC_����p�v�ł͂Ȃ��ustrREC�v�Ō���
                    CMD����_�J�n�� = strREC.find(" THEN ")
                    CMD���� = "IF"
                    IF�p�� = False
                    if CMD����_�J�n�� >= 15:
                        PARM������ = Mid(strREC, 15, CMD����_�J�n�� - 15 + 1 ) + "'THEN" # '�K���ɱ�߽��̨�ǉ�
                        COMMENT������ = strREC[CMD����_�J�n�� + 6:72]  ##  '�����͎��M�Ȃ��B�B
                    else: #   'MHI�Č��@PROC����if���ɋK���͂Ȃ�����
                        PARM������ = strREC[CMD����_�J�n�� + 1:72]  # '�����͎��M�Ȃ��B�B
                        COMMENT������ = "" #'�悭�킩��Ȃ��̂ŉ�
                    #'�p���s_flg = False                                  '"IF"���͒ʏ��PC����͍s��Ȃ�
#'ADD END

                # �X�e�[�g�����g:Null
                # �t�B�[���h    ://
                elif Mid(strREC, 2, 69) == EndLineString:
                    CMD���� = "�k��"
                    �p���s_flg = False
                #'�Ή��҂�
                # �X�e�[�g�����g:COMMAND
                # �t�B�[���h    ://[name]  COMMAND �ecommand command-operand�f  [comments]

                # �X�e�[�g�����g:CNTL
                # �t�B�[���h    ://label   CNTL   [*  comments]
                # �X�e�[�g�����g:ENDCNTL
                # �t�B�[���h    ://[label]   ENDCNTL   [comments]

                # �X�e�[�g�����g:EXPORT
                # �t�B�[���h    ://[label]   EXPORT   [comments]

                # �X�e�[�g�����g:OUTPUT JCL
                # �t�B�[���h    ://name   OUTPUT   parameter   [comments]

                # �X�e�[�g�����g:SCHEDULE
                # �t�B�[���h    ://[name]  SCHEDULE  parameter   [comments]

                # �X�e�[�g�����g:SET
                # �t�B�[���h    ://[name]  SET  parameter   [comments]

                # �X�e�[�g�����g:XMIT
                # �t�B�[���h    ://[name]   XMIT   parameter[,parameter] [comments]

            # 'NAME�s���Z�b�g
            if JCL�s���� == "�ʏ�s" and �p���s_flg == False and CMD���� != "�k��":
                TmpSheet_GYO[2] = Mid(strREC, 2, CMD����_�J�n�� - 3 + 1).replace(" ", "")

            #'CMD�s���Z�b�g
            if JCL�s���� == "�ʏ�s":
                TmpSheet_GYO[3] = CMD���� # '��L�ȊO�̏ꍇ�͑O�s�̏�񂪈����p�����
            else:
                TmpSheet_GYO[3] = ""

            #'PARM���&COMMENT��񎯕�
            if JCL�s���� == "�ʏ�s" and CMD���� != "�k��":
                #'�X�e�[�g�����g���ނ̎��ʏ��(JOB EXEC DD�Ȃ�)������s�̏���
                if �p���s_flg == False:
                #  'PARM������ = Mid(strREC, PARM_�J�n��, 72 - PARM_�J�n��)
                    A�p�� = False
                    P�p�� = False
                    PC���� = "������"  #'PARM��or�R�����g���������ʂ���
                # 'PARM���ƃR�����g���ɕ���
                    SUB_PC����_JCL()

                #'�X�e�[�g�����g���ނ̎��ʏ��(JOB EXEC DD�Ȃ�)���Ȃ��s�̏���
                else:
                    # 20241111 detao.wang �֓d UPD START
                    # 20240703 jiafu.luan ��t UPD START
                    if C�p�� and not P�p��:
                        PARM������ = ""
                        COMMENT������ = Mid(strREC, 3, 68)
                    elif A�p��:
                    # if A�p��:
                    # 20241111 detao.wang �֓d UPD END
                        PARM_�J�n�� = 16
                        for i in range(2,16):
                            if strREC[i] != " ":
                                PARM_�J�n�� = min(PARM_�J�n��,i)
                        # 'PARM������ = Mid(strREC, PARM_�J�n��, 72 - PARM_�J�n��)
                        PC���� = "PARM"

                        SUB_PC����_JCL()

                    elif P�p��:

                        PC���� = "������"
                        PARM_�J�n�� = 2 # '4���ڈȍ~�̔C�ӂ̌�����ĊJ�����i�ŏ��̃X�y�[�X���X�L�b�v�j
                                        #   '���[�v���ŃJ�E���g�A�b�v���Ă���̂ŏ����l�� -1 ���Ă���
                        for i in range(PARM_�J�n��,min(72,len(strREC))):
                            if strREC[i] != " ":
                                PARM_�J�n�� = i
                                break
                        if PARM_�J�n�� == 2:
                            PARM_�J�n�� = 72

                        #'PARM������ = Mid(strREC, PARM_�J�n��, 72 - PARM_�J�n��)

                        SUB_PC����_JCL()
                    # 20241111 detao.wang �֓d UPD START
                    # elif C�p��:
                    #     PARM������ = ""
                    #     COMMENT������ = Mid(strREC, 3, 68)
                    # # # 20240703 jiafu.luan ��t UPD END
                    # 20241111 detao.wang �֓d UPD END
                    else:
                        first = -1
                        last = -1
                        for i in range(2,min(len(strREC),72)):
                            if strREC[i] != " ":
                                if first == -1:
                                    first = i
                                last = i

                        PARM������ = Mid(strREC,first,last-first+1)
                        COMMENT������ = ""
                        CMD���� = ""
                        TmpSheet_GYO[3] = ""
                        # if strREC.startswith("//"):
                        #     PARM������ = ""
                        #     COMMENT������ = ""
                        MSG = "�z��O�̃p�^�[��"


# '�k���s
            elif JCL�s���� == "�ʏ�s" and CMD���� == "�k��":
                PARM������ = "�k��"
                COMMENT������ = ""
            #'�ʏ�s�ȊO
            else:

                if JCL�s���� == "���čs":
                    PARM������ = ""
                    COMMENT������ = Mid(strREC, 0, 71) #' �u=�v�Ŏn�܂镶������Z���ɃZ�b�g�ł��Ȃ��̂�
                elif JCL�s���� == "��؍s":
                    PARM������ = ""
                    COMMENT������ = Mid(strREC, 2, 69)
                elif JCL�s���� == "SYSIN�s":
                    PARM������ = Mid(strREC, 0, 80)
                    COMMENT������ = ""
                elif JCL�s���� == "�I���s":                      # '���R�ʉ^�Ή�
                    PARM������ = ""
                    COMMENT������ = ""
                elif JCL�s���� == "NET�s":                       #  '���R�ʉ^�Ή�
                    PARM������ = RTrim(Mid(strREC, 3, 68))
                    COMMENT������ = ""

#'20111209�@ADD
            #'PARM���Z�b�g
            if PARM������.replace(" ", "") == "":   #'SPACE�݂̂Ȃ�NULL
                TmpSheet_GYO[4] = ""
            # elif PARM������[0] == "'":
            #     TmpSheet_GYO[4] = "'" + PARM������ #'�擪���A�X�^���X�N�̏ꍇ�͒ǉ��ŕt�^
            else:
                TmpSheet_GYO[4] = PARM������
# 'ADD END

            # 'COMMENT���Z�b�g
            TmpSheet_GYO[5] = COMMENT������

            # 'PARM�p�����Z�b�g
            if IF�p��:
                TmpSheet_GYO[6] = "IF�p��"
            if A�p��:
                TmpSheet_GYO[6] = "A�p��"
            if P�p��:
                TmpSheet_GYO[6] = "P�p��"



            # '�p���s���Z�b�g
            if len(strREC) > 71 and get_ZENKAKU_str(strREC,71,1) != " ":  # '72�����ڂ܂ő��݂��Ȃ��ꍇ�͌p���s�Ƃ��Ȃ�
                C�p�� = True
            else:
                C�p�� = False

            TmpSheet_GYO[7] = get_ZENKAKU_str(strREC,71,1)
            # '������Z�b�g
            TmpSheet_GYO[8] = Mid(strREC, 72, 8)
            # '�����Y�s�ԍ��Z�b�g
            TmpSheet_GYO[9] = GYO - 1
            # '�����Y�s���Z�b�g
            TmpSheet_GYO[10] = strREC

            # 'A-AUTO����Ǘ����Z�b�g                               '2020/4/13 ADD
            if AAUTO������Ǘ� == "�@A-AUTO����̂܂܏o��":
                TmpSheet_GYO[11] = Trim(Mid(strREC, 70, 1))


            TmpSheet.append(TmpSheet_GYO)
            GYO += 1


    return TmpSheet