#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
import re

import unicodedata

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

言語_判定 = "COBOL"
PATTERN_COMMENT = re.compile(r"^\s*\*")


def comment_line_check(line):
    if PATTERN_COMMENT.match(line[4:]):
        return True
    else:
        return False


def get_ZENKAKU_str(string, HANKAKU_start, HANKAKU_len):
    num = 0
    for i, s in enumerate(string):
        if unicodedata.east_asian_width(s) in "FWA":
            num += 2
        else:
            num += 1
        if num == HANKAKU_start:
            string = string[i + 1:]
            break
    if num < HANKAKU_start:
        return ""
    num = 0
    for i, s in enumerate(string):
        if unicodedata.east_asian_width(s) in "FWA":
            num += 2
        else:
            num += 1
        if num == HANKAKU_len:
            return string[:i + 1]

    return string


def analysis1_2_read_text_COBOL(Filename):

    TmpSheet = []

    GYO = 2
    file = get_filename(Filename)
    with open(Filename, errors="ignore") as TS:
        for strREC in TS:
            strREC = strREC.replace("\n", "")
            strREC = strREC.replace("PERFORM BREAK", "PERFORM_BREAK")
            if " TALLYING " in strREC:
                print(
                    file,
                    "で TALLYING を含む行がありました。現在は無限ループに入ってしまう可能性があるため、解析対象からスキップします。"
                )
                print(strREC)
                GYO = GYO + 1
                continue
        	 
            TmpSheet_GYO = [""] * 12
            #         'ADD 20111202 takei
            # '        if strREC.startswith(//*":
            # '           if コメント行制御 = "出力する":
            # '              GYO = GYO + 1
            # '              TmpSheet_GYO[1] = "*"
            # '              TmpSheet_GYO[2] = strREC
            # '           End if
            # '        else
            # '            GYO = GYO + 1
            # '            TmpSheet_GYO[2] = strREC
            # '        End if

            制御文字 = Mid(strREC, 6, 1)

            if 制御文字 == "*" or 制御文字 == "/":
                COBOL行分類 = "ｺﾒﾝﾄ行"
            # elif 制御文字 == "D" or 制御文字 == "d":
            #     COBOL行分類 = "ﾃﾞﾊﾞｯｸﾞ行"
            elif 制御文字 == "-":
                COBOL行分類 = "継続行"
            elif Mid(strREC, 6, min(66, len(strREC))).replace(" ", "") == "":
                COBOL行分類 = "空白行"
            else:
                COBOL行分類 = "通常行"

            if comment_line_check(strREC):
                COBOL行分類 = "ｺﾒﾝﾄ行"
            # '行情報
            TmpSheet_GYO[1] = COBOL行分類

            #'標識情報
            TmpSheet_GYO[2] = 制御文字

            #'領域A OR 領域B　判定
            if COBOL行分類 == "ｺﾒﾝﾄ行":
                TmpSheet_GYO[3] = Mid(strREC, 8, min(
                    65, len(strREC)))  #'エクセル対応（エクセルで入力値エラーがでる場合があるので「'」を付与）
            elif COBOL行分類 == "ﾃﾞﾊﾞｯｸﾞ行":
                # 'TmpSheet_GYO[3] = Mid(strREC, 8, min(65,len(strREC)))
                # '通常行と同じ対応にする
                if Mid(strREC, 7, 4).replace(" ", "") == "":
                    if strREC[11] == "'" or strREC[11] == "=":
                        # '先頭がカンマの場合 " "　を付与（暫定対応）
                        # '先頭が"="の場合 " "　を付与（20120117追加）
                        TmpSheet_GYO[4] = " " + get_ZENKAKU_str(
                            strREC, 11, min(61, len(strREC)))
                    else:
                        TmpSheet_GYO[4] = get_ZENKAKU_str(
                            strREC, 11, min(61, len(strREC)))
                else:
                    TmpSheet_GYO[3] = get_ZENKAKU_str(strREC, 7,
                                                      min(65, len(strREC)))

            elif COBOL行分類 == "継続行":
                # '2013/03/08　継続行対応 FROM
                # '最初のリテラルは開始位置とみなす。二つ目のリテラルがあれば終了位置とみなす。
                # 'エクセル対応として先頭位置に継続行開始文字を挿入

                継続行文字列 = Mid(strREC, 12, min(61,
                                             len(strREC)))  # 'とりあえずダブルバイト未対応

                継続行位置 = 継続行文字列.find("'")  # 'ダブルコーテーションは未対応
                if 継続行位置 >= 0:
                    if Mid(継続行文字列, 0, 継続行位置).replace(" ", "") == "":
                        継続行文字列 = Mid(継続行文字列, 継続行位置, min(61, len(strREC)))
                        継続行位置 = 継続行文字列.find("'")
                        if 継続行位置 >= 0:
                            継続行文字列_SV = 継続行文字列
                            継続行文字列 = Mid(継続行文字列, 0, 継続行位置 + 1)
                            if Mid(継続行文字列_SV, 継続行位置, min(
                                    61, len(strREC))).replace(" ", "") != "":
                                継続行文字列 = 継続行文字列 + "."  # '暫定対応、本当は文字列分割処理が必要。

                TmpSheet_GYO[4] = "継続行" + 継続行文字列

            # '2013/03/08　継続行対応 TO
            elif COBOL行分類 == "通常行":
                if Mid(strREC, 7, 4).replace(" ", "") == "":
                    if Mid(strREC, 11, 1) == "'" or Mid(strREC, 11, 1) == "=":
                        # '先頭がカンマの場合 " "　を付与（暫定対応）
                        # '先頭が"="の場合 " "　を付与（20120117追加）
                        TmpSheet_GYO[4] = " " + get_ZENKAKU_str(
                            strREC, 11, len(strREC))
                    else:
                        TmpSheet_GYO[4] = get_ZENKAKU_str(
                            strREC, 11, len(strREC))
                else:
                    TmpSheet_GYO[3] = get_ZENKAKU_str(strREC, 6, len(strREC))
            else:
                pass

            # '●富士通COBOL　行中コメント対応 START
            # 'A領域
            i = TmpSheet_GYO[3].find(" /*")
            if i >= 0:
                TmpSheet_GYO[3] = Mid(TmpSheet_GYO[3], 0, i + 1)
            # 'B領域
            i = TmpSheet_GYO[4].find(" /*")
            if i >= 0:
                TmpSheet_GYO[4] = Mid(TmpSheet_GYO[4], 0, i + 1)
            # End If

            # '富士通COBOL　行中コメント対応 END

            # 'ｼｰｹﾝｽ域
            TmpSheet_GYO[5] = Mid(strREC, 0, 6)

            # '73-80
            if len(strREC) >= 80:
                TmpSheet_GYO[6] = get_ZENKAKU_str(strREC, 72, 8)

            # '元資産行番号
            TmpSheet_GYO[7] = GYO - 1

            # '元資産行情報
            TmpSheet_GYO[8] = strREC

            GYO = GYO + 1
            TmpSheet.append(TmpSheet_GYO)

    return TmpSheet