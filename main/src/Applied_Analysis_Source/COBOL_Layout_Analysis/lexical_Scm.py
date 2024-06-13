#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

KEY_STR = ""
def 分離文字判定(STR, str2, str3):
      
    if STR == " ":
        return True
    elif STR == ".":
        if str2 == " " or str2 == "":
           return True
        else:
           return False
    
    elif STR == ",":
        # 'if KEY_STR <> "データ部":   'データ部の ZZZ,ZZ9 の様な場合は分離させない
        # '   return True
        # 'else:
        return False
        
    elif STR == ";":
        if str2 == " ":
           return True
        else:
           return False
    
    elif STR == ":":
        return True
    elif STR == "'":
        if str2 == " ":
           return True
        else:
           return False
    
    elif STR == "\"":
        if str2 == " ":
           return True
        else:
           return False
    
    elif STR == "(":
        return True
    elif STR == ")":
        return True
    # '注："=="は疑似ﾃｷｽﾄを表す区切り文字であるがｴｸｾﾙ対応が必要な為上位モジュールで処理する
    elif STR == "=":
            return True
    elif STR == "X":
        if str2 == "\"" or str2 == "\'":
           return True
        else:
           return False
    
    elif STR == "Z":
        if str2 == "\"" or str2 == "'":
           return True
        else:
           return False
    
    elif STR == "N":
        if str2 == "\"" or str2 == "'":
           return True
        elif str2 == "X" and \
           (str3 == "\"" or str3 == "'"):
           return True
    # '2013/9/19 ADD 富士通COBOL？対応
        elif str2 == "C" and \
           (str3 == "\"" or str3 == "'"):
           return True
        elif str2 == "A" and \
           (str3 == "\"" or str3 == "'"):
           return True
        elif str2 == "K" and \
           (str3 == "\"" or str3 == "'"):
           return True
        elif str2 == "H" and \
           (str3 == "\"" or str3 == "'"):
           return True
        elif str2 == "N" and \
           (str3 == "\"" or str3 == "'"):
           return True
        else:
           return False
    
    elif STR == "G":
        if str2 == "\"" or str2 == "'":
           return True
        else:
           return False
    
    # '2013/9/19 ADD 富士通COBOL？対応
    elif STR == "B":
        if str2 == "\"" or str2 == "'":
           return True
        else:
           return False
    
    else:
        return False


def lexical_Scm(TmpSheet):
    global KEY_STR
     
   
    基準列 = 5
    検索行 = 2      #'TempSheet　行ポインタ
    出力行 = 1
    出力列 = 5
    KEY_STR = "ヘッダー"
    TokenSheet_GYO = [""]*5
    TokenSheet = []
    検索行 = 1    #  'TempSheet　行ポインタ
   
    for 検索行 in range(len(TmpSheet)):
        CMD_fld = TmpSheet[検索行]
        出力行 = 出力行 + 1 # '出力時カウントアップ
        TokenSheet_GYO = []
        TokenSheet_GYO.append(検索行+1)
        出力列 = 1
        
        # 'コマンド情報分解
        i = 0
        while i < len(CMD_fld):
            判定対象文字 = Mid(CMD_fld, i, 1)
            判定対象文字2 = Mid(CMD_fld, i + 1, 1)
            判定対象文字3 = Mid(CMD_fld, i + 2, 1)
            判定対象文字_from = i
            判定対象文字_to = i

        #   '上から優先して判定する
            if 判定対象文字 == "'":
                apost_cnt = 1
                apost_start = True
                apost_end = False

                while True:
                    判定対象文字_to = 判定対象文字_to + 1
                    if Mid(CMD_fld, 判定対象文字_to, 1) == "'":
                        apost_cnt = apost_cnt + 1       #   '開始時にアポストロフィが続く場合の考慮
                    else:
                        apost_start = False  # '一旦アポストロフィーが途切れる
                        apost_cnt = 0      #途中で途切れたらカウントをリセット
                           
                    temp_num = apost_cnt %2 #  '連続アポストリフィが奇数だったらおわり
                           
                    if apost_start:
                        if apost_cnt > 3 and temp_num == 0: #'最初からアポストロフィが4つ以上偶数個連続する場合は終了
                            apost_end = True
                        else:
                            apost_end = False
                    else:
                        if temp_num == 1: # '一旦途切れたアポストロフィの場合は奇数個のアポストロフィが1個以上の場合終了
                            apost_end = True
                        else:
                            apost_end = False

                    if (Mid(CMD_fld, 判定対象文字_to, 1) == "'" and Mid(CMD_fld, 判定対象文字_to + 1, 1) != "'" and apost_end) or \
                        判定対象文字_to >= 72:
                        break

                #   '[判定対象文字_to]　の結果は [判定対象文字_from]の文字数を指し引かれた結果になる
                対象文字数 = 判定対象文字_to - 判定対象文字_from + 1
                i = i + 対象文字数                                  #  '
                出力列 = 出力列 + 1
                # '注意：EXCELシートに再出力する際「'」が除去されるので余分に「''」を付与する
             
                TokenSheet_GYO.append("'" + Mid(CMD_fld, 判定対象文字_from, 対象文字数))
                #    '「"」を区切で使うかどうか要確認（使わないのであれば↓は削除可）
            elif 判定対象文字 == "\"":
                判定対象文字_to = Mid(CMD_fld, 判定対象文字_from + 1, 80).find("\"")
                # '[判定対象文字_to]　の結果は [判定対象文字_from]の文字数を指し引かれた結果になる
                対象文字数 = 判定対象文字_to + 2 
                i = i + 対象文字数                                    
                出力列 = 出力列 + 1
   
            elif 分離文字判定(判定対象文字, 判定対象文字2,判定対象文字3) == True:
                 
                if 判定対象文字 == " ":
                    i = i + 1
                    #  '分離文字（出力あり）
                elif 判定対象文字 == "=" and 判定対象文字2 == "=":
                    判定対象文字_to = Mid(CMD_fld, 判定対象文字_from + 1, 80).find("==")
                    # '[判定対象文字_to]　の結果は [判定対象文字_from]の文字数を指し引かれた結果になる
                    対象文字数 = 判定対象文字_to + 3
                    i = i + 対象文字数                                    
                    出力列 = 出力列 + 1
                    # '注意：EXCELに出力するには「==」はエラーになるので先頭に「'」を付与する
                    TokenSheet_GYO.append("'" + Mid(CMD_fld, 判定対象文字_from, 対象文字数))
                
                elif 判定対象文字 in ("X","Z","N","G"):
                            
                    if 判定対象文字2 == "'":
                        判定対象文字_to = Mid(CMD_fld, 判定対象文字_from + 2, 80).find(判定対象文字2)
                        対象文字数 = 判定対象文字_to + 2 + 1
                    elif 判定対象文字2 == "\"":
                        判定対象文字_to = Mid(CMD_fld, 判定対象文字_from + 2, 80).find(判定対象文字2)
                        対象文字数 = 判定対象文字_to + 2 + 1
                    elif 判定対象文字2 == "X":
                        判定対象文字_to = Mid(CMD_fld, 判定対象文字_from + 3, 80).find(判定対象文字3)
                        対象文字数 = 判定対象文字_to + 3 +1
                    elif 判定対象文字2 == "C":
                        判定対象文字_to = Mid(CMD_fld, 判定対象文字_from + 3, 80).find(判定対象文字3)
                        対象文字数 = 判定対象文字_to + 3 + 1
                    elif 判定対象文字2 == "A":
                        判定対象文字_to = Mid(CMD_fld, 判定対象文字_from + 3, 80).find(判定対象文字3)
                        対象文字数 = 判定対象文字_to + 3 + 1
                    elif 判定対象文字2 == "K":
                        判定対象文字_to = Mid(CMD_fld, 判定対象文字_from + 3, 80).find(判定対象文字3)
                        対象文字数 = 判定対象文字_to + 3 + 1
                    elif 判定対象文字2 == "H":
                        判定対象文字_to = Mid(CMD_fld, 判定対象文字_from + 3, 80).find(判定対象文字3)
                        対象文字数 = 判定対象文字_to + 3 + 1
                    elif 判定対象文字2 == "N":
                        判定対象文字_to = Mid(CMD_fld, 判定対象文字_from + 3, 80).find(判定対象文字3)
                        対象文字数 = 判定対象文字_to + 3 + 1
                    else:
                        MSG = "想定外の処理"
                            
                    i = i + 対象文字数                                    
                    出力列 = 出力列 + 1
                    TokenSheet_GYO.append(Mid(CMD_fld, 判定対象文字_from, 対象文字数))
                            
                else:
                    i = i + 1
                    出力列 = 出力列 + 1
                    TokenSheet_GYO.append(判定対象文字)
   
            else:
            # '先頭が分離文字ではない場合
                i2 = i
                while True:
                    i2 = i2 + 1
                    if i2 >= len(CMD_fld) or 分離文字判定(Mid(CMD_fld, i2, 1), Mid(CMD_fld, i2 + 1, 1), Mid(CMD_fld, i2 + 2, 1)) == True:
                        break
              
                if i2 >= 80:
                    判定対象文字_to = 80
                    i = 80 #'後続検索終了
                    対象文字数 = 判定対象文字_to - 判定対象文字_from + 1
                    出力列 = 出力列 + 1
                    TokenSheet_GYO.append(Mid(CMD_fld, 判定対象文字_from, 対象文字数))

                else:
                    判定対象文字_to = i2 - 1
                    対象文字数 = 判定対象文字_to - 判定対象文字_from + 1
                    i = i + 対象文字数                                    
                    出力列 = 出力列 + 1
                    TokenSheet_GYO.append(Mid(CMD_fld, 判定対象文字_from, 対象文字数))

        TokenSheet.append(TokenSheet_GYO)        
    
    return TokenSheet