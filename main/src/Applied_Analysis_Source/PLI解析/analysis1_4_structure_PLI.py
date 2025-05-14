#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

SUB_SQL生成_PLI_0_ = None
SUB_SQL生成_PLI_3_ = None
SUB_SQL生成_PLI_4_ = None

def replace_parm(line, m_code, m_db, m_seg):
    if m_code == "未定義" and m_db == "未定義" and m_seg == "未定義":
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
    global ファイル名, PLI_ID, CMD_SEQ, 元資産行, PLI領域分類, PLI階層情報, PLI分岐判定, 分析行TYPE, 検索行文字列, 行CHK, \
        ライブラリID, PGM_ID, ファイルIO有無, PARM有無, サブルーチン有無, SQL有無, 画面有無, ALL_chk_ok, \
        PLI_関連区分, PLI_関連資産, PLI_関連資産_TRANID, \
        P_ファイル名, P_CBL_ID, P_CMD分類, P_呼出資産, P_呼出PARM, \
        re_flg

    re_flg = False
    ライブラリID = ""
    ファイル名 = ""
    PLI_ID = ""
    PLI領域分類 = ""
    PLI階層情報 = ""
    PLI分岐判定 = ""
    検索行文字列 = ""
    分析行TYPE = ""
    行CHK = False
    CMD_SEQ = 0
    元資産行 = 0
    PGM_ID = ""
    ファイルIO有無 = ""
    PARM有無 = ""
    サブルーチン有無 = ""
    SQL有無 = ""
    画面有無 = ""
    ALL_chk_ok = True
    PLI_関連区分 = ""
    PLI_関連資産 = ""
    PLI_関連資産_TRANID = ""

    P_ファイル名 = ""
    P_CBL_ID = ""
    P_CMD分類 = ""
    P_呼出資産 = ""
    P_呼出PARM = ""


class SUB_SQL生成_PLI_0:

    def __init__(self, conn, cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "②COBOL_基本情報"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}

    def insert(self):
        if self.dic == None:
            self.setup()

        global ファイル名, ライブラリID, PLI_ID, PGM_ID, CMD_SEQ, ファイルIO有無, PARM有無, サブルーチン有無, SQL有無, 画面有無, ALL_chk_ok

        if ALL_chk_ok == True:
            L_CHK = "OK"
        else:
            L_CHK = "NG"

        key_list = [
            "資産ID", "LIBRARY_ID", "メンバ名", "モジュール名", "CMD行数", "解析結果",
            "ファイルIO有無", "PARM有無", "サブルーチン有無", "SQL有無", "画面有無"
        ]
        value_list = [
            ファイル名, ライブラリID, PLI_ID, PGM_ID, CMD_SEQ, L_CHK, ファイルIO有無, PARM有無,
            サブルーチン有無, SQL有無, 画面有無
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


class SUB_SQL生成_PLI_3:

    def __init__(self, conn, cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "②COBOL_関連資産"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}

    def insert(self):
        if self.dic == None:
            self.setup()

        global ファイル名, PLI_ID, PLI_関連区分, PLI_関連資産, PLI_関連資産_TRANID

        key_list = ["資産ID", "COBOL_ID", "関連区分", "関連資産", "関連資産_TRANID"]
        value_list = [
            ファイル名, PLI_ID, PLI_関連区分, PLI_関連資産,
            PLI_関連資産_TRANID.replace("'", "")
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


class SUB_SQL生成_PLI_4:

    def __init__(self, conn, cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "②COBOL_CMD情報"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}

    def insert(self):
        if self.dic == None:
            self.setup()

        global ファイル名, PLI_ID, CMD_SEQ, 元資産行, PLI領域分類, PLI階層情報, PLI分岐判定, 分析行TYPE, 検索行文字列, 行CHK

        CMD_SEQ = CMD_SEQ + 1

        key_list = [
            "資産ID", "COBOL_ID", "CMD_SEQ", "元資産行情報", "記述領域", "段落", "分岐判定",
            "CMD分類", "PARM", "行CHK結果"
        ]
        value_list = [
            ファイル名, PLI_ID, CMD_SEQ, 元資産行, PLI領域分類, PLI階層情報, "", "CALL", 検索行文字列,
            行CHK
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
                              設定条件HIT情報出力=False,
                              分析条件HIT情報出力=False,
                              設計条件HIT情報出力=False,
                              設定条件HIT_NG情報出力=True,
                              conn=None,
                              cursor=None):
    global SUB_SQL生成_PLI_3_

    global ファイル名, PLI_ID, CMD_SEQ, 元資産行, PLI領域分類, PLI階層情報, PLI分岐判定, 分析行TYPE, 検索行文字列, 行CHK, \
        ライブラリID, PGM_ID, ファイルIO有無, PARM有無, サブルーチン有無, SQL有無, 画面有無, ALL_chk_ok, \
        PLI_関連区分, PLI_関連資産, PLI_関連資産_TRANID, \
        P_ファイル名, P_CBL_ID, P_CMD分類, P_呼出資産, P_呼出PARM, \
        re_flg

    reset_all()

    SUB_SQL生成_PLI_0_ = SUB_SQL生成_PLI_0(conn, cursor)
    SUB_SQL生成_PLI_3_ = SUB_SQL生成_PLI_3(conn, cursor)
    SUB_SQL生成_PLI_4_ = SUB_SQL生成_PLI_4(conn, cursor)

    ALL_chk_ok = True

    #    '変数初期化
    #    'PLI_ID = Replace(Replace(ファイル名, ".cob", ""), ".cbl", "") '拡張子に合わせて設定
    #    'PLI_ID = Replace(Replace(モジュールID, ".cob", ""), ".cbl", "") '拡張子に合わせて設定 TODO 号機とのずれ対応
    ファイル名, ライブラリID, _, PLI_ID = GetFileInfo(fileName)

    PGM_ID = PLI_ID.split(".")[0]

    FILE_SEQ = 0
    CMD_SEQ = 0

    ファイルIO有無 = ""
    PARM有無 = ""
    サブルーチン有無 = ""
    SQL有無 = ""
    画面有無 = ""
    基準列 = 6  # 'TokenSheet2 列ポインタ

    行CHK = "OK"
    PLI領域分類 = "PL/I"

    md_code = "未定義"
    md_db_name = "未定義"
    md_seg_name = "未定義"


    for item in TokenSheet2:
        元資産行 = item[1]
        PLI階層情報 = item[4]

        # @PARM@ 設定
        if item[基準列] == r"\\MD_CODE":
            md_code = item[基準列 + 2]
        elif item[基準列] == r"\\MD_DBNAME":
            md_db_name = item[基準列 + 2]
        elif item[基準列] == r"\\MD_SEGNAME":
            md_seg_name = item[基準列 + 2]

        # Find CALL
        if pli_keyword_dict.get(item[基準列]) == "CALL" or pli_function_dict.get(item[基準列]) != None:
            検索行文字列 = TmpSheet[元資産行 - 1][8]
            検索行文字列 = replace_parm(検索行文字列, md_code, md_db_name, md_seg_name)
            SUB_SQL生成_PLI_4_.insert()

    # COBOL_関連資産
    for item in call_list:
        PLI_関連区分 = item[1]
        PLI_関連資産 = item[2]
        PLI_関連資産_TRANID = item[3]
        SUB_SQL生成_PLI_3_.insert()

    # '基本情報だけど後から追加したので「0」にする
    SUB_SQL生成_PLI_0_.insert()

    return ALL_chk_ok
