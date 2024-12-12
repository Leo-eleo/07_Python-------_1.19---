#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import sys
import os
import unicodedata

import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


EndLineString = " "*69 ### JCL,PROC における終了行
AAUTO世代情報管理 = "①A-AUTO世代のまま出力"
strREC = ""
# ADD 20240619 yi.a.qian
IN_LINE_COMMENT_STR = ["<<-", "<-"]
# ADD END

def get_ZENKAKU_str(string,HANKAKU_start,HANKAKU_len):
    num = 0
    for i,s in enumerate(string):
        if unicodedata.east_asian_width(s) in "FWA":
            num += 2
        else:
            num += 1
        if num == HANKAKU_start:
            string = string[i+1:]
            break
    if num < HANKAKU_start:
        return ""
    num = 0
    for i,s in enumerate(string):
        if unicodedata.east_asian_width(s) in "FWA":
            num += 2
        else:
            num += 1
        if num == HANKAKU_len:
            return string[:i+1]

    return string

def SUB_PC判定_JCL():
    global A継続,C継続,P継続,IF継続,strREC,PC判定,PARM_開始桁,PARM_終了桁,COM_開始桁,COMMENT文字列,MSG,PARM文字列
    # ADD 20240613 yi.a.qian
    global next_rec
    # ADD END

    PARM_終了桁 = 71
    for i in range(PARM_開始桁,min(72,len(strREC))):

        判定対象文字 = strREC[i]

        if 判定対象文字 ==  "'":
            if PC判定 == "PARM":
                if A継続:
                    A継続 = False
                else:
                    A継続 = True
# '20111209 ADD
            elif PC判定 == "未処理":
                    PC判定 = "PARM"
                    PARM_開始桁 = i
                    A継続 = True
# 'ADD END
        elif 判定対象文字 ==  " ":
            if A継続:
                pass
            else:
                if PC判定 == "PARM":

                    PARM_終了桁 = i - 1
                    PC判定 = ""
# '20111209 ADD
        elif 判定対象文字 ==  "":    # '移行後資産などで途中で改行が入っている場合想定
            if A継続:
                pass
            else:
                if PC判定 == "PARM":

                    PARM_終了桁 = i - 1
                    PC判定 = ""
# 'ADD END

        else:
            if PC判定 == "":
                PC判定 = "COMMENT"
                COM_開始桁 = i
            elif PC判定 == "未処理":
                PC判定 = "PARM"
                PARM_開始桁 = i


    # 'PARM部
    if A継続:
#'20240205 UPD qian.e.wang
        #PARM文字列 = Mid(strREC, PARM_開始桁, 72 - PARM_開始桁)#+1)
        PARM文字列 = Mid(strREC, PARM_開始桁, 72 - PARM_開始桁)
#'UPD END

    else:
        # 'if PARM_開始桁 = PARM_終了桁:
        # '    PARM文字列 = ""
        # 'else:
        PARM文字列 = Mid(strREC, PARM_開始桁, PARM_終了桁 - PARM_開始桁 + 1)

    MSG = PARM文字列[-1]
    if MSG == ",":
        # UPD 20240613 yi.a.qian
        if not next_rec == "" and len(next_rec) > 3:
            third_char = next_rec[2]
            if third_char == " " or next_rec.startswith("//*") or next_rec.startswith("//-"):
                P継続 = True
            else:
                P継続 = False
        else:
            P継続 = True
        # UPD END
    else:
        P継続 = False

    # 'COMEENT部
    if PC判定 == "未処理" or PC判定 == "PARM" or PC判定 == "":
        COMMENT文字列 = ""
    else:
        COMMENT文字列 = Mid(strREC, COM_開始桁, 72 - COM_開始桁+1)

# ADD 20240619 yi.a.qian
def remove_inline_comment(s: str) -> str:
    for comment_str in IN_LINE_COMMENT_STR:
        if comment_str in s:
            return s[:s.index(comment_str)]
    return s
# ADD END

def analysis1_2_read_text_JCL(Filename,AAUTO世代情報管理):

    global DLM_flg,最終行_flg,解析中止_flg, NET行継続,A継続,C継続,P継続,IF継続,strREC
    global PC判定,PARM_開始桁,PARM_終了桁,COM_開始桁,COMMENT文字列,MSG,PARM文字列
    # ADD 20240613 yi.a.qian
    global next_rec
    # ADD END
    TmpSheet = []

    DLM_flg = False
    最終行_flg = False
    解析中止_flg = False
    NET行継続 = False
    A継続 = False
    C継続 = False
    P継続 = False
    IF継続 = False
    PARM文字列 = ""
    COMMENT文字列 = ""

    CMD分類 = ""
    GYO = 2

    with open(Filename,errors="ignore") as TS:

        # UPD 20240613 yi.a.qian
        lines = TS.readlines()
        for rec_index, strREC in enumerate(lines):
        # UPD END

            # UPD 20240619 yi.a.qian
            # strREC = strREC.replace("\n","")
            strREC = remove_inline_comment(strREC.replace("\n",""))
            # UPD END
            TmpSheet_GYO = [""]*12

            # ADD 20240613 yi.a.qian
            if not rec_index + 1 >= len(lines):
                next_rec = lines[rec_index + 1]
            else:
                next_rec = ""
            # ADD END
#         'ADD 20111202 takei
            # '        if strREC.startswith(//*":
            # '           if コメント行制御 = "出力する":
            # '              GYO = GYO + 1
            # '              TmpSheet_GYO[1] = "*"
            # '              TmpSheet_GYO[2] = strREC
            # '           End if
            # '        else
            # '            GYO = GYO + 1
            # '            TmpSheet_GYO[2] = strREC
            # '        End if

            # '行情報判定
            if 解析中止_flg:
                JCL行分類 = "終了行"

                #    '再度「JOB文」がきたら再解析開始 20140724 H.Takei
                # UPD 20240613 yi.a.qian
                if strREC.startswith("//") and strREC[2] != "*" and " JOB " in strREC:
                # if (strREC.startswith("//") or strREC.startswith("/\\")) and strREC[2] != "*" and " JOB " in strREC:
                # UPD END
                    解析中止_flg = False
                    最終行_flg = False
                    JCL行分類 = "通常行"

            elif NET行継続:
                JCL行分類 = "NET行"
                if Trim(Mid(strREC, 3, 68)).endswith(","):
                    pass
                else:
                    NET行継続 = False

            # 'elif 最終行_flg:
            elif strREC.startswith("//*NET "):   #'富士通 DLM対応
                JCL行分類 = "NET行"
                #'MSG = Right(Trim(Mid(strREC, 8, 64)), 1)
                if Trim(Mid(strREC, 7, 64)).endswith(","):
                    NET行継続 = True

            # UPD 20240613 yi.a.qian
            elif strREC.startswith("/\\"):
                continue
                # JCL行分類 = "/\行"   #'JFE倉敷で追加
            # UPD END
            elif strREC.startswith("//*") or strREC.startswith("//-"):  #'"//-"は福山通運用暫定対応（終了行の後にある場合がある）
                JCL行分類 = "ｺﾒﾝﾄ行"

            # UPD 20240613 yi.a.qian
            elif strREC.startswith("//"):
            # elif strREC.startswith("//") or strREC.startswith("/\\"):
            # UPD END
                if 最終行_flg:
                    if " JOB " in strREC:
                        最終行_flg = False
                        JCL行分類 = "通常行"
                    elif Mid(strREC, 2, 69) == EndLineString:
                        JCL行分類 = "終了行"
                        #'解析中止にはしない
                    else:
                        解析中止_flg = True
                        JCL行分類 = "終了行"
                elif Mid(strREC, 2, 69) == EndLineString:
                    JCL行分類 = "終了行"                              #'福山通運資産対応（終了行の直後はJOB文以外なら解析終了）
                    最終行_flg = True
                else:
                    JCL行分類 = "通常行"
            elif DLM_flg == False and strREC.startswith("/*"):
                if 最終行_flg:
                    解析中止_flg = True
                    JCL行分類 = "終了行"
                else:
                    JCL行分類 = "区切行"

            elif DLM_flg and strREC.startswith(DLM文字): #'DLMで指定した区切行
                JCL行分類 = "区切行"
                DLM_flg = False                              #    'DLM指定解除
            else:
                if 最終行_flg:
                    解析中止_flg = True
                    JCL行分類 = "終了行"
                else:
                    JCL行分類 = "SYSIN行"


            TmpSheet_GYO[1] = JCL行分類

            #'区切文字判定
            if JCL行分類 == "通常行" and  "DLM='" in strREC:
                DLM_flg = True
                DLM文字 = Mid(strREC, strREC.find("DLM='") + 5, 2)
            elif JCL行分類 == "通常行" and "DLM=" in strREC:
                DLM_flg = True
                DLM文字 = Mid(strREC, strREC.find("DLM=") + 4, 2)
            #'注：アポストロフィー自体またはアンパサンドは未対応

            #'ステートメント分類情報判定
            継続行_flg = True      # 'ステートメント分類の識別情報(JOB EXEC DDなど)が検索されない場合

            #'20111209 ADD
            strREC_判定桁 = strREC.find("'") + 1
            if strREC_判定桁 > 0:
                strREC_判定用 = strREC[:strREC_判定桁]
            else:
                #strREC_判定用 = strREC.startswith
                strREC_判定用 = strREC[:30]  # '右側コメント領域に「 JOB 」等のキーワードがある場合があり検索範囲を限定

#'ADD END

            if JCL行分類 == "通常行":
                # ステートメント:JOB
                # フィールド    ://jobname   JOB   [parameter   [comments]]
                #                //jobname   JOB
                if " JOB " in strREC_判定用:
                    CMD分類_開始桁 = strREC.find(" JOB ")
                    CMD分類 = "JOB"
                    PARM_開始桁 = CMD分類_開始桁 + 5
                    継続行_flg = False
                # ステートメント:DD
                # フィールド    ://[ddname]   DD  [parameter   [comments]]
                #                //[ddname]   DD
                elif  " DD " in strREC_判定用:
                    CMD分類_開始桁 = strREC.find(" DD ")
                    CMD分類 = "DD"
                    PARM_開始桁 = CMD分類_開始桁 + 4
                    継続行_flg = False
                # ステートメント:EXEC
                # フィールド    ://[stepname]   EXEC   parameter   [comments]
                elif " EXEC " in strREC_判定用:
                    CMD分類_開始桁 = strREC.find(" EXEC ")
                    CMD分類 = "EXEC"
                    PARM_開始桁 = CMD分類_開始桁 + 6
                    継続行_flg = False
                # ステートメント:PROC (cataloged)
                # フィールド    ://[name]   PROC   [parameter   [comments]]
                #                //[name]   PROC
                # ステートメント:PROC (in-stream)
                # フィールド    ://name   PROC   [parameter   [comments]]
                #                //name   PROC
                elif " PROC " in strREC_判定用:
                    CMD分類_開始桁 = strREC.find(" PROC ")
                    CMD分類 = "PROC"
                    PARM_開始桁 = CMD分類_開始桁 + 6
                    継続行_flg = False
                # ステートメント:PEND
                # フィールド    ://[name]   PEND   [comments]
                elif " PEND " in strREC_判定用:
                    CMD分類_開始桁 = strREC.find(" PEND ")
                    CMD分類 = "PEND"
                    PARM_開始桁 = CMD分類_開始桁 + 6
                    継続行_flg = False
                # ステートメント:JCLLIB
                # フィールド    ://[name]  JCLLIB   parameter   [comments]
                elif " JCLLIB " in strREC_判定用:
                    CMD分類_開始桁 = strREC.find(" JCLLIB ")
                    CMD分類 = "JCLLIB"
                    PARM_開始桁 = CMD分類_開始桁 + 8
                    継続行_flg = False
#'20240131 ADD qian.e.wang
                # ステートメント:INCLUDE
                # フィールド    ://[name]  INCLUDE  parameter   [comments]
                elif " INCLUDE " in strREC_判定用:
                    CMD分類_開始桁 = strREC.find(" INCLUDE ")
                    CMD分類 = "INCLUDE"
                    PARM_開始桁 = CMD分類_開始桁 + 9
                    PARM文字列 = Mid(strREC, PARM_開始桁, 72 - PARM_開始桁)
                    継続行_flg = False
#'ADD END

#'20111215 ADD takei
                # ステートメント:IF/THEN/ELSE/ENDIF
                # フィールド    ://name IF [relational expression] THEN  [comments]
                #                //name ELSE  [comments]
                #                //name ENDIF  [comments]
                elif " IF " in strREC_判定用:
                    CMD分類_開始桁 = strREC.find(" IF ")
                    CMD分類 = "IF"
                    PARM_開始桁 = CMD分類_開始桁 + 4
                    #'継続行_flg = False                                      '"IF"文は通常のPC判定は行わない
                    #'if ":") > 0:
                    if " THEN" in strREC:                   #    'THENの場合「strREC_判定用」ではなく「strREC」で検索
                        IF継続 = False
                        #'PARM_終了桁 = ":")
                        PARM_終了桁 = strREC.find(" THEN")
                        PARM文字列 = "'" + Mid(strREC, PARM_開始桁, PARM_終了桁 - PARM_開始桁 - 1) + "'THEN"  #'適当にｱﾎﾟｽﾄﾛﾌｨ追加
                        COMMENT文字列 = strREC[PARM_終了桁 + 5:72]   # '桁数は自信なし。。
                    else:
                        IF継続 = True
                        PARM文字列 = "'" + strREC[PARM_開始桁:72]  # '桁数は自信なし。。
                        COMMENT文字列 = ""

                elif " ELSE " in strREC:
                    CMD分類_開始桁 = strREC.find(" ELSE ")
                    CMD分類 = "ELSE"
                    PARM_開始桁 = CMD分類_開始桁 + 6
                    継続行_flg = False
                elif " ENDIF " in strREC:
                    CMD分類_開始桁 = strREC.find(" ENDIF ")
                    CMD分類 = "ENDIF"
                    PARM_開始桁 = CMD分類_開始桁 + 7
                    継続行_flg = False
                elif IF継続 and " THEN " in strREC:  #'THENの場合「strREC_判定用」ではなく「strREC」で検索
                    CMD分類_開始桁 = strREC.find(" THEN ")
                    CMD分類 = "IF"
                    IF継続 = False
                    if CMD分類_開始桁 >= 15:
                        PARM文字列 = Mid(strREC, 15, CMD分類_開始桁 - 15 + 1 ) + "'THEN" # '適当にｱﾎﾟｽﾄﾛﾌｨ追加
                        COMMENT文字列 = strREC[CMD分類_開始桁 + 6:72]  ##  '桁数は自信なし。。
                    else: #   'MHI案件　PROC内のif分に規則はなさそう
                        PARM文字列 = strREC[CMD分類_開始桁 + 1:72]  # '桁数は自信なし。。
                        COMMENT文字列 = "" #'よくわからないので仮
                    #'継続行_flg = False                                  '"IF"文は通常のPC判定は行わない
#'ADD END

                # ステートメント:Null
                # フィールド    ://
                elif Mid(strREC, 2, 69) == EndLineString:
                    CMD分類 = "ヌル"
                    継続行_flg = False
                #'対応待ち
                # ステートメント:COMMAND
                # フィールド    ://[name]  COMMAND ‘command command-operand’  [comments]

                # ステートメント:CNTL
                # フィールド    ://label   CNTL   [*  comments]
                # ステートメント:ENDCNTL
                # フィールド    ://[label]   ENDCNTL   [comments]

                # ステートメント:EXPORT
                # フィールド    ://[label]   EXPORT   [comments]

                # ステートメント:OUTPUT JCL
                # フィールド    ://name   OUTPUT   parameter   [comments]

                # ステートメント:SCHEDULE
                # フィールド    ://[name]  SCHEDULE  parameter   [comments]

                # ステートメント:SET
                # フィールド    ://[name]  SET  parameter   [comments]

                # ステートメント:XMIT
                # フィールド    ://[name]   XMIT   parameter[,parameter] [comments]

            # 'NAME行情報セット
            if JCL行分類 == "通常行" and 継続行_flg == False and CMD分類 != "ヌル":
                TmpSheet_GYO[2] = Mid(strREC, 2, CMD分類_開始桁 - 3 + 1).replace(" ", "")

            #'CMD行情報セット
            if JCL行分類 == "通常行":
                TmpSheet_GYO[3] = CMD分類 # '上記以外の場合は前行の情報が引き継がれる
            else:
                TmpSheet_GYO[3] = ""

            #'PARM情報&COMMENT情報識別
            if JCL行分類 == "通常行" and CMD分類 != "ヌル":
                #'ステートメント分類の識別情報(JOB EXEC DDなど)がある行の処理
                if 継続行_flg == False:
                #  'PARM文字列 = Mid(strREC, PARM_開始桁, 72 - PARM_開始桁)
                    A継続 = False
                    P継続 = False
                    PC判定 = "未処理"  #'PARM部orコメント部かを識別する
                # 'PARM部とコメント分に分割
                    SUB_PC判定_JCL()

                #'ステートメント分類の識別情報(JOB EXEC DDなど)がない行の処理
                else:
                    # 20241111 detao.wang 関電 UPD START
                    # 20240703 jiafu.luan 千葉 UPD START
                    if C継続 and not P継続:
                        PARM文字列 = ""
                        COMMENT文字列 = Mid(strREC, 3, 68)
                    elif A継続:
                    # if A継続:
                    # 20241111 detao.wang 関電 UPD END
                        PARM_開始桁 = 16
                        for i in range(2,16):
                            if strREC[i] != " ":
                                PARM_開始桁 = min(PARM_開始桁,i)
                        # 'PARM文字列 = Mid(strREC, PARM_開始桁, 72 - PARM_開始桁)
                        PC判定 = "PARM"

                        SUB_PC判定_JCL()

                    elif P継続:

                        PC判定 = "未処理"
                        PARM_開始桁 = 2 # '4桁目以降の任意の桁から再開される（最初のスペースをスキップ）
                                        #   'ループ内でカウントアップしているので初期値は -1 している
                        for i in range(PARM_開始桁,min(72,len(strREC))):
                            if strREC[i] != " ":
                                PARM_開始桁 = i
                                break
                        if PARM_開始桁 == 2:
                            PARM_開始桁 = 72

                        #'PARM文字列 = Mid(strREC, PARM_開始桁, 72 - PARM_開始桁)

                        SUB_PC判定_JCL()
                    # 20241111 detao.wang 関電 UPD START
                    # elif C継続:
                    #     PARM文字列 = ""
                    #     COMMENT文字列 = Mid(strREC, 3, 68)
                    # # # 20240703 jiafu.luan 千葉 UPD END
                    # 20241111 detao.wang 関電 UPD END
                    else:
                        first = -1
                        last = -1
                        for i in range(2,min(len(strREC),72)):
                            if strREC[i] != " ":
                                if first == -1:
                                    first = i
                                last = i

                        PARM文字列 = Mid(strREC,first,last-first+1)
                        COMMENT文字列 = ""
                        CMD分類 = ""
                        TmpSheet_GYO[3] = ""
                        # if strREC.startswith("//"):
                        #     PARM文字列 = ""
                        #     COMMENT文字列 = ""
                        MSG = "想定外のパターン"


# 'ヌル行
            elif JCL行分類 == "通常行" and CMD分類 == "ヌル":
                PARM文字列 = "ヌル"
                COMMENT文字列 = ""
            #'通常行以外
            else:

                if JCL行分類 == "ｺﾒﾝﾄ行":
                    PARM文字列 = ""
                    COMMENT文字列 = Mid(strREC, 0, 71) #' 「=」で始まる文字列をセルにセットできないので
                elif JCL行分類 == "区切行":
                    PARM文字列 = ""
                    COMMENT文字列 = Mid(strREC, 2, 69)
                elif JCL行分類 == "SYSIN行":
                    PARM文字列 = Mid(strREC, 0, 80)
                    COMMENT文字列 = ""
                elif JCL行分類 == "終了行":                      # '福山通運対応
                    PARM文字列 = ""
                    COMMENT文字列 = ""
                elif JCL行分類 == "NET行":                       #  '福山通運対応
                    PARM文字列 = RTrim(Mid(strREC, 3, 68))
                    COMMENT文字列 = ""

#'20111209　ADD
            #'PARM情報セット
            if PARM文字列.replace(" ", "") == "":   #'SPACEのみならNULL
                TmpSheet_GYO[4] = ""
            # elif PARM文字列[0] == "'":
            #     TmpSheet_GYO[4] = "'" + PARM文字列 #'先頭がアスタリスクの場合は追加で付与
            else:
                TmpSheet_GYO[4] = PARM文字列
# 'ADD END

            # 'COMMENT情報セット
            TmpSheet_GYO[5] = COMMENT文字列

            # 'PARM継続情報セット
            if IF継続:
                TmpSheet_GYO[6] = "IF継続"
            if A継続:
                TmpSheet_GYO[6] = "A継続"
            if P継続:
                TmpSheet_GYO[6] = "P継続"



            # '継続行情報セット
            if len(strREC) > 71 and get_ZENKAKU_str(strREC,71,1) != " ":  # '72文字目まで存在しない場合は継続行としない
                C継続 = True
            else:
                C継続 = False

            TmpSheet_GYO[7] = get_ZENKAKU_str(strREC,71,1)
            # '制御情報セット
            TmpSheet_GYO[8] = Mid(strREC, 72, 8)
            # '元資産行番号セット
            TmpSheet_GYO[9] = GYO - 1
            # '元資産行情報セット
            TmpSheet_GYO[10] = strREC

            # 'A-AUTO世代管理情報セット                               '2020/4/13 ADD
            if AAUTO世代情報管理 == "①A-AUTO世代のまま出力":
                TmpSheet_GYO[11] = Trim(Mid(strREC, 70, 1))


            TmpSheet.append(TmpSheet_GYO)
            GYO += 1


    return TmpSheet