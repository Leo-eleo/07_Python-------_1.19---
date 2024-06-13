#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

     
class SUB_SQL生成_共通_1:
    def __init__(self,conn,cursor):
        self.dic = {}
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
        self.dic = {}
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
   
   
class スキーマ_基本情報:
    def __init__(self,conn,cursor):
        self.dic = {}
        self.conn = conn
        self.cursor = cursor
        self.dbname = "スキーマ_基本情報"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self,err_info):
        if self.dic == None:
            self.setup()
            
        global レイアウト名,COPY_レコード名,COPY_レコード長,マルチレイアウト判定,REDIFINE_有無,X項目のみ,レイアウト行数,ALL_chk_ok
  
        # if ALL_chk_ok == False:
        #     l_err = "エラー有"
        # else:
        #     l_err = ""
        if COPY_レコード長 == "":
            COPY_レコード長 = 0
            
        key_list = ["レイアウト名","レコード名","レコード長","マルチレイアウト判定","REDIFINE有無","X項目のみ","レイアウト行数","エラー情報"]
        value_list = [レイアウト名,COPY_レコード名,COPY_レコード長,マルチレイアウト判定,REDIFINE_有無,X項目のみ,レイアウト行数,err_info]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        
class レイアウト解析情報:
    def __init__(self,conn,cursor):
        self.dic = {}
        self.conn = conn
        self.cursor = cursor
        self.dbname = "レイアウト解析情報"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self,layout_string):
        if self.dic == None:
            self.setup()
            
        global レイアウト名

        key_list = ["レイアウト名","レイアウト情報"]
        value_list = [レイアウト名,layout_string]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        
def 検索行文字列生成処理(TokenSheet_str):
    
    TokenSheet_str = [str(s) for s in TokenSheet_str]
    検索行文字列 = " ".join(TokenSheet_str)
     
    return DB文字(検索行文字列)

def 設定値一致色分け処理_COPY(parm_val,code_val,code_val2):

    global COPY_変数,COPY_レコード名,REDIFINE_判定_レベル,OCCOURS_判定_レベル,OCCOURS_回数,OCCOURS_バイトカウント,COPY_タイプ2,X項目のみ,COPY_サイン,N項目有無,\
            COPY_桁数,COPY_桁数_文字列,COPY_REDIFINE,REDIFINE_有無,マルチレイアウト判定,VALUE有無,COPY_レベル,COPY_タイプ,COPY_OCCURS
    
    parm_val = str(parm_val)
    code_val = str(code_val)
    code_val2 = str(code_val2)
    # '変数名
    if parm_val == "変数名":
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
       
        COPY_レベル = int(code_val)
        if IsNumeric(code_val) and int(code_val) == 1 and COPY_レコード名 == "":
            COPY_レコード名 = code_val2   # '次のトークンを先読み

# '       if 先頭レベル = "":
# '          先頭レベル = code_val
# '       
       
    #    'Redifine処理解除
        if COPY_レベル <= REDIFINE_判定_レベル:
            REDIFINE_判定_レベル = 0
    #    'OCCOURS_判定_レベル解除
        if COPY_レベル <= OCCOURS_判定_レベル:
    # '          COPY_レコード長 = COPY_レコード長 + OCCOURS_バイトカウント * OCCOURS_回数
    # '          COPY_相対位置 = COPY_相対位置 + OCCOURS_バイトカウント * OCCOURS_回数
            OCCOURS_判定_レベル = 0
            OCCOURS_回数 = 0
            OCCOURS_バイトカウント = 0
    # 'USAGE
    elif "USAGE" in parm_val: 
        COPY_タイプ2 = code_val
    
    
    # '予約後（上記条件以外）
    elif parm_val == code_val:
        pass

    # '変数セット処理

    if parm_val == "変数_タイプ①":
        
        
        if code_val == "." and code_val2 == "":
            return
        
        COPY_桁数 += len(code_val.replace("V","").replace("S","").replace("P",""))-1
        
        COPY_タイプ = code_val.replace("+","").replace("\\","").replace("-","").replace("V","")
        
        # if COPY_タイプ.replace("X", ""):
        #     X項目のみ = ""
        if COPY_タイプ.replace("X", "") != "" and COPY_タイプ.replace("9","") != "":
            X項目のみ = ""
        
        if "+" in code_val:
            COPY_サイン = "+"
            
        if "S" in COPY_タイプ:
            COPY_サイン = "S"
        
    # '↓追加　20150714　Takei
        if "N" in COPY_タイプ:
            N項目有無 = "●"
         
    elif parm_val == "変数_タイプ②":
        if code_val == "." and code_val2 == "":
            return
        
        COPY_桁数 += len(code_val.replace("V","").replace("S","").replace("P",""))-1
        
        if code_val2 == "(":
            pass
        else:
            if "9" not in code_val and "P" not in code_val:
                print("PIC定義の想定外パターン",code_val,"変数_タイプ②")
            COPY_桁数_文字列 = COPY_桁数_文字列 + " " + str(len(code_val.replace("V","").replace("+","").replace("-","")))
            COPY_桁数 += len(code_val.replace("V","").replace("P",""))
            
    elif parm_val == "変数_タイプ③":
        if code_val == "." and code_val2 == "":
            return
        
        COPY_桁数 += len(code_val.replace("V","").replace("S","").replace("P",""))-1
        if code_val2 == "(":
            pass
        else:
            if "9" not in code_val and "P" not in code_val:
                print("PIC定義の想定外パターン",code_val,"変数_タイプ②")
            COPY_桁数_文字列 = COPY_桁数_文字列 + " " + str(len(code_val.replace("V","").replace("+","").replace("-","")))
            COPY_桁数 += len(code_val.replace("V","").replace("P",""))

            
    elif parm_val == "桁数_数値":
        COPY_桁数 += int(code_val)
        COPY_桁数_文字列 = code_val
 
    elif parm_val == "小数桁数_数値":
        COPY_桁数 = COPY_桁数 + int(code_val)
        COPY_桁数_文字列 = COPY_桁数_文字列 + " " + code_val
    elif parm_val == "桁数補助_数値":
        COPY_桁数 += int(code_val)
        COPY_桁数_文字列 = COPY_桁数_文字列 + "," + code_val
    elif parm_val == "変数_REDEFINES":
        COPY_REDIFINE = code_val
        REDIFINE_判定_レベル = COPY_レベル
        REDIFINE_有無 = "●"
        マルチレイアウト判定 = ""
    elif parm_val == "OCCURS_数値":
            COPY_OCCURS = int(code_val)
            OCCOURS_判定_レベル = COPY_レベル
            OCCOURS_回数 = COPY_OCCURS
    elif parm_val == "変数_タイプ不定":
        # if str(code_val).startswith("\\"):
        #     code_val = code_val[1:]
        
        code_val = code_val.replace("V","").replace("P","")
        if "CR" in code_val or "DB" in code_val:
            code_val = code_val.replace("CR","").replace("DB","")
            COPY_桁数 += 1
            
        COPY_桁数 += len(code_val.replace("V", ""))
        COPY_桁数_文字列 = str(len(code_val.replace("V", "")))
    
        
        if "X" in code_val:
            COPY_タイプ = "X"
        elif "9" in code_val:
            COPY_タイプ = "9"
            
        elif "Z" in code_val or "0" in code_val or "P" in code_val or "*" in code_val:
            if COPY_タイプ == "":
                COPY_タイプ = "9"
                if "Z" in code_val:
                    COPY_サイン = "Z"
                elif "P" in code_val:
                    COPY_サイン = "P"
                elif "*" in code_val:
                    COPY_サイン = "*"
                elif "0" in code_val:
                    COPY_サイン = "0"

            else:
                pass
        elif "\\" in code_val:
            if COPY_タイプ == "":
                COPY_タイプ = "X"
                COPY_サイン = "\\"
        else:
            print("想定外のCOPY_タイプ",code_val)
            COPY_タイプ = code_val
            
    elif parm_val == "変数_タイプ不定2":

        # if str(code_val).startswith("\\"):
        #     code_val = code_val[1:]
        
        code_val = code_val.replace("V","").replace("P","")
        if "CR" in code_val or "DB" in code_val:
            code_val = code_val.replace("CR","").replace("DB","")
            COPY_桁数 += 1
            
        COPY_桁数 += len(code_val.replace("V", ""))
        COPY_桁数_文字列 += " " + str(len(code_val.replace("V", "")))
    # '↓追加　20140708　Takei
    elif parm_val == "補足タイプ":
        COPY_タイプ = COPY_タイプ + code_val.replace("V", "")  #'Pはどうするか決めていない
        COPY_桁数 = COPY_桁数 + len(code_val.replace("V", "").replace("P",""))
    # '↓追加　20150714　Takei
    elif parm_val == "VALUE":
        VALUE有無 = "●"
    else:
        pass

 
def 設定値USAGEチェック_COPY(parm_str):
    
    global バイナリ項目有無
    
    if parm_str =="BINARY":
        バイナリ項目有無 = "●"
        return True
    elif parm_str =="COMP":
        バイナリ項目有無 = "●"
        return True
    elif parm_str =="COMP-1":
        バイナリ項目有無 = "●"
        return True
    elif parm_str =="COMP-2":
        バイナリ項目有無 = "●"
        return True
    elif parm_str =="COMP-3":
        バイナリ項目有無 = "●"
        return True
    elif parm_str =="COMP-4":
        バイナリ項目有無 = "●"
        return True
    elif parm_str =="COMP-5":
        バイナリ項目有無 = "●"
        return True
    elif parm_str =="PACKED-DECIMAL":
        バイナリ項目有無 = "●"
        return True
    elif parm_str =="BIT":
        バイナリ項目有無 = "●"
        return True
    else:
        return False


def 設定値数値チェック_COPY(parm_str):
    if IsNumeric(parm_str):
        return  "数値"
    else:
        return "文字列"



def 設定値タイプチェック_COPY(parm_str):

    if "'" in parm_str:
       return "定数"
    else:
       return "変数"

def 設定値一致チェック(parm_val,code_val):
    
    global COPY_レベル
    
    parm_val,code_val = str(parm_val),str(code_val)    
    code_val = code_val.replace("PICTURE", "PIC")  #'PICTURE指定は強制的にPICに変換
    
    global MODE指定有無
    
    設定値タイプ = 設定値タイプチェック_COPY(code_val)
    
    # 'レベル
    if "レベル" in parm_val and \
        設定値数値チェック_COPY(code_val) == "数値" and COPY_レベル == 0:
        if int(code_val) < 50:                               #    'COPY句としてのレベルは1～49を想定
            return True
       
    # '変数
    if "変数" in parm_val and \
        設定値タイプ == "変数":
        return True
    # '定数
    elif "定数" in parm_val and \
        設定値タイプ == "定数":
        return True
    # '数値
    elif "数値" in parm_val and \
        設定値数値チェック_COPY(code_val) == "数値":
        return True
    # 'USAGE
    elif "USAGE" in parm_val and \
        設定値タイプ == "変数" and \
        設定値USAGEチェック_COPY(code_val) == True:
        return True
    # '変数不定
    elif parm_val == "変数_タイプ不定" and \
        code_val.replace("X", "").replace("9", "").replace("V", "") == "":
        return True
    # 'モードタイプ MODE-1,MODE-2,MODE-3,MODE-4.....
    elif parm_val == "モードタイプ":
        if code_val == "MODE-1" or code_val == "MODE-2" or code_val == "MODE-3" or code_val == "MODE-4":
            MODE指定有無 = "●"
            return True
            
    # '補足タイプ
    elif parm_val == "補足タイプ" and \
        code_val.replace("P", "").replace("9", "").replace("V", "").replace("+", "").replace("-", "") == "":
        return True
    # '変数_NotKeyWord [VALUE, CHARACTER, PRINTING]
    elif parm_val == "NotKeyWord":
        if code_val == "VALUE" or code_val == "CHARACTER" or code_val == "PRINTING":
            return False
        else:
            return True
    elif parm_val == code_val:
       return True
    else:
       return False


def 検索行文字列生成処理(TokenSheet_str):

    TokenSheet_str = [str(s) for s in TokenSheet_str]
    検索行文字列 = " ".join(TokenSheet_str)
     
    return DB文字(検索行文字列)


def バイナリ桁処理():
    global COPY_桁数,COPY_バイト数
    
    if COPY_桁数 <= 4:
       COPY_バイト数 = 2
    elif COPY_桁数 <= 9:
       COPY_バイト数 = 4
    else:                      # '10～18桁を想定
       COPY_バイト数 = 8
       
       
def バイト数加算_COPY():
    global COPY_タイプ2,COPY_バイト数,COPY_桁数,COPY_タイプ,OCCOURS_バイトカウント
    

    if COPY_タイプ2 == "BINARY":
        バイナリ桁処理()
    elif COPY_タイプ2 == "COMP":
        バイナリ桁処理()
    elif COPY_タイプ2 == "COMP-1":
        COPY_バイト数 = 4
    elif COPY_タイプ2 == "COMP-2":
        COPY_バイト数 = 8
    elif COPY_タイプ2 == "PACKED-DECIMAL":
        temp_num = (COPY_桁数 + 2) // 2
        COPY_バイト数 = temp_num
    elif COPY_タイプ2 == "COMP-3":
        temp_num = (COPY_桁数 + 2) // 2
        COPY_バイト数 = temp_num
        # 'RoundUp(temp_num, 0)
    elif COPY_タイプ2 == "COMP-4":
        バイナリ桁処理()
    elif COPY_タイプ2 == "COMP-5":
        バイナリ桁処理()
    elif COPY_タイプ2 == "BIT":
        temp_num = COPY_桁数 // 8
        COPY_バイト数 = temp_num
    else:
        if COPY_タイプ == "N":
            COPY_バイト数 = COPY_桁数 * 2
        elif COPY_タイプ == "G":
            COPY_バイト数 = COPY_桁数 * 2
        else:
            COPY_バイト数 = COPY_桁数   
       
    if REDIFINE_判定_レベル > 0:
        return 0
    else:
        if OCCOURS_判定_レベル > 0:
            OCCOURS_バイトカウント = OCCOURS_バイトカウント + COPY_バイト数
            return 0
        else:
            return COPY_バイト数

def MC文字列明細(m_sigh,m_type,m_type2,m_byte): #ＭＣ＝マルチレイアウトチェック

    m_type = str(m_type).replace("S", "").replace("V", "")
    m_type2 = str(m_type2)
    
    if "X" in m_type:
       r_str = "X"
    elif "A" in m_type:
        r_str = "X"
    elif "N" in m_type or "G" in m_type:
       r_str = "N"
    elif "9" in m_type:
        if m_type2 == "COMP":
            r_str = "B"
        elif m_type2 == "COMP-1":
            r_str = "?"
        elif m_type2 == "COMP-2":
            r_str = "?"
        elif m_type2 == "COMP-3":
            r_str = "P"
        elif m_type2 == "COMP-4":
            r_str = "B"
        elif m_type2 == "COMP-5":
            r_str = "B"
        elif m_type2 == "PACKED-DECIMAL":
            r_str = "P"
        elif m_type2 == "BINARY":
            r_str = "B"
        elif m_type2 == "":
            if m_sigh == "S":
                r_str = "Z"
            else:
                r_str = "9"
        else:
            r_str = "?"
            
    elif "1" in m_type:
        r_str = "B"             #    '暫定対応（要確認）
    else:
        r_str = "?"
        MSG = "想定外の内容"
        # print(MSG,"MC文字列詳細",m_type,m_sigh)
    
    global X項目のみ
    if r_str != "X" and r_str != "9":
        X項目のみ = ""
        
    return r_str*int(m_byte)
    
    
def 共通_マルチレイアウト判定(P_STR):

    if  " " in P_STR:
       return False
    elif "?" in P_STR:
       return True
    elif P_STR == "XX":
       return False
    elif P_STR == "99":
       return False
    elif P_STR == "ZZ":
       return False
    elif P_STR == "BB":
       return False
    elif P_STR == "PP":
       return False
    elif P_STR == "NN":
       return False
    elif P_STR == "X9" or P_STR == "9X":
       return False
    elif P_STR == "XZ" or P_STR == "ZX":
       return True
    elif P_STR == "XB" or P_STR == "BX":
       return True
    elif P_STR == "XP" or P_STR == "PX":
       return True
    elif P_STR == "XN" or P_STR == "NX":
       return True
    elif P_STR == "9Z" or P_STR == "Z9":
       return True
    elif P_STR == "9B" or P_STR == "B9":
       return True
    elif P_STR == "9P" or P_STR == "P9":
       return True
    elif P_STR == "9N" or P_STR == "N9":
       return True
    elif P_STR == "ZB" or P_STR == "BZ":
       return True
    elif P_STR == "ZP" or P_STR == "PZ":
       return True
    elif P_STR == "ZN" or P_STR == "NZ":
       return True
    elif P_STR == "BP" or P_STR == "PB":   # 'マルチレイアウトではない
       return False
    elif P_STR == "PN" or P_STR == "NP":
       return True
    else:
       return True

def G項目バイト数計算処理(AnalyzeSheet):
    
    global byte_each_rows,occurs_each_rows,group_end_each_rows
    global g0byte_flag
    
    row_num = len(AnalyzeSheet)
    byte_each_rows = [0]*row_num
    occurs_each_rows = [1]*row_num
    group_end_each_rows = [row_num]*row_num
    
    row_data_queue = []
    
    now_occurs = 1
    for i in range(row_num):
        level = int(AnalyzeSheet[i][3])
        byte = int(AnalyzeSheet[i][10])
        occurs = int(AnalyzeSheet[i][12])
        
        occurs = max(occurs,1)
        
        while row_data_queue and level <= row_data_queue[-1][0]:
            b_level,b_occurs,b_index = row_data_queue.pop()
            group_end_each_rows[b_index] = i
            now_occurs //= b_occurs
        now_occurs *= occurs
        occurs_each_rows[i] = now_occurs
        byte_each_rows[i] = now_occurs * byte
        row_data_queue.append([level,occurs,i])
            

    child_group = [[] for i in range(row_num)]
    
    row_levels = [[] for i in range(100)]
    for i in range(row_num):
        row_levels[AnalyzeSheet[i][3]].append(i)
        
    level_queue = []
    for i in range(row_num)[::-1]:
  
        
        level = AnalyzeSheet[i][3]
        while level_queue and level_queue[-1][0] > level:
            b_level,b_index = level_queue.pop()
            child_group[i].append(b_index)
        
        if AnalyzeSheet[i][11] != "":
            continue
        level_queue.append([level,i])
    
    
    layout_chk_string_list = [0]*row_num
    layout_chk_string_list_bef_occurs = [0]*row_num
    for i in range(100)[::-1]:
        for index in row_levels[i]:
            tmp_str = 0
            if AnalyzeSheet[index][9] == "":
                tmp_str += int(AnalyzeSheet[index][10])
            for child_index in child_group[index]:
                tmp_str += layout_chk_string_list[child_index]
            layout_chk_string_list_bef_occurs[index] = tmp_str
            if AnalyzeSheet[index][12] > 0:
                tmp_str *= AnalyzeSheet[index][12]
            layout_chk_string_list[index] = tmp_str
        
    
    for i in range(row_num):
        if group_end_each_rows[i] != i+1:
            AnalyzeSheet[i][9] = layout_chk_string_list_bef_occurs[i]
        
        if AnalyzeSheet[i][9] == "" and int(AnalyzeSheet[i][10]) == 0:
            g0byte_flag = True
            
   
       
        
    
    return AnalyzeSheet
    
    
    
def 明細行相対位置解析処理(AnalyzeSheet):
    global byte_each_rows,occurs_each_rows,group_end_each_rows
    global ALL_chk_ok,redefine_flg
    position = 1
    now_occurs = 1
    size_val_dic = {}
    left_byte_size = [0]
    row_num = len(AnalyzeSheet)
    
    occurs_que = []
    for i in range(row_num):
        occurs = occurs_each_rows[i]
        size = AnalyzeSheet[i][10]
        level = int(AnalyzeSheet[i][3])
        def_occurs = int(AnalyzeSheet[i][12])
        val = AnalyzeSheet[i][11]
        # print(i,level,size,def_occurs,val,position,left_byte_size,occurs_que)
        # print(occurs_que)
        while occurs_que and occurs_que[-1][0] >= level:
            blevel,mul = occurs_que.pop()
            last_size = left_byte_size.pop()
            position += last_size * (mul - 1) 
            left_byte_size[-1] += last_size * mul  
        # print(left_byte_size,occurs_que)
        if def_occurs > 1:
            left_byte_size.append(0)
            occurs_que.append([level,def_occurs])
        # elif now_occurs > occurs:
        #     mul = now_occurs // occurs
        #     last_size = left_byte_size.pop()
        #     position += last_size * (mul - 1)
        #     left_byte_size[-1] += last_size * (mul - 1)
        
        if val != "":
            if val not in size_val_dic:
                
                ALL_chk_ok = False
                redefine_flg = True
                print("REDEFINE変数",val,"は存在しません")
            else:
                
                mul = occurs //occurs_each_rows[i] 
                # print(val,size_val_dic[val],mul)
                bsize,bposition = size_val_dic[val]
                position -= bsize * mul
                left_byte_size[-1] -= bsize * mul
                less = bposition - position
                if less > 0:
                    # print(less,"サイズ不足分")
                    position += less
                    left_byte_size[-1] += less
                elif less < 0:
                    print("REDEFINEサイズ不正")
                    redefine_flg = True
                    ALL_chk_ok = False
                 
        AnalyzeSheet[i][13] = position
        if AnalyzeSheet[i][9] != "":
            size_val_dic[AnalyzeSheet[i][4]] = [AnalyzeSheet[i][9],position]
        else:
            size_val_dic[AnalyzeSheet[i][4]] = [AnalyzeSheet[i][10],position]
        position += size
        left_byte_size[-1] += size
        
        # size_val_dic[AnalyzeSheet[i][4]] = [AnalyzeSheet[i][10]
        
            
            
        now_occurs = occurs
            
    return AnalyzeSheet
            
    
def 単独マルチレイアウト判定(AnalyzeSheet,multicheck_folder):
    
    global ALL_chk_ok,マルチレイアウト判定
    global レイアウト解析情報_
    global レイアウト名
    
    row_num = len(AnalyzeSheet)
    child_group = [[] for i in range(row_num)]
    
    row_levels = [[] for i in range(100)]
    for i in range(row_num):
        row_levels[AnalyzeSheet[i][3]].append(i)
        
    level_queue = []
    for i in range(row_num)[::-1]:
  
        
        level = AnalyzeSheet[i][3]
        while level_queue and level_queue[-1][0] > level:
            b_level,b_index = level_queue.pop()
            child_group[i].append(b_index)
        
        if AnalyzeSheet[i][11] != "":
            continue
        level_queue.append([level,i])
    
    
    layout_chk_string_list = [""]*row_num
    layout_chk_string_list_bef_occurs = [""]*row_num
    for i in range(100)[::-1]:
        for index in row_levels[i]:
            tmp_str = ""
            if AnalyzeSheet[index][9] == "":
                tmp_str += MC文字列明細(AnalyzeSheet[index][5],AnalyzeSheet[index][6],AnalyzeSheet[index][7],AnalyzeSheet[index][10])
            for child_index in child_group[index]:
                tmp_str += layout_chk_string_list[child_index]
            layout_chk_string_list_bef_occurs[index] = tmp_str
            if AnalyzeSheet[index][12] > 0:
                tmp_str *= AnalyzeSheet[index][12]
            layout_chk_string_list[index] = tmp_str
            
    
    if len(layout_chk_string_list_bef_occurs[0]) != AnalyzeSheet[0][9] and len(layout_chk_string_list_bef_occurs[0]) != int(AnalyzeSheet[0][10]) :
        ALL_chk_ok = False  
        return
    
    redefine_flag = 0
    chk_str1 = layout_chk_string_list[0]
    
    multicheck_list = []
    if multicheck_folder != None:
        multicheck_list.append(chk_str1)
    for i in range(row_num):
        if AnalyzeSheet[i][11] == "":
            continue
        redefine_flag = 1
        pos_start = AnalyzeSheet[i][13]-1
        chk_str2 = layout_chk_string_list_bef_occurs[i]
        # print(AnalyzeSheet[i][4])
        # print(chk_str2)
        # print(pos_start)
        if len(chk_str2)+pos_start > len(chk_str1) or pos_start < 0:
            ALL_chk_ok = False
            # print(pos_start,len(chk_str1),len(chk_str2),chk_str1,chk_str2)
            # print("レコード長が不足しています。scmファイルを確認してください。",レイアウト名)
            continue
        
        if multicheck_folder != None:
            chk_str2_full = " "*pos_start + chk_str2 + " " * (len(chk_str1) - len(chk_str2) - pos_start)
            multicheck_list.append(chk_str2_full)
        for j in range(len(chk_str2)):
            try:
                if 共通_マルチレイアウト判定(chk_str1[pos_start+j]+chk_str2[j]) == True:
                    マルチレイアウト判定 = "YES"
            except:
                print(pos_start)
                print(chk_str2)
                print(chk_str1)
                # exit()
      
    レイアウト解析情報_.insert(layout_chk_string_list[0])
    if マルチレイアウト判定 != "YES" and redefine_flag:
        マルチレイアウト判定 = "NO"    
    
    if multicheck_folder != None and redefine_flag:
        multicheck_out_path = os.path.join(multicheck_folder,レイアウト名 + "_単体CHK.txt")
        with open(multicheck_out_path,"w") as f:
            for line in multicheck_list:
                f.write(line + "\n")
    
    return 


# def check_PIC_definition(TokenSheet2_GYO,検索列):
#     検索列 += 1
#     if 検索列 >= len(TokenSheet2_GYO):
#         print("PIC定義が正しくありません。スキーマファイルを確認してください。")
#         return 検索列
    
#     global X項目のみ,COPY_バイト数,COPY_タイプ,COPY_サイン,COPY_桁数
    
#     while 検索列 < len(TokenSheet2_GYO):
#         code_val = TokenSheet2_GYO[検索列]
        
#         ### 順番を考慮 or どれか一つが当てはまるとすべきかも
#         if str(code_val).startswith("V"):
#             code_val = code_val[1:] # V はレコード長などには関係しない
        
#         if str(code_val).startswith("."):
#             code_val = code_val[1:]
            
#         if str(code_val).startswith("B"):
#             code_val = code_val[1:]
            
#         #################################
        
#         if 検索列 + 1 < len(TokenSheet2_GYO) and TokenSheet2_GYO[検索列 + 1] == "(":
#             code_val = str(code_val).replace("+","").replace("-","").replace("\\","")  ### ( ) が続く定義のこれらの記号はレコード長などには関係しない
            
#             if code_val not in ("X","A","9","S9"):
#                 print("想定外のPIC定義",code_val)
#                 print(TokenSheet2_GYO)
                
#             if code_val != "X":
#                 X項目のみ = ""
                
#         else:
            
        
        
        
#         # if code_val in ("USAGE","REDEFINES","RENAMES","OCCURS")
        


    

def structure_Scm(TokenSheet2,ScmSheet,レイアウト, ログ解析有 = True,conn=None, cursor=None,レイアウト_len=0,multicheck_folder=None):

    global COPY_変数,COPY_レコード名,REDIFINE_判定_レベル,OCCOURS_判定_レベル,OCCOURS_回数,OCCOURS_バイトカウント,COPY_タイプ2,X項目のみ,COPY_サイン,N項目有無,\
            COPY_桁数,COPY_桁数_文字列,COPY_REDIFINE,REDIFINE_有無,マルチレイアウト判定,VALUE有無,COPY_ライブラリ,先頭レベル,COPY句分類 ,COPY_タイプ,COPY_レベル,COPY_バイト数,COPY_OCCURS,ALL_chk_ok
    
    global レイアウト名,COPY_レコード長,レイアウト行数
    global レイアウト解析情報_
    global depending_on_flag,indexed_by_flag,g0byte_flag,redefine_flg
    
    
    err_info = ""
    depending_on_flag = False
    indexed_by_flag = False
    g0byte_flag = False
    redefine_flg = False
    レイアウト名 = レイアウト
    レイアウト行数 = レイアウト_len
    SUB_SQL生成_共通_1_ = SUB_SQL生成_共通_1(conn,cursor)
    SUB_SQL生成_共通_2_ = SUB_SQL生成_共通_2(conn,cursor)
    スキーマ_基本情報_ = スキーマ_基本情報(conn,cursor)
    レイアウト解析情報_ = レイアウト解析情報(conn,cursor)
    
    ALL_chk_ok = True    #'シート単位で全ての設定パターンが登録されているかどうか（初期値True）
    REDIFINE_有無 = ""
    マルチレイアウト判定 = ""
    X項目のみ = "●"
    N項目有無 = ""
    バイナリ項目有無 = ""   #'廃止（20140527）
    
    # '変数初期化
    # 'COPY句 = Replace(レイアウト名, ".scm", "") '拡張子に合わせて設定
    COPY句 = レイアウト名
    COPY_ライブラリ = ""
    COPY_レコード名 = ""
    COPY_レコード長 = 0
    
    REDIFINE_判定_レベル = 0
    OCCOURS_判定_レベル = 0
    
    OCCOURS_回数 = 0
    OCCOURS_バイトカウント = 0
    先頭レベル = ""
    # 'COPY_相対位置 = 1       '↓の計算処理で設定する

    検索行 = 0    #  'TokenSheet2　行ポインタ
    # '分析行TYPE = "COBOL"  '「COBOL」「PL/I」など
    COPY句分類 = "copy-data" #'デフォルト値
   
    AnalyzeSheet = []
    
    while 検索行 < len(TokenSheet2):

        TokenSheet2_GYO = TokenSheet2[検索行]
        if "DEPENDING" in TokenSheet2_GYO:
            depending_on_flag = True
            
        if "INDEXED" in TokenSheet2_GYO:
            indexed_by_flag = True
            
            
        # '変数初期化
        COPY_対象行 = 検索行
        COPY_レベル = 0
        COPY_変数 = ""
        COPY_サイン = ""
        COPY_タイプ = ""
        COPY_タイプ2 = ""
        COPY_桁数 = 0
        COPY_桁数_文字列 = "" #'追加
        COPY_バイト数 = 0
        COPY_REDIFINE = ""
        COPY_OCCURS = 0
        
        # '20150714 ADD
        バイナリ項目有無 = "" #'20140527廃止 →　201507復活（集団項目に設定、配下にBINARY、PAC項目があるか）
        N項目有無 = "" #'201507追加（集団項目に設定、配下にN項目があるか）
        VALUE有無 = "" #'201507追加（基本項目に設定、VALUE句があるか）
        MODE指定有無 = "" #'201507追加（基本・集団項目に設定、富士通COBOLのmode指定の影響を受けている項目に設定）
        # '20150714 ADD END
        
        検索列 = 1
        
        while True:
            PARM行 = 0      #'Parm行ポインタ
            parm_hit = False
            
            # if 検索列 < len(TokenSheet2_GYO) and TokenSheet2_GYO[検索列] == "PIC":
            #     検索列 = check_PIC_definition(TokenSheet2_GYO,検索列)
                
            #     if 検索列 >= len(TokenSheet2_GYO):
            #         break
                
            while True:
                
                PARM列 = 4     # 'Parm列ポインタ
                hit_flg = True
                parm_cnt = 0
                here = 0
                while PARM列 < len(ScmSheet[PARM行]):
                    
                    if ScmSheet[PARM行][1] == "Key101":
                        if 検索列 >= len(TokenSheet2_GYO):
                            hit_flg = False
                            break
                        code_val = TokenSheet2_GYO[検索列].replace("V","").replace("9","").replace("S","").replace("Z","").replace("P","").replace(",","").replace("*","").replace(".","").replace("\\","").replace("A","").replace("B","").replace("X","").replace("0","") 
                        if code_val != "" or TokenSheet2_GYO[検索列] == ".":
                            hit_flg = False
                            break
                        
                        if 検索列 == 1 or TokenSheet2_GYO[検索列-1] != ")":
                            hit_flg = False
                            break
                        
                        here = 1
                        
                
                        
                    if ScmSheet[PARM行][PARM列] != "":
                        parm_cnt = parm_cnt + 1
                    
                    parm_val = ScmSheet[PARM行][PARM列]
                    code_val = ""
                    if 検索列+parm_cnt-1 < len(TokenSheet2_GYO):
                        code_val = TokenSheet2_GYO[検索列+parm_cnt-1]
                        
                    parm_chk = 設定値一致チェック(parm_val,code_val)
                    if not (parm_chk):
                        hit_flg = False
                    PARM列 = PARM列 + 1
                    
                    if PARM列 >= len(ScmSheet[PARM行]) or ScmSheet[PARM行][PARM列] == "" or hit_flg == False:
                        break
            
                # 'チェック結果
                if hit_flg:
                    parm_hit = True
                    分析ID = ScmSheet[PARM行][2]
                
                    if ログ解析有 and 分析ID != "":
                        検索行文字列 = 検索行文字列生成処理(TokenSheet2_GYO[1:])  #  '処理開始列（2列目を引数にする）
                        SUB_SQL生成_共通_1_.insert("分析ID", "", レイアウト名, 検索行+2, 分析ID, 検索行文字列)
                
                else:
                    PARM行 = PARM行 + 1
                
                if PARM行 >= len(ScmSheet) or ScmSheet[PARM行][1] == "" or parm_hit == True:
                    break
            # '検索列更新
            if parm_hit:
                # 'PARM列 = 6
                PARM列 = 4
                # print(TokenSheet2_GYO)
                # print(ScmSheet[PARM行])
                for i in range(parm_cnt):
                    parm_val = ""
                    if PARM列 + i < len(ScmSheet[PARM行]):
                        parm_val = ScmSheet[PARM行][PARM列 + i]
                    code_val = ""
                    if 検索列+i < len(TokenSheet2_GYO):
                        code_val = TokenSheet2_GYO[検索列+i]
                        
                    code_val2 = ""
                    if 検索列+i+1 < len(TokenSheet2_GYO):
                        code_val2 = TokenSheet2_GYO[検索列+i+1]
                        
                    設定値一致色分け処理_COPY(parm_val,code_val,code_val2)
                
                検索列 = 検索列 + parm_cnt
            else:
                # '判定NG処理
                ALL_chk_ok = False         # 'ひとつでもNGがあるとシート単位でNG
         
                COPY句分類 = "copy-source"
            
                if ログ解析有:
                    # '検索行文字列作成
                    検索行文字列 = 検索行文字列生成処理(TokenSheet2_GYO[1:])   # '処理開始列（2列目を引数にする）
                    # 'NG時関連情報出力
                    SUB_SQL生成_共通_2_.insert("COPY", "", COPY句, 検索行+2, 検索行文字列)
                                

                検索列 = 検索列 + 1
            
            if 検索列 >= len(TokenSheet2_GYO):
                break
        
        # 'バイト数
        
        COPY_レコード長 = COPY_レコード長 + バイト数加算_COPY()
        
        AnalyzeSheet_GYO = [""]*18
        
        AnalyzeSheet_GYO[1] = COPY句
        AnalyzeSheet_GYO[2] = COPY_対象行
        AnalyzeSheet_GYO[3] = COPY_レベル
        AnalyzeSheet_GYO[4] = COPY_変数
        AnalyzeSheet_GYO[5] = COPY_サイン
        AnalyzeSheet_GYO[6] = COPY_タイプ
        AnalyzeSheet_GYO[7] = COPY_タイプ2
        AnalyzeSheet_GYO[8] = COPY_桁数_文字列
        AnalyzeSheet_GYO[10] = COPY_バイト数
        AnalyzeSheet_GYO[11] = COPY_REDIFINE
        AnalyzeSheet_GYO[12] = COPY_OCCURS
        # AnalyzeSheet_GYO[13] = COPY_相対位置  '↓の再解析処理内で計算・出力

        AnalyzeSheet_GYO[14] = バイナリ項目有無
        AnalyzeSheet_GYO[15] = N項目有無
        AnalyzeSheet_GYO[16] = VALUE有無
        AnalyzeSheet_GYO[17] = MODE指定有無
        AnalyzeSheet.append(AnalyzeSheet_GYO)
        
        検索行 = 検索行 + 1
       
        # 'debug
        # 'if 検索行 = 4:
        # '    検索行 = 4
    
    err_before = False
    if ALL_chk_ok == False:
        err_before = True
        
    AnalyzeSheet = G項目バイト数計算処理(AnalyzeSheet)
    AnalyzeSheet = 明細行相対位置解析処理(AnalyzeSheet)
    
    # if REDIFINE_有無 == "●":
    単独マルチレイアウト判定(AnalyzeSheet,multicheck_folder)
    
    COPY_レコード長 = AnalyzeSheet[0][9]
    if COPY_レコード長 == "":
        COPY_レコード長 = AnalyzeSheet[0][10]
        
    if err_before:
        err_info = "エラー: 文法パターン対象外"
    else:
        err_info = ""
    if depending_on_flag:
        if err_info == "":
            err_info = "エラー: DEPENDING ON 使用"
        else:
            err_info += ", DEPENDING ON 使用"
    
    if indexed_by_flag:
        if err_info == "":
            err_info = "エラー: INDEXED BY 使用"
        else:
            err_info += ", INDEXED BY 使用"
            
    if g0byte_flag:
        if err_info == "":
            err_info = "エラー: 0byteのG項目あり"
        else:
            err_info += ", 0byteのG項目あり"
    
    if redefine_flg:
        if err_info == "":
            err_info = "エラー: REDEFINE句 定義なし or サイズ不正"
        else:
            err_info += ",  REDEFINE句 定義なし or サイズ不正"
            
        
    スキーマ_基本情報_.insert(err_info)
    
    return AnalyzeSheet
    