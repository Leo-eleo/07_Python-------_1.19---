#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
import reserved_word_table_COBOL

import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

SUB_SQL����_COBOL_0_ = None
SUB_SQL����_COBOL_3_ = None
SUB_SQL����_COBOL_4_ = None

natural_analysis_keyword = reserved_word_table_COBOL.get_natural_keyword()

def natural_analysis_check(word):
    if word in natural_analysis_keyword:
        return True
    return False

def reset_all():
    global �t�@�C����,COBOL_ID,CMD_SEQ,�����Y�s,COBOL�̈敪��,COBOL�K�w���,COBOL���򔻒�,���͍sTYPE,�����s������,�sCHK, \
            ���C�u����ID,PGM_ID,�t�@�C��IO�L��,PARM�L��,�T�u���[�`���L��,SQL�L��,��ʗL��,ALL_chk_ok, \
            COBOL_�֘A�敪,COBOL_�֘A���Y,COBOL_�֘A���Y_TRANID,\
            P_�t�@�C����,P_CBL_ID,P_CMD����,P_�ďo���Y,P_�ďoPARM, \
            re_flg

    re_flg = False
    ���C�u����ID = ""
    �t�@�C���� = ""
    COBOL_ID = ""
    COBOL�̈敪�� = ""
    COBOL�K�w��� = ""
    COBOL���򔻒� = ""
    �����s������ = ""
    ���͍sTYPE = ""
    �sCHK = False
    CMD_SEQ = 0
    �����Y�s = 0
    PGM_ID = ""
    �t�@�C��IO�L�� = ""
    PARM�L�� = ""
    �T�u���[�`���L�� = ""
    SQL�L�� = ""
    ��ʗL�� = ""
    ALL_chk_ok = True
    COBOL_�֘A�敪 = ""
    COBOL_�֘A���Y = ""
    COBOL_�֘A���Y_TRANID = ""

    P_�t�@�C���� = ""
    P_CBL_ID = ""
    P_CMD���� = ""
    P_�ďo���Y = ""
    P_�ďoPARM = ""


class SUB_SQL����_COBOL_0:

    def __init__(self, conn, cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�ACOBOL_��{���"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}

    def insert(self):
        if self.dic == None:
            self.setup()

        global �t�@�C����, ���C�u����ID, COBOL_ID, PGM_ID, CMD_SEQ, �t�@�C��IO�L��, PARM�L��, �T�u���[�`���L��, SQL�L��, ��ʗL��, ALL_chk_ok

        if ALL_chk_ok == True:
            L_CHK = "OK"
        else:
            L_CHK = "NG"

        key_list = [
            "���YID", "LIBRARY_ID", "�����o��", "���W���[����", "CMD�s��", "��͌���",
            "�t�@�C��IO�L��", "PARM�L��", "�T�u���[�`���L��", "SQL�L��", "��ʗL��"
        ]
        value_list = [
            �t�@�C����, ���C�u����ID, COBOL_ID, PGM_ID, CMD_SEQ, L_CHK, �t�@�C��IO�L��, PARM�L��,
            �T�u���[�`���L��, SQL�L��, ��ʗL��
        ]

        sql, value = make_insert_sql(self.dbname, value_list, key_list)

        self.cursor.execute(sql, value)

        return True

    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close()

    def close_conn(self):
        self._close_conn()


class SUB_SQL����_COBOL_3:

    def __init__(self, conn, cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�ACOBOL_�֘A���Y"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}

    def insert(self):
        if self.dic == None:
            self.setup()

        global �t�@�C����, COBOL_ID, COBOL_�֘A�敪, COBOL_�֘A���Y, COBOL_�֘A���Y_TRANID

        key_list = ["���YID", "COBOL_ID", "�֘A�敪", "�֘A���Y", "�֘A���Y_TRANID"]
        value_list = [
            �t�@�C����, COBOL_ID, COBOL_�֘A�敪, COBOL_�֘A���Y,
            COBOL_�֘A���Y_TRANID.replace("'", "")
        ]

        sql, value = make_insert_sql(self.dbname, value_list, key_list)

        self.cursor.execute(sql, value)

        return True

    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close()

    def close_conn(self):
        self._close_conn()


class SUB_SQL����_COBOL_4:

    def __init__(self, conn, cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�ACOBOL_CMD���"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}

    def insert(self):
        if self.dic == None:
            self.setup()

        global �t�@�C����, COBOL_ID, CMD_SEQ, �����Y�s, COBOL�̈敪��, COBOL�K�w���, COBOL���򔻒�, ���͍sTYPE, �����s������, �sCHK

        CMD_SEQ = CMD_SEQ + 1

        key_list = [
            "���YID", "COBOL_ID", "CMD_SEQ", "�����Y�s���", "�L�q�̈�", "�i��", "���򔻒�",
            "CMD����", "PARM", "�sCHK����"
        ]
        value_list = [
            �t�@�C����, COBOL_ID, CMD_SEQ, �����Y�s, COBOL�̈敪��, COBOL�K�w���, COBOL���򔻒�,
            ���͍sTYPE, �����s������, �sCHK
        ]

        sql, value = make_insert_sql(self.dbname, value_list, key_list)

        self.cursor.execute(sql, value)

        return True

    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close()

    def close_conn(self):
        self._close_conn()


def PARM�`����񔻒�_COBOL_AREA(cbl_area, parm_area):

    if cbl_area == "�̈�A����":
        if parm_area == "�C��" or parm_area == "�̈�A":
            return True
        else:
            return False
    if cbl_area == "�̈�B�̂�":
        if parm_area == "�C��" or parm_area == "�̈�B":
            return True
        else:
            return False
    else:
        MSG = "�z��O�̏���"
        return False


def PARM�`����񔻒�_COBOL_DIVISION(cbl_div, parm_div):

    if cbl_div == parm_div or parm_div == "����":
        return True
    else:
        return False


def ��O�L�[_COBOL(key):

    if key == "���x��" or key == "�ϐ�_SECTION��" or key == "�ϐ�_�i����":
        return True
    else:
        return False


def �ݒ�l���l�`�F�b�N_COBOL(parm_str):
    # 'if parm_str = "0":
    # '   MsgBox (parm_str & " : " & IsNumeric(parm_str))
    if IsNumeric(parm_str):
        return "���l"
    else:
        return "������"


def �ݒ�l�^�C�v�`�F�b�N_COBOL(parm_str):

    if "'" in str(parm_str) or "==" in str(parm_str) or "\"" in str(parm_str):
        return "�萔"
    else:
        return "�ϐ�"


def �ݒ�l��v�`�F�b�N_COBOL(parm_val, code_val):

    parm_val, code_val = str(parm_val), str(code_val)
    Rtn_Cd = False
    �ݒ�l�^�C�v = �ݒ�l�^�C�v�`�F�b�N_COBOL(code_val)

    #     '���̔���͏������d���̂œ��ʂɕ�����
    # '    if "��\��" in parm_val:
    # '       if not (�\��ꔻ��(code_val, 1)):
    # '            return True
    # '    else

    # '���x��
    if "���x��" in parm_val and \
        �ݒ�l���l�`�F�b�N_COBOL(code_val) == "���l":
        return True
    # '�R�s�[��
    elif "�R�s�[��" in parm_val and \
        �ݒ�l�^�C�v == "�ϐ�":
        return True
    # '�T�u���[�`��
    elif "�T�u���[�`��" in parm_val and \
        �ݒ�l�^�C�v == "�ϐ�":
        return True
    # '�ϐ�
    elif "�ϐ�" in parm_val:
        # '�ϐ���     '20130919 �x�m�ʑΉ��i���R�ʉ^�Č��j
        if parm_val == "�ϐ���":
            if �ݒ�l�^�C�v == "�ϐ�" and \
                code_val != "PIC" and code_val != "REDEFINES" and code_val != ")":
                return True
        else:
            if �ݒ�l�^�C�v == "�ϐ�":
                return True
    # '�萔
    elif "�萔" in parm_val and \
        �ݒ�l�^�C�v == "�萔":
        return True
    # '���l
    elif "���l" in parm_val and \
        �ݒ�l���l�`�F�b�N_COBOL(code_val) == "���l":
        return True
    # '�\���i��L�����ȊO�j
    elif parm_val == code_val:
        return True
    else:
        return False

    return Rtn_Cd


def �����s�����񐶐�����(TokenSheet_str):

    TokenSheet_str = [str(s) for s in TokenSheet_str]
    �����s������ = " ".join(TokenSheet_str)

    return DB����(�����s������)


def �ݒ�l��v�F��������_COBOL(parm_val, code_val, proc_cond):
    global SUB_SQL����_COBOL_3_
    global COBOL_�֘A�敪, COBOL_�֘A���Y, COBOL_�֘A���Y_TRANID, COPY_�ϐ�, �T�u���[�`���L��, COPY_���x��, re_flg
    ### �Z���̐F�����͑�ςɂȂ�̂�python�łł͈�U��߂�

    if re_flg:
        pass

    # '�Z�N�V����
    elif "SECTION��" in parm_val:
        pass

    # '�i��
    elif "�i����" in parm_val:
        pass

    # '�R�s�[��
    elif "�R�s�[��" in parm_val:
        COBOL_�֘A�敪 = "COPY"
        COBOL_�֘A���Y = code_val
        COBOL_�֘A���Y_TRANID = ""
        SUB_SQL����_COBOL_3_.insert()

    # '�T�u���[�`��
    elif "�T�u���[�`��" in parm_val:
        COBOL_�֘A�敪 = "CALL"
        COBOL_�֘A���Y = code_val
        COBOL_�֘A���Y_TRANID = ""
        SUB_SQL����_COBOL_3_.insert()
        #    '�T�u���[�`���L���ݒ�
        �T�u���[�`���L�� = "��"

    # 'EXEC CICS LINK PROGRAM
    elif "ECLP" in parm_val:
        COBOL_�֘A�敪 = "ECLP"
        COBOL_�֘A���Y = code_val
        COBOL_�֘A���Y_TRANID = ""
        SUB_SQL����_COBOL_3_.insert()

    # 'EXEC CICS START TRANSID
    elif "ECST" in parm_val:
        COBOL_�֘A�敪 = "ECST"
        COBOL_�֘A���Y = ""
        COBOL_�֘A���Y_TRANID = code_val
        SUB_SQL����_COBOL_3_.insert()

    # 'EXEC CICS SEND MAP
    elif "ECSM" in parm_val:
        COBOL_�֘A�敪 = "ECSM"
        COBOL_�֘A���Y = code_val
        COBOL_�֘A���Y_TRANID = ""
        SUB_SQL����_COBOL_3_.insert()

    # 'EXEC CICS HANDLE ABEND PROGRAM
    elif "ECHA" in parm_val:
        COBOL_�֘A�敪 = "ECHA"
        COBOL_�֘A���Y = code_val
        COBOL_�֘A���Y_TRANID = ""
        SUB_SQL����_COBOL_3_.insert()

    # 'EXEC CICS WRITEQ TD QUEUE
    elif "ECWTQ" in parm_val:
        COBOL_�֘A�敪 = "ECWTQ"
        COBOL_�֘A���Y = code_val
        COBOL_�֘A���Y_TRANID = ""
        SUB_SQL����_COBOL_3_.insert()

    # 'EXEC CICS READ TRANSACTION
    elif "ECRT" in parm_val:
        COBOL_�֘A�敪 = "ECRT"
        COBOL_�֘A���Y = ""
        COBOL_�֘A���Y_TRANID = code_val
        SUB_SQL����_COBOL_3_.insert()

    # 'EXEC CICS READ UPDATE DATASET
    elif "ECRUD" in parm_val:
        COBOL_�֘A�敪 = "ECRUD"
        COBOL_�֘A���Y = code_val
        COBOL_�֘A���Y_TRANID = ""
        SUB_SQL����_COBOL_3_.insert()

    # 'EXEC CICS READ DATASET
    elif "ECRD" in parm_val:
        COBOL_�֘A�敪 = "ECRD"
        COBOL_�֘A���Y = code_val
        COBOL_�֘A���Y_TRANID = ""
        SUB_SQL����_COBOL_3_.insert()

    # '�ϐ���
    elif parm_val == "�ϐ���":
        COPY_�ϐ� = code_val
    # '�ϐ�
    elif "�ϐ�" in parm_val:
        pass

    # '�萔
    elif "�萔" in parm_val:
        pass

    # '���l
    elif "���l" in parm_val:
        pass

    # '���x����
    elif "���x��" in parm_val:
        COPY_���x�� = code_val

    # '������
    elif proc_cond == "PROC-����":
        pass

    # '�\���i��L�����ȊO�j
    elif parm_val == code_val:
        pass

    else:
        pass


#     '�ϐ��Z�b�g����
# '    Select Case parm_val
# '           Case "JOB"
# '                JOB_ID = TokenSheet2.Cells(�����s, 2).Value
# '           Case "�萔_�R�����g"
# '                JOB_�R�����g = code_val
# '           Case "�ϐ�_�^�C�v�@"
# '                COPY_�^�C�v = code_val
# '           Case "����_���l"
# '                COPY_���� = code_val
# '                COPY_����_������ = code_val
# '           Case "�����⏕_���l"
# '                COPY_���� = code_val
# '                COPY_����_������ = COPY_����_������ & "," & code_val
# '           Case "�ϐ�_REDEFINES"
# '                COPY_REDIFINE = code_val
# '                REDIFINE_����_���x�� = COPY_���x��
# '           Case "OCCURS_���l"
# '                COPY_OCCURS = code_val
# '                OCCOURS_����_���x�� = COPY_���x��
# '                OCCOURS_�� = COPY_OCCURS
# '           Case "COMP-3"
# '                COPY_�^�C�v2 = "COMP-3"
# '           Case "�ϐ�_�^�C�v�A"     '�uCOMP-3�v�ȂǗD�悵�Đ��䂵�������̂�����ΑO�ɐݒ肷��
# '                COPY_�^�C�v2 = code_val


def analysis1_5_structure_COBOL(TokenSheet2,
                                fileName,
                                db_path,
                                �ݒ����HIT���o��=False,
                                ���͏���HIT���o��=False,
                                �݌v����HIT���o��=False,
                                �ݒ����HIT_NG���o��=True,
                                conn=None,
                                cursor=None):
    global SUB_SQL����_COBOL_3_

    global �t�@�C����,COBOL_ID,CMD_SEQ,�����Y�s,COBOL�̈敪��,COBOL�K�w���,COBOL���򔻒�,���͍sTYPE,�����s������,�sCHK, \
            ���C�u����ID,PGM_ID,�t�@�C��IO�L��,PARM�L��,�T�u���[�`���L��,SQL�L��,��ʗL��,ALL_chk_ok, \
            COBOL_�֘A�敪,COBOL_�֘A���Y,COBOL_�֘A���Y_TRANID,\
            P_�t�@�C����,P_CBL_ID,P_CMD����,P_�ďo���Y,P_�ďoPARM, \
            re_flg

    reset_all()

    SUB_SQL����_COBOL_0_ = SUB_SQL����_COBOL_0(conn, cursor)
    SUB_SQL����_COBOL_3_ = SUB_SQL����_COBOL_3(conn, cursor)
    SUB_SQL����_COBOL_4_ = SUB_SQL����_COBOL_4(conn, cursor)

    ALL_chk_ok = True  #'�V�[�g�P�ʂőS�Ă̐ݒ�p�^�[�����o�^����Ă��邩�ǂ����i�����lTrue�j

    #    '�ϐ�������
    #    'COBOL_ID = Replace(Replace(�t�@�C����, ".cob", ""), ".cbl", "") '�g���q�ɍ��킹�Đݒ�
    #    'COBOL_ID = Replace(Replace(���W���[��ID, ".cob", ""), ".cbl", "") '�g���q�ɍ��킹�Đݒ� TODO ���@�Ƃ̂���Ή�
    �t�@�C����, ���C�u����ID, _, COBOL_ID = GetFileInfo(fileName)

    PGM_ID = "��"

    FILE_SEQ = 0
    CMD_SEQ = 0

    �t�@�C��IO�L�� = ""
    PARM�L�� = ""
    �T�u���[�`���L�� = ""
    SQL�L�� = ""
    ��ʗL�� = ""

    �sCHK = "NOT_CEHCK"
    �����s = 0  #'TokenSheet�@�s�|�C���^
    ��� = 6  #   'TokenSheet2 ��|�C���^
    ���2 = 7  #   'CobolSheet ��|�C���^
    #'���͍sTYPE = ""     '�s�P�ʏ��Ȃ̂ł����ł͂Ȃ�

    # �@: �ACOBOL_CMD��� Process
    for item in TokenSheet2:
        COBOL_�֘A���Y_TRANID = ""
        COBOL_�֘A�敪 = item[���]

        if not natural_analysis_check(COBOL_�֘A�敪):
            continue

        # �ACOBOL_CMD��� Insert
        �����Y�s = item[1]
        COBOL�K�w��� = item[4]
        �����s������ = �����s�����񐶐�����(
            item[6:]
        )
        ���͍sTYPE = item[���]
        SUB_SQL����_COBOL_4_.insert()

        # �ACOBOL_�֘A���Y Process
        if COBOL_�֘A�敪 == "CALL":
            COBOL_�֘A���Y = item[���2]
            SUB_SQL����_COBOL_3_.insert()

        elif COBOL_�֘A�敪 == "CALLNAT":
            COBOL_�֘A���Y = item[���2]
            SUB_SQL����_COBOL_3_.insert()

        elif COBOL_�֘A�敪 == "FETCH":
            COBOL_�֘A���Y = item[���2]
            SUB_SQL����_COBOL_3_.insert()

        elif COBOL_�֘A�敪 == "PERFORM":
            COBOL_�֘A���Y = item[���2]
            SUB_SQL����_COBOL_3_.insert()

        elif COBOL_�֘A�敪 == "STACK":
            if len(item) <= 8:
                continue
            else:
                COBOL_�֘A���Y = item[8]
                SUB_SQL����_COBOL_3_.insert()

        elif COBOL_�֘A�敪 == "INPUT":
            for index, input in enumerate(item):
                if input == "USING" and item[index + 1] == "MAP":
                    COBOL_�֘A�敪 = "MAP"
                    COBOL_�֘A���Y = item[index + 2]
                    SUB_SQL����_COBOL_3_.insert()
                    break

    SUB_SQL����_COBOL_0_.insert()  #'��{��񂾂��ǌォ��ǉ������̂Łu0�v�ɂ���

    return ALL_chk_ok
