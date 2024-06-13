#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

def GetFileInfo(FileName):
    """ return FileName, library, gouki, and module name

    Args:
        FileName (_string_): _FileName is consider the case like U.ADL.SOU#B%B%ACS3 _

    Returns:
        _type_: _FileName, library, gouki, and module name_
    """
    # BaseName = take_extensions(FileName)
    if FileName.find("%") == -1:
        return "A", "B", "C", FileName
    tmp_list = FileName.split("%")

    assert len(tmp_list) == 3, "Filename format is invalid : " + FileName

    library,gouki,module = tmp_list
    return FileName,library,"%"+gouki,module

def reset_all():
    global ���C�u����ID, �t�@�C����, PLI_ID, SELECT_ID, DD_ID, SELECT_LINE_INFO, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE, FDSD_INFO, ITEM_INFO, RECORD_SIZE_STR

    ���C�u����ID = ""
    �t�@�C���� = ""
    PLI_ID = ""
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


class SUB_SQL����_PLI_1:

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

        global �t�@�C����, PLI_ID, SELECT_ID, DD_ID, SELECT_LINE_INFO

        key_list = ["���YID", "COBOL_ID", "SELECT_ID", "ASSIGN_ID", "LINE_INFO"]
        value_list = [�t�@�C����, PLI_ID, SELECT_ID, DD_ID, SELECT_LINE_INFO]

        sql, value = make_insert_sql(self.dbname, value_list, key_list)

        self.cursor.execute(sql, value)

        return True

    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close()

    def close_conn(self):
        self._close_conn()


class SUB_SQL����_PLI_2:

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

        global �t�@�C����, PLI_ID, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE, FDSD_INFO, ITEM_INFO

        key_list = [
            "���YID", "COBOL_ID", "FILE_ID", "RECORD_ID", "COPY", "RECORD_SIZE",
            "FDSD_INFO", "LINE_INFO"
        ]
        value_list = [
            �t�@�C����, PLI_ID, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE, FDSD_INFO,
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


class SUB_SQL����_PLI_5:

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

        global �t�@�C����, PLI_ID, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE_STR, FDSD_INFO, ITEM_INFO

        key_list = [
            "���YID", "COBOL_ID", "FILE_ID", "RECORD_ID", "COPY", "RECORD_SIZE",
            "FDSD_INFO", "LINE_INFO"
        ]
        value_list = [
            �t�@�C����, PLI_ID, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE_STR,
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


def ���R�[�hID�L������_PLI(P_�ڑ���, P_�ڑ���, P_�z��):
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


def PLI_IO_Info(TokenSheet2, fileName, db_path, conn, cursor,
                filename_dd_io_table, filename_copy_relation_table,
                io_filename_table):
    global ���C�u����ID, �t�@�C����, PLI_ID, SELECT_ID, DD_ID, SELECT_LINE_INFO, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE, FDSD_INFO, ITEM_INFO, RECORD_SIZE_STR

    reset_all()
    SUB_SQL����_PLI_1_ = SUB_SQL����_PLI_1(conn, cursor)
    SUB_SQL����_PLI_2_ = SUB_SQL����_PLI_2(conn, cursor)
    SUB_SQL����_PLI_5_ = SUB_SQL����_PLI_5(conn, cursor)
    SUB_SQL����_����_3_ = SUB_SQL����_����_3(conn, cursor)

    ALL_chk_ok = True  #'�V�[�g�P�ʂőS�Ă̐ݒ�p�^�[�����o�^����Ă��邩�ǂ����i�����lTrue�j

    #    '�ϐ�������
    #    'PLI_ID = Replace(Replace(�t�@�C����, ".cob", ""), ".cbl", "") '�g���q�ɍ��킹�Đݒ�
    #    'PLI_ID = Replace(Replace(���W���[��ID, ".cob", ""), ".cbl", "") '�g���q�ɍ��킹�Đݒ� TODO ���@�Ƃ̂���Ή�
    �t�@�C����, ���C�u����ID, _, PLI_ID = GetFileInfo(fileName)

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

    # PLI_���o�͏��1 Insert
    for item in filename_dd_io_table:
        SELECT_ID = item[0]
        DD_ID = item[1]
        SELECT_LINE_INFO = item[3]
        SUB_SQL����_PLI_1_.insert()

    # COBOL_���o�͏��2 Insert
    # #### Now is Blank

    # ����_PGM_IO��� Insert
    for item in io_filename_table:
        SUB_SQL����_����_3_.insert("PL/I", ���C�u����ID, PLI_ID, item[0], item[1])

    return ALL_chk_ok
