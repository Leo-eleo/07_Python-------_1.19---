#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


def reset_all():
    global ���C�u����ID, �t�@�C����, COBOL_ID, SELECT_ID, DD_ID, SELECT_LINE_INFO, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE, FDSD_INFO, ITEM_INFO, RECORD_SIZE_STR

    ���C�u����ID = ""
    �t�@�C���� = ""
    COBOL_ID = ""
    SELECT_ID = ""
    DD_ID = ""
    SELECT_LINE_INFO = ""
    FDSD_ID = ""
    RECORD_ID = ""
    COPY = ""
    RECORD_SIZE = ""
    FDSD_INFO = ""
    ITEM_INFO = ""
    RECORD_SIZE_STR = ""


class SUB_SQL����_COBOL_1:

    def __init__(self, conn, cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�ACOBOL_���o�͏��1"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}

    def insert(self):
        if self.dic == None:
            self.setup()

        global �t�@�C����, COBOL_ID, SELECT_ID, DD_ID, SELECT_LINE_INFO

        key_list = ["���YID", "COBOL_ID", "SELECT_ID", "ASSIGN_ID", "LINE_INFO"]
        value_list = [�t�@�C����, COBOL_ID, SELECT_ID, DD_ID, SELECT_LINE_INFO]

        sql, value = make_insert_sql(self.dbname, value_list, key_list)

        self.cursor.execute(sql, value)

        return True

    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close()

    def close_conn(self):
        self._close_conn()


class SUB_SQL����_COBOL_2:

    def __init__(self, conn, cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�ACOBOL_���o�͏��2"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}

    def insert(self):
        if self.dic == None:
            self.setup()

        global �t�@�C����, COBOL_ID, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE, FDSD_INFO, ITEM_INFO

        key_list = [
            "���YID", "COBOL_ID", "FILE_ID", "RECORD_ID", "COPY", "RECORD_SIZE",
            "FDSD_INFO", "LINE_INFO"
        ]
        value_list = [
            �t�@�C����, COBOL_ID, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE, FDSD_INFO,
            ITEM_INFO
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


class SUB_SQL����_COBOL_5:

    def __init__(self, conn, cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�ACOBOL_���o�͏��3"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}

    def insert(self):
        if self.dic == None:
            self.setup()

        global �t�@�C����, COBOL_ID, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE_STR, FDSD_INFO, ITEM_INFO

        key_list = [
            "���YID", "COBOL_ID", "FILE_ID", "RECORD_ID", "COPY", "RECORD_SIZE",
            "FDSD_INFO", "LINE_INFO"
        ]
        value_list = [
            �t�@�C����, COBOL_ID, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE_STR,
            FDSD_INFO, ITEM_INFO
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


class SUB_SQL����_����_3:

    def __init__(self, conn, cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "����_PGM_IO���"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}

    def insert(self, info1, lib2, id3, io4, file5):
        if self.dic == None:
            self.setup()

        key_list = ["���Y����", "LIBRARY_ID", "���YID", "���o�͋敪", "�t�@�C����"]
        value_list = [info1, lib2, id3, io4, file5]

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


def ���R�[�hID�L������_COBOL(P_�ڑ���, P_�ڑ���, P_�z��):
    if "\"" in P_�ڑ��� or "\"" in P_�ڑ���:
        return False

    elif P_�ڑ��� == "SPACE" or P_�ڑ��� == "SPACE":
        return False

    elif P_�ڑ��� == "ZERO" or P_�ڑ��� == "ZERO":
        return False

    # '���ɂ�����Ƃ��������Ƃ肠����

    for i in range(len(P_�z��)):

        if P_�z��[i] == P_�ڑ��� or P_�z��[i] == P_�ڑ���:
            return True

    return False


def COBOL_IO_Info(TokenSheet2, fileName, db_path, conn, cursor):
    global ���C�u����ID, �t�@�C����, COBOL_ID, SELECT_ID, DD_ID, SELECT_LINE_INFO, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE, FDSD_INFO, ITEM_INFO, RECORD_SIZE_STR

    reset_all()
    SUB_SQL����_COBOL_1_ = SUB_SQL����_COBOL_1(conn, cursor)
    SUB_SQL����_COBOL_2_ = SUB_SQL����_COBOL_2(conn, cursor)
    SUB_SQL����_COBOL_5_ = SUB_SQL����_COBOL_5(conn, cursor)
    SUB_SQL����_����_3_ = SUB_SQL����_����_3(conn, cursor)

    ALL_chk_ok = True  #'�V�[�g�P�ʂőS�Ă̐ݒ�p�^�[�����o�^����Ă��邩�ǂ����i�����lTrue�j

    #    '�ϐ�������
    #    'COBOL_ID = Replace(Replace(�t�@�C����, ".cob", ""), ".cbl", "") '�g���q�ɍ��킹�Đݒ�
    #    'COBOL_ID = Replace(Replace(���W���[��ID, ".cob", ""), ".cbl", "") '�g���q�ɍ��킹�Đݒ� TODO ���@�Ƃ̂���Ή�
    �t�@�C����, ���C�u����ID, _, COBOL_ID = GetFileInfo(fileName)

    �����s = 0  #'TokenSheet�@�s�|�C���^
    ��� = 6  #   'TokenSheet2 ��|�C���^
    #'���͍sTYPE = ""     '�s�P�ʏ��Ȃ̂ł����ł͂Ȃ�

    L_MOVE�� = ""
    L_MOVE�� = ""
    L_varArray = []
    # 'L_varResult As Variant

    L_varCnt = 0

    �w�b�_�o��_SELECT = False
    �w�b�_�o��_FDSD = False
    WORK�̈�_STRART = False
    �w�b�_�o��_INOUT = False
    �o�͍s = 0

    #    '�@***********  ���o�͊֘A���Č���  ***********

    for i in range(len(TokenSheet2)):
        �����s = i
        TokenSheet2_GYO = TokenSheet2[i]
        # '������ = 5
        ������ = ���
        # 'COBOL�K�w��� = TokenSheet2_GYO[3]
        COBOL�K�w��� = TokenSheet2_GYO[4]
        # 'CMD_fld = TokenSheet2_GYO[5]
        CMD_fld = TokenSheet2_GYO[6]

        # 'code_val = TokenSheet2_GYO[������]

        # '�K�w���ɂ�镪��
        # AnalyzeSheet.Select

        if COBOL�K�w��� == "����":
            if CMD_fld == "SELECT":

                if �w�b�_�o��_SELECT == False:
                    �o�͍s = �o�͍s + 2
                    # AnalyzeSheet.Cells(�o�͍s, 1] = "�t�@�C����"
                    # AnalyzeSheet.Cells(�o�͍s, 2] = "DD��"
                    # AnalyzeSheet.Cells(�o�͍s, 3] = "���o�͏��"

                    �w�b�_�o��_SELECT = True

                # '�����s������쐬
                # 'SUB_�����s�����񐶐����� (5)   '�����J�n��i5��ڂ������ɂ���j
                �����s������ = �����s�����񐶐�����(TokenSheet2_GYO[���:])  #'�����J�n��i5��ڂ������ɂ���j
                SELECT_LINE_INFO = �����s������

                # 'SELECT_ID�ݒ�i�K�{�j
                # 'if TokenSheet2_GYO[6] = "OPTIONAL":
                if len(TokenSheet2_GYO
                       ) > 7 and TokenSheet2_GYO[7] == "OPTIONAL":
                    # 'SELECT_ID = TokenSheet2_GYO[7]
                    if len(TokenSheet2_GYO) > 8:
                        SELECT_ID = TokenSheet2_GYO[8]
                    else:
                        SELECT_ID = ""
                else:
                    # 'SELECT_ID = TokenSheet2_GYO[6]
                    if len(TokenSheet2_GYO) > 7:
                        SELECT_ID = TokenSheet2_GYO[7]
                    else:
                        SELECT_ID = ""

                # 'ASSIGN_ID�ݒ�i�K�{�j
                DD_ID = ""
                while ������ < len(TokenSheet2_GYO):
                    code_val = TokenSheet2_GYO[������]
                    if code_val == "ASSIGN":
                        if ������ + 1 < len(TokenSheet2_GYO) and TokenSheet2_GYO[
                                ������ + 1] == "TO":
                            if ������ + 2 < len(TokenSheet2_GYO):
                                DD_ID = TokenSheet2_GYO[������ + 2]
                            else:
                                DD_ID = ""
                        else:
                            if ������ + 1 < len(TokenSheet2_GYO):
                                DD_ID = TokenSheet2_GYO[������ + 1]
                            else:
                                DD_ID = ""

                    ������ = ������ + 1

                SUB_SQL����_COBOL_1_.insert()

        elif COBOL�K�w��� == "�f�[�^��":
            if CMD_fld == "FD" or CMD_fld == "SD":

                if �w�b�_�o��_FDSD == False:
                    �o�͍s = �o�͍s + 2
                    # AnalyzeSheet.Cells(�o�͍s, 1] = "�t�@�C����"
                    # AnalyzeSheet.Cells(�o�͍s, 2] = "���R�[�h��"
                    # AnalyzeSheet.Cells(�o�͍s, 3] = "�֘A�R�s�[��"
                    # AnalyzeSheet.Cells(�o�͍s, 4] = "���o�̓p�����[�^"
                    # AnalyzeSheet.Cells(�o�͍s, 5] = "���o�͒�`���"

                    �w�b�_�o��_FDSD = True
                # '�����s������쐬
                # 'SUB_�����s�����񐶐����� (5)   '�����J�n��i5��ڂ������ɂ���j
                �����s������ = �����s�����񐶐�����(TokenSheet2_GYO[���:])  #'�����J�n��i5��ڂ������ɂ���j
                FDSD_INFO = �����s������

                # '�t�@�C�����ݒ�i�K�{�j
                # 'FDSD_ID = TokenSheet2_GYO[6]
                if len(TokenSheet2_GYO) > 7:
                    FDSD_ID = TokenSheet2_GYO[7]
                else:
                    FDSD_ID = ""

                COPY = ""
                RECORD_ID = ""
                ITEM_INFO = ""
                �����s2 = �����s  #'�����s�ޔ�
                �����s = �����s + 1  #'���ڏ�񌟍��̈׃J�E���g�A�b�v
                while �����s < len(TokenSheet2):
                    TokenSheet2_temp = TokenSheet2[�����s]
                    # 'code_val = TokenSheet2_GYO[5]
                    code_val = TokenSheet2_temp[���]
                    # '�����s������쐬
                    �����s������ = �����s�����񐶐�����(
                        TokenSheet2_temp[���:])  #   '�����J�n��i5��ڂ������ɂ���j
                    if ITEM_INFO == "":
                        ITEM_INFO = �����s������
                    else:
                        ITEM_INFO = ITEM_INFO + "\n" + �����s������

                    if code_val == "1" or code_val == "01":
                        # 'RECORD_ID = TokenSheet2_GYO[6]
                        if len(TokenSheet2_temp) > 7:
                            RECORD_ID = TokenSheet2_temp[7]
                        else:
                            RECORD_ID = ""

                        L_varCnt = L_varCnt + 1
                        # '���C�A�E�g�����p�̃��R�[�hID�̔z��������Ő�������
                        L_varArray.append(RECORD_ID)

                    elif code_val == "COPY":
                        if COPY == "":
                            # 'COPY = TokenSheet2_GYO[6]
                            if len(TokenSheet2_temp) > 7:
                                COPY = TokenSheet2_temp[7]
                        else:
                            # 'COPY = COPY + "," + TokenSheet2_GYO[6]
                            if len(TokenSheet2_temp) > 7:
                                COPY = COPY + "," + TokenSheet2_temp[7]

                    �����s = �����s + 1
                    # 'Loop Until TokenSheet2_GYO[5] != "COPY" or _
                    # '    Not IsNumeric(TokenSheet2_GYO[5])
                    if �����s >= len(TokenSheet2):
                        break
                    if TokenSheet2[�����s][���] != "COPY" or IsNumeric(
                            TokenSheet2[�����s][���]) == False:
                        break

                RECORD_SIZE = 0  #'�Œ�ŏo��
                SUB_SQL����_COBOL_2_.insert()

                �����s = �����s2  #'�s�J�E���g��߂�

            if WORK�̈�_STRART:

                if CMD_fld == "01" or CMD_fld == "1":

                    if len(TokenSheet2_GYO) > 7:
                        FDSD_ID = TokenSheet2_GYO[7]
                    else:
                        FDSD_ID = ""
                    RECORD_ID = ""
                    COPY = "WORK�̈�"
                    RECORD_SIZE_STR = ""  # '�Œ�ŏo��
                    ITEM_INFO = ""
                    FDSD_INFO = ""
                    SUB_SQL����_COBOL_5_.insert()

            else:

                if CMD_fld == "WORKING-STORAGE":
                    WORK�̈�_STRART = True

        elif COBOL�K�w��� == "�葱����":

            if �w�b�_�o��_INOUT == False:
                �o�͍s = �o�͍s + 2
                # AnalyzeSheet.Cells(�o�͍s, 1] = "���o�͋敪"
                # AnalyzeSheet.Cells(�o�͍s, 2] = "�t�@�C����"

                �w�b�_�o��_INOUT = True
            if CMD_fld == "OPEN":
                # 'PGM_IO = TokenSheet2_GYO[6]
                # 'PGM_IO = TokenSheet2_GYO[��� + 1]
                # '������ = 7
                # '������ = ��� + 2
                ������ = ��� + 1
                while ������ < len(TokenSheet2_GYO):
                    io = TokenSheet2_GYO[������]
                    if io == "INPUT":
                        PGM_IO = "INPUT"
                    elif io == "OUTPUT":
                        PGM_IO = "OUTPUT"
                    elif io == "I-O":
                        PGM_IO = "I-O"
                    elif io == "EXTEND":
                        PGM_IO = "EXTEND"
                    elif io == ",":
                        pass
                    else:
                        SUB_SQL����_����_3_.insert("COBOL", ���C�u����ID, COBOL_ID,
                                               PGM_IO, TokenSheet2_GYO[������])
                        # 'Call SUB_SQL����_����_3("COBOL", ���C�u����ID, �t�@�C����, PGM_IO, TokenSheet2_GYO[������])
                        # '�\����̓V�[�g�o��
                        �o�͍s = �o�͍s + 1
                        # AnalyzeSheet.Cells(�o�͍s, 1] = PGM_IO
                        # AnalyzeSheet.Cells(�o�͍s, 2] = TokenSheet2_GYO[������]

                    ������ = ������ + 1
                    if ������ >= len(
                            TokenSheet2_GYO) or TokenSheet2_GYO[������] == ".":
                        break

            # '���C�A�E�g�O���[�s���O
            if CMD_fld == "READ" and len(
                    TokenSheet2_GYO) > 9 and TokenSheet2_GYO[8] == "INTO":

                FDSD_ID = TokenSheet2_GYO[7]
                RECORD_ID = TokenSheet2_GYO[9]
                COPY = "�O���[�s���O"
                RECORD_SIZE_STR = "NULL"  # '�Œ�ŏo��
                ITEM_INFO = "READ"
                FDSD_INFO = "�@"
                SUB_SQL����_COBOL_5_.insert()

            elif CMD_fld == "WRITE" and len(
                    TokenSheet2_GYO) > 9 and TokenSheet2_GYO[8] == "FROM":

                FDSD_ID = TokenSheet2_GYO[7]
                RECORD_ID = TokenSheet2_GYO[9]
                COPY = "�O���[�s���O"
                RECORD_SIZE_STR = "NULL"  #'�Œ�ŏo��
                ITEM_INFO = "WRITE"
                FDSD_INFO = "�A"
                SUB_SQL����_COBOL_5_.insert()

            elif CMD_fld == "MOVE" and L_varCnt > 0:
                if len(TokenSheet2_GYO) > 7:
                    L_MOVE�� = TokenSheet2_GYO[7]
                else:
                    L_MOVE�� = ""

                ������ = ��� + 2  #'MOVE�̌�̃L�[���[�h�͎擾�����̂Ŏ���TO�̌��T���B�i�����̈ڑ��悪����ꍇ�͍��͍l�����Ȃ��j
                hit_flg = False

                while ������ < len(TokenSheet2_GYO):
                    code_val = TokenSheet2_GYO[������]

                    if code_val == "TO":
                        if ������ + 1 < len(TokenSheet2_GYO):
                            L_MOVE�� = TokenSheet2_GYO[������ + 1]  #'TO�̌�̃L�[���[�h���擾
                        else:
                            L_MOVE�� = ""
                        hit_flg = True

                    ������ = ������ + 1
                    if ������ >= len(TokenSheet2_GYO) or TokenSheet2_GYO[
                            ������] == "." or hit_flg == True:
                        break

                # 'if InStr(L_MOVE��, """") > 0 or InStr(L_MOVE��, """") > 0:
                # '    '�����ꂩ���萔�̏ꍇ�̓`�F�b�N���Ȃ�
                # 'else
                #     'MOVE���߂̈ڑ����܂��͈ڑ���̕ϐ������R�[�hID�̔z��Ɋ܂܂�Ă���Ώo�͑Ώ�

                if ���R�[�hID�L������_COBOL(L_MOVE��, L_MOVE��, L_varArray):

                    # 'if Filter(L_varArray, L_MOVE��) != -1 or Filter(L_varArray, L_MOVE��) != -1:
                    FDSD_ID = L_MOVE��
                    RECORD_ID = L_MOVE��
                    COPY = "�O���[�s���O"
                    RECORD_SIZE_STR = "NULL"  #'�Œ�ŏo��
                    ITEM_INFO = "MOVE"
                    FDSD_INFO = "�B"
                    SUB_SQL����_COBOL_5_.insert()

        else:

            �����s = �����s + 1

    return ALL_chk_ok
