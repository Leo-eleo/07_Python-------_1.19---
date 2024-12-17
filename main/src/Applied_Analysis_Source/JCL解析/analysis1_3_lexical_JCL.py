#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

def 分離文字判定_JCL(STR):
    
    if STR in ",()=/\'":
        return True
    
    return False



def analysis1_3_lexical_JCL(TmpSheet):
    

    基準列 = 7      # '2020/4/14 6→7
    A継続 = False    #'20111207 ADD
    
    TokenSheet = []
    for i in range(len(TmpSheet)):
        TmpSheet_GYO = TmpSheet[i]
        
        if TmpSheet_GYO[1] == "ｺﾒﾝﾄ行":
            # '20111207 ADD
            if TmpSheet_GYO[6] == "A継続":   # 'アポストロフィが継続している場合
                A継続 = True
            else:
                A継続 = False
            #'ADD END
            
            continue
              
        #'行情報解析
        ID_fld = TmpSheet_GYO[1]
        Name_fld = TmpSheet_GYO[2]
        CMD_fld = TmpSheet_GYO[3]
        PARM_fld = TmpSheet_GYO[4]
        元資産行_From = TmpSheet_GYO[9]
        
        TokenSheet_GYO = [""]*7
            
        # 出力行 = 出力行 + 1 '出力時カウントアップ
        TokenSheet_GYO[1] = 元資産行_From
        TokenSheet_GYO[2] = ID_fld
        TokenSheet_GYO[3] = Name_fld
        TokenSheet_GYO[4] = CMD_fld
        TokenSheet_GYO[5] = TmpSheet_GYO[6]
        TokenSheet_GYO[6] = TmpSheet_GYO[11]   # '2020/4/14 ADD
         
        if ID_fld == "通常行":
            出力列 = 基準列 - 1     #'出力時カウントアップ
            #'コマンド情報分解
            i = 0
            while i < len(PARM_fld):
                判定対象文字 = PARM_fld[i]
                判定対象文字_from = i
                判定対象文字_to = i
               # '上から優先して判定する
                
#'                if 判定対象文字 = "'":
                if 判定対象文字 == "'" or A継続:  #'20111207 ADD
 
#'                        判定対象文字_to = InStr(Mid(PARM_fld, 判定対象文字_from + 1, 80), 判定対象文字)
                    判定対象文字_to = PARM_fld[判定対象文字_from+1:].find("'")
                    if 判定対象文字_to < 0:
                        判定対象文字_to = 71
                        #'[判定対象文字_to]　の結果は [判定対象文字_from]の文字数を指し引かれた結果になる
                    対象文字数 = 判定対象文字_to + 2
                    i = i + 対象文字数                             #       '
                    出力列 = 出力列 + 1
                    if 判定対象文字 == "'":
                        判定対象文字_from += 1
                        対象文字数 -= 2
                        
                    TokenSheet_GYO.append(Mid(PARM_fld, 判定対象文字_from, 対象文字数))
                    A継続 = False  #  '20111207 ADD
                        
                elif 分離文字判定_JCL(判定対象文字) == True:
#                     'コメント部
#                     'if 判定対象文字 = "/":
#                     '    if Mid(CMD_fld, i, 2) = "/*": '後続はコメント行
#                     '        i = 80 '後続検索終了
#                     '    else
#                     '        'MsgBox ("想定外の文字　'/' が利用されました ")
#                     '        dummy = エラー処理("想定外の文字 / が利用されました ", CMD_fld)
#                     '        i = 80
#                     '    End If
#                     '例外文字列
# '                    if 判定対象文字 = "'":
# '                        判定対象文字_to = InStr(Mid(PARM_fld, 判定対象文字_from + 1, 80), 判定対象文字)
# '                        if 判定対象文字_to < 1:
# '                           判定対象文字_to = 71
# '                        End If
#                         '[判定対象文字_to]　の結果は [判定対象文字_from]の文字数を指し引かれた結果になる
# '                        対象文字数 = 判定対象文字_to + 1
# '                        i = i + 対象文字数                                    '
# '                        出力列 = 出力列 + 1
# '                        TokenSheet_GYO[出力列] = Mid(PARM_fld, 判定対象文字_from, 対象文字数)
#                         'スペース（出力なし）
#                     'elif 判定対象文字 = " ": ' =>スペースは分離文字ではない
#                     '    i = i + 1
#                     '    '分離文字（出力あり）
#                     'else
                        
                    i = i + 1
                    出力列 = 出力列 + 1
                    TokenSheet_GYO.append(判定対象文字)
                else:
                # '先頭が分離文字ではない場合
                    i2 = i
                    while True:
                        i2 += 1
                        if  i2 >= len(PARM_fld) or 分離文字判定_JCL(PARM_fld[i2]) == True:
                            break
                    
              
                    if i2 >= len(PARM_fld):
                        判定対象文字_to = 80
                        i = 80 #'後続検索終了
                        対象文字数 = 判定対象文字_to - 判定対象文字_from + 2
                        出力列 = 出力列 + 1
                        TokenSheet_GYO.append(Mid(PARM_fld, 判定対象文字_from, 対象文字数))
                        # Exit Do 'Todo 80超え文字の無限ループ抑止対応
                    else:
                        判定対象文字_to = i2
                        対象文字数 = 判定対象文字_to - 判定対象文字_from
                        i = i + 対象文字数                                   # '
                        出力列 = 出力列 + 1
                        TokenSheet_GYO.append(Mid(PARM_fld, 判定対象文字_from, 対象文字数))
                 
    
        elif ID_fld == "SYSIN行" or ID_fld == "NET行" or ID_fld == "/\\行":
        # 'SYSIN行の場合
            TokenSheet_GYO.append(PARM_fld) #'コメント行については別途要検討

        TokenSheet.append(TokenSheet_GYO)
    # '20111207 ADD
        if TmpSheet_GYO[6] == "A継続":   # 'アポストロフィが継続している場合
            A継続 = True
        else:
            A継続 = False
    #'ADD END

    
    return TokenSheet