#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

import time
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


def setting_re_pattern_sheet(PLISheet):
    """ 共通正規表現設定、置換を毎回実行するのは負荷が大きいので最初に全て置換しておく

    """

    リテラル = "(B|N|NC|NA|NK|NH|NN|X)?[ぁ-ヴー｡-ﾟ一-龠、-熙A-Z0-9\S\s" "]+"  # '⇒竹井改良版2(富士通PLI対応版)

    #    '全角処理変更　20130226
    PLI基本ID = "([A-Z0-9-.]+|[^\x01-\x7E]+)(\sOF\s([A-Z0-9-]+|[^\x01-\x7E]+))*(\s\(((\s,)?\s([A-Z0-9-]+|[^\x01-\x7E]+))+\s\))?(\s\(\s([A-Z0-9-]+|[^\x01-\x7E]+)(\s(\+|\-|\*|\/)\s([A-Z0-9-]+|[^\x01-\x7E]+))?\s:(\s([A-Z0-9-]+|[^\x01-\x7E]+)(\s(\+|\-|\*|\/)\s([A-Z0-9-]+|[^\x01-\x7E]+))?)?\s\))?"

    単項演算子 = "((\s\()*((\s(\+|\-))?\s[0-9]+\.[0-9]+|\sPLI基本ID|\sZERO)(\s\))*|((\s(\+|\-))?\s\s[0-9]+\.[0-9]+|\sPLI基本ID|\sZERO))"
    指数演算子 = "(\s\(単項演算子(\s\*\*単項演算子)*\s\)|単項演算子(\s\*\*単項演算子)*)"
    乗除演算子 = "(\s\(指数演算子(\s(\*|\/)指数演算子)*\s\)|指数演算子(\s(\*|\/)指数演算子)*)"
    加減演算子 = "(\s\(乗除演算子(\s(\+|\-)乗除演算子)*\s\)|乗除演算子(\s(\+|\-)乗除演算子)*)"
    算術式 = "加減演算子"

    for i in range(len(PLISheet)):
        re_Pattern = PLISheet[i][7]
        if "正規表現_" not in str(re_Pattern):

            continue

        re_Pattern = re_Pattern.replace("算術式", 算術式)
        re_Pattern = re_Pattern.replace("加減演算子", 加減演算子)
        re_Pattern = re_Pattern.replace("乗除演算子", 乗除演算子)
        re_Pattern = re_Pattern.replace("指数演算子", 指数演算子)
        re_Pattern = re_Pattern.replace("単項演算子", 単項演算子)
        re_Pattern = re_Pattern.replace("PLI基本ID", PLI基本ID)
        re_Pattern = re_Pattern.replace("リテラル", リテラル)
        PLISheet[i][7] = re_Pattern
        word_set = set()
        re_str = re_Pattern[5:]
        if re_str.startswith("("):
            re_str = re_str[:re_str.find(")")]
            re_str = re.split('[()\|\[\]]', re_str)
            for s in re_str:
                if s == "\s" or s == "":
                    continue

                if s.endswith("\\s"):
                    s = s[:-2]
                word_set.add(s)

        else:
            s = re.split('[()\|\[\]]', re_str)[0]
            if "\\s" in s:
                s = s.split("\\s")[0]
            word_set.add(s)
        PLISheet[i].append(word_set)
    return PLISheet
