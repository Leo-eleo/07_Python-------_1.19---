#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

def analysis1_4_rebuild_Token_JCL(TokenSheet):
    
    基準列 = 7          #  'TokenSheet    2020/4/14 6→7
    基準列2 = 6         #  'TokenSheet2   2020/4/14 5→6
    検索行 = 0          # 'TokenSheet　行ポインタ
   
    TokenSheet2 = []
    TokenSheet_last = ["@@@@@@@"]*10
    
    while 検索行 < len(TokenSheet):
  
        TokenSheet_GYO = TokenSheet[検索行]
        TokenSheet2_GYO = [""]*6
    #    '福山通運対応　終了行の直後がJOB文でなければ以降の解析は行わない
    #    'if TokenSheet_GYO[2] = "終了行":
    #    '   最終行_flg = True
    #    '   '検索行 = 検索行 + 1
    #    'else:
    #    '
    #    '   if 最終行_flg:
    #    '     if TokenSheet_GYO[2] = "通常行" and TokenSheet_GYO[4] = "JOB":
    #    '         最終行_flg = False
    #    '     elif TokenSheet_GYO[2] = "通常行" and TokenSheet_GYO[4] != "JOB":
    #    '         解析中止_flg = True
    #    '     elif TokenSheet_GYO[2] = "SYSIN行":
    #    '         解析中止_flg = True
    #    '     End If
    #    '   End If
    #    'End If
       
    #    'if Not (解析中止_flg):
       
        TokenSheet2_GYO[1] = TokenSheet_GYO[1]   #'元資産行番号
        TokenSheet2_GYO[2] = TokenSheet_GYO[2]   #'行分類
        TokenSheet2_GYO[3] = TokenSheet_GYO[6]   #'A-AUTO世代  2020/4/14 ADD
        TokenSheet2_GYO[4] = TokenSheet_GYO[3]   #'NAME
        TokenSheet2_GYO[5] = TokenSheet_GYO[4]   #'CMD

        #'出力列 = 4
        出力列 = 基準列2
        while True:
            
            # '検索列 = 5
            検索列 = 基準列
            while 検索列 < len(TokenSheet_GYO):
                
                # 'if 検索列 = 5 and TokenSheet_last[4] = "A継続":
                if 検索列 == 基準列 and TokenSheet_last[5] == "A継続":
                    出力列 = 出力列 - 1
                    TokenSheet2_GYO[出力列] = TokenSheet2_GYO[出力列] + TokenSheet_GYO[検索列]
                    検索列 = 検索列 + 1
                    出力列 = 出力列 + 1
                elif 検索列 == 基準列 and TokenSheet_GYO[2] == "NET行" and TokenSheet_last[2] == "NET行":
                    # '富士通対応
                    # 'NET行が継続する場合は1行にまとめる
                    出力列 = 出力列 - 1
                    TokenSheet2_GYO[出力列] = TokenSheet2_GYO[出力列] + TokenSheet_GYO[検索列]
                    検索列 = 検索列 + 1
                    出力列 = 出力列 + 1
                else:
                    if TokenSheet_GYO[検索列] != "'":
                        TokenSheet2_GYO.append("")
                        TokenSheet2_GYO[出力列] = TokenSheet_GYO[検索列]
                        出力列 = 出力列 + 1
                    検索列 = 検索列 + 1
                    
            
               
            TokenSheet_last = TokenSheet_GYO[:]
          
            検索行 = 検索行 + 1
            
            if 検索行 >= len(TokenSheet):
                break
            
            TokenSheet_GYO = TokenSheet[検索行]
          
            # '継続条件
            # 'if TokenSheet_last[4] = "":
            if TokenSheet_last[5] == "":
                継続解除 = True
            else:
                継続解除 = False

            # '行情報ブレイク
            # 'if TokenSheet_GYO[1] != TokenSheet_last[1]:
            if TokenSheet_GYO[2] != TokenSheet_last[2]:
                IDブレイク = True
            else:
                IDブレイク = False

           
            # 'NAME情報ブレイク
            # 'if TokenSheet_GYO[2] != TokenSheet_last[2]:
            if TokenSheet_GYO[3] != TokenSheet_last[3]:
                Nameブレイク = True
            else:
                Nameブレイク = False

           
            # 'CMD情報ブレイク
            # 'if TokenSheet_GYO[3] != TokenSheet_last[3] Or
            if TokenSheet_GYO[4] != TokenSheet_last[4] or \
                TokenSheet_GYO[4] == "EXEC" or \
                TokenSheet_GYO[4] == "DD":
                CMDブレイク = True
            else:
                CMDブレイク = False
            
            # '無限ループ対応 V1.27.01で追加
            if TokenSheet_GYO[1] == "" and TokenSheet_GYO[2] == "" and TokenSheet_GYO[3] == "" and TokenSheet_GYO[4] == "":
                break
                
            if 継続解除 and (IDブレイク or Nameブレイク or CMDブレイク):
                break

        TokenSheet2.append(TokenSheet2_GYO)
 
        
    return TokenSheet2