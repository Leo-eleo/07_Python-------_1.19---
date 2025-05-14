#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *



def 改行判定_COBOL():
    global  直前トークン,直前トークン2,改行制御FLG,検索文字列
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
    global 直前トークン,直前トークン2

    直前トークン2 = 直前トークン    #'次のトークンの改行判定に利用
    直前トークン = P_STR            #'次のトークンの改行判定に利用
      
            
def rebuild_Token_Scm(TokenSheet,layout_name):
    
   
    TokenSheet2 = []
    
    検索行 = 0
    while 検索行 < len(TokenSheet):
        hit_flg = False
        TokenSheet2_GYO = [layout_name]
        while 検索行 < len(TokenSheet) and hit_flg == False:
            
            検索列 = 1
            TokenSheet_GYO = TokenSheet[検索行]
            while 検索列 < len(TokenSheet_GYO):
                TokenSheet2_GYO.append(TokenSheet_GYO[検索列])
                if TokenSheet_GYO[検索列] == ".":
                    hit_flg = True
                    
                検索列 += 1
                
                if hit_flg:
                    break
            
            検索行 += 1
            if hit_flg:
                break
        TokenSheet2.append(TokenSheet2_GYO)
    
    return TokenSheet2
            