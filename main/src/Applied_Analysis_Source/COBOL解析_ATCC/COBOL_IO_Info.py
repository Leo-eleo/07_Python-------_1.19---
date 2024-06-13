#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


def reset_all():
    global ライブラリID, ファイル名, COBOL_ID, SELECT_ID, DD_ID, SELECT_LINE_INFO, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE, FDSD_INFO, ITEM_INFO, RECORD_SIZE_STR

    ライブラリID = ""
    ファイル名 = ""
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


class SUB_SQL生成_COBOL_1:

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

        global ファイル名, COBOL_ID, SELECT_ID, DD_ID, SELECT_LINE_INFO

        key_list = ["資産ID", "COBOL_ID", "SELECT_ID", "ASSIGN_ID", "LINE_INFO"]
        value_list = [ファイル名, COBOL_ID, SELECT_ID, DD_ID, SELECT_LINE_INFO]

        sql, value = make_insert_sql(self.dbname, value_list, key_list)

        self.cursor.execute(sql, value)

        return True

    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close()

    def close_conn(self):
        self._close_conn()


class SUB_SQL生成_COBOL_2:

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

        global ファイル名, COBOL_ID, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE, FDSD_INFO, ITEM_INFO

        key_list = [
            "資産ID", "COBOL_ID", "FILE_ID", "RECORD_ID", "COPY", "RECORD_SIZE",
            "FDSD_INFO", "LINE_INFO"
        ]
        value_list = [
            ファイル名, COBOL_ID, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE, FDSD_INFO,
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


class SUB_SQL生成_COBOL_5:

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

        global ファイル名, COBOL_ID, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE_STR, FDSD_INFO, ITEM_INFO

        key_list = [
            "資産ID", "COBOL_ID", "FILE_ID", "RECORD_ID", "COPY", "RECORD_SIZE",
            "FDSD_INFO", "LINE_INFO"
        ]
        value_list = [
            ファイル名, COBOL_ID, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE_STR,
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


def レコードID有無判定_COBOL(P_移送元, P_移送先, P_配列):
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


def COBOL_IO_Info(TokenSheet2, fileName, db_path, conn, cursor):
    global ライブラリID, ファイル名, COBOL_ID, SELECT_ID, DD_ID, SELECT_LINE_INFO, FDSD_ID, RECORD_ID, COPY, RECORD_SIZE, FDSD_INFO, ITEM_INFO, RECORD_SIZE_STR

    reset_all()
    SUB_SQL生成_COBOL_1_ = SUB_SQL生成_COBOL_1(conn, cursor)
    SUB_SQL生成_COBOL_2_ = SUB_SQL生成_COBOL_2(conn, cursor)
    SUB_SQL生成_COBOL_5_ = SUB_SQL生成_COBOL_5(conn, cursor)
    SUB_SQL生成_共通_3_ = SUB_SQL生成_共通_3(conn, cursor)

    ALL_chk_ok = True  #'シート単位で全ての設定パターンが登録されているかどうか（初期値True）

    #    '変数初期化
    #    'COBOL_ID = Replace(Replace(ファイル名, ".cob", ""), ".cbl", "") '拡張子に合わせて設定
    #    'COBOL_ID = Replace(Replace(モジュールID, ".cob", ""), ".cbl", "") '拡張子に合わせて設定 TODO 号機とのずれ対応
    ファイル名, ライブラリID, _, COBOL_ID = GetFileInfo(fileName)

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

    #    '　***********  入出力関連情報再検索  ***********

    for i in range(len(TokenSheet2)):
        検索行 = i
        TokenSheet2_GYO = TokenSheet2[i]
        # '検索列 = 5
        検索列 = 基準列
        # 'COBOL階層情報 = TokenSheet2_GYO[3]
        COBOL階層情報 = TokenSheet2_GYO[4]
        # 'CMD_fld = TokenSheet2_GYO[5]
        CMD_fld = TokenSheet2_GYO[6]

        # 'code_val = TokenSheet2_GYO[検索列]

        # '階層情報による分類
        # AnalyzeSheet.Select

        if COBOL階層情報 == "環境部":
            if CMD_fld == "SELECT":

                if ヘッダ出力_SELECT == False:
                    出力行 = 出力行 + 2
                    # AnalyzeSheet.Cells(出力行, 1] = "ファイル名"
                    # AnalyzeSheet.Cells(出力行, 2] = "DD名"
                    # AnalyzeSheet.Cells(出力行, 3] = "入出力情報"

                    ヘッダ出力_SELECT = True

                # '検索行文字列作成
                # 'SUB_検索行文字列生成処理 (5)   '処理開始列（5列目を引数にする）
                検索行文字列 = 検索行文字列生成処理(TokenSheet2_GYO[基準列:])  #'処理開始列（5列目を引数にする）
                SELECT_LINE_INFO = 検索行文字列

                # 'SELECT_ID設定（必須）
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

                # 'ASSIGN_ID設定（必須）
                DD_ID = ""
                while 検索列 < len(TokenSheet2_GYO):
                    code_val = TokenSheet2_GYO[検索列]
                    if code_val == "ASSIGN":
                        if 検索列 + 1 < len(TokenSheet2_GYO) and TokenSheet2_GYO[
                                検索列 + 1] == "TO":
                            if 検索列 + 2 < len(TokenSheet2_GYO):
                                DD_ID = TokenSheet2_GYO[検索列 + 2]
                            else:
                                DD_ID = ""
                        else:
                            if 検索列 + 1 < len(TokenSheet2_GYO):
                                DD_ID = TokenSheet2_GYO[検索列 + 1]
                            else:
                                DD_ID = ""

                    検索列 = 検索列 + 1

                SUB_SQL生成_COBOL_1_.insert()

        elif COBOL階層情報 == "データ部":
            if CMD_fld == "FD" or CMD_fld == "SD":

                if ヘッダ出力_FDSD == False:
                    出力行 = 出力行 + 2
                    # AnalyzeSheet.Cells(出力行, 1] = "ファイル名"
                    # AnalyzeSheet.Cells(出力行, 2] = "レコード名"
                    # AnalyzeSheet.Cells(出力行, 3] = "関連コピー句"
                    # AnalyzeSheet.Cells(出力行, 4] = "入出力パラメータ"
                    # AnalyzeSheet.Cells(出力行, 5] = "入出力定義情報"

                    ヘッダ出力_FDSD = True
                # '検索行文字列作成
                # 'SUB_検索行文字列生成処理 (5)   '処理開始列（5列目を引数にする）
                検索行文字列 = 検索行文字列生成処理(TokenSheet2_GYO[基準列:])  #'処理開始列（5列目を引数にする）
                FDSD_INFO = 検索行文字列

                # 'ファイル名設定（必須）
                # 'FDSD_ID = TokenSheet2_GYO[6]
                if len(TokenSheet2_GYO) > 7:
                    FDSD_ID = TokenSheet2_GYO[7]
                else:
                    FDSD_ID = ""

                COPY = ""
                RECORD_ID = ""
                ITEM_INFO = ""
                検索行2 = 検索行  #'検索行退避
                検索行 = 検索行 + 1  #'項目情報検索の為カウントアップ
                while 検索行 < len(TokenSheet2):
                    TokenSheet2_temp = TokenSheet2[検索行]
                    # 'code_val = TokenSheet2_GYO[5]
                    code_val = TokenSheet2_temp[基準列]
                    # '検索行文字列作成
                    検索行文字列 = 検索行文字列生成処理(
                        TokenSheet2_temp[基準列:])  #   '処理開始列（5列目を引数にする）
                    if ITEM_INFO == "":
                        ITEM_INFO = 検索行文字列
                    else:
                        ITEM_INFO = ITEM_INFO + "\n" + 検索行文字列

                    if code_val == "1" or code_val == "01":
                        # 'RECORD_ID = TokenSheet2_GYO[6]
                        if len(TokenSheet2_temp) > 7:
                            RECORD_ID = TokenSheet2_temp[7]
                        else:
                            RECORD_ID = ""

                        L_varCnt = L_varCnt + 1
                        # 'レイアウト調査用のレコードIDの配列をここで生成する
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

                    検索行 = 検索行 + 1
                    # 'Loop Until TokenSheet2_GYO[5] != "COPY" or _
                    # '    Not IsNumeric(TokenSheet2_GYO[5])
                    if 検索行 >= len(TokenSheet2):
                        break
                    if TokenSheet2[検索行][基準列] != "COPY" or IsNumeric(
                            TokenSheet2[検索行][基準列]) == False:
                        break

                RECORD_SIZE = 0  #'固定で出力
                SUB_SQL生成_COBOL_2_.insert()

                検索行 = 検索行2  #'行カウントを戻す

            if WORK領域_STRART:

                if CMD_fld == "01" or CMD_fld == "1":

                    if len(TokenSheet2_GYO) > 7:
                        FDSD_ID = TokenSheet2_GYO[7]
                    else:
                        FDSD_ID = ""
                    RECORD_ID = ""
                    COPY = "WORK領域"
                    RECORD_SIZE_STR = ""  # '固定で出力
                    ITEM_INFO = ""
                    FDSD_INFO = ""
                    SUB_SQL生成_COBOL_5_.insert()

            else:

                if CMD_fld == "WORKING-STORAGE":
                    WORK領域_STRART = True

        elif COBOL階層情報 == "手続き部":

            if ヘッダ出力_INOUT == False:
                出力行 = 出力行 + 2
                # AnalyzeSheet.Cells(出力行, 1] = "入出力区分"
                # AnalyzeSheet.Cells(出力行, 2] = "ファイル名"

                ヘッダ出力_INOUT = True
            if CMD_fld == "OPEN":
                # 'PGM_IO = TokenSheet2_GYO[6]
                # 'PGM_IO = TokenSheet2_GYO[基準列 + 1]
                # '検索列 = 7
                # '検索列 = 基準列 + 2
                検索列 = 基準列 + 1
                while 検索列 < len(TokenSheet2_GYO):
                    io = TokenSheet2_GYO[検索列]
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
                        SUB_SQL生成_共通_3_.insert("COBOL", ライブラリID, COBOL_ID,
                                               PGM_IO, TokenSheet2_GYO[検索列])
                        # 'Call SUB_SQL生成_共通_3("COBOL", ライブラリID, ファイル名, PGM_IO, TokenSheet2_GYO[検索列])
                        # '構造解析シート出力
                        出力行 = 出力行 + 1
                        # AnalyzeSheet.Cells(出力行, 1] = PGM_IO
                        # AnalyzeSheet.Cells(出力行, 2] = TokenSheet2_GYO[検索列]

                    検索列 = 検索列 + 1
                    if 検索列 >= len(
                            TokenSheet2_GYO) or TokenSheet2_GYO[検索列] == ".":
                        break

            # 'レイアウトグルーピング
            if CMD_fld == "READ" and len(
                    TokenSheet2_GYO) > 9 and TokenSheet2_GYO[8] == "INTO":

                FDSD_ID = TokenSheet2_GYO[7]
                RECORD_ID = TokenSheet2_GYO[9]
                COPY = "グルーピング"
                RECORD_SIZE_STR = "NULL"  # '固定で出力
                ITEM_INFO = "READ"
                FDSD_INFO = "①"
                SUB_SQL生成_COBOL_5_.insert()

            elif CMD_fld == "WRITE" and len(
                    TokenSheet2_GYO) > 9 and TokenSheet2_GYO[8] == "FROM":

                FDSD_ID = TokenSheet2_GYO[7]
                RECORD_ID = TokenSheet2_GYO[9]
                COPY = "グルーピング"
                RECORD_SIZE_STR = "NULL"  #'固定で出力
                ITEM_INFO = "WRITE"
                FDSD_INFO = "②"
                SUB_SQL生成_COBOL_5_.insert()

            elif CMD_fld == "MOVE" and L_varCnt > 0:
                if len(TokenSheet2_GYO) > 7:
                    L_MOVE元 = TokenSheet2_GYO[7]
                else:
                    L_MOVE元 = ""

                検索列 = 基準列 + 2  #'MOVEの後のキーワードは取得したので次はTOの後を探す。（複数の移送先がある場合は今は考慮しない）
                hit_flg = False

                while 検索列 < len(TokenSheet2_GYO):
                    code_val = TokenSheet2_GYO[検索列]

                    if code_val == "TO":
                        if 検索列 + 1 < len(TokenSheet2_GYO):
                            L_MOVE先 = TokenSheet2_GYO[検索列 + 1]  #'TOの後のキーワードを取得
                        else:
                            L_MOVE先 = ""
                        hit_flg = True

                    検索列 = 検索列 + 1
                    if 検索列 >= len(TokenSheet2_GYO) or TokenSheet2_GYO[
                            検索列] == "." or hit_flg == True:
                        break

                # 'if InStr(L_MOVE元, """") > 0 or InStr(L_MOVE先, """") > 0:
                # '    'いずれかが定数の場合はチェックしない
                # 'else
                #     'MOVE命令の移送元または移送先の変数がレコードIDの配列に含まれていれば出力対象

                if レコードID有無判定_COBOL(L_MOVE元, L_MOVE元, L_varArray):

                    # 'if Filter(L_varArray, L_MOVE元) != -1 or Filter(L_varArray, L_MOVE先) != -1:
                    FDSD_ID = L_MOVE元
                    RECORD_ID = L_MOVE先
                    COPY = "グルーピング"
                    RECORD_SIZE_STR = "NULL"  #'固定で出力
                    ITEM_INFO = "MOVE"
                    FDSD_INFO = "③"
                    SUB_SQL生成_COBOL_5_.insert()

        else:

            検索行 = 検索行 + 1

    return ALL_chk_ok
