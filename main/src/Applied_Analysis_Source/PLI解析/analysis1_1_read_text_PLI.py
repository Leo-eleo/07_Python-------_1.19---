#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import sys

import unicodedata

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

����_���� = "PLI"


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
            #print("��DEBUG strREC :", strREC)
            TmpSheet_GYO = [""] * 9
            strREC = strREC.replace("\n", "")

            # ���`�����̒ǉ��@20240527�@wangqian
            trimmed_strREC = strREC.strip()
            if trimmed_strREC[:2] == "*/":
                strREC = trimmed_strREC[2:] + ' ' * (80 - len(trimmed_strREC[2:]))

            #TODO MUTB�ꎞ���C�@20240527�@wangqian
            #���䕶�� = strREC[1]
            ���䕶�� = strREC[0]
            if ���䕶�� == "*" or ���䕶�� == "/":
                PLI�s���� = "���čs"
            # elif ���䕶�� == "D" or ���䕶�� == "d":
            #     PLI�s���� = "���ޯ�ލs"
            # elif ���䕶�� == "-":
            #     PLI�s���� = "�p���s"

            #TODO MUTB�ꎞ���C�@20240527�@wangqian
            #elif Mid(strREC, 6, min(66,len(strREC))).replace(" ", "") == "":
            elif strREC[0:66].replace(" ", "") == "":
                PLI�s���� = "�󔒍s"
            else:
                PLI�s���� = "�ʏ�s"

            # '�s���
            TmpSheet_GYO[1] = PLI�s����
            #print("��DEBUG �s��� :", PLI�s����)

            # '�W�����
            TmpSheet_GYO[2] = ""

            # '�����Y�s�ԍ�
            TmpSheet_GYO[7] = GYO - 1

            # '�����Y�s���
            TmpSheet_GYO[8] = strREC
            #print("��DEBUG �����Y�s��� :", strREC)

            GYO = GYO + 1
            TmpSheet.append(TmpSheet_GYO)

    return TmpSheet
