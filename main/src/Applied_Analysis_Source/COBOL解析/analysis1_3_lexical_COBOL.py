#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

KEY_STR = ""
def 分離文字判定_COBOL(STR, str2, str3):
    global KEY_STR
    
    if STR == " ":
        return True
    elif STR == ".":
        if str2 == " " or str2 == "":
           return True
        else:
           return False
    elif STR == ",":
        if KEY_STR != "データ部":   #'データ部の ZZZ,ZZ9 の様な場合は分離させない
           return True
        else:
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
        if str2 == "\"" or str2 == "'":
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



def analysis1_3_lexical_COBOL(TmpSheet):
    global KEY_STR
     
   
    基準列 = 5
    検索行 = 2      #'TempSheet　行ポインタ
    出力行 = 1
    出力列 = 5
    KEY_STR = "ヘッダー"
    TokenSheet_GYO = [""]*5
    TokenSheet = []
    for i in range(len(TmpSheet)):
        TmpSheet_GYO = TmpSheet[i]
        
        COBOL行分類 = TmpSheet_GYO[1]
        
        # '2013/03/08　継続行対応 FROM
        if COBOL行分類 == "継続行":
            #'出力行のカウントアップはしない
            CMD_fld = TmpSheet_GYO[4].replace("継続行", "")
            TokenSheet_GYO[-1] = TokenSheet_GYO[-1] + CMD_fld
            if CMD_fld.endswith("."):
                #'継続行終了行には5列目に"."が入る
                TokenSheet_GYO.append(".")
            
        # '2013/03/08　継続行対応 TO
        elif COBOL行分類 != "ｺﾒﾝﾄ行" and \
            COBOL行分類 != "ﾃﾞﾊﾞｯｸﾞ行" and \
            COBOL行分類 != "空白行": #'コメント行&空行をスキップ (デバッグ行もごみが多いのでスキップ（福通店所）)
       # '行情報解析
            
            if TmpSheet_GYO[3] != "":
                COBOL領域分類 = "領域Aあり"
                CMD_fld = TmpSheet_GYO[3]
            elif TmpSheet_GYO[4] != "":
                COBOL領域分類 = "領域Bのみ"
                CMD_fld = TmpSheet_GYO[4]
            else:
                MSG = "想定外の処理"
            
            # 'CMD_fld = Mid(TmpSheet_GYO[2], 8, 65)
            if CMD_fld.replace(" ", "") != "":   #  '行中コメントがある場合、通常行でも空白になる可能性がある
                if TokenSheet_GYO != [""]*5:
                    TokenSheet.append(TokenSheet_GYO)
                TokenSheet_GYO = [""]*5
                出力行 = 出力行 + 1 #'出力時カウントアップ
                
                #'元資産行番号
                TokenSheet_GYO[1] = TmpSheet_GYO[7]
                #'行情報
                #'TokenSheet_GYO[1] = COBOL行分類
                TokenSheet_GYO[2] = COBOL行分類
                #'記述領域
                #'TokenSheet_GYO[2] = COBOL領域分類
                TokenSheet_GYO[3] = COBOL領域分類
            
               # 'KEY情報判定
                KEY_TEMP = CMD_fld.replace(" ", "")
                if "IDENTIFICATIONDIVISION" in KEY_TEMP or "IDDIVISION" in KEY_TEMP:
                    KEY_STR = "見出し部"
                elif "ENVIRONMENTDIVISION" in KEY_TEMP:
                    KEY_STR = "環境部"
                elif "DATADIVISION" in KEY_TEMP:
                    KEY_STR = "データ部"
                elif "PROCEDUREDIVISION" in KEY_TEMP:
                    KEY_STR = "手続き部"
                
                # '階層情報
                # 'TokenSheet_GYO[3] = KEY_STR
                TokenSheet_GYO[4] = KEY_STR
                
                # '出力列 = 3
                出力列 = 基準列 - 1
                # 'コマンド情報分解
                i = 0
                while i < len(CMD_fld):
                    判定対象文字 = Mid(CMD_fld, i, 1)
                    判定対象文字2 = Mid(CMD_fld, i + 1, 1)
                    判定対象文字3 = Mid(CMD_fld, i + 2, 1)
                    判定対象文字4 = Mid(CMD_fld, i + 3, 1)
                    判定対象文字_from = i
                    判定対象文字_to = i
                    # '上から優先して判定する
                            
                    if 判定対象文字 == "'":
                        apost_cnt = 1
                        apost_start = True
                        apost_end = False
                        
                        while True:
                            判定対象文字_to = 判定対象文字_to + 1
                            if Mid(CMD_fld, 判定対象文字_to, 1) == "'":
                                apost_cnt = apost_cnt + 1         # '開始時にアポストロフィが続く場合の考慮
                            else:
                                apost_start = False   #'一旦アポストロフィーが途切れる
                                apost_cnt = 0    #  '途中で途切れたらカウントをリセット
                            
                            temp_num = apost_cnt % 2 #  '連続アポストリフィが奇数だったらおわり
                            
                            if apost_start:
                                if apost_cnt > 3 and temp_num == 0: #'最初からアポストロフィが4つ以上偶数個連続する場合は終了
                                    apost_end = True
                                else:
                                    apost_end = False
                            else:
                                if temp_num == 1:  #'一旦途切れたアポストロフィの場合は奇数個のアポストロフィが1個以上の場合終了
                                    apost_end = True
                                else:
                                    apost_end = False
                                
                            if (Mid(CMD_fld, 判定対象文字_to, 1) == "'" and Mid(CMD_fld, 判定対象文字_to + 1, 1) != "'" and apost_end) or 判定対象文字_to >= 72:
                                break

                        # '[判定対象文字_to]　の結果は [判定対象文字_from]の文字数を指し引かれた結果になる
                        対象文字数 = 判定対象文字_to - 判定対象文字_from + 1
                        i = i + 対象文字数                                    
                        出力列 = 出力列 + 1
                        # '注意：EXCELシートに再出力する際「'」が除去されるので余分に「''」を付与する
                        TokenSheet_GYO.append(Mid(CMD_fld, 判定対象文字_from, 対象文字数))
                        
                    # '「"」を区切で使うかどうか要確認（使わないのであれば↓は削除可）
                    elif 判定対象文字 == "\"":
                            判定対象文字_to = Mid(CMD_fld, 判定対象文字_from + 1, 80).find("\"")
                                              
                            # '[判定対象文字_to]　の結果は [判定対象文字_from]の文字数を指し引かれた結果になる
                            対象文字数 = 判定対象文字_to + 1 + 1
                            i = i + 対象文字数                                    
                            出力列 = 出力列 + 1
                            TokenSheet_GYO.append(Mid(CMD_fld, 判定対象文字_from, 対象文字数))
                    elif 分離文字判定_COBOL(判定対象文字, 判定対象文字2, 判定対象文字3) == True:
                    # 'コメント部
                        if 判定対象文字 == " ":
                            i = i + 1

                        elif 判定対象文字 == "=" and 判定対象文字2 == "=":
                            判定対象文字_to = Mid(CMD_fld, 判定対象文字_from + 1, 80).find("==")
                            if 判定対象文字3 == "=" and 判定対象文字4 == "=":
                                # '福山通運資産 「====」対応
                                対象文字数 = 判定対象文字_to + 3 + 1
                            else:
                                判定対象文字_to = Mid(CMD_fld, 判定対象文字_from + 1, 80).find("==")
                                # '[判定対象文字_to]　の結果は [判定対象文字_from]の文字数を指し引かれた結果になる
                                対象文字数 = 判定対象文字_to + 2 + 1
                            i = i + 対象文字数                                    
                            出力列 = 出力列 + 1
                            # '注意：EXCELに出力するには「==」はエラーになるので先頭に「'」を付与する
                            TokenSheet_GYO.append(Mid(CMD_fld, 判定対象文字_from, 対象文字数))
                        
                        elif 判定対象文字 == "X" or \
                            判定対象文字 == "Z" or \
                            判定対象文字 == "N" or \
                            判定対象文字 == "G" or \
                            判定対象文字 == "B":
                                
                            if 判定対象文字2 ==  "'":
                                判定対象文字_to = Mid(CMD_fld, 判定対象文字_from + 2, 80).find(判定対象文字2)
                                対象文字数 = 判定対象文字_to + 2 + 1
                            elif 判定対象文字2 ==  "\"":
                                判定対象文字_to = Mid(CMD_fld, 判定対象文字_from + 2, 80).find(判定対象文字2)
                                対象文字数 = 判定対象文字_to + 2 + 1
                            elif 判定対象文字2 ==  "X":
                                判定対象文字_to = Mid(CMD_fld, 判定対象文字_from + 3, 80).find(判定対象文字3)
                                対象文字数 = 判定対象文字_to + 3 + 1
                                # '富士通日本語対応　FROM
                            elif 判定対象文字2 ==  "C":
                                判定対象文字_to = Mid(CMD_fld, 判定対象文字_from + 3, 80).find(判定対象文字3)
                                対象文字数 = 判定対象文字_to + 3 + 1
                            elif 判定対象文字2 ==  "A":
                                判定対象文字_to = Mid(CMD_fld, 判定対象文字_from + 3, 80).find(判定対象文字3)
                                対象文字数 = 判定対象文字_to + 3 + 1
                            elif 判定対象文字2 ==  "K":
                                判定対象文字_to = Mid(CMD_fld, 判定対象文字_from + 3, 80).find(判定対象文字3)
                                対象文字数 = 判定対象文字_to + 3 + 1
                            elif 判定対象文字2 ==  "H":
                                判定対象文字_to = Mid(CMD_fld, 判定対象文字_from + 3, 80).find(判定対象文字3)
                                対象文字数 = 判定対象文字_to + 3 + 1
                            elif 判定対象文字2 ==  "N":
                                判定対象文字_to = Mid(CMD_fld, 判定対象文字_from + 3, 80).find(判定対象文字3)
                                対象文字数 = 判定対象文字_to + 3 + 1
                    # '        富士通日本語対応 TO
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
                            if i2 >= len(CMD_fld) or 分離文字判定_COBOL(Mid(CMD_fld, i2, 1), Mid(CMD_fld, i2 + 1, 1), Mid(CMD_fld, i2 + 2, 1)) == True:
                                break
                            
# '2025/1/30 UPD 東洋アルミ解析不能対応 qian.e.wang
                        # WHEN または THEN キーワードが検出された場合、次の出力行とする
                        # if Mid(CMD_fld, i, 4) == "WHEN" or Mid(CMD_fld, i, 4) == "THEN":
                        #     TokenSheet.append(TokenSheet_GYO)  # これまでの内容を追加
                        #     TokenSheet_GYO = [""]*5  # 新しい命令を始めるためにリセット
                        #     TokenSheet_GYO[1] = TmpSheet_GYO[7]
                        #     TokenSheet_GYO[2] = COBOL行分類
                        #     TokenSheet_GYO[3] = COBOL領域分類
                        #     TokenSheet_GYO[4] = KEY_STR
                        #     TokenSheet_GYO.append(Mid(CMD_fld, i, 4))
                        #     i += 4
                        if i2 >= len(CMD_fld):
                        # elif i2 >= len(CMD_fld):
# UPD END
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
                    
                            # 'デバック
                            # 'Dim tmp_str As String
                            # 'tmp_str = TokenSheet_GYO[出力列]

    TokenSheet.append(TokenSheet_GYO)        
    
    return TokenSheet