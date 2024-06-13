#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

from reserved_word_table_COBOL import reserved_word_table_COBOL

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

Rwords = reserved_word_table_COBOL()


def 予約語判定_COBOL(STR):

    if STR in Rwords:
        return True
    else:
        return False


def 改行判定_COBOL():
    global 直前トークン, 直前トークン2, 改行制御FLG, 検索文字列
    # '改行制御フラグ
    # 'EXEC SQL ～ END-EXEC などの途中に改行キーワードが来ても改行させないように制御する
    if 改行制御FLG:
        if 検索文字列 == "END-EXEC":
            改行制御FLG = False
            return True  #'実際に改行になるのは検索文字列が予約語条件を満たす場合
    else:

        if 直前トークン2 == "EXEC" and 直前トークン == "SQL":
            改行制御FLG = True
            return False


# '        elif 直前トークン2 = "CURSOR" and 直前トークン = "FOR": # '改行制御フラグの追加によりこの場合は起きない
# '            return False
        elif 直前トークン2 == "EXEC" and 直前トークン == "CICS":
            return False
        else:
            return True
    return False


def トークン出力_COBOL(P_STR):
    global 直前トークン, 直前トークン2

    直前トークン2 = 直前トークン  #'次のトークンの改行判定に利用
    直前トークン = P_STR  #'次のトークンの改行判定に利用


def analysis1_4_rebuild_Token_COBOL(TokenSheet):

    global 直前トークン, 直前トークン2, 改行制御FLG, 検索文字列

    基準列 = 5  #'TokenSheet　列ポインタ
    基準列2 = 6  #'TokenSheet2 列ポインタ
    検索行 = 0  #'TokenSheet　行ポインタ
    直前トークン = ""
    直前トークン2 = ""
    出力行 = 1
    改行制御FLG = False
    検索文字列 = ""
    TokenSheet2 = []
    TokenSheet2_GYO = [""] * 6
    hit_flg = False
    while 検索行 < len(TokenSheet):
        TokenSheet_GYO = TokenSheet[検索行]

        if TokenSheet_GYO[4] != "ヘッダー":  #'ヘッダーは処理しない
            # '最初の処理行の情報を出力
            if TokenSheet2_GYO != [""] * 6:
                TokenSheet2.append(TokenSheet2_GYO)
            TokenSheet2_GYO = [""] * 6
            出力行 = 出力行 + 1
            TokenSheet2_GYO[1] = TokenSheet_GYO[1]  #'元資産行番号
            TokenSheet2_GYO[2] = TokenSheet_GYO[2]  #'行情報
            TokenSheet2_GYO[3] = TokenSheet_GYO[3]  #'記述領域
            TokenSheet2_GYO[4] = TokenSheet_GYO[4]  #'階層情報

            # '出力列 = 5
            出力列 = 基準列2
            hit_flg = False

            while True:

                #'検索列 = 4
                検索列 = 基準列

                while True:
                    検索文字列 = TokenSheet_GYO[検索列]

                    #   if 予約語判定_COBOL(検索文字列) and 改行判定_COBOL()and 出力列 > 基準列2:

                    if 改行判定_COBOL() and 予約語判定_COBOL(検索文字列) and 出力列 > 基準列2:

                        if TokenSheet2_GYO != [""] * 6:
                            TokenSheet2.append(TokenSheet2_GYO)
                        TokenSheet2_GYO = [""] * 6

                        出力行 = 出力行 + 1
                        TokenSheet2_GYO[1] = TokenSheet_GYO[1]
                        TokenSheet2_GYO[2] = TokenSheet_GYO[2]
                        TokenSheet2_GYO[3] = TokenSheet_GYO[3]
                        TokenSheet2_GYO[4] = TokenSheet_GYO[4]
                        # '出力列 = 5
                        出力列 = 基準列2
                        直前トークン = ""
                        直前トークン2 = ""

                    # '対象トークン出力および過去2回分のトークンを退避する
                    トークン出力_COBOL(検索文字列)
                    TokenSheet2_GYO.append(検索文字列)

                    #                 'Call トークン出力_COBOL(TokenSheet_GYO[検索列])

                    #                 'トークン再構築の行終了条件を満たすか
                    # 'MERGER FROM Ver1.13.1
                    #                 'まれに１行に複数の終了文字を含むばあいあり
                    # '                if (TokenSheet_GYO[検索列] = "." or \
                    # '                    TokenSheet_GYO[検索列] = ";" or \
                    # '                    TokenSheet_GYO[検索列] = ",") and \
                    # '                   TokenSheet_GYO[検索列 + 1] = "":
                    # '                   hit_flg = True
                    # '                End if
                    if (TokenSheet_GYO[検索列] == "." or TokenSheet_GYO[検索列] == ";") and \
                        検索列 + 1 >= len(TokenSheet_GYO):
                        hit_flg = True

                    # '***** ADD START *****
                    #                 'EJECT、SKIPの判定
                    if (TokenSheet_GYO[検索列] == "EJECT" or \
                        TokenSheet_GYO[検索列] == "SKIP1" or \
                        TokenSheet_GYO[検索列] == "SKIP2" or \
                        TokenSheet_GYO[検索列] == "SKIP3") and \
                        検索列 + 1 >= len(TokenSheet_GYO):
                        hit_flg = True
                    # '***** ADD END   *****

                    検索列 = 検索列 + 1
                    出力列 = 出力列 + 1
                    if 検索列 >= len(TokenSheet_GYO) or hit_flg:
                        break

                検索行 = 検索行 + 1

                if 検索行 >= len(TokenSheet) or hit_flg:
                    break
                TokenSheet_GYO = TokenSheet[検索行]

        #   '出力行 = 出力行 + 1  '出力時にカウントアップに変更

        #   'ヘッダー行の場合はリードスキップ
        else:
            検索行 = 検索行 + 1

        if 検索行 >= len(TokenSheet):
            break
    if TokenSheet2_GYO != [""] * 6:
        TokenSheet2.append(TokenSheet2_GYO)
    #    '制御処理行にマーク
    #         'ELSE END-** の判定で「-1」を制御する判定で一部不具合あり、今後の課題（TAKEI）
    検索行 = 2  #'TokenSheet2　行ポインタ
    条件CNT = 0

    for i in range(len(TokenSheet2)):
        # '検索列 = 5
        検索列 = 基準列2
        hit_flg = False
        while 検索列 < len(TokenSheet2[i]) and hit_flg == False:
            if TokenSheet2[i][検索列] == "IF":
                条件CNT = 条件CNT + 1
                TokenSheet2[i][基準列2 - 1] = "IF-" + str(条件CNT)
                hit_flg = True
            elif TokenSheet2[i][検索列] == "EVALUATE":
                条件CNT = 条件CNT + 1
                TokenSheet2[i][基準列2 - 1] = "EVALUATE-" + str(条件CNT)
                hit_flg = True
            elif TokenSheet2[i][検索列] == "WHEN":
                # '条件CNT = 条件CNT + 1
                TokenSheet2[i][基準列2 - 1] = "WHEN-" + str(条件CNT)
                hit_flg = True
            elif TokenSheet2[i][検索列] == "THEN":
                TokenSheet2[i][基準列2 - 1] = "THEN-" + str(条件CNT)
                hit_flg = True
            elif TokenSheet2[i][検索列] == "ELSE":
                TokenSheet2[i][基準列2 - 1] = "ELSE-" + str(条件CNT)
                # '                条件CNT = 条件CNT - 1                                       'ここで　-1　すべきかどうか
                hit_flg = True
            elif TokenSheet2[i][検索列] == "END-IF":
                TokenSheet2[i][基準列2 - 1] = "END-IF-" + str(条件CNT)
                条件CNT = 条件CNT - 1  #            'ELSE　が　指定されていると -1 したら減らしすぎ
                hit_flg = True
            elif TokenSheet2[i][検索列] == "END-EVALUATE":
                TokenSheet2[i][基準列2 - 1] = "END-EVALUATE-" + str(条件CNT)
                条件CNT = 条件CNT - 1
                hit_flg = True
            elif TokenSheet2[i][検索列] == ".":
                条件CNT = 0

            検索列 = 検索列 + 1

    TokenSheet2 = [i for i in TokenSheet2 if not (i[6] == "STRING")]

    return TokenSheet2