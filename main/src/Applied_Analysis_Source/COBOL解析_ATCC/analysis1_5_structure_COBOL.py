#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

import reserved_word_table_COBOL

cobol_analysis_keyword_dict = reserved_word_table_COBOL.get_cobol_analysis_keyword_dict()

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

SUB_SQL����_COBOL_0_ = None
SUB_SQL����_COBOL_3_ = None
SUB_SQL����_COBOL_4_ = None

def check_analysis_line(���͍sTYPE):
    if ���͍sTYPE in cobol_analysis_keyword_dict:
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

    �����s = 0  #'TokenSheet�@�s�|�C���^
    ��� = 6  #   'TokenSheet2 ��|�C���^
    ���2 = 7  #   'CobolSheet ��|�C���^
    #'���͍sTYPE = ""     '�s�P�ʏ��Ȃ̂ł����ł͂Ȃ�
    �sCHK = "NOT_CEHCK"

    for cobol_line in TokenSheet2:
        COBOL�K�w��� = cobol_line[4]
        COBOL�̈敪�� = cobol_line[3]
        COBOL���򔻒� = cobol_line[5]
        �����Y�s = cobol_line[1]
        ���͍sTYPE = cobol_line[���]
        # '�s���x���̏����ł��邪�s���Z���������O�Ŏ��{����Ă��肱���ōs���K�v������
        # '���R�}���h���ݒ�i�ڍ׉��̗]�n����j
        if IsNumeric(cobol_line[���]):
            ���͍sTYPE = "�f�[�^��`"
        elif COBOL�̈敪�� == "�̈�A����":
            if ��� + 1 < len(cobol_line) and cobol_line[��� + 1] == "DIVISION":
                ���͍sTYPE = "DIVISION"
            elif ��� + 1 < len(cobol_line) and cobol_line[��� + 1] == "SECTION":
                ���͍sTYPE = "SECTION"
                if cobol_line[���] == "LINKAGE":  #'PARM�L���ݒ�
                    PARM�L�� = "��"
            else:
                if COBOL�K�w��� == "�葱����":
                    ���͍sTYPE = "���x��"
                else:
                    ���͍sTYPE = cobol_line[���]

                    if ���͍sTYPE == "PROGRAM-ID":
                        if ��� + 1 < len(cobol_line) and cobol_line[��� + 1] == ".":
                            if ��� + 2 < len(cobol_line):
                                PGM_ID = cobol_line[��� + 2]
                            else:
                                PGM_ID = ""
                        else:
                            if ��� + 1 < len(cobol_line):
                                PGM_ID = cobol_line[��� + 1]
                            else:
                                PGM_ID = ""
        else:
            ���͍sTYPE = cobol_line[���]
            if ���͍sTYPE == "EXEC" and cobol_line[��� + 1] == "SQL":
                ���͍sTYPE = "SQL"
                SQL�L�� = "��"
            elif ���͍sTYPE == "OPEN":
                �t�@�C��IO�L�� = "��"

        # Analysis CALL�ACOPY
        if not check_analysis_line(���͍sTYPE):
            continue

        �����s������ = �����s�����񐶐�����(cobol_line[���:])
        �ݒ�l��v�F��������_COBOL(cobol_analysis_keyword_dict[���͍sTYPE], cobol_line[���2], COBOL���򔻒�)
        SUB_SQL����_COBOL_4_.insert()

    SUB_SQL����_COBOL_0_.insert()  #'��{��񂾂��ǌォ��ǉ������̂Łu0�v�ɂ���

    return ALL_chk_ok
