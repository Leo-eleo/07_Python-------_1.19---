#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import sys

import unicodedata

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

言語_判定 = "PLI"


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


def analysis1_1_read_text_PLI(fileName):
    TmpSheet = []

    GYO = 2
    with open(fileName, "r", encoding="CP932") as TS:
        for strREC in TS:
            #print("■DEBUG strREC :", strREC)
            TmpSheet_GYO = [""] * 9
            strREC = strREC.replace("\n", "")

            # 整形処理の追加　20240527　wangqian
            trimmed_strREC = strREC.strip()
            if trimmed_strREC[:2] == "*/":
                strREC = trimmed_strREC[2:] + ' ' * (80 - len(trimmed_strREC[2:]))

            #TODO MUTB一時改修　20240527　wangqian
            #制御文字 = strREC[1]
            制御文字 = strREC[0]
            if 制御文字 == "*" or 制御文字 == "/":
                PLI行分類 = "ｺﾒﾝﾄ行"
            # elif 制御文字 == "D" or 制御文字 == "d":
            #     PLI行分類 = "ﾃﾞﾊﾞｯｸﾞ行"
            # elif 制御文字 == "-":
            #     PLI行分類 = "継続行"

            #TODO MUTB一時改修　20240527　wangqian
            #elif Mid(strREC, 6, min(66,len(strREC))).replace(" ", "") == "":
            elif strREC[0:66].replace(" ", "") == "":
                PLI行分類 = "空白行"
            else:
                PLI行分類 = "通常行"

            # '行情報
            TmpSheet_GYO[1] = PLI行分類
            #print("■DEBUG 行情報 :", PLI行分類)

            # '標識情報
            TmpSheet_GYO[2] = ""

            # '元資産行番号
            TmpSheet_GYO[7] = GYO - 1

            # '元資産行情報
            TmpSheet_GYO[8] = strREC
            #print("■DEBUG 元資産行情報 :", strREC)

            GYO = GYO + 1
            TmpSheet.append(TmpSheet_GYO)

    return TmpSheet
