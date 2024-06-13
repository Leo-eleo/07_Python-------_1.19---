#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

SUB_SQL生成_COBOL_0_ = None
SUB_SQL生成_COBOL_3_ = None
SUB_SQL生成_COBOL_4_ = None



def reset_all():            
    global ファイル名,COBOL_ID,CMD_SEQ,元資産行,COBOL領域分類,COBOL階層情報,COBOL分岐判定,分析行TYPE,検索行文字列,行CHK, \
            ライブラリID,PGM_ID,ファイルIO有無,PARM有無,サブルーチン有無,SQL有無,画面有無,ALL_chk_ok, \
            COBOL_関連区分,COBOL_関連資産,COBOL_関連資産_TRANID,\
            P_ファイル名,P_CBL_ID,P_CMD分類,P_呼出資産,P_呼出PARM, \
            re_flg
            
    re_flg = False
    ライブラリID = ""
    ファイル名 = ""
    COBOL_ID = ""
    COBOL領域分類 = ""
    COBOL階層情報 = ""
    COBOL分岐判定 = ""
    検索行文字列 = ""
    分析行TYPE = ""
    行CHK = False
    CMD_SEQ = 0
    元資産行 = 0
    PGM_ID = ""
    ファイルIO有無 = ""
    PARM有無 = ""
    サブルーチン有無 = ""
    SQL有無 = ""
    画面有無 = ""
    ALL_chk_ok = True
    COBOL_関連区分 = ""
    COBOL_関連資産 = ""
    COBOL_関連資産_TRANID = ""

    
    P_ファイル名 = ""
    P_CBL_ID = ""
    P_CMD分類 = ""
    P_呼出資産 = ""
    P_呼出PARM = ""

    
    
    
class SUB_SQL生成_COBOL_0:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "②COBOL_基本情報"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self):
        if self.dic == None:
            self.setup()
            
        global ファイル名,ライブラリID,COBOL_ID,PGM_ID,CMD_SEQ ,ファイルIO有無,PARM有無,サブルーチン有無,SQL有無,画面有無,ALL_chk_ok
        
        if ALL_chk_ok == True:
            L_CHK = "OK"
        else:
            L_CHK = "NG"
        
      
        key_list = ["資産ID","LIBRARY_ID","メンバ名","モジュール名","CMD行数","解析結果","ファイルIO有無","PARM有無","サブルーチン有無","SQL有無","画面有無"]
        value_list = [ファイル名,ライブラリID,COBOL_ID,PGM_ID,CMD_SEQ ,L_CHK,ファイルIO有無,PARM有無,サブルーチン有無,SQL有無,画面有無]
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()


class SUB_SQL生成_COBOL_3:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "②COBOL_関連資産"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self):
        if self.dic == None:
            self.setup()
            
        global ファイル名,COBOL_ID,COBOL_関連区分,COBOL_関連資産,COBOL_関連資産_TRANID
        
        key_list = ["資産ID","COBOL_ID","関連区分","関連資産","関連資産_TRANID"]
        value_list = [ファイル名,COBOL_ID,COBOL_関連区分,COBOL_関連資産,COBOL_関連資産_TRANID.replace("'", "")]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        
        
class SUB_SQL生成_COBOL_4:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "②COBOL_CMD情報"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self):
        if self.dic == None:
            self.setup()
            
        global ファイル名,COBOL_ID,CMD_SEQ,元資産行,COBOL領域分類,COBOL階層情報,COBOL分岐判定,分析行TYPE,検索行文字列,行CHK
        
        CMD_SEQ = CMD_SEQ + 1
      
        key_list = ["資産ID","COBOL_ID","CMD_SEQ","元資産行情報","記述領域","段落","分岐判定","CMD分類","PARM","行CHK結果"]
        value_list = [ファイル名,COBOL_ID,CMD_SEQ,元資産行,COBOL領域分類,COBOL階層情報,COBOL分岐判定,分析行TYPE,検索行文字列,行CHK]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
       
        

class SUB_SQL生成_COBOL_6:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "②COBOL_関連資産"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self,開始列,TokenSheet2_GYO):
        if self.dic == None:
            self.setup()
            
        global  P_ファイル名,P_CBL_ID,P_CMD分類,P_呼出資産,P_呼出PARM
        
  
        key_list = ["資産ID","COBOL_ID","関連区分","関連資産","関連資産_TRANID"]
        value_list = [P_ファイル名,P_CBL_ID,DB文字(P_CMD分類),DB文字(P_呼出資産),DB文字(P_呼出PARM)]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
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
            self.cursor.close()
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
            self.cursor.close()
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
   
   
def PARM形式情報判定_COBOL_AREA(cbl_area, parm_area):
    

    if cbl_area == "領域Aあり":
        if parm_area == "任意" or parm_area == "領域A":
            return True
        else:
            return False
    if cbl_area == "領域Bのみ":
        if parm_area == "任意" or parm_area == "領域B":
            return True
        else:
            return False
    else:
        MSG = "想定外の処理"
        return False       
    
def PARM形式情報判定_COBOL_DIVISION(cbl_div, parm_div):

    if cbl_div == parm_div or parm_div == "共通":
       return True
    else:
       return False

def 例外キー_COBOL(key):

    if key == "レベル" or key == "変数_SECTION名" or key == "変数_段落名":
        return True
    else:
        return False
    
def 設定値数値チェック_COBOL(parm_str):
    # 'if parm_str = "0":
    # '   MsgBox (parm_str & " : " & IsNumeric(parm_str))
    if IsNumeric(parm_str):
        return  "数値"
    else:
        return "文字列"



def 設定値タイプチェック_COBOL(parm_str):

    if "'" in str(parm_str) or "==" in str(parm_str) or "\"" in str(parm_str):
       return "定数"
    else:
        return "変数"

def 設定値一致チェック_COBOL(parm_val,code_val):
    
    parm_val,code_val = str(parm_val),str(code_val)
    Rtn_Cd = False
    設定値タイプ = 設定値タイプチェック_COBOL(code_val)
    
    #     'この判定は処理が重いので特別に分けた
    # '    if "非予約" in parm_val:
    # '       if not (予約語判定(code_val, 1)):
    # '            return True
    # '    else
    
    # 'レベル
    if "レベル" in parm_val and \
        設定値数値チェック_COBOL(code_val) == "数値":
        return True
    # 'コピー句
    elif "コピー句" in parm_val and \
        設定値タイプ == "変数":
        return True
    # 'サブルーチン
    elif "サブルーチン" in parm_val and \
        設定値タイプ == "変数":
        return True
    # '変数
    elif "変数" in parm_val:
        # '変数名     '20130919 富士通対応（福山通運案件）
        if parm_val == "変数名":
            if 設定値タイプ == "変数" and \
                code_val != "PIC" and code_val != "REDEFINES" and code_val != ")":
                return True
        else:
            if 設定値タイプ == "変数":
                return True
    # '定数
    elif "定数" in parm_val and \
        設定値タイプ == "定数":
        return True
    # '数値
    elif "数値" in parm_val and \
        設定値数値チェック_COBOL(code_val) == "数値":
        return True
    # '予約後（上記条件以外）
    elif parm_val == code_val:
        return True
    else:
        return False

    return Rtn_Cd


def 検索行文字列生成処理(TokenSheet_str):

    TokenSheet_str = [str(s) for s in TokenSheet_str]
    検索行文字列 = " ".join(TokenSheet_str)
     
    return DB文字(検索行文字列)



def 設定値一致色分け処理_COBOL(parm_val,code_val,proc_cond):
    global SUB_SQL生成_COBOL_3_
    global COBOL_関連区分,COBOL_関連資産,COBOL_関連資産_TRANID,COPY_変数,サブルーチン有無,COPY_レベル, re_flg
    ### セルの色分けは大変になるのでpython版では一旦やめる

    if re_flg:
        pass

    # 'セクション
    elif "SECTION名" in parm_val:
        pass

    # '段落
    elif "段落名" in parm_val:
        pass

    
    # 'コピー句
    elif "コピー句" in parm_val:
       COBOL_関連区分 = "COPY"
       COBOL_関連資産 = code_val
       COBOL_関連資産_TRANID = ""
       SUB_SQL生成_COBOL_3_.insert()
    
    # 'サブルーチン
    elif "サブルーチン" in parm_val:
       COBOL_関連区分 = "CALL"
       COBOL_関連資産 = code_val
       COBOL_関連資産_TRANID = ""
       SUB_SQL生成_COBOL_3_.insert()
    #    'サブルーチン有無設定
       サブルーチン有無 = "●"
    
    # 'EXEC CICS LINK PROGRAM
    elif "ECLP" in parm_val:
       COBOL_関連区分 = "ECLP"
       COBOL_関連資産 = code_val
       COBOL_関連資産_TRANID = ""
       SUB_SQL生成_COBOL_3_.insert()
    
    # 'EXEC CICS START TRANSID
    elif "ECST" in parm_val:
       COBOL_関連区分 = "ECST"
       COBOL_関連資産 = ""
       COBOL_関連資産_TRANID = code_val
       SUB_SQL生成_COBOL_3_.insert()
    
    # 'EXEC CICS SEND MAP
    elif "ECSM" in parm_val:
       COBOL_関連区分 = "ECSM"
       COBOL_関連資産 = code_val
       COBOL_関連資産_TRANID = ""
       SUB_SQL生成_COBOL_3_.insert()
    
    # 'EXEC CICS HANDLE ABEND PROGRAM
    elif "ECHA" in parm_val:
       COBOL_関連区分 = "ECHA"
       COBOL_関連資産 = code_val
       COBOL_関連資産_TRANID = ""
       SUB_SQL生成_COBOL_3_.insert()
    
    # 'EXEC CICS WRITEQ TD QUEUE
    elif "ECWTQ" in parm_val:
       COBOL_関連区分 = "ECWTQ"
       COBOL_関連資産 = code_val
       COBOL_関連資産_TRANID = ""
       SUB_SQL生成_COBOL_3_.insert()
    
    # 'EXEC CICS READ TRANSACTION
    elif "ECRT" in parm_val:
       COBOL_関連区分 = "ECRT"
       COBOL_関連資産 = ""
       COBOL_関連資産_TRANID = code_val
       SUB_SQL生成_COBOL_3_.insert()
    
    # 'EXEC CICS READ UPDATE DATASET
    elif "ECRUD" in parm_val:
       COBOL_関連区分 = "ECRUD"
       COBOL_関連資産 = code_val
       COBOL_関連資産_TRANID = ""
       SUB_SQL生成_COBOL_3_.insert()
    
    # 'EXEC CICS READ DATASET
    elif "ECRD" in parm_val:
       COBOL_関連区分 = "ECRD"
       COBOL_関連資産 = code_val
       COBOL_関連資産_TRANID = ""
       SUB_SQL生成_COBOL_3_.insert()
    
    # '変数名
    elif parm_val == "変数名":
       COPY_変数 = code_val
    # '変数
    elif "変数" in parm_val:
        pass

    # '定数
    elif "定数" in parm_val:
        pass

    # '数値
    elif "数値" in parm_val:
        pass

    # 'レベル￥
    elif "レベル" in parm_val:
       COPY_レベル = code_val
       
    # '条件語
    elif proc_cond == "PROC-条件":
        pass
 
        
    # '予約語（上記条件以外）
    elif parm_val == code_val:
        pass

    else:
        pass
    
#     '変数セット処理
# '    Select Case parm_val
# '           Case "JOB"
# '                JOB_ID = TokenSheet2.Cells(検索行, 2).Value
# '           Case "定数_コメント"
# '                JOB_コメント = code_val
# '           Case "変数_タイプ①"
# '                COPY_タイプ = code_val
# '           Case "桁数_数値"
# '                COPY_桁数 = code_val
# '                COPY_桁数_文字列 = code_val
# '           Case "桁数補助_数値"
# '                COPY_桁数 = code_val
# '                COPY_桁数_文字列 = COPY_桁数_文字列 & "," & code_val
# '           Case "変数_REDEFINES"
# '                COPY_REDIFINE = code_val
# '                REDIFINE_判定_レベル = COPY_レベル
# '           Case "OCCURS_数値"
# '                COPY_OCCURS = code_val
# '                OCCOURS_判定_レベル = COPY_レベル
# '                OCCOURS_回数 = COPY_OCCURS
# '           Case "COMP-3"
# '                COPY_タイプ2 = "COMP-3"
# '           Case "変数_タイプ②"     '「COMP-3」など優先して制御したいものがあれば前に設定する
# '                COPY_タイプ2 = code_val

  
def analysis1_5_structure_COBOL(TokenSheet2,CobolSheet,fileName,db_path, 設定条件HIT情報出力 = False,分析条件HIT情報出力 = False,設計条件HIT情報出力 = False,設定条件HIT_NG情報出力 = True, conn=None, cursor=None):
    global SUB_SQL生成_COBOL_3_
    
    global ファイル名,COBOL_ID,CMD_SEQ,元資産行,COBOL領域分類,COBOL階層情報,COBOL分岐判定,分析行TYPE,検索行文字列,行CHK, \
            ライブラリID,PGM_ID,ファイルIO有無,PARM有無,サブルーチン有無,SQL有無,画面有無,ALL_chk_ok, \
            COBOL_関連区分,COBOL_関連資産,COBOL_関連資産_TRANID,\
            P_ファイル名,P_CBL_ID,P_CMD分類,P_呼出資産,P_呼出PARM, \
            re_flg
    

    reset_all()
    SUB_SQL生成_COBOL_0_ = SUB_SQL生成_COBOL_0(conn,cursor)
    SUB_SQL生成_COBOL_3_ = SUB_SQL生成_COBOL_3(conn,cursor)
    SUB_SQL生成_COBOL_4_ = SUB_SQL生成_COBOL_4(conn,cursor)
    SUB_SQL生成_COBOL_6_ = SUB_SQL生成_COBOL_6(conn,cursor)
    
    SUB_SQL生成_共通_1_ = SUB_SQL生成_共通_1(conn,cursor)
    SUB_SQL生成_共通_2_ = SUB_SQL生成_共通_2(conn,cursor)


    ALL_chk_ok = True    #'シート単位で全ての設定パターンが登録されているかどうか（初期値True）
   
#    '変数初期化
#    'COBOL_ID = Replace(Replace(ファイル名, ".cob", ""), ".cbl", "") '拡張子に合わせて設定
#    'COBOL_ID = Replace(Replace(モジュールID, ".cob", ""), ".cbl", "") '拡張子に合わせて設定 TODO 号機とのずれ対応
    ファイル名,ライブラリID,_,COBOL_ID = GetFileInfo(fileName)

    PGM_ID = "未"
   
    FILE_SEQ = 0
    CMD_SEQ = 0
    
    
    ファイルIO有無 = ""
    PARM有無 = ""
    サブルーチン有無 = ""
    SQL有無 = ""
    画面有無 = ""
    
    検索行 = 0      #'TokenSheet　行ポインタ
    基準列 = 6       #   'TokenSheet2 列ポインタ
    基準列2 = 7       #   'CobolSheet 列ポインタ
    #'分析行TYPE = ""     '行単位情報なのでここではない
    
    while 検索行 < len(TokenSheet2):

        TokenSheet2_GYO = TokenSheet2[検索行]

        #   '検索列 = 5         'TokenSheet2　列ポインタ
        検索列 = 基準列         #'TokenSheet2　列ポインタ
        行CHK = "OK" #'CMD行単位でのチェック結果
        
        #   '基本的にこのタイミングで行う
        元資産行 = TokenSheet2_GYO[1]
        COBOL領域分類 = TokenSheet2_GYO[3]
        COBOL階層情報 = TokenSheet2_GYO[4]
        COBOL分岐判定 = TokenSheet2_GYO[5]
        # print(TokenSheet2_GYO)
        while True:
        
            # ' "."は共通で処理対象外とする
            
            if 検索列 >=len(TokenSheet2_GYO) or (検索列+1 >= len(TokenSheet2_GYO) and (TokenSheet2_GYO[検索列] == ".")):
                
                # '行が変わる前に行単位処理を実施
                if len(TokenSheet2_GYO) >= 7:
                    検索行文字列 = 検索行文字列生成処理(TokenSheet2_GYO[6:])
                    SUB_SQL生成_COBOL_4_.insert()
                
                検索行 = 検索行 + 1
                if 検索行 >= len(TokenSheet2):
                    SUB_SQL生成_COBOL_0_.insert()
                    return ALL_chk_ok
                
                TokenSheet2_GYO = TokenSheet2[検索行]
                # print(TokenSheet2_GYO)
                # '検索列 = 5
                検索列 = 基準列
                行CHK = "OK" #'CMD行単位でのチェック結果

                元資産行 = TokenSheet2_GYO[1]
                COBOL領域分類 = TokenSheet2_GYO[3]
                COBOL階層情報 = TokenSheet2_GYO[4]
                COBOL分岐判定 = TokenSheet2_GYO[5]
  
                

            # '行レベルの処理であるが行加算処理が直前で実施されておりここで行う必要がある
            # '★コマンド情報設定（詳細化の余地あり）
            if IsNumeric(TokenSheet2_GYO[基準列]):
                分析行TYPE = "データ定義"
            elif COBOL領域分類 == "領域Aあり":
                if 基準列 + 1 < len(TokenSheet2_GYO) and TokenSheet2_GYO[基準列 + 1]  == "DIVISION":
                    分析行TYPE = "DIVISION"
                elif  基準列 + 1 < len(TokenSheet2_GYO) and TokenSheet2_GYO[基準列 + 1] == "SECTION":
                    分析行TYPE = "SECTION"
                    if TokenSheet2_GYO[基準列] == "LINKAGE": #'PARM有無設定
                        PARM有無 = "●"
                else:
                    if COBOL階層情報 == "手続き部":
                        分析行TYPE = "ラベル"
                    else:
                        分析行TYPE = TokenSheet2_GYO[基準列]
                        
                        if 分析行TYPE == "PROGRAM-ID":
                            if 基準列 + 1 < len(TokenSheet2_GYO)  and TokenSheet2_GYO[基準列 + 1] == ".":
                                if 基準列 + 2 < len(TokenSheet2_GYO):
                                    PGM_ID = TokenSheet2_GYO[基準列 + 2]
                                else:
                                    PGM_ID = "" 
                            else:
                                if 基準列 + 1 < len(TokenSheet2_GYO):
                                    PGM_ID = TokenSheet2_GYO[基準列 + 1]
                                else:
                                    PGM_ID = "" 
   
            else:
                分析行TYPE = TokenSheet2_GYO[基準列]

                if 分析行TYPE == "EXEC" and TokenSheet2_GYO[基準列 + 1] == "SQL":
                    分析行TYPE = "SQL"
                    SQL有無 = "●"
                elif 分析行TYPE == "OPEN":
                    ファイルIO有無 = "●"
    
            # 'PARM数カウント
            PARM行 = 0     # 'Parm行ポインタ
            parm_hit = False
            
            # '処理時間改善対応（長いSQL命令などがある場合に処理時間が異常にかかるための改善）
            検索行文字列 = 検索行文字列生成処理(TokenSheet2_GYO[6:])   #'処理開始列（6列目を引数にする）'検索行文字列が大きすぎる場合は処理をスキップする 2016/02/26
            # '文字列が10000文字を超える場合はチェックしない
            if len(検索行文字列) < 10000:
        
                while True:
                    # 'PARM列 = 7      'Parm列ポインタ
                    PARM列 = 基準列2      #'Parm列ポインタ
                    hit_flg = True
                    parm_cnt = 0
                    re_flg = False

                    # 'PARM形式情報判定
                    #     '設定条件の階層情報（「見出し部」「手続き部」等）が一致しているもののみ処理する
                    #     '設定条件の記述領域情報（「領域A」「領域B」）が一致しているもののみ処理する
                    # '元資産行 = TokenSheet2_GYO[1]
                    # 'COBOL領域分類 = TokenSheet2_GYO[3]
                    # 'COBOL階層情報 = TokenSheet2_GYO[4]
                    PARM領域分類 = CobolSheet[PARM行][5]
                    PARM階層情報 = CobolSheet[PARM行][6]
            
          
                    if PARM形式情報判定_COBOL_AREA(COBOL領域分類, PARM領域分類) and \
                        PARM形式情報判定_COBOL_DIVISION(COBOL階層情報, PARM階層情報):
                    
                        # '先頭のトークン比較(最初が違う場合は列のカウントアップ不要)
                        if TokenSheet2_GYO[検索列] == CobolSheet[PARM行][PARM列] or \
                            例外キー_COBOL(CobolSheet[PARM行][PARM列]):
                            while True:
                                if CobolSheet[PARM行][PARM列] != "":
                                    parm_cnt = parm_cnt + 1
                                parm_val = CobolSheet[PARM行][基準列2+parm_cnt-1]
                                code_val = ""
                                if 検索列+parm_cnt-1 < len(TokenSheet2_GYO):
                                    code_val = TokenSheet2_GYO[検索列+parm_cnt-1]
                                parm_chk = 設定値一致チェック_COBOL(parm_val,code_val)
                                if parm_chk == False:
                                    hit_flg = False
                                PARM列 = PARM列 + 1
                            
                                if PARM列 >= len(CobolSheet[PARM行]) or CobolSheet[PARM行][PARM列] == "" or hit_flg == False:
                                    break
                        
                        # '先頭トークンが正規表現の場合
                        elif str(CobolSheet[PARM行][PARM列]).startswith("正規表現_"):
                            # '検索対象文字列再構成
                            tokenstr = ""
                            tokencnt = 検索列
                            re_flg = True
                            word_set = CobolSheet[PARM行][-1]
                            start_word_check = False
                            while tokencnt < len(TokenSheet2_GYO):
                                s = TokenSheet2_GYO[tokencnt]
                                if s in word_set:
                                    start_word_check = True
                                tokenstr = tokenstr + s + " "
                                tokencnt = tokencnt + 1

                            if start_word_check == False:
                                for s in word_set:
                                    if tokenstr.startswith(s):
                                        start_word_check = True
                                        break
                                
                            if start_word_check == False:
                                hit_flg = False
                            else:
                            
                                re_pattern = CobolSheet[PARM行][PARM列].replace("正規表現_", "")
 
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

                        else:
                            hit_flg = False
                    else:
                        hit_flg = False
                

            
                    # 'チェック結果
                    if hit_flg:
                        parm_hit = True
                        CobolSheet[PARM行][4] = CobolSheet[PARM行][4] + 1  # '設定値カウントアップ
                        #'分析行TYPE = CobolSheet[PARM行][6]
                    
                        if 設定条件HIT情報出力 or 分析条件HIT情報出力 or 設計条件HIT情報出力:
                    
                            # '検索行文字列作成
                            # 'SUB_検索行文字列生成処理 (5)   '処理開始列（5列目を引数にする）       '20120208 ADD
                            検索行文字列 = 検索行文字列生成処理(TokenSheet2_GYO[6:])  # '処理開始列（6列目を引数にする）       '20120411 UPD
                    
                            if 設定条件HIT情報出力:
                                # 'HIT時関連情報出力
                                SUB_SQL生成_共通_1_.insert("キーID", ライブラリID, COBOL_ID, 元資産行, CobolSheet[PARM行][1], 検索行文字列)
                    
                            if 分析条件HIT情報出力 and CobolSheet[PARM行][2] != "":
                                # 'HIT時関連情報出力
                                SUB_SQL生成_共通_1_.insert("分析ID", ライブラリID, COBOL_ID, 元資産行, CobolSheet[PARM行][2], 検索行文字列)
                    
                            if 設計条件HIT情報出力 and CobolSheet[PARM行][3] != "":
                                # 'HIT時関連情報出力
                                SUB_SQL生成_共通_1_.insert("設計ID", ライブラリID, COBOL_ID, 元資産行, CobolSheet[PARM行][3], 検索行文字列)
                    
                    
                    else:
                        PARM行 = PARM行 + 1

                    if PARM行 >= len(CobolSheet) or parm_hit == True:
                        break
            
            else:  # '処理時間改善対応（検索行文字列が一定の長さを超える場合は処理スキップ）
                検索列 = 16000 #'これ以上の列があったらちょっと処理がおかしくなるかも
            
        
        # '        'チェック結果にかかわらず行単位の情報を出力するのでここで生成（20150326 takei）
        # '        検索行文字列 = 検索行文字列生成処理(TokenSheet2_GYO[6:])
        # '        'Call SUB_検索行文字列生成処理(基準列)  'CALLで呼ぶと基準列が加算される？値参照？
        
            # '検索列更新
            if parm_hit:

                PARM列 = 基準列2
                for i in range(parm_cnt):
                    parm_val = ""
                    if PARM列 + i < len(CobolSheet[PARM行]):
                        parm_val = CobolSheet[PARM行][PARM列 + i]
                    code_val = ""
                    if 検索列+i < len(TokenSheet2_GYO):
                        code_val = TokenSheet2_GYO[検索列+i]
                    設定値一致色分け処理_COBOL(parm_val,code_val,CobolSheet[PARM行][5])
                re_flg = False
                検索列 = 検索列 + parm_cnt
            else:
                # '判定NG処理
                ALL_chk_ok = False      #    'ひとつでもNGがあるとシート単位でNG
                行CHK = "NG"
        
                if 設定条件HIT_NG情報出力:
                    #    '検索行文字列作成
                    # ' → CHK結果に関係なく行文字列を生成するのでIF分の外に出す。'20150309 takei
                    # 'SUB_検索行文字列生成処理 (基準列)   '処理開始列（6列目を引数にする）       '20120411 UPD
                    # 'NG時関連情報出力
                    SUB_SQL生成_共通_2_.insert("COBOL", ライブラリID, COBOL_ID, 元資産行, 検索行文字列)

                検索列 = 検索列 + 1

            if 検索列 >= len(TokenSheet2_GYO):
                    break
 
 
        # 'チェック結果にかかわらず行単位の情報を出力するのでここで生成（20150326 takei）
        検索行文字列 = 検索行文字列生成処理(TokenSheet2_GYO[6:])
        # 'Call SUB_検索行文字列生成処理(基準列)  'CALLで呼ぶと基準列が加算される？値参照？
        SUB_SQL生成_COBOL_4_.insert()
    
    
        検索行 = 検索行 + 1
        
        
        
        if 検索行 >= len(TokenSheet2):
            break
    
    SUB_SQL生成_COBOL_0_.insert() #'基本情報だけど後から追加したので「0」にする

    return ALL_chk_ok
    