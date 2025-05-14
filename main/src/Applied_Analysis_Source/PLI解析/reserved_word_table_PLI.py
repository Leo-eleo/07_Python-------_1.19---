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
    RWords[30] = "RETURN"  # 'EXEC CICS コマンドで使用するので設定不可→復活（福通店所）
    RWords[31] = "REWRITE"  # 'EXEC CICS コマンドで使用するので設定不可→復活（福通店所）
    RWords[32] = "SEARCH"
    RWords[33] = "SET"  #'EXEC CICS コマンドで使用するので設定不可→復活（福通店所）
    RWords[34] = "SORT"
    RWords[35] = "START"  # 'EXEC CICS コマンドで使用するので設定不可→復活（福通店所）
    RWords[36] = "STOP"
    RWords[37] = "STRING"
    RWords[38] = "SUBTRACT"
    RWords[39] = "UNSTRING"
    RWords[40] = "COPY"
    RWords[41] = "XML"
    RWords[42] = "SELECT"  #'福山通運対応
    RWords[43] = "WRITE"  #'EXEC CICS/SQL　命令を利用しない場合は復活させるべき→復活（福通店所）
    RWords[44] = "CLOSE"  #'EXEC CICS/SQL　命令を利用しない場合は復活させるべき→復活（福通店所）
    RWords[45] = "OPEN"  #'EXEC CICS/SQL　命令を利用しない場合は復活させるべき→復活（福通店所）
    RWords[46] = "READ"  #'EXEC CICS/SQL　命令を利用しない場合は復活させるべき→復活（福通店所）
    RWords[47] = "READY"  #'EXEC CICS/SQL　命令を利用しない場合は復活させるべき→復活（福通店所）
    RWords[48] = "APPLY"  #'福山通運店所対応
    RWords[49] = "END-READ"  #'福山通運店所対応
    RWords[50] = "CANCEL"  #'EXEC CICS コマンドで使用するので設定不可→復活（福通店所）

    RWords = set(RWords)
    return RWords