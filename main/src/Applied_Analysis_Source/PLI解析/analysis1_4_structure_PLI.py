#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

SUB_SQL����_PLI_0_ = None
SUB_SQL����_PLI_3_ = None
SUB_SQL����_PLI_4_ = None

def replace_parm(line, m_code, m_db, m_seg):
    if m_code == "����`" and m_db == "����`" and m_seg == "����`":
        return line
    else:
        return line.replace("@PARM@", fr"@PARM@(\\MD_CODE = {m_code}, \\MD_DBNAME = {m_db}, \\MD_SEGNAME = {m_seg})")

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
    global �t�@�C����, PLI_ID, CMD_SEQ, �����Y�s, PLI�̈敪��, PLI�K�w���, PLI���򔻒�, ���͍sTYPE, �����s������, �sCHK, \
        ���C�u����ID, PGM_ID, �t�@�C��IO�L��, PARM�L��, �T�u���[�`���L��, SQL�L��, ��ʗL��, ALL_chk_ok, \
        PLI_�֘A�敪, PLI_�֘A���Y, PLI_�֘A���Y_TRANID, \
        P_�t�@�C����, P_CBL_ID, P_CMD����, P_�ďo���Y, P_�ďoPARM, \
        re_flg

    re_flg = False
    ���C�u����ID = ""
    �t�@�C���� = ""
    PLI_ID = ""
    PLI�̈敪�� = ""
    PLI�K�w��� = ""
    PLI���򔻒� = ""
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
    PLI_�֘A�敪 = ""
    PLI_�֘A���Y = ""
    PLI_�֘A���Y_TRANID = ""

    P_�t�@�C���� = ""
    P_CBL_ID = ""
    P_CMD���� = ""
    P_�ďo���Y = ""
    P_�ďoPARM = ""


class SUB_SQL����_PLI_0:

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

        global �t�@�C����, ���C�u����ID, PLI_ID, PGM_ID, CMD_SEQ, �t�@�C��IO�L��, PARM�L��, �T�u���[�`���L��, SQL�L��, ��ʗL��, ALL_chk_ok

        if ALL_chk_ok == True:
            L_CHK = "OK"
        else:
            L_CHK = "NG"

        key_list = [
            "���YID", "LIBRARY_ID", "�����o��", "���W���[����", "CMD�s��", "��͌���",
            "�t�@�C��IO�L��", "PARM�L��", "�T�u���[�`���L��", "SQL�L��", "��ʗL��"
        ]
        value_list = [
            �t�@�C����, ���C�u����ID, PLI_ID, PGM_ID, CMD_SEQ, L_CHK, �t�@�C��IO�L��, PARM�L��,
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


class SUB_SQL����_PLI_3:

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

        global �t�@�C����, PLI_ID, PLI_�֘A�敪, PLI_�֘A���Y, PLI_�֘A���Y_TRANID

        key_list = ["���YID", "COBOL_ID", "�֘A�敪", "�֘A���Y", "�֘A���Y_TRANID"]
        value_list = [
            �t�@�C����, PLI_ID, PLI_�֘A�敪, PLI_�֘A���Y,
            PLI_�֘A���Y_TRANID.replace("'", "")
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


class SUB_SQL����_PLI_4:

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

        global �t�@�C����, PLI_ID, CMD_SEQ, �����Y�s, PLI�̈敪��, PLI�K�w���, PLI���򔻒�, ���͍sTYPE, �����s������, �sCHK

        CMD_SEQ = CMD_SEQ + 1

        key_list = [
            "���YID", "COBOL_ID", "CMD_SEQ", "�����Y�s���", "�L�q�̈�", "�i��", "���򔻒�",
            "CMD����", "PARM", "�sCHK����"
        ]
        value_list = [
            �t�@�C����, PLI_ID, CMD_SEQ, �����Y�s, PLI�̈敪��, PLI�K�w���, "", "CALL", �����s������,
            �sCHK
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


def analysis1_4_structure_PLI(TokenSheet2,
                              PLISheet,
                              fileName,
                              db_path,
                              call_list,
                              TmpSheet,
                              pli_keyword_dict,
                              pli_function_dict,
                              �ݒ����HIT���o��=False,
                              ���͏���HIT���o��=False,
                              �݌v����HIT���o��=False,
                              �ݒ����HIT_NG���o��=True,
                              conn=None,
                              cursor=None):
    global SUB_SQL����_PLI_3_

    global �t�@�C����, PLI_ID, CMD_SEQ, �����Y�s, PLI�̈敪��, PLI�K�w���, PLI���򔻒�, ���͍sTYPE, �����s������, �sCHK, \
        ���C�u����ID, PGM_ID, �t�@�C��IO�L��, PARM�L��, �T�u���[�`���L��, SQL�L��, ��ʗL��, ALL_chk_ok, \
        PLI_�֘A�敪, PLI_�֘A���Y, PLI_�֘A���Y_TRANID, \
        P_�t�@�C����, P_CBL_ID, P_CMD����, P_�ďo���Y, P_�ďoPARM, \
        re_flg

    reset_all()

    SUB_SQL����_PLI_0_ = SUB_SQL����_PLI_0(conn, cursor)
    SUB_SQL����_PLI_3_ = SUB_SQL����_PLI_3(conn, cursor)
    SUB_SQL����_PLI_4_ = SUB_SQL����_PLI_4(conn, cursor)

    ALL_chk_ok = True

    #    '�ϐ�������
    #    'PLI_ID = Replace(Replace(�t�@�C����, ".cob", ""), ".cbl", "") '�g���q�ɍ��킹�Đݒ�
    #    'PLI_ID = Replace(Replace(���W���[��ID, ".cob", ""), ".cbl", "") '�g���q�ɍ��킹�Đݒ� TODO ���@�Ƃ̂���Ή�
    �t�@�C����, ���C�u����ID, _, PLI_ID = GetFileInfo(fileName)

    PGM_ID = PLI_ID.split(".")[0]

    FILE_SEQ = 0
    CMD_SEQ = 0

    �t�@�C��IO�L�� = ""
    PARM�L�� = ""
    �T�u���[�`���L�� = ""
    SQL�L�� = ""
    ��ʗL�� = ""
    ��� = 6  # 'TokenSheet2 ��|�C���^

    �sCHK = "OK"
    PLI�̈敪�� = "PL/I"

    md_code = "����`"
    md_db_name = "����`"
    md_seg_name = "����`"


    for item in TokenSheet2:
        �����Y�s = item[1]
        PLI�K�w��� = item[4]

        # @PARM@ �ݒ�
        if item[���] == r"\\MD_CODE":
            md_code = item[��� + 2]
        elif item[���] == r"\\MD_DBNAME":
            md_db_name = item[��� + 2]
        elif item[���] == r"\\MD_SEGNAME":
            md_seg_name = item[��� + 2]

        # Find CALL
        if pli_keyword_dict.get(item[���]) == "CALL" or pli_function_dict.get(item[���]) != None:
            �����s������ = TmpSheet[�����Y�s - 1][8]
            �����s������ = replace_parm(�����s������, md_code, md_db_name, md_seg_name)
            SUB_SQL����_PLI_4_.insert()

    # COBOL_�֘A���Y
    for item in call_list:
        PLI_�֘A�敪 = item[1]
        PLI_�֘A���Y = item[2]
        PLI_�֘A���Y_TRANID = item[3]
        SUB_SQL����_PLI_3_.insert()

    # '��{��񂾂��ǌォ��ǉ������̂Łu0�v�ɂ���
    SUB_SQL����_PLI_0_.insert()

    return ALL_chk_ok
