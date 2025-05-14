#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

import time
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


def setting_re_pattern_sheet(PLISheet):
    """ ���ʐ��K�\���ݒ�A�u���𖈉���s����͕̂��ׂ��傫���̂ōŏ��ɑS�Ēu�����Ă���

    """

    ���e���� = "(B|N|NC|NA|NK|NH|NN|X)?[��-���[�-߈�-ꞁA-�A-Z0-9\S\s" "]+"  # '�˒|����ǔ�2(�x�m��PLI�Ή���)

    #    '�S�p�����ύX�@20130226
    PLI��{ID = "([A-Z0-9-.]+|[^\x01-\x7E]+)(\sOF\s([A-Z0-9-]+|[^\x01-\x7E]+))*(\s\(((\s,)?\s([A-Z0-9-]+|[^\x01-\x7E]+))+\s\))?(\s\(\s([A-Z0-9-]+|[^\x01-\x7E]+)(\s(\+|\-|\*|\/)\s([A-Z0-9-]+|[^\x01-\x7E]+))?\s:(\s([A-Z0-9-]+|[^\x01-\x7E]+)(\s(\+|\-|\*|\/)\s([A-Z0-9-]+|[^\x01-\x7E]+))?)?\s\))?"

    �P�����Z�q = "((\s\()*((\s(\+|\-))?\s[0-9]+\.[0-9]+|\sPLI��{ID|\sZERO)(\s\))*|((\s(\+|\-))?\s\s[0-9]+\.[0-9]+|\sPLI��{ID|\sZERO))"
    �w�����Z�q = "(\s\(�P�����Z�q(\s\*\*�P�����Z�q)*\s\)|�P�����Z�q(\s\*\*�P�����Z�q)*)"
    �揜���Z�q = "(\s\(�w�����Z�q(\s(\*|\/)�w�����Z�q)*\s\)|�w�����Z�q(\s(\*|\/)�w�����Z�q)*)"
    �������Z�q = "(\s\(�揜���Z�q(\s(\+|\-)�揜���Z�q)*\s\)|�揜���Z�q(\s(\+|\-)�揜���Z�q)*)"
    �Z�p�� = "�������Z�q"

    for i in range(len(PLISheet)):
        re_Pattern = PLISheet[i][7]
        if "���K�\��_" not in str(re_Pattern):

            continue

        re_Pattern = re_Pattern.replace("�Z�p��", �Z�p��)
        re_Pattern = re_Pattern.replace("�������Z�q", �������Z�q)
        re_Pattern = re_Pattern.replace("�揜���Z�q", �揜���Z�q)
        re_Pattern = re_Pattern.replace("�w�����Z�q", �w�����Z�q)
        re_Pattern = re_Pattern.replace("�P�����Z�q", �P�����Z�q)
        re_Pattern = re_Pattern.replace("PLI��{ID", PLI��{ID)
        re_Pattern = re_Pattern.replace("���e����", ���e����)
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
