#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import sys

sys.path.append(os.path.abspath("."))


def reserved_word_table_PLI():
    RWords = [""] * 51

    RWords[0] = "ACCEPT"
    RWords[1] = "ADD"
    RWords[2] = "ALTER"
    RWords[3] = "CALL"
    RWords[4] = "COMPUTE"
    RWords[5] = "CONTINUE"
    RWords[6] = "DISPLAY"
    RWords[7] = "DIVIDE"
    RWords[8] = "ENTRY"
    RWords[9] = "EVALUATE"
    RWords[10] = "WHEN"
    RWords[11] = "END-EVALUATE"
    RWords[12] = "EXEC"
    RWords[13] = "EXIT"
    RWords[14] = "GO"
    RWords[15] = "GOBACK"
    RWords[16] = "IF"
    RWords[17] = "THEN"
    RWords[18] = "ELSE"
    RWords[19] = "END-IF"
    RWords[20] = "IDENTIFICATION"
    RWords[21] = "INITIALIZE"
    RWords[22] = "INSPECT"
    RWords[23] = "INVOKE"
    RWords[24] = "MERGE"
    RWords[25] = "MOVE"
    RWords[26] = "MULTIPLY"
    RWords[27] = "PERFORM"
    RWords[28] = "END-PERFORM"
    RWords[29] = "RELEASE"
    RWords[30] = "RETURN"  # 'EXEC CICS �R�}���h�Ŏg�p����̂Őݒ�s�������i���ʓX���j
    RWords[31] = "REWRITE"  # 'EXEC CICS �R�}���h�Ŏg�p����̂Őݒ�s�������i���ʓX���j
    RWords[32] = "SEARCH"
    RWords[33] = "SET"  #'EXEC CICS �R�}���h�Ŏg�p����̂Őݒ�s�������i���ʓX���j
    RWords[34] = "SORT"
    RWords[35] = "START"  # 'EXEC CICS �R�}���h�Ŏg�p����̂Őݒ�s�������i���ʓX���j
    RWords[36] = "STOP"
    RWords[37] = "STRING"
    RWords[38] = "SUBTRACT"
    RWords[39] = "UNSTRING"
    RWords[40] = "COPY"
    RWords[41] = "XML"
    RWords[42] = "SELECT"  #'���R�ʉ^�Ή�
    RWords[43] = "WRITE"  #'EXEC CICS/SQL�@���߂𗘗p���Ȃ��ꍇ�͕���������ׂ��������i���ʓX���j
    RWords[44] = "CLOSE"  #'EXEC CICS/SQL�@���߂𗘗p���Ȃ��ꍇ�͕���������ׂ��������i���ʓX���j
    RWords[45] = "OPEN"  #'EXEC CICS/SQL�@���߂𗘗p���Ȃ��ꍇ�͕���������ׂ��������i���ʓX���j
    RWords[46] = "READ"  #'EXEC CICS/SQL�@���߂𗘗p���Ȃ��ꍇ�͕���������ׂ��������i���ʓX���j
    RWords[47] = "READY"  #'EXEC CICS/SQL�@���߂𗘗p���Ȃ��ꍇ�͕���������ׂ��������i���ʓX���j
    RWords[48] = "APPLY"  #'���R�ʉ^�X���Ή�
    RWords[49] = "END-READ"  #'���R�ʉ^�X���Ή�
    RWords[50] = "CANCEL"  #'EXEC CICS �R�}���h�Ŏg�p����̂Őݒ�s�������i���ʓX���j

    RWords = set(RWords)
    return RWords