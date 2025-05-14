#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import re
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


SUB_SQL生成_JCL_1_ = None
SUB_SQL生成_JCL_3_ = None
SUB_SQL生成_JCL_4_ = None



def reset_all():
    global ライブラリID,ファイル名,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_NAME,STEP_PGM,STEP_PROC,DD_NAME,SYSIN_SEQ,SYSIN_LINE, \
            PROC_ID,JCL分類,JOB_コメント,JOB_CLASS,JOB_MSGCLASS,JOB_MSGLEVEL,JOB_COND,検索行文字列,分析行TYPE,行CHK,CMD_SEQ,元資産行,\
            DD_DSN,DD_GDG,DD_SYSIN,DD_DISP,DD_SYSOUT,DD_WRITER,DD_FORM,DD_UNIT,DD_SPACE,DD_RECFM,DD_LRECL,DD_BLKSIZE,DD_VOL,DD_LABEL,DD_AAUTO世代,\
            PGM_CMD_判定,DB出力判定_JCL1,re_flg,STEP_PARM1,STEP_PARM2
            
    ライブラリID = ""
    ファイル名 = ""
    JOB_SEQ = 0
    JOB_ID = ""
    STEP_SEQ = 0
    STEP_NAME = ""
    STEP_PGM = ""
    STEP_PROC = "" 
    DD_NAME = "" 
    SYSIN_SEQ = 0
    SYSIN_LINE = ""

    PROC_ID = ""
    JCL分類 = ""
    JOB_コメント = ""
    JOB_CLASS = ""
    JOB_MSGCLASS = ""
    JOB_MSGLEVEL = ""
    JOB_COND = ""

    検索行文字列 = ""
    分析行TYPE = ""
    行CHK = False
    CMD_SEQ = 0
    元資産行 = 0

    DD_DSN = ""
    DD_GDG = ""
    DD_SYSIN = ""
    DD_DISP = ""
    DD_SYSOUT = ""
    DD_WRITER = ""
    DD_FORM = ""
    DD_UNIT = ""
    DD_SPACE = ""
    DD_RECFM = ""
    DD_LRECL = ""
    DD_BLKSIZE = ""
    DD_VOL = ""
    DD_LABEL = ""
    DD_AAUTO世代 = ""  # '2020/4/14 ADD
    PGM_CMD_判定 = False
    DB出力判定_JCL1 = False
    re_flg = False

    STEP_PARM1 = ""
    STEP_PARM2 = ""
    
    
class SUB_SQL生成_JCL_1:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "①JCL_基本情報"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self):
        if self.dic == None:
            self.setup()
            
        global ファイル名,ライブラリID,JOB_SEQ ,JOB_ID,PROC_ID,JCL分類,JOB_コメント,JOB_CLASS,JOB_MSGCLASS,JOB_MSGLEVEL,JOB_COND
  
        key_list = ["JCL名","LIBRARY_ID","JOB_SEQ","JOB_ID","PROC_ID","JCL分類","JOB_コメント","CLASS","MSGCLASS","MSGLEVEL","COND" ]
        value_list = [ファイル名,ライブラリID,JOB_SEQ ,JOB_ID,PROC_ID,JCL分類,DB文字(JOB_コメント),JOB_CLASS,JOB_MSGCLASS,JOB_MSGLEVEL,JOB_COND]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        

class SUB_SQL生成_JCL_2:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "①JCL_STEP_SYSIN"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self):
        if self.dic == None:
            self.setup()
            
        global ライブラリID,ファイル名,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_NAME,STEP_PGM,STEP_PROC, DD_NAME, SYSIN_SEQ,SYSIN_LINE

        # ADD 20240618 yi.a.qian
        # PROC_NAME Setting
        # if JOB_SEQ == 0:
        #     if STEP_PROC == "":
        #         global PROC_ID
        #         STEP_PROC = PROC_ID
        # ADD END
        key_list = ["LIBRARY_ID","JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP_ID","PGM_NAME","PROC_NAME","SYSIN_PGM","SYSIN_DD","SYSIN_SEQ","SYSIN"]
        value_list = [ライブラリID,ファイル名,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_NAME,STEP_PGM,STEP_PROC,"", DD_NAME, SYSIN_SEQ,DB文字(SYSIN_LINE)]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()



class SUB_SQL生成_JCL_3:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "①JCL_STEP情報"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self):
        if self.dic == None:
            self.setup()
            
        global ライブラリID,ファイル名,JOB_SEQ, JOB_ID,PROC_ID,STEP_SEQ,STEP_NAME,STEP_PGM,STEP_PROC,STEP_PARM1,STEP_PARM2

        STEP_SEQ += 1
        # ADD 20240618 yi.a.qian
        # PROC_NAME Setting
        # if JOB_SEQ == 0:
        #     if STEP_PROC == "":
        #         # global PROC_ID
        #         STEP_PROC = PROC_ID
        # ADD END
        key_list = ["LIBRARY_ID","JCL_NAME","JOB_SEQ","JOB_ID","PROC_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","PARM_VAR_LIST","PARM_VALUE_LIST"]
        value_list = [ライブラリID,ファイル名,JOB_SEQ, JOB_ID,PROC_ID,STEP_SEQ,STEP_NAME,STEP_PGM,STEP_PROC,STEP_PARM1,DB文字(STEP_PARM2)]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        
        
class SUB_SQL生成_JCL_4:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "①JCL_PGM_DSN"
        # self.db_path = db_path
        
    def setup(self):
        self.dic = {}
        
    def insert(self):
        if self.dic == None:
            self.setup()
            
        global ライブラリID,ファイル名,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_NAME,STEP_PGM,STEP_PROC,DD_NAME,DD_DSN,DD_GDG,DD_AAUTO世代,DD_SYSIN,DD_DISP,DD_SYSOUT,DD_WRITER,DD_FORM,DD_UNIT,DD_SPACE,DD_RECFM,DD_LRECL,DD_BLKSIZE,DD_VOL,DD_LABEL
        
        # ADD 20240618 yi.a.qian
        # PROC_NAME Setting
        # if JOB_SEQ == 0:
        #     if STEP_PROC == "":
        #         global PROC_ID
        #         STEP_PROC = PROC_ID
        # ADD END
        key_list = ["LIBRARY_ID","JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","SYSIN_PGM","DD_NAME","DSN","GDG","SYSIN","DISP","SYSOUT","WRITER","FORM","UNIT","SPACE_Q","DCB_RECFM","DCB_LRECL","DCB_BLKSIZE","VOL","LABEL"]
        value_list = [ライブラリID,ファイル名,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_NAME,STEP_PGM,STEP_PROC,"",DD_NAME,DD_DSN,DD_GDG + DD_AAUTO世代,DD_SYSIN,DD_DISP,DD_SYSOUT,DD_WRITER,DD_FORM,DD_UNIT,DD_SPACE,DD_RECFM,DD_LRECL,DD_BLKSIZE,DD_VOL,DD_LABEL]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
       
        
class SUB_SQL生成_JCL_5:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "①JCL_CMD情報"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self):
        if self.dic == None:
            self.setup()
            
        global ファイル名,JOB_SEQ,JOB_ID,L_STEP_SEQ,STEP_NAME,STEP_PGM,STEP_PROC,DD_NAME,CMD_SEQ,元資産行,分析行TYPE,検索行文字列,行CHK
        
        if 分析行TYPE == "EXEC":
           L_STEP_SEQ = STEP_SEQ + 1
        else:
           L_STEP_SEQ = STEP_SEQ

        CMD_SEQ = CMD_SEQ + 1
        # ADD 20240618 yi.a.qian
        # PROC_NAME Setting
        # if JOB_SEQ == 0:
        #     if STEP_PROC == "":
        #         global PROC_ID
        #         STEP_PROC = PROC_ID
        # ADD END
        key_list = ["資産ID","JOB_SEQ","JCL_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","DD_NAME","CMD_SEQ","元資産行情報","CMD分類","PARM","行CHK結果"]
        value_list = [ファイル名,JOB_SEQ,JOB_ID,L_STEP_SEQ,STEP_NAME,STEP_PGM,STEP_PROC,DD_NAME,CMD_SEQ,元資産行,分析行TYPE,検索行文字列,行CHK]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()

class SUB_SQL生成_JCL_6:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "①PROC_PARM"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self,開始列,TokenSheet2_GYO):
        if self.dic == None:
            self.setup()
            
        global ファイル名,PROC_ID,JCL分類
        
        L_文字列1 = ""
        L_文字列2 = ""
        L_文字列3 = ""
        L_PARM_KEY = ""
        L_PARM_VALUE = ""

        開始列 = 開始列 + 1

        for i in range(開始列,len(TokenSheet2_GYO)):
            L_PARM_KEY = ""
            L_PARM_VALUE = ""
            L_文字列1 = TokenSheet2_GYO[i]
            L_文字列2 = ""
            if i+1 < len(TokenSheet2_GYO):
                L_文字列2 = TokenSheet2_GYO[i + 1]
            L_文字列3 = ""
            if i+2 < len(TokenSheet2_GYO):
                L_文字列3 = TokenSheet2_GYO[i + 2]
            
            
            if L_文字列1 != "" and L_文字列2 == "=":
            
                L_PARM_KEY = L_文字列1
                if L_文字列3 == "," or L_文字列3 == "":
                    L_PARM_VALUE = ""
                else:
                    L_PARM_VALUE = L_文字列3.replace("'", "")
  
                key_list = ["資産ID","PROC_ID","PROC_TYPE","PARM_KEY","PARM_VALUE"]
                value_list = [ファイル名,PROC_ID,JCL分類,L_PARM_KEY,L_PARM_VALUE]
                
                sql,value = make_insert_sql(self.dbname,value_list,key_list)
                
                self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        
class SUB_SQL生成_共通_1:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "共通_資産解析_関連情報"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self,info1, lib2, id3, row4 , key5, hit6):
        if self.dic == None:
            self.setup()
            
  
        key_list = ["分類キー","LIBRARY_ID","資産ID","最終行番号","設定情報キー","資産行情報"]
        value_list = [info1, lib2, id3, row4 , key5, hit6]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
    
class SUB_SQL生成_共通_2:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "共通_資産解析_NG情報"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self,info1, lib2, id3, row4 , str5):
        if self.dic == None:
            self.setup()
            
  
        key_list = ["実行分類","LIBRARY_ID","資産ID","最終行番号","資産行情報"]
        value_list = [info1, lib2, id3, row4 , str5]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
          
    
def 設定値数値チェック(parm_str):
    
    if IsNumeric(parm_str):
        return  "数値"
    else:
        return "文字列"

def 設定値予約語以外チェック(parm_str):

    #'CHECK対象の予約語を指定　　とりあえずは福山通運のJOB文対応
    if parm_str in ("CLASS ","MSGCLASS "):
        return False
    else:
        return True

def 設定値タイプチェック(parm_str):

    if "'" in str(parm_str):
       return "定数"
    else:
        return "変数"

def 設定値一致チェック(parm_val,code_val):
    
    parm_val,code_val = str(parm_val),str(code_val)
    Rtn_Cd = False
    設定値タイプ = 設定値タイプチェック(code_val)
    
    #'変数_予約語以外                                    '20140226ADD
    if parm_val == "変数_予約語以外" and \
       設定値予約語以外チェック(code_val) and \
       設定値タイプ== "変数":
       return  True
    #'変数
    elif "変数" in parm_val and \
       設定値タイプ == "変数":
       return True
    #'定数
    elif "定数" in parm_val and \
       設定値タイプ == "定数":
       return True
    #'数値
    elif "数値" in parm_val and \
       設定値数値チェック(code_val) == "数値":
       return True
    #'DSN名
    elif "DSN名" in parm_val and \
       設定値タイプ == "変数":
       return True
    #'PGM名
    elif "PGM名" in parm_val and \
       設定値タイプ == "変数":
       return True
    #'PROC名
    elif "PROC名" in parm_val and \
       設定値タイプ== "変数":
       return True
    #'MACRO名
    elif "MACRO名" in parm_val and \
       設定値タイプ== "変数":
        if "MACRO_" in code_val:
           return True
        else:
           return False
       
    #'SYSIN名
    elif "SYSIN名" in parm_val and \
       設定値タイプ == "変数":
       return True
    #'予約後（上記条件以外）
    elif parm_val == code_val:
       return True
    else:
       return False
    
    return Rtn_Cd


def 検索行文字列生成処理(TokenSheet_str):

    TokenSheet_str = [str(s) for s in TokenSheet_str if s != "'"]
    検索行文字列 = " ".join(TokenSheet_str)
    return DB文字(検索行文字列)

  
def DISP変換(STR):
    if STR == "SHR":
        return "S"
    elif STR == "RNW":
        return "R"
    elif STR == "NEW":
        return "N"
    elif STR == "CATLG":
        return "C"
    elif STR == "DELETE":
        return "D"
    elif STR == "KEEP":
        return "K"
    elif STR == "OLD":
        return "O"
    elif STR == "PASS":
        return "P"
    elif STR == "MOD":
        return "M"
    elif STR == ",":
        return ""
    elif STR == "(":
        return ""
    elif STR == ")":
        return "END"
    else:
        return "END"

    return ""

def 設定値一致色分け処理(parm_val,code_val,dd_name_cand):
    ### セルの色分けは大変になるのでpython版では一旦やめる

    global re_flg,DD_DSN,STEP_PGM,STEP_PROC,DD_SYSIN
    global JOB_コメント,JOB_CLASS,JOB_MSGCLASS,JOB_MSGLEVEL,JOB_MSGLEVEL,JOB_COND
    global DD_GDG,DD_DISP,DD_SYSOUT,DD_NAME,DD_WRITER,DD_UNIT,DD_SPACE,DD_RECFM,DD_LRECL,DD_BLKSIZE,DD_VOL,DD_LABEL,DD_FORM
# 'ADD(20111128-takei)
#     '正規表現
    if re_flg:
        pass
#        TokenSheet2_GYO[検索列 + i).Select
#        セル色分け ("濃緑")
# 'ADD END(↓のelif の elseを外す)
#     '変数
    elif "変数" in parm_val:
        pass
    #    TokenSheet2_GYO[検索列 + i).Select
    #    セル色分け ("薄黄")
    # '定数
    elif "定数" in parm_val: 
        pass
    #    TokenSheet2_GYO[検索列 + i).Select
    #    セル色分け ("オレンジ")
    # '数値
    elif "数値" in parm_val: 
        pass
    #    TokenSheet2_GYO[検索列 + i).Select
    #    セル色分け ("オレンジ")
    # 'DSN名
    elif "DSN名" in parm_val:
    #    TokenSheet2_GYO[検索列 + i).Select
    #    セル色分け ("紫")
       
    #    'DD_NAME = TokenSheet2_GYO[2]
        DD_DSN = code_val
       
    # 'PGM名
    elif "PGM名"in parm_val:
    #    TokenSheet2_GYO[検索列 + i).Select
    #    セル色分け ("青")
       
    #    'STEP_NAME = TokenSheet2_GYO[2]
       STEP_PGM = code_val
       
    # 'PROC名
    elif "PROC名" in parm_val:
    #    TokenSheet2_GYO[検索列 + i).Select
    #    セル色分け ("赤")
       
    #    'STEP_NAME = TokenSheet2_GYO[2]
       STEP_PROC = code_val
       
    # 'SYSIN名
    elif "SYSIN名" in parm_val:
    #    TokenSheet2_GYO[検索列 + i).Select
       
       DD_SYSIN = code_val
       
    #    セル色分け ("緑")
    # '予約後（上記条件以外）
    elif parm_val == code_val:
        pass
    #    TokenSheet2_GYO[検索列 + i).Select
    #    セル色分け ("黄")
    # else
    # End if
    
    # '変数セット処理
    
    # '       elif parm_val ==  "JOB"
    # '            JOB_ID = TokenSheet2_GYO[2]
    if parm_val ==  "定数_コメント":
        JOB_コメント = code_val
    elif parm_val ==  "変数_CLASS":
        JOB_CLASS = code_val
    elif parm_val ==  "変数_MSGCLASS":
        JOB_MSGCLASS = code_val
    elif parm_val ==  "変数_MSGLEVEL①":
        JOB_MSGLEVEL = code_val
    elif parm_val ==  "変数_MSGLEVEL②":
        JOB_MSGLEVEL = JOB_MSGLEVEL + "," + code_val
    elif parm_val ==  "変数_COND①":
        JOB_COND = code_val
    elif parm_val ==  "変数_COND②":
        JOB_COND = JOB_COND + "," + code_val
    elif parm_val ==  "数値_GDG":
        DD_GDG = code_val
    elif parm_val ==  "変数_DISP①":
        DD_DISP = DISP変換(code_val)
    elif parm_val ==  "変数_DISP②":
        DD_DISP = DD_DISP + "," + DISP変換(code_val)
    elif parm_val ==  "変数_SYSOUT":
        DD_SYSOUT = code_val
        DD_NAME = dd_name_cand
    elif parm_val ==  "変数_WTR":
        DD_WRITER = code_val
# '           elif parm_val ==  "変数_FORM"
# '                DD_FORM = code_val
    elif parm_val ==  "変数_FLASH":
        DD_FORM = code_val
    elif parm_val ==  "変数_UNIT":
        DD_UNIT = code_val
    # 'UNIT_AFF パタン追加
    elif parm_val ==  "変数_UNITAFF":
        DD_UNIT = "AFF_" + code_val
    elif parm_val ==  "変数_SPACE①":
        DD_SPACE = code_val
    elif parm_val ==  "変数_SPACE②":
        DD_SPACE = DD_SPACE + "," + code_val
    elif parm_val ==  "変数_RECFM":
        DD_RECFM = code_val
    elif parm_val ==  "変数_LRECL":
        DD_LRECL = code_val
    elif parm_val ==  "変数_BLKSIZE":
        DD_BLKSIZE = code_val
    elif parm_val ==  "変数_VOL名":
        if DD_VOL == "":
            DD_VOL = code_val
        else:
            DD_VOL = DD_VOL + "," + code_val
        
    # '20140716追加
    elif parm_val ==  "変数_LABEL":
        if DD_LABEL == "":
            DD_LABEL = code_val
        else:
            DD_LABEL = DD_LABEL + "," + code_val
    elif parm_val ==  "定数_LABEL":
        if DD_LABEL == "":
            DD_LABEL = code_val
        else:
            DD_LABEL = DD_LABEL + "," + code_val
    elif parm_val ==  "DUMMY":
        DD_DSN = "DUMMY"
                
     
def PARMLIST生成_JCL(TokenSheet2_GYO):
    
         
    global STEP_PARM1,STEP_PARM2
    
    STEP_PARM1 = ""
    STEP_PARM2 = ""

    TokenSheet2_GYO += [""]*10
    #'EXEC命令から最初の「,」まではスキップ
    tmp_row = 4  #'4列目は「EXEC」である前提
    while True:
        tmp_row = tmp_row + 1
        if TokenSheet2_GYO[tmp_row] == "," or TokenSheet2_GYO[tmp_row] == "":
            break

    #'PARMLISTの生成
    if TokenSheet2_GYO[tmp_row] == ",":
        tmp_row = tmp_row + 1
        
        while True:
            # 'MSG = TokenSheet2_GYO[tmp_row] + TokenSheet2_GYO[tmp_row + 1] + TokenSheet2_GYO[tmp_row + 2]
        
            # '想定しているPARM形式であればリストを更新
            #     'EXEC命令のパラメータ（COND=）については随時除外するロジックを追加
            if TokenSheet2_GYO[tmp_row] == "COND":
               # '処理スキップ
                return  # '★★★課題：暫定的に解析処理を終了（PARMLISTの部分の記述は完了している想定）
            elif TokenSheet2_GYO[tmp_row] != "" and TokenSheet2_GYO[tmp_row + 1] == "=" and TokenSheet2_GYO[tmp_row + 2] != "":
               # '最初の値かどうか
                if STEP_PARM1 != "":
                    STEP_PARM1 = STEP_PARM1 + " " + TokenSheet2_GYO[tmp_row]
                    STEP_PARM2 = STEP_PARM2 + " " + TokenSheet2_GYO[tmp_row + 2]
                else:
                    STEP_PARM1 = TokenSheet2_GYO[tmp_row]
                    STEP_PARM2 = TokenSheet2_GYO[tmp_row + 2]
                tmp_row = tmp_row + 4   #'4列毎
            else:
                tmp_row = tmp_row + 1   #'1列毎

            if TokenSheet2_GYO[tmp_row] == "":
                break
            
    return 

def DB出力判定_JCL(TokenSheet2_GYO):
    global SUB_SQL生成_JCL_1_,SUB_SQL生成_JCL_3_,SUB_SQL生成_JCL_4_
    
    global 分析行TYPE
    global DD_DSN,DD_GDG,DD_SYSIN,DD_DISP,DD_SYSOUT,DD_WRITER,DD_FORM,DD_UNIT,DD_SPACE,DD_RECFM,DD_LRECL,DD_BLKSIZE,DD_VOL,DD_LABEL,DD_AAUTO世代
    global PGM_CMD_判定,STEP_SEQ,DB出力判定_JCL1
    #'DB出力判定(変数再セット前に出力)
    if 分析行TYPE == "JOB":
        SUB_SQL生成_JCL_1_.insert()
        STEP_SEQ = 0
        DB出力判定_JCL1 = True
            
    elif 分析行TYPE == "PROC":
        SUB_SQL生成_JCL_1_.insert()
        STEP_SEQ = 0   #'ここは見直しが必要かも
        DB出力判定_JCL1 = True
                
    elif 分析行TYPE == "EXEC":
        # '★★★　セコム案件仮対応　★★★
        # 'パラメータリストの生成
        PARMLIST生成_JCL(TokenSheet2_GYO)

        SUB_SQL生成_JCL_3_.insert()
        # '出力後変数初期化
        # 'STEP_NAME = ""    'DDで利用する
        # 'STEP_PGM = ""     'DDで利用する
        # 'STEP_SYSIN = ""
        PGM_CMD_判定 = ""
    elif 分析行TYPE == "DD":
        # 'DD_NAME = Name_fld
        SUB_SQL生成_JCL_4_.insert()
        # 'DD_NAME = ""
        DD_DSN = ""
        DD_GDG = ""
        DD_SYSIN = ""
        DD_DISP = ""
        DD_SYSOUT = ""
        DD_WRITER = ""
        DD_FORM = ""
        DD_UNIT = ""
        DD_SPACE = ""
        DD_RECFM = ""
        DD_LRECL = ""
        DD_BLKSIZE = ""
        DD_VOL = ""
        DD_LABEL = ""
        DD_AAUTO世代 = ""  # '2020/4/14 ADD
                
    
def analysis1_5_structure_JCL(TokenSheet2,JCLSheet,fileName,conn,cursor, 設定条件HIT情報出力 = False,分析条件HIT情報出力 = False,設計条件HIT情報出力 = False,設定条件HIT_NG情報出力 = True):
    global SUB_SQL生成_JCL_1_,SUB_SQL生成_JCL_3_,SUB_SQL生成_JCL_4_
    
    global ライブラリID,ファイル名,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_NAME,STEP_PGM,STEP_PROC, DD_NAME, SYSIN_SEQ,SYSIN_LINE
    global PROC_ID,JCL分類,JOB_コメント,JOB_CLASS,JOB_MSGCLASS,JOB_MSGLEVEL,JOB_COND
    global 検索行文字列,分析行TYPE,行CHK,CMD_SEQ,元資産行,DB出力判定_JCL1,ID_fld,Name_fld,CMD_fld,PARM_fld,行CHK
    global re_flg
    global DD_DSN,DD_GDG,DD_SYSIN,DD_DISP,DD_SYSOUT,DD_WRITER,DD_FORM,DD_UNIT,DD_SPACE,DD_RECFM,DD_LRECL,DD_BLKSIZE,DD_VOL,DD_LABEL,DD_AAUTO世代
    global PGM_CMD_判定,STEP_PARM1,STEP_PARM2
    
    reset_all()
    
    SUB_SQL生成_JCL_1_ = SUB_SQL生成_JCL_1(conn,cursor)
    SUB_SQL生成_JCL_2_ = SUB_SQL生成_JCL_2(conn,cursor)
    SUB_SQL生成_JCL_3_ = SUB_SQL生成_JCL_3(conn,cursor)
    SUB_SQL生成_JCL_4_ = SUB_SQL生成_JCL_4(conn,cursor)
    SUB_SQL生成_JCL_5_ = SUB_SQL生成_JCL_5(conn,cursor)
    SUB_SQL生成_JCL_6_ = SUB_SQL生成_JCL_6(conn,cursor)
    
    SUB_SQL生成_共通_1_ = SUB_SQL生成_共通_1(conn,cursor)
    SUB_SQL生成_共通_2_ = SUB_SQL生成_共通_2(conn,cursor)
    

    #構造解析シート初期化_JCL
    基準列 = 5       #'TokenSheet2　列ポインタ 2020/4/14 4→5
    基準列2 = 6      # 'JCLSheet　列ポインタ
   
   
    ALL_chk_ok = True   # 'シート単位で全ての設定パターンが登録されているかどうか（初期値True）
    検索行 = 2           #'TokenSheet2　行ポインタ
    分析行TYPE = ""      #'
    CMD_SEQ = 0
    

   
    #'入力ファイル単位で初期化
    # UPD 20240618 yi.a.qian
    ファイル名,ライブラリID,_,member = GetFileInfo(fileName)
    
    JOB_ID = member
    JOB_SEQ = 0
    PROC_ID = member
    # UPD END
    #'JCL分類 = "外部PROC" 'パラメータがない場合、PROCキーワードがない場合がある 201911MHI対応で不具合が出るためコメント化
    JCL分類 = ""
    DD_NAME = ""
    DB出力判定_JCL1 = False
   
   #'Todo空ファイル判定U.LB.JCL%A%CYDOBJ.txt
    for i in range(len(TokenSheet2)):
        検索列 = 基準列
        TokenSheet2_GYO = TokenSheet2[i]
    
        元資産行 = TokenSheet2_GYO[1]
        ID_fld = TokenSheet2_GYO[2]
        DD_AAUTO世代 = TokenSheet2_GYO[3]
        Name_fld = TokenSheet2_GYO[4]
        CMD_fld = TokenSheet2_GYO[5]
        分析行TYPE = CMD_fld
        PARM_fld = TokenSheet2_GYO[検索列]
     
        #'*****
        if Name_fld != "":
            DD_NAME = Name_fld
        # '*****
        
        # 'if TokenSheet2_GYO[2] != "":
        # '   DD_NAME = TokenSheet2_GYO[2]
     
        if CMD_fld ==  "JOB":
            JOB_ID = Name_fld
            JOB_SEQ = JOB_SEQ + 1
            # ADD 20240618 yi.a.qian
            PROC_ID = ""
            # ADD END
            JCL分類 = "JCL"
            DD_NAME = ""
          #  '検索列 = 3         'TokenSheet2　列ポインタ
            検索列 = 基準列       #  'TokenSheet2　列ポインタ
        elif CMD_fld == "EXEC":
            STEP_NAME = Name_fld
            STEP_PGM = ""
            STEP_PROC = ""
            STEP_PARM1 = ""
            STEP_PARM2 = ""
            DD_NAME = ""
            #'検索列 = 3         'TokenSheet2　列ポインタ
            検索列 = 基準列       #  'TokenSheet2　列ポインタ
        elif CMD_fld == "DD":
          #  '検索列 = 3         'TokenSheet2　列ポインタ
            検索列 = 基準列       #  'TokenSheet2　列ポインタ
        elif CMD_fld == "JCLLIB":
           # '検索列 = 3         'TokenSheet2　列ポインタ
            検索列 = 基準列      #   'TokenSheet2　列ポインタ
        elif CMD_fld == "PROC":
            if JCL分類 == "JCL":
                PROC_ID = Name_fld
                JCL分類 = "内部PROC"
                DD_NAME = ""
            elif JCL分類 ==  "":
                #'JOB_ID = Name_fld
                PROC_ID = Name_fld
                JCL分類 = "外部PROC"
                DD_NAME = ""
                # ADD 20241008 j.d.lin
                JOB_ID = ""
                STEP_PROC = ""
                # ADD END
            #'検索列 = 3         'TokenSheet2　列ポインタ
            検索列 = 基準列      #   'TokenSheet2　列ポインタ
        elif CMD_fld == "PEND":
            PROC_ID = ""
            JCL分類 = "JCL"
            #'検索列 = 3         #'TokenSheet2　列ポインタ
            検索列 = 基準列      #   'TokenSheet2　列ポインタ
#'20240131 ADD qian.e.wang
        elif CMD_fld == "INCLUDE":
            PROC_ID = ""
            JCL分類 = "JCL"
            #'検索列 = 3         #'TokenSheet2　列ポインタ
            検索列 = 基準列      #   'TokenSheet2　列ポインタ
#'ADD END
        
#'ADD
        elif CMD_fld == "IF":
           # '検索列 = 3      #   'TokenSheet2　列ポインタ
            検索列 = 基準列   #      'TokenSheet2　列ポインタ
        elif CMD_fld == "ELSE":
           # '検索列 = 3        # 'TokenSheet2　列ポインタ
            検索列 = 基準列     #    'TokenSheet2　列ポインタ
        elif CMD_fld == "ENDIF":
            #'検索列 = 3         #'TokenSheet2　列ポインタ
            検索列 = 基準列      #   'TokenSheet2　列ポインタ
#'ADD END
        else:
            #'検索列 = 4         'TokenSheet2　列ポインタ
            検索列 = 基準列 + 1      #  'TokenSheet2　列ポインタ

     
        # '検索開始列の退避　検索文字列出力時に利用
        検索開始列 = 検索列
        行CHK = "OK" #'CMD行単位でのチェック結果
     

        if ID_fld == "SYSIN行":
#      '   DD_NAME = "SYSIN"
# '            DD_NAME = Name_fld
            SYSIN_SEQ = 0
            while 検索列 < len(TokenSheet2_GYO):
                SYSIN_SEQ = SYSIN_SEQ + 1
                SYSIN_LINE = TokenSheet2_GYO[検索列]  #  'SYSIN明細
                SUB_SQL生成_JCL_2_.insert()
                検索列 = 検索列 + 1
                 #'Loop Until TokenSheet2_GYO[検索列] = "" #   'SYSIN行に空白行がある場合出力が中断する場合の対応（3行以上連続しない想定）
        
        elif ID_fld == "NET行":    #'SYSIN用TABLEに出力
            SYSIN_SEQ = 0
            SYSIN_列位置_FROM = 0
            SYSIN_列位置_TO = len(TokenSheet2_GYO[検索列])*2
            
            while True:
                SYSIN_SEQ = SYSIN_SEQ + 1
                SYSIN_TEMP = Mid(TokenSheet2_GYO[検索列], SYSIN_列位置_FROM, len(TokenSheet2_GYO[検索列])*2)
                if len(SYSIN_TEMP)*2 < 255:
                   SYSIN_列位置_FROM = SYSIN_列位置_FROM + 255  #'ループ終了条件
                else:
                   SYSIN_列位置_TO = Mid(SYSIN_TEMP, 0, 255).rfind(",")
                   SYSIN_TEMP = Mid(SYSIN_TEMP, SYSIN_列位置_FROM, SYSIN_列位置_TO+1)
                   SYSIN_列位置_FROM = SYSIN_列位置_TO + 1
                
                SYSIN_LINE = SYSIN_TEMP   # 'SYSIN明細
                STEP_NAME = "NET"
                STEP_PGM = "NET"
                STEP_PROC = ""
                SUB_SQL生成_JCL_2_.insert()
                
                if SYSIN_列位置_FROM >= len(TokenSheet2_GYO[検索列])*2:
                    break
                
            # '    検索列 = 検索列 + 1

            
        elif ID_fld == "通常行":
            while True:
         
                #'PARM数カウント
                PARM行 = 0     #'Parm行ポインタ
                parm_hit = False
                while True:
                    #'PARM列 = 6      'Parm列ポインタ
                    PARM列 = 基準列2     # 'Parm列ポインタ
                    hit_flg = True
                    parm_cnt = 0
                    re_flg = False
                
                    #'先頭のトークン比較(最初が違う場合は列のカウントアップ不要)
                
                    if len(TokenSheet2_GYO) > 検索列 and TokenSheet2_GYO[検索列] == JCLSheet[PARM行][PARM列]:
                      
                        while True:
                            if JCLSheet[PARM行][PARM列] != "":
                                parm_cnt = parm_cnt + 1

                            parm_val = JCLSheet[PARM行][基準列2+parm_cnt-1]
                            code_val = ""
                            if 検索列+parm_cnt-1 < len(TokenSheet2_GYO):
                                code_val = TokenSheet2_GYO[検索列+parm_cnt-1]
                            parm_chk = 設定値一致チェック(parm_val,code_val)
                            if parm_chk == False:
                                hit_flg = False
                            PARM列 = PARM列 + 1
                            
                        
                            if PARM列 >= len(JCLSheet[PARM行]) or JCLSheet[PARM行][PARM列] == "" or hit_flg == False:
                                break
# 'ADD(20111128-takei)
                    # '先頭トークンが正規表現の場合
                    elif str(JCLSheet[PARM行][PARM列]).startswith("正規表現_"):
                        # '検索対象文字列再構成
                        tokenstr = ""
                        tokencnt = 検索列
                        re_flg = True
                        while tokencnt < len(TokenSheet2_GYO):
                            tokenstr = tokenstr + TokenSheet2_GYO[tokencnt] + " "
                            tokencnt = tokencnt + 1
                    
                        re_pattern = JCLSheet[PARM行][PARM列].replace("正規表現_", "")
                        mc = re.search(re_pattern,tokenstr)
                        if mc:
                            matchstr = str(mc.group(0)) # '最初に一致した検索文字列
                           # '先頭の文字列から一致している場合のみ(先頭の文字列の一部が正規表現にHITしているものは対象外)
                            if tokenstr.startswith(matchstr) and \
                               len(TokenSheet2_GYO[検索列]) <= len(matchstr):
                        
                                # '一致したパラメータ数カウント
                                tokencnt = 検索列
                                re_exit = False #'ﾊﾟﾗﾒｰﾀが完全一致しなければ処理を抜ける
                                while True:
                                    if str(TokenSheet2_GYO[tokencnt]) in matchstr:
                                        matchstr = matchstr.replace(str(TokenSheet2_GYO[tokencnt]), "",1) ### 先頭からマッチした１つだけをreplaceする
                                        tokencnt = tokencnt + 1
                                        parm_cnt = parm_cnt + 1
                                    else:
                                        re_exit = True
                                     #'↓念の為無限ループしないように配慮↓
                                    if matchstr.replace(" ","") == "" or re_exit == True:
                                        break
                        
                            else:
                                hit_flg = False
                        
                        else:
                            hit_flg = False

# 'ADD END
                    else:
                        hit_flg = False
            
                    # 'チェック結果
                    if hit_flg:

                        parm_hit = True
                        # JCLSheet[PARM行][4] = JCLSheet[PARM行][4] + 1 #  '設定値カウントアップ
                    #     'MsgBox ("検索値： " + TokenSheet2_GYO[検索列] + " PARM-Key： " + JCLSheet[PARM行][1])
                    #     '分析行TYPE = JCLSheet[PARM行][5]       'ここではセットしない
                
                    #    '検索行文字列作成
                        検索行文字列 = 検索行文字列生成処理(TokenSheet2_GYO[検索開始列:])   #'処理開始列（検索列を引数にする）       '20120208 ADD
                
                        if 設定条件HIT情報出力:
                        #  'HIT時関連情報出力
                            SUB_SQL生成_共通_1_.insert("キーID", ライブラリID, ファイル名, 元資産行, JCLSheet[PARM行][1], 検索行文字列)
                
                        if 分析条件HIT情報出力 and JCLSheet[PARM行][2] != "":
                            
                            # '★★★福山通運暫定対応★★★
                            if JCLSheet[PARM行][2] == "VOL":  #'VOLの場合
                                検索行文字列 = JOB_ID + "-" + STEP_NAME + "-" + DD_NAME + ": " + 検索行文字列
                            
                            # '★★★福山通運暫定対応★★★
                            if JCLSheet[PARM行][2] == "LABEL":  #'LABELの場合
                                検索行文字列 = JOB_ID + "-" + STEP_NAME + "-" + DD_NAME + ": " + 検索行文字列
                            
                            SUB_SQL生成_共通_1_.insert("分析ID", ライブラリID, ファイル名, 元資産行, JCLSheet[PARM行][2], 検索行文字列)
                
                        if 設計条件HIT情報出力 and JCLSheet[PARM行][3] != "":
                            #    'HIT時関連情報出力
                            SUB_SQL生成_共通_1_.insert("設計ID", ライブラリID, ファイル名, 元資産行, JCLSheet[PARM行][3], 検索行文字列)
                    
                    else:
                        PARM行 = PARM行 + 1

                    if PARM行 >= len(JCLSheet) or parm_hit == True:
                        break
           
                # '検索列更新
                
                # '行単位の情報を出力するのでここでも生成（20150810 takei）
                検索行文字列 = 検索行文字列生成処理(TokenSheet2_GYO[検索開始列:]) 
                if parm_hit:
                    PARM列 = 基準列2
                    for i in range(parm_cnt):
                        parm_val = ""
                        if PARM列 + i < len(JCLSheet[PARM行]):
                            parm_val = JCLSheet[PARM行][PARM列 + i]
                        code_val = ""
                        if 検索列+i < len(TokenSheet2_GYO):
                            code_val = TokenSheet2_GYO[検索列+i]
                        設定値一致色分け処理(parm_val,code_val,TokenSheet2_GYO[4])
                    re_flg = False
                    検索列 = 検索列 + parm_cnt
                else:
                    # '判定NG処理
                    ALL_chk_ok = False      #    'ひとつでもNGがあるとシート単位でNG
                    行CHK = "NG"
            
                    if 設定条件HIT_NG情報出力:
                       # '検索行文字列作成
                        検索行文字列 = 検索行文字列生成処理(TokenSheet2_GYO[検索開始列:])    #'処理開始列（検索列を引数にする）       '20120208 ADD
                        # 'NG時関連情報出力
                        SUB_SQL生成_共通_2_.insert("JCL", ライブラリID, ファイル名, 元資産行, 検索行文字列)

                    検索列 = 検索列 + 1
             
                if 検索列 >= len(TokenSheet2_GYO):
                    break
                
        
        elif ID_fld == "区切行":
            pass
            # '何もしない
        
    
    #  'JCL_CMD情報の出力（2015/08/10追加）
        if ID_fld == "通常行":
            SUB_SQL生成_JCL_5_.insert()
            
            # 'PROC_PARMの出力（2019/10/8追加）
            # 'if PROC_ID != "" and CMD_fld = "PROC":  'PROC資産内のPROCコマンド行を出力
            if CMD_fld == "PROC":  # 'PROC_IDはこの時点でセットされていない。
            
                SUB_SQL生成_JCL_6_.insert(検索開始列,TokenSheet2_GYO)
        
        # 'DB出力判定(変数再セット前に出力)
        DB出力判定_JCL(TokenSheet2_GYO)
  
     

    # 'SUB_SQL生成_JCL_1 が実行されていない場合は「外部PROCとして出力する」
    if not (DB出力判定_JCL1):
       SUB_SQL生成_JCL_1_.insert()

    
    return ALL_chk_ok
    