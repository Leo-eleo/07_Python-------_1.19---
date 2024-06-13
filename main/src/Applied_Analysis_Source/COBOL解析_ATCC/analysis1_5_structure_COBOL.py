#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

import reserved_word_table_COBOL

cobol_analysis_keyword_dict = reserved_word_table_COBOL.get_cobol_analysis_keyword_dict()

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

SUB_SQL生成_COBOL_0_ = None
SUB_SQL生成_COBOL_3_ = None
SUB_SQL生成_COBOL_4_ = None

def check_analysis_line(分析行TYPE):
    if 分析行TYPE in cobol_analysis_keyword_dict:
        return True
    return False


def reset_all():
    global ファイル名,COBOL_ID,CMD_SEQ,元資産行,COBOL領域分類,COBOL階層情報,COBOL分岐判定,分析行TYPE,検索行文字列,行CHK, \
            ライブラリID,PGM_ID,ファイルIO有無,PARM有無,サブルーチン有無,SQL有無,画面有無,ALL_chk_ok, \
            COBOL_関連区分,COBOL_関連資産,COBOL_関連資産_TRANID,\
            P_ファイル名,P_CBL_ID,P_CMD分類,P_呼出資産,P_呼出PARM, \
            re_flg

    re_flg = False
    ライブラリID = ""
    ファイル名 = ""
    COBOL_ID = ""
    COBOL領域分類 = ""
    COBOL階層情報 = ""
    COBOL分岐判定 = ""
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
    COBOL_関連区分 = ""
    COBOL_関連資産 = ""
    COBOL_関連資産_TRANID = ""

    P_ファイル名 = ""
    P_CBL_ID = ""
    P_CMD分類 = ""
    P_呼出資産 = ""
    P_呼出PARM = ""


class SUB_SQL生成_COBOL_0:

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

        global ファイル名, ライブラリID, COBOL_ID, PGM_ID, CMD_SEQ, ファイルIO有無, PARM有無, サブルーチン有無, SQL有無, 画面有無, ALL_chk_ok

        if ALL_chk_ok == True:
            L_CHK = "OK"
        else:
            L_CHK = "NG"

        key_list = [
            "資産ID", "LIBRARY_ID", "メンバ名", "モジュール名", "CMD行数", "解析結果",
            "ファイルIO有無", "PARM有無", "サブルーチン有無", "SQL有無", "画面有無"
        ]
        value_list = [
            ファイル名, ライブラリID, COBOL_ID, PGM_ID, CMD_SEQ, L_CHK, ファイルIO有無, PARM有無,
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


class SUB_SQL生成_COBOL_3:

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

        global ファイル名, COBOL_ID, COBOL_関連区分, COBOL_関連資産, COBOL_関連資産_TRANID

        key_list = ["資産ID", "COBOL_ID", "関連区分", "関連資産", "関連資産_TRANID"]
        value_list = [
            ファイル名, COBOL_ID, COBOL_関連区分, COBOL_関連資産,
            COBOL_関連資産_TRANID.replace("'", "")
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


class SUB_SQL生成_COBOL_4:

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

        global ファイル名, COBOL_ID, CMD_SEQ, 元資産行, COBOL領域分類, COBOL階層情報, COBOL分岐判定, 分析行TYPE, 検索行文字列, 行CHK

        CMD_SEQ = CMD_SEQ + 1

        key_list = [
            "資産ID", "COBOL_ID", "CMD_SEQ", "元資産行情報", "記述領域", "段落", "分岐判定",
            "CMD分類", "PARM", "行CHK結果"
        ]
        value_list = [
            ファイル名, COBOL_ID, CMD_SEQ, 元資産行, COBOL領域分類, COBOL階層情報, COBOL分岐判定,
            分析行TYPE, 検索行文字列, 行CHK
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



def 検索行文字列生成処理(TokenSheet_str):

    TokenSheet_str = [str(s) for s in TokenSheet_str]
    検索行文字列 = " ".join(TokenSheet_str)

    return DB文字(検索行文字列)


def 設定値一致色分け処理_COBOL(parm_val, code_val, proc_cond):
    global SUB_SQL生成_COBOL_3_
    global COBOL_関連区分, COBOL_関連資産, COBOL_関連資産_TRANID, COPY_変数, サブルーチン有無, COPY_レベル, re_flg
    ### セルの色分けは大変になるのでpython版では一旦やめる

    if re_flg:
        pass

    # 'セクション
    elif "SECTION名" in parm_val:
        pass

    # '段落
    elif "段落名" in parm_val:
        pass

    # 'コピー句
    elif "コピー句" in parm_val:
        COBOL_関連区分 = "COPY"
        COBOL_関連資産 = code_val
        COBOL_関連資産_TRANID = ""
        SUB_SQL生成_COBOL_3_.insert()

    # 'サブルーチン
    elif "サブルーチン" in parm_val:
        COBOL_関連区分 = "CALL"
        COBOL_関連資産 = code_val
        COBOL_関連資産_TRANID = ""
        SUB_SQL生成_COBOL_3_.insert()
        #    'サブルーチン有無設定
        サブルーチン有無 = "●"

    # 'EXEC CICS LINK PROGRAM
    elif "ECLP" in parm_val:
        COBOL_関連区分 = "ECLP"
        COBOL_関連資産 = code_val
        COBOL_関連資産_TRANID = ""
        SUB_SQL生成_COBOL_3_.insert()

    # 'EXEC CICS START TRANSID
    elif "ECST" in parm_val:
        COBOL_関連区分 = "ECST"
        COBOL_関連資産 = ""
        COBOL_関連資産_TRANID = code_val
        SUB_SQL生成_COBOL_3_.insert()

    # 'EXEC CICS SEND MAP
    elif "ECSM" in parm_val:
        COBOL_関連区分 = "ECSM"
        COBOL_関連資産 = code_val
        COBOL_関連資産_TRANID = ""
        SUB_SQL生成_COBOL_3_.insert()

    # 'EXEC CICS HANDLE ABEND PROGRAM
    elif "ECHA" in parm_val:
        COBOL_関連区分 = "ECHA"
        COBOL_関連資産 = code_val
        COBOL_関連資産_TRANID = ""
        SUB_SQL生成_COBOL_3_.insert()

    # 'EXEC CICS WRITEQ TD QUEUE
    elif "ECWTQ" in parm_val:
        COBOL_関連区分 = "ECWTQ"
        COBOL_関連資産 = code_val
        COBOL_関連資産_TRANID = ""
        SUB_SQL生成_COBOL_3_.insert()

    # 'EXEC CICS READ TRANSACTION
    elif "ECRT" in parm_val:
        COBOL_関連区分 = "ECRT"
        COBOL_関連資産 = ""
        COBOL_関連資産_TRANID = code_val
        SUB_SQL生成_COBOL_3_.insert()

    # 'EXEC CICS READ UPDATE DATASET
    elif "ECRUD" in parm_val:
        COBOL_関連区分 = "ECRUD"
        COBOL_関連資産 = code_val
        COBOL_関連資産_TRANID = ""
        SUB_SQL生成_COBOL_3_.insert()

    # 'EXEC CICS READ DATASET
    elif "ECRD" in parm_val:
        COBOL_関連区分 = "ECRD"
        COBOL_関連資産 = code_val
        COBOL_関連資産_TRANID = ""
        SUB_SQL生成_COBOL_3_.insert()

    # '変数名
    elif parm_val == "変数名":
        COPY_変数 = code_val
    # '変数
    elif "変数" in parm_val:
        pass

    # '定数
    elif "定数" in parm_val:
        pass

    # '数値
    elif "数値" in parm_val:
        pass

    # 'レベル￥
    elif "レベル" in parm_val:
        COPY_レベル = code_val

    # '条件語
    elif proc_cond == "PROC-条件":
        pass

    # '予約語（上記条件以外）
    elif parm_val == code_val:
        pass

    else:
        pass


def analysis1_5_structure_COBOL(TokenSheet2,
                                fileName,
                                db_path,
                                設定条件HIT情報出力=False,
                                分析条件HIT情報出力=False,
                                設計条件HIT情報出力=False,
                                設定条件HIT_NG情報出力=True,
                                conn=None,
                                cursor=None):
    global SUB_SQL生成_COBOL_3_

    global ファイル名,COBOL_ID,CMD_SEQ,元資産行,COBOL領域分類,COBOL階層情報,COBOL分岐判定,分析行TYPE,検索行文字列,行CHK, \
            ライブラリID,PGM_ID,ファイルIO有無,PARM有無,サブルーチン有無,SQL有無,画面有無,ALL_chk_ok, \
            COBOL_関連区分,COBOL_関連資産,COBOL_関連資産_TRANID,\
            P_ファイル名,P_CBL_ID,P_CMD分類,P_呼出資産,P_呼出PARM, \
            re_flg

    reset_all()
    SUB_SQL生成_COBOL_0_ = SUB_SQL生成_COBOL_0(conn, cursor)
    SUB_SQL生成_COBOL_3_ = SUB_SQL生成_COBOL_3(conn, cursor)
    SUB_SQL生成_COBOL_4_ = SUB_SQL生成_COBOL_4(conn, cursor)

    ALL_chk_ok = True  #'シート単位で全ての設定パターンが登録されているかどうか（初期値True）

    #    '変数初期化
    #    'COBOL_ID = Replace(Replace(ファイル名, ".cob", ""), ".cbl", "") '拡張子に合わせて設定
    #    'COBOL_ID = Replace(Replace(モジュールID, ".cob", ""), ".cbl", "") '拡張子に合わせて設定 TODO 号機とのずれ対応
    ファイル名, ライブラリID, _, COBOL_ID = GetFileInfo(fileName)

    PGM_ID = "未"

    FILE_SEQ = 0
    CMD_SEQ = 0

    ファイルIO有無 = ""
    PARM有無 = ""
    サブルーチン有無 = ""
    SQL有無 = ""
    画面有無 = ""

    検索行 = 0  #'TokenSheet　行ポインタ
    基準列 = 6  #   'TokenSheet2 列ポインタ
    基準列2 = 7  #   'CobolSheet 列ポインタ
    #'分析行TYPE = ""     '行単位情報なのでここではない
    行CHK = "NOT_CEHCK"

    for cobol_line in TokenSheet2:
        COBOL階層情報 = cobol_line[4]
        COBOL領域分類 = cobol_line[3]
        COBOL分岐判定 = cobol_line[5]
        元資産行 = cobol_line[1]
        分析行TYPE = cobol_line[基準列]
        # '行レベルの処理であるが行加算処理が直前で実施されておりここで行う必要がある
        # '★コマンド情報設定（詳細化の余地あり）
        if IsNumeric(cobol_line[基準列]):
            分析行TYPE = "データ定義"
        elif COBOL領域分類 == "領域Aあり":
            if 基準列 + 1 < len(cobol_line) and cobol_line[基準列 + 1] == "DIVISION":
                分析行TYPE = "DIVISION"
            elif 基準列 + 1 < len(cobol_line) and cobol_line[基準列 + 1] == "SECTION":
                分析行TYPE = "SECTION"
                if cobol_line[基準列] == "LINKAGE":  #'PARM有無設定
                    PARM有無 = "●"
            else:
                if COBOL階層情報 == "手続き部":
                    分析行TYPE = "ラベル"
                else:
                    分析行TYPE = cobol_line[基準列]

                    if 分析行TYPE == "PROGRAM-ID":
                        if 基準列 + 1 < len(cobol_line) and cobol_line[基準列 + 1] == ".":
                            if 基準列 + 2 < len(cobol_line):
                                PGM_ID = cobol_line[基準列 + 2]
                            else:
                                PGM_ID = ""
                        else:
                            if 基準列 + 1 < len(cobol_line):
                                PGM_ID = cobol_line[基準列 + 1]
                            else:
                                PGM_ID = ""
        else:
            分析行TYPE = cobol_line[基準列]
            if 分析行TYPE == "EXEC" and cobol_line[基準列 + 1] == "SQL":
                分析行TYPE = "SQL"
                SQL有無 = "●"
            elif 分析行TYPE == "OPEN":
                ファイルIO有無 = "●"

        # Analysis CALL、COPY
        if not check_analysis_line(分析行TYPE):
            continue

        検索行文字列 = 検索行文字列生成処理(cobol_line[基準列:])
        設定値一致色分け処理_COBOL(cobol_analysis_keyword_dict[分析行TYPE], cobol_line[基準列2], COBOL分岐判定)
        SUB_SQL生成_COBOL_4_.insert()

    SUB_SQL生成_COBOL_0_.insert()  #'基本情報だけど後から追加したので「0」にする

    return ALL_chk_ok
