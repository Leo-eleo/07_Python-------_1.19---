#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

レコード長取得_ = None
ActSheet = []
ActSheet_x = []
JCL_NAME_WK = ""
PGM_NAME = ""
STEP_SEQ = 0
JCL_NAME_SV = ""
JOB_SEQ_SV = ""
STEP_SEQ_SV = 0
PROC_ID = ""
分割文字列 = []
分割文字列2 = []

PGM_SYSIN = ""
L_GDG = ""
L_DISP = ""
L_SYSIN = ""
L_DSN = ""
P_データ種別 = ""
P_入出力判定 = ""
TMP_DSN = ""
PGM_PROC = ""
BMCP_PGM = ""
parm = ""
vbCrLf = "\n"


class レコード長取得:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "DATA_DSN別データ分類情報"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for dsn,record in zip(df["DSN"],df["レコード長"]):
            self.dic[dsn] = record


    def get(self,P_DSN):
        if self.dic == None:
            self.setup()
        
        if P_DSN in self.dic:
            return self.dic[P_DSN]
        else:
            return ""
    

def analysis3(ActSheet,conn,cursor):
    global レコード長取得_ 
    レコード長取得_ = レコード長取得(conn,cursor)
    
    
    # 'DSN出現順序設定
    x = 0
    sheet_length = len(ActSheet)
    if sheet_length == 0:
        print("データが空です")
        return ActSheet
    
    x_save = x
    save_key = ActSheet[x][1]  # 'JOBNET版
    
    STEP_SEQ列 = 7                       #'ADD 20200617
    STEP_SEQ列2 = 8                      #'ADD 20200617
    
    PGM列 = 10
    PGM_SYSIN列 = 12
    照合ポイント生成オプション = "①全ての出力項目"
    
    DD名情報列 = 14          #'13⇒14
    DSN情報列 = 15           #'14⇒15
    GDG世代情報列 = 16       #'15⇒16
    SYSINメンバ列 = 17       #'16⇒17
    レコード長列 = 36        #'35⇒36
    データ種別列 = 19        #'MHI案件ではとりあえずデータ種別2を利用 19⇒20

    出現順序列 = 38          #'34→37⇒38
    入出力判定列 = 22        #'21⇒22
    受領判定列 = 23          #'21⇒23
    受領判定列_TEST = 37     #'36⇒37
    コメント列 = 43          #'42⇒43
        
    #' 20220215 王 受領判定問題対応　元々はDSNでソートしたうえの処理と認識　先勝ちの形に直し
    dsn_key = ""
    JCL_ID列 = 3
    #'end_chk = False ' 20220215 王 受領判定問題対応より削除

    while True:
        if x == sheet_length:
            break
      
   
    #   ' 20220215 王 受領判定問題対応より追加 Start
        if ActSheet[x][出現順序列] == "":
            y = x
            JCL_ID_BEFORE = ActSheet[x][JCL_ID列]
            dsn_key_count_dic = {} ### ファイル内で dsn_key が既に出現しているか、何回出現しているかを格納する
            while True:
                if y == sheet_length:
                    break
                
                if ActSheet[y][1] == "": #' 空白値は処理しない
                    break
                
                if ActSheet[y][JCL_ID列] != JCL_ID_BEFORE:
                    break
                
                if ActSheet[y][出現順序列] == "":
                    if ActSheet[y][入出力判定列] == "INPUT" or \
                       ActSheet[y][入出力判定列] == "I-O" or \
                       ActSheet[y][入出力判定列] == "OUTPUT" or \
                       ActSheet[y][入出力判定列] == "DELETE" or \
                       ActSheet[y][入出力判定列] == "INPUT-DELETE" or \
                       ActSheet[y][入出力判定列] == "EXTEND":
                        
                        find_key = ActSheet[y][DSN情報列] + "-" + \
                                   ActSheet[y][GDG世代情報列] + "-" + \
                                   ActSheet[y][SYSINメンバ列]
                        if find_key in dsn_key_count_dic:
                            dsn_key_count_dic[find_key] += 1
                            ActSheet[y][出現順序列] = dsn_key_count_dic[find_key]
                        else:
                            dsn_key_count_dic[find_key] = 1
                            ActSheet[y][出現順序列] = 1
   
                y = y + 1
    #   ' 20220215 王 受領判定問題対応より追加 End
        dsn_key = ""
#    ' 20220215 王 受領判定問題対応より削除
#    'Loop Until (ActSheet[x][1] = "" and end_chk) or x > 1048576
   
#    ' 20220215 王 受領判定問題対応より追加 Start
        x = y
#    Loop Until ActSheet[x][1] = "" or x > 1048576
#    ' 20220215 王 受領判定問題対応より追加 End

#    '「入力」チェック処理
    x = 0
    while True:
        if x == sheet_length:
            break
        if ActSheet[x][1] == "": #' 空白値は処理しない
            break
        # 'TB暫定追加
        # '一時ファイル、DUMMY照合対象外にする HP李 2013/11/26
        
        if "&&" not in ActSheet[x][DSN情報列] and ActSheet[x][DSN情報列] != "DUMMY":
            if (ActSheet[x][入出力判定列] == "INPUT" or \
               ActSheet[x][入出力判定列] == "INPUT-DELETE" or \
               ActSheet[x][入出力判定列] == "I-O" or \
               ActSheet[x][入出力判定列] == "EXTEND") and \
               ActSheet[x][出現順序列] == 1:
                if ActSheet[x][データ種別列] == "空ファイル":   #  '空ファイルはテスト用のみ判定する
                    ActSheet[x][受領判定列_TEST] = "入力"
                else:
                    ActSheet[x][受領判定列] = "入力"
                    ActSheet[x][受領判定列_TEST] = "入力"
        x = x + 1
    
#    '「照合」チェック処理(顧客毎に条件を変更する)
#    '全ての出力を照合ポイントにする
    if 照合ポイント生成オプション == "①全ての出力項目":
        x = 0
        x_save = x
        save_key = ActSheet[x][1]
        while True:
            if x == sheet_length:
                break
            if ActSheet[x][1] == "": #' 空白値は処理しない
                break
    
            if save_key != ActSheet[x][1]:
                x_save = x
                save_key = ActSheet[x][1]
        
            # '入出力情報は"EXTEND"場合、「入力/照合」に判定する HP李 2014/01/29
            if ActSheet[x][入出力判定列] == "I-O" or \
                ActSheet[x][入出力判定列] == "DLI_I-O" or \
                ActSheet[x][入出力判定列] == "OUTPUT" or \
                ActSheet[x][入出力判定列] == "EXTEND":
                x2 = x
                x_save = x
                dsn_key = ActSheet[x][DSN情報列] + ActSheet[x][GDG世代情報列]
                x_save2 = 0
                x_save3 = 0
                while True:
                    if x2 == sheet_length:
                        break
                    if ActSheet[x2][1] == "": #' 空白値は処理しない
                        break
                    if ActSheet[x2][1] != save_key:
                        break
                    
                    if ActSheet[x2][DSN情報列] + ActSheet[x2][GDG世代情報列] == dsn_key:
                        # '入出力情報は"EXTEND"場合、「入力/照合」に判定する HP李 2014/01/29
                        if ActSheet[x2][入出力判定列] == "I-O" or \
                            ActSheet[x2][入出力判定列] == "DLI_I-O" or \
                            ActSheet[x2][入出力判定列] == "OUTPUT" or \
                            ActSheet[x2][入出力判定列] == "EXTEND":
                            x_save2 = x2
                    
                        if ActSheet[x2][入出力判定列] == "DELETE" or \
                            ActSheet[x2][入出力判定列] == "INPUT-DELETE":
                            x_save3 = x2
                    x2 = x2 + 1
            
                # '一時ファイル,DUMMY照合対象外にする HP李 2013/11/26
                if "&&" not in ActSheet[x_save2][DSN情報列] and ActSheet[x_save2][DSN情報列] != "DUMMY":
                
                    if "照合" in ActSheet[x_save2][受領判定列]:
                        pass
                
                    else:
                    # '○取得用受領判定
                        if ActSheet[x_save2][データ種別列] != "IMSDB_SEGMENT":    # '
                            if x_save3 > x_save2:   # '最後の照合ポイント以降に削除される場合
                                if ActSheet[x_save2][受領判定列] == "入力":
                                    ActSheet[x_save2][受領判定列] = "入力/照合D"
                                else:
                                    ActSheet[x_save2][受領判定列] = "照合D"
                            else:
                                if ActSheet[x_save2][受領判定列] == "入力":
                                    ActSheet[x_save2][受領判定列] = "入力/照合"
                                else:
                                    ActSheet[x_save2][受領判定列] = "照合"
                    
                    # '○テスト用受領判定
                        if ActSheet[x_save2][データ種別列] != "IMSDB_TABLE":   #  '
                            if x_save3 > x_save2:    #'最後の照合ポイント以降に削除される場合
                                if ActSheet[x_save2][受領判定列_TEST] == "入力":
                                    ActSheet[x_save2][受領判定列_TEST] = "入力/照合D"
                                else:
                                    ActSheet[x_save2][受領判定列_TEST] = "照合D"
                            else:
                                if ActSheet[x_save2][受領判定列_TEST] == "入力":
                                    ActSheet[x_save2][受領判定列_TEST] = "入力/照合"
                                else:
                                    ActSheet[x_save2][受領判定列_TEST] = "照合"
            
                x = x_save
           
            x = x + 1
    
    #    'テスト実施単位における最後の出力を照合ポイントにする
    else:
        pass
    
    # '===今後も使いそうにないので一旦削除　★重複メンテが面倒な為 ===

    # '    x = 2
    # '    x_save = x
    # '    save_key = ActSheet[x][1]
    # '    Do
    # '        if save_key != ActSheet[x][1]:
    # '        '一時ファイル,DUMMYは照合対象外にする HP李 2013/11/26
    # '           if (InStr(ActSheet[x][ave, DSN情報列], "++")) = 0 and ActSheet[x][ave, DSN情報列] != "DUMMY":
    # '               if ActSheet[x][ave, 受領判定列] = "入力":
    # '                   ActSheet[x][ave, 受領判定列) = "入力/照合"
    # '               else
    # '                   ActSheet[x][ave, 受領判定列) = "照合"
    # '               End if
    # '
    # '           End if
    # '           save_key = ActSheet[x][1]
    # '        End if
    # '
    # '        '入出力情報は"EXTEND"場合、「入力/照合」に判定する HP李 2014/01/29
    # '        if ActSheet[x][入出力判定列] = "I-O" or \
    # '           ActSheet[x][入出力判定列] = "OUTPUT" or \
    # '           ActSheet[x][入出力判定列] = "EXTEND":
    # '           x_save = x
    # '        End if
    # '        x = x + 1
    # '    Loop Until (ActSheet[x][1] = "" and ActSheet[x][ 1, 1] = "") or x > 1048575
    # '
    # '    '一時ファイルは照合対象外にする HP李 2013/11/26
    # '    if (InStr(ActSheet[x][ave, DSN情報列), "++")) = 0:
    # '        ActSheet[x][ave, 受領判定列) = "照合"
    # '    End if
    # '
    # '===================================================================
    
  
   
    #    '【MHI暫定】取得対象DSNにレコード長情報付与 レコード長列
    #    '【MHI暫定】STではUtilityの出力ファイルは照合対象としない
    x = 0
    while True:
        if x == sheet_length:
            break
        if ActSheet[x][1] == "": #' 空白値は処理しない
            break
        # '取得対象DSNにレコード長情報付与 レコード長列
        if ActSheet[x][受領判定列] != "" and ActSheet[x][DSN情報列] != "":
            ActSheet[x][レコード長列] = レコード長取得_.get(ActSheet[x][DSN情報列])
        
        # '受領判定変更
        if "照合D" not in ActSheet[x][受領判定列] and "照合" in ActSheet[x][受領判定列]:
        
            if ActSheet[x][PGM列] == "ADRDSSU":
                ActSheet[x][受領判定列] = ActSheet[x][受領判定列].replace("照合", "照合X")
                ActSheet[x][コメント列] = "ADRDSSUによる出力"
            elif ActSheet[x][PGM列] == "IDCAMS":
                ActSheet[x][受領判定列] = ActSheet[x][受領判定列].replace("照合", "照合X")
                ActSheet[x][コメント列] = "IDCAMSによる出力"
            elif ActSheet[x][PGM列] == "IEBGENER":
                ActSheet[x][受領判定列] = ActSheet[x][受領判定列].replace("照合", "照合X")
                ActSheet[x][コメント列] = "IEBGENERによる出力"
            elif ActSheet[x][PGM列] == "SORT":
                ActSheet[x][受領判定列] = ActSheet[x][受領判定列].replace("照合", "照合X")
                ActSheet[x][コメント列] = "IDCAMSによる出力"
            elif ActSheet[x][PGM_SYSIN列] == "DFSUDMP0":
                ActSheet[x][受領判定列] = ActSheet[x][受領判定列].replace("照合", "照合X")
                ActSheet[x][コメント列] = "DFSUDMP0による出力"
            elif ActSheet[x][STEP_SEQ列2] == 0 and "DBOUT" in ActSheet[x][DD名情報列]:
                ActSheet[x][受領判定列] = ActSheet[x][受領判定列].replace("照合", "照合X")
                ActSheet[x][コメント列] = "DFSUDMP0による出力2"
            elif ActSheet[x][STEP_SEQ列2] == 0 and  "_SYSD001" in ActSheet[x][DD名情報列] and ActSheet[x][PGM列] == "":
                ActSheet[x][受領判定列] = ActSheet[x][受領判定列].replace("照合", "照合X")
                ActSheet[x][コメント列] = "LOAD処理"
            
        
        # 'TEST用受領判定変更
        if "照合D" not in ActSheet[x][受領判定列_TEST] and "照合" in ActSheet[x][受領判定列_TEST]:
        
            if ActSheet[x][PGM列] == "ADRDSSU":
                ActSheet[x][受領判定列_TEST] = ActSheet[x][受領判定列_TEST].replace("照合", "照合X")
                ActSheet[x][コメント列] = "ADRDSSUによる出力"
            elif ActSheet[x][PGM列] == "IDCAMS":
                ActSheet[x][受領判定列_TEST] = ActSheet[x][受領判定列_TEST].replace("照合", "照合X")
                ActSheet[x][コメント列] = "IDCAMSによる出力"
            elif ActSheet[x][PGM列] == "IEBGENER":
                ActSheet[x][受領判定列_TEST] = ActSheet[x][受領判定列_TEST].replace("照合", "照合X")
                ActSheet[x][コメント列] = "IEBGENERによる出力"
            elif ActSheet[x][PGM列] == "SORT":
                ActSheet[x][受領判定列_TEST] = ActSheet[x][受領判定列_TEST].replace("照合", "照合X")
                ActSheet[x][コメント列] = "IDCAMSによる出力"
            elif ActSheet[x][PGM_SYSIN列] == "DFSUDMP0":
                ActSheet[x][受領判定列_TEST] = ActSheet[x][受領判定列_TEST].replace("照合", "照合X")
                ActSheet[x][コメント列] = "DFSUDMP0による出力"
            elif ActSheet[x][STEP_SEQ列2] == 0 and "DBOUT" in ActSheet[x][DD名情報列]:
                ActSheet[x][受領判定列_TEST] = ActSheet[x][受領判定列_TEST].replace("照合", "照合X")
                ActSheet[x][コメント列] = "DFSUDMP0による出力2"
            elif ActSheet[x][STEP_SEQ列2] == 0 and "_SYSD001" in ActSheet[x][DD名情報列] and ActSheet[x][PGM列] == "":
                ActSheet[x][受領判定列_TEST] = ActSheet[x][受領判定列_TEST].replace("照合", "照合X")
                ActSheet[x][コメント列] = "LOAD処理"
            
        
        x = x + 1
        
    return ActSheet