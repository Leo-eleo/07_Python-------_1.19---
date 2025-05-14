#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os


import time
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

def setting_re_pattern_sheet(CobolSheet):
    """ ���ʐ��K�\���ݒ�A�u���𖈉���s����͕̂��ׂ��傫���̂ōŏ��ɑS�Ēu�����Ă���

    """
    
    ���e���� = "(B|N|NC|NA|NK|NH|NN|X)?[��-���[�-߈�-ꞁA-�A-Z0-9\S\s""]+" # '�˒|����ǔ�2(�x�m��COBOL�Ή���)
   
#    'COBOL��{ID = "[A-Z0-9-]+(\sOF\s[A-Z0-9-]+)?(\s\(((\s,)?\s[A-Z0-9-]+)+\s\))?(\s\(\s[A-Z0-9-]+\s:(\s[A-Z0-9-]+)?\s\))?"
#    'COBOL��{ID = "[A-Z0-9-]+(\sOF\s[A-Z0-9-]+)*(\s\(((\s,)?\s[A-Z0-9-]+)+\s\))?(\s\(\s[A-Z0-9-]+(\s(\+|\-|\*|\/)\s[A-Z0-9-]+)?\s:(\s[A-Z0-9-]+(\s(\+|\-|\*|\/)\s[A-Z0-9-]+)?)?\s\))?"
   
#    '�S�p�����ύX�@20130226
# '   COBOL��{ID = "[A-Z0-9-.]+(\sOF\s[A-Z0-9-]+)*(\s\(((\s,)?\s[A-Z0-9-]+)+\s\))?(\s\(\s[A-Z0-9-]+(\s(\+|\-|\*|\/)\s[A-Z0-9-]+)?\s:(\s[A-Z0-9-]+(\s(\+|\-|\*|\/)\s[A-Z0-9-]+)?)?\s\))?"
# '   COBOL��{ID = "([A-Z0-9-.]+|\x0e[^\x01-\x7E]+\x0f)(\sOF\s([A-Z0-9-]+|\x0e[^\x01-\x7E]+\x0f))*(\s\(((\s,)?\s([A-Z0-9-]+|\x0e[^\x01-\x7E]+\x0f))+\s\))?(\s\(\s([A-Z0-9-]+|\x0e[^\x01-\x7E]+\x0f)(\s(\+|\-|\*|\/)\s([A-Z0-9-]+|\x0e[^\x01-\x7E]+\x0f))?\s:(\s([A-Z0-9-]+|\x0e[^\x01-\x7E]+\x0f)(\s(\+|\-|\*|\/)\s([A-Z0-9-]+|\x0e[^\x01-\x7E]+\x0f))?)?\s\))?"
    COBOL��{ID = "([A-Z0-9-.]+|[^\x01-\x7E]+)(\sOF\s([A-Z0-9-]+|[^\x01-\x7E]+))*(\s\(((\s,)?\s([A-Z0-9-]+|[^\x01-\x7E]+))+\s\))?(\s\(\s([A-Z0-9-]+|[^\x01-\x7E]+)(\s(\+|\-|\*|\/)\s([A-Z0-9-]+|[^\x01-\x7E]+))?\s:(\s([A-Z0-9-]+|[^\x01-\x7E]+)(\s(\+|\-|\*|\/)\s([A-Z0-9-]+|[^\x01-\x7E]+))?)?\s\))?"
    #    '�P�����Z�q = "(\s\((\sCOBOL��{ID|\sZERO|(\s(\+|\-))?\s[0-9\.]+)\s\)|(\sCOBOL��{ID|\sZERO|(\s(\+|\-))?\s[0-9\.]+))"
    #    '�P�����Z�q = "((\s\()*((\s(\+|\-))?\s[0-9\.]+|\sCOBOL��{ID|\sZERO)(\s\))*|((\s(\+|\-))?\s[0-9\.]+|\sCOBOL��{ID|\sZERO))"
    �P�����Z�q = "((\s\()*((\s(\+|\-))?\s[0-9]+\.[0-9]+|\sCOBOL��{ID|\sZERO)(\s\))*|((\s(\+|\-))?\s\s[0-9]+\.[0-9]+|\sCOBOL��{ID|\sZERO))"
    �w�����Z�q = "(\s\(�P�����Z�q(\s\*\*�P�����Z�q)*\s\)|�P�����Z�q(\s\*\*�P�����Z�q)*)"
    �揜���Z�q = "(\s\(�w�����Z�q(\s(\*|\/)�w�����Z�q)*\s\)|�w�����Z�q(\s(\*|\/)�w�����Z�q)*)"
    �������Z�q = "(\s\(�揜���Z�q(\s(\+|\-)�揜���Z�q)*\s\)|�揜���Z�q(\s(\+|\-)�揜���Z�q)*)"
    �Z�p�� = "�������Z�q"
    
    for i in range(len(CobolSheet)):
        re_Pattern = CobolSheet[i][7]
        if "���K�\��_" not in str(re_Pattern):

            continue
        
        re_Pattern = re_Pattern.replace("�Z�p��", �Z�p��)
        re_Pattern = re_Pattern.replace("�������Z�q", �������Z�q)
        re_Pattern = re_Pattern.replace("�揜���Z�q", �揜���Z�q)
        re_Pattern = re_Pattern.replace("�w�����Z�q", �w�����Z�q)
        re_Pattern = re_Pattern.replace("�P�����Z�q", �P�����Z�q)
        re_Pattern = re_Pattern.replace("COBOL��{ID", COBOL��{ID)
        re_Pattern = re_Pattern.replace("���e����", ���e����)
        CobolSheet[i][7] = re_Pattern
        word_set = set()
        re_str = re_Pattern[5:]
        if re_str.startswith("("):
            re_str = re_str[:re_str.find(")")]
            re_str = re.split('[()\|\[\]]',re_str)
            for s in re_str:
                if s == "\s" or s == "":
                    continue
        
                if s.endswith("\\s"):
                    s = s[:-2]
                word_set.add(s)
            
        else:
            s = re.split('[()\|\[\]]',re_str)[0]
            if "\\s" in s:
                s = s.split("\\s")[0]
            word_set.add(s)
        CobolSheet[i].append(word_set)
    return CobolSheet
        
