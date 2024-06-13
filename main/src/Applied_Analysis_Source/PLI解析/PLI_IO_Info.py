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
    global ライブラリID, ファイル名, PLI_ID, SELECT_ID, DD_ID, SELECT_LINE_INFO, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE, FDSD_INFO, ITEM_INFO, RECORD_SIZE_STR

    ライブラリID = ""
    ファイル名 = ""
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


class SUB_SQL生成_PLI_1:

    def __init__(self, conn, cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "②COBOL_入出力情報1"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}

    def insert(self):
        if self.dic == None:
            self.setup()

        global ファイル名, PLI_ID, SELECT_ID, DD_ID, SELECT_LINE_INFO

        key_list = ["資産ID", "COBOL_ID", "SELECT_ID", "ASSIGN_ID", "LINE_INFO"]
        value_list = [ファイル名, PLI_ID, SELECT_ID, DD_ID, SELECT_LINE_INFO]

        sql, value = make_insert_sql(self.dbname, value_list, key_list)

        self.cursor.execute(sql, value)

        return True

    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close()

    def close_conn(self):
        self._close_conn()


class SUB_SQL生成_PLI_2:

    def __init__(self, conn, cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "②COBOL_入出力情報2"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}

    def insert(self):
        if self.dic == None:
            self.setup()

        global ファイル名, PLI_ID, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE, FDSD_INFO, ITEM_INFO

        key_list = [
            "資産ID", "COBOL_ID", "FILE_ID", "RECORD_ID", "COPY", "RECORD_SIZE",
            "FDSD_INFO", "LINE_INFO"
        ]
        value_list = [
            ファイル名, PLI_ID, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE, FDSD_INFO,
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


class SUB_SQL生成_PLI_5:

    def __init__(self, conn, cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "②COBOL_入出力情報3"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}

    def insert(self):
        if self.dic == None:
            self.setup()

        global ファイル名, PLI_ID, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE_STR, FDSD_INFO, ITEM_INFO

        key_list = [
            "資産ID", "COBOL_ID", "FILE_ID", "RECORD_ID", "COPY", "RECORD_SIZE",
            "FDSD_INFO", "LINE_INFO"
        ]
        value_list = [
            ファイル名, PLI_ID, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE_STR,
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


class SUB_SQL生成_共通_3:

    def __init__(self, conn, cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "共通_PGM_IO情報"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}

    def insert(self, info1, lib2, id3, io4, file5):
        if self.dic == None:
            self.setup()

        key_list = ["資産分類", "LIBRARY_ID", "資産ID", "入出力区分", "ファイル名"]
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


def 検索行文字列生成処理(TokenSheet_str):

    TokenSheet_str = [str(s) for s in TokenSheet_str]
    検索行文字列 = " ".join(TokenSheet_str)

    return DB文字(検索行文字列)


def レコードID有無判定_PLI(P_移送元, P_移送先, P_配列):
    if "\"" in P_移送元 or "\"" in P_移送先:
        return False

    elif P_移送元 == "SPACE" or P_移送先 == "SPACE":
        return False

    elif P_移送元 == "ZERO" or P_移送先 == "ZERO":
        return False

    # '他にもあるとおもうがとりあえず

    for i in range(len(P_配列)):

        if P_配列[i] == P_移送元 or P_配列[i] == P_移送先:
            return True

    return False


def PLI_IO_Info(TokenSheet2, fileName, db_path, conn, cursor,
                filename_dd_io_table, filename_copy_relation_table,
                io_filename_table):
    global ライブラリID, ファイル名, PLI_ID, SELECT_ID, DD_ID, SELECT_LINE_INFO, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE, FDSD_INFO, ITEM_INFO, RECORD_SIZE_STR

    reset_all()
    SUB_SQL生成_PLI_1_ = SUB_SQL生成_PLI_1(conn, cursor)
    SUB_SQL生成_PLI_2_ = SUB_SQL生成_PLI_2(conn, cursor)
    SUB_SQL生成_PLI_5_ = SUB_SQL生成_PLI_5(conn, cursor)
    SUB_SQL生成_共通_3_ = SUB_SQL生成_共通_3(conn, cursor)

    ALL_chk_ok = True  #'シート単位で全ての設定パターンが登録されているかどうか（初期値True）

    #    '変数初期化
    #    'PLI_ID = Replace(Replace(ファイル名, ".cob", ""), ".cbl", "") '拡張子に合わせて設定
    #    'PLI_ID = Replace(Replace(モジュールID, ".cob", ""), ".cbl", "") '拡張子に合わせて設定 TODO 号機とのずれ対応
    ファイル名, ライブラリID, _, PLI_ID = GetFileInfo(fileName)

    検索行 = 0  #'TokenSheet　行ポインタ
    基準列 = 6  #   'TokenSheet2 列ポインタ
    #'分析行TYPE = ""     '行単位情報なのでここではない

    L_MOVE元 = ""
    L_MOVE先 = ""
    L_varArray = []
    # 'L_varResult As Variant

    L_varCnt = 0

    ヘッダ出力_SELECT = False
    ヘッダ出力_FDSD = False
    WORK領域_STRART = False
    ヘッダ出力_INOUT = False
    出力行 = 0

    # PLI_入出力情報1 Insert
    for item in filename_dd_io_table:
        SELECT_ID = item[0]
        DD_ID = item[1]
        SELECT_LINE_INFO = item[3]
        SUB_SQL生成_PLI_1_.insert()

    # COBOL_入出力情報2 Insert
    # #### Now is Blank

    # 共通_PGM_IO情報 Insert
    for item in io_filename_table:
        SUB_SQL生成_共通_3_.insert("PL/I", ライブラリID, PLI_ID, item[0], item[1])

    return ALL_chk_ok
