#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
# sys.path.append(os.path.dirname(__file__))
import pandas as pd
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


DB自動登録時PARM = "自動設定（JFE_DB特定）" 
関連資産 = ""
JFE_データ分類 = ""
JFE_レコード関連引数位置 = 0
JFE_CRUD判定 = ""
JFE_IO判定 = ""
分割文字列 = []
JFE_DATA関連PGM判定_ = None

ActSheet = []
ActSheet_x = []

output_header = ["資産ID","COBOL_ID","調査対象PGM名","処理データ分類","元資産行情報","PARM_ALL",\
                "処理レコード①","処理レコード②","処理レコード③","処理レコード④","処理レコード⑤","パラメータ","CRUD判定","IO判定",\
                "関連DSN","関連性設定","PGM-IO","JCL_PGM_DSN","関連PGM（親含む）","補足","JSI用XDBREF"
]

class JFE_DATA関連PGM判定:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "【暫定】JFE_DATA関連PGM設定"
        # self.db_path = db_path

    def setup(self):
        
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        
        for module,data,record,crud,io in zip(df["関連モジュール"],df["データ分類"],df["レコード関連引数位置"],df["CRUD判定"],df["IO判定"]):
            self.dic[module] = [data,record,crud,io]
            
        
    def get(self):
        global 関連資産
        global JFE_データ分類,JFE_レコード関連引数位置,JFE_CRUD判定,JFE_IO判定
        
        if self.dic == None:
            self.setup()
            
        関連資産 = 関連資産.replace("\"","")
        
        if 関連資産 in self.dic:
            JFE_データ分類,JFE_レコード関連引数位置,JFE_CRUD判定,JFE_IO判定 = self.dic[関連資産]
            return True
        
        else:
            return False
   
   
def reformat_record(record):
    
#'20240209 UPD qian.e.wang
    #record = str(record)
    record = str(record).replace("\"","")
#'UPD END
    
    if "-" not in record:
        return record
    
    split_record = record.split("-")
    m = max([len(rec) for rec in split_record])
    if m < 4:
        return record
    
    for rec in split_record:
        if len(rec) == m:
            return rec
        
   
def NDB判定(P_PARM,ActSheet_x):     
    global 分割文字列,JFE_レコード関連引数位置
    if len(分割文字列) > 7:
        ActSheet_x[7] = reformat_record(分割文字列[JFE_レコード関連引数位置])
    ActSheet_x[12] = P_PARM

    if "MODIFY" in P_PARM:
        ActSheet_x[13] = "U"
        ActSheet_x[14] = "I-O"
    elif "STORE" in P_PARM or "STR" in P_PARM:
        ActSheet_x[13] = "C"
        ActSheet_x[14] = "I-O"
    elif "ERASE" in P_PARM or "ERS" in P_PARM:
        ActSheet_x[13] = "D"
        ActSheet_x[14] = "I-O"
    elif "GET" in P_PARM or "FIND" in P_PARM:
        ActSheet_x[13] = "R"
        ActSheet_x[14] = "INPUT"
    elif "CON" in P_PARM or "DCN" in P_PARM or "TEST" in P_PARM:
        ActSheet_x[13] = "NA"
        ActSheet_x[14] = "NA"
    return ActSheet_x
    
def ACSAPI判定(P_PARM, ActSheet_x):
    global 分割文字列

    if len(分割文字列) > 3:
        ActSheet_x[12] = 分割文字列[3]

    if  " DSREAD " in P_PARM:
        ActSheet_x[13] = "R"
        ActSheet_x[14] = "INPUT"
    elif  " DSWRITE " in P_PARM:
        ActSheet_x[13] = "C"
        ActSheet_x[14] = "I-O"
    elif  " DSFREE " in P_PARM:
        ActSheet_x[13] = "NA"
        ActSheet_x[14] = "NA"
        
    return ActSheet_x    


### VBAでは行番号を増やしていたが、代わりにnActSheet_x に行番号を増やした後の情報を入力して ActSheet_x は全体に追加して、nActSheet_xを新しい ActSheet_xとする
### ActSheet.Cells(x, が nActSheet_x
### ActSheet.Cells(x - 1, がActSheet_x のような関係
def XDBREF判定(ActSheet_x):
    global ActSheet,分割文字列
    
    if len(分割文字列) > 6:
       if 分割文字列[6] != ".":
            ActSheet_x[7] = reformat_record(分割文字列[6])
            ActSheet_x[13] = "R"
            ActSheet_x[14] = "INPUT"
            ActSheet_x[21] = 分割文字列[5]
    
    
    if len(分割文字列) > 7:
       if 分割文字列[7] != ".":
            nActSheet_x = [""]*22
            for i in range(1,7):
                nActSheet_x[i] = ActSheet_x[i]
            
            nActSheet_x[7] = reformat_record(分割文字列[7])
            nActSheet_x[13] = "R"
            nActSheet_x[14] = "INPUT"
            ActSheet.append(ActSheet_x)
            ActSheet_x = nActSheet_x
    
    if len(分割文字列) > 8:
       if 分割文字列[8] != ".":            
            nActSheet_x = [""]*22
            for i in range(1,7):
                nActSheet_x[i] = ActSheet_x[i]
            
            nActSheet_x[7] = reformat_record(分割文字列[8])
            nActSheet_x[13] = "R"
            nActSheet_x[14] = "INPUT"
            ActSheet.append(ActSheet_x)
            ActSheet_x = nActSheet_x

    if len(分割文字列) > 9:
       if 分割文字列[9] != ".":
            nActSheet_x = [""]*22
            for i in range(1,7):
                nActSheet_x[i] = ActSheet_x[i]
            
            nActSheet_x[7] = reformat_record(分割文字列[9])
            nActSheet_x[13] = "R"
            nActSheet_x[14] = "INPUT"
            ActSheet.append(ActSheet_x)
            ActSheet_x = nActSheet_x

    if len(分割文字列) > 10:
       if 分割文字列[10] != ".":
            nActSheet_x = [""]*22
            for i in range(1,7):
                nActSheet_x[i] = ActSheet_x[i]
            
            nActSheet_x[7] = reformat_record(分割文字列[10])
            nActSheet_x[13] = "R"
            nActSheet_x[14] = "INPUT"
            ActSheet.append(ActSheet_x)
            ActSheet_x = nActSheet_x
    
    return ActSheet_x    
    
    
    
def COBOL_CALL命令解析(data):
    
    global JFE_DATA関連PGM判定_
    global 関連資産,JFE_データ分類,JFE_レコード関連引数位置,JFE_CRUD判定,JFE_IO判定
    global 資産ID,COBOL_ID,元資産行情報,PARM_CMD
    global 分割文字列
    global ActSheet_x
    
    ActSheet_x = [""]*22
    資産ID = data["資産ID"]
    COBOL_ID = data["COBOL_ID"]
    元資産行情報 = data["元資産行情報"]
    PARM_CMD = data["PARM"]
    
    分割文字列 = ArrayEmptyDelete(PARM_CMD.split(" "))     ###若干であるが区切り文字がスペース1つでない場合がある

    ActSheet_x[1] = 資産ID
    ActSheet_x[2] = COBOL_ID
    ActSheet_x[5] = 元資産行情報
    ActSheet_x[6] = PARM_CMD
    
    if len(分割文字列) > 1: ###解析結果が「.」のみの場合があるので対象外とする
        関連資産 = 分割文字列[1]
        if  "\"" not in 関連資産:
            ActSheet_x[3] = "対象外(変数)"
        elif JFE_DATA関連PGM判定_.get() == False:
            ActSheet_x[3] = "対象外"
        else:
            ActSheet_x[3] = 関連資産
            ActSheet_x[4] = JFE_データ分類
    
            ###DAMIR一般
            if JFE_データ分類 == "DAM" and 関連資産 == "XXDAMDL":
    
                if len(分割文字列) > 6:
                    if 分割文字列[6] != ".":
                        ActSheet_x[7] = reformat_record(分割文字列[6])
                    else:
                        ActSheet_x[7] = "要再調査"
                else:
                    ActSheet_x[7] = "要再調査"
                    
                ActSheet_x[13] = JFE_CRUD判定
                ActSheet_x[14] = JFE_IO判定

    
            ###DAMIRトラッキング
            elif JFE_データ分類 == "DAM" and 関連資産 in ("XXTFRD","XXTFDL","XXTFAD","XXTFMDF","XXTFMV"):
        
                if len(分割文字列) > 7:
                    ActSheet_x[7] = reformat_record(分割文字列[6])
                    if 分割文字列[7] != ".":
                        ActSheet_x[8] = reformat_record(分割文字列[7])
                elif len(分割文字列) > 6:
                    if 分割文字列[6] != ".":
                        ActSheet_x[7] = reformat_record(分割文字列[6])
                    else:
                        ActSheet_x[7] = "要再調査"
                else:
                    ActSheet_x[7] = "要再調査"
                ActSheet_x[13] = JFE_CRUD判定
                ActSheet_x[14] = JFE_IO判定

    
            elif JFE_データ分類 == "NDB" and 関連資産 == "XDBMCR":
                if len(分割文字列) > 5:
                    JFE_NDB_PARM = 分割文字列[5]
                    ActSheet_x = NDB判定(JFE_NDB_PARM,ActSheet_x)
                
            elif JFE_データ分類 == "NDB" and 関連資産 == "XDBREF":
            
                ActSheet_x = XDBREF判定(ActSheet_x)
                
                ###行カウントアップは行わない「XDBREF判定」内で実施
        
            elif JFE_データ分類 == "独自DAM" and 関連資産 == "ACSAPI":
        
                JFE_ACSAPI_PARM = PARM_CMD
                ActSheet_x = ACSAPI判定(JFE_ACSAPI_PARM,ActSheet_x)
        
            ####素材系列一般 独自DAM
            elif JFE_データ分類 == "独自DAM" and 関連資産 in ("SXDAMRD","SXDAMWT","SXDAMAD","SXDAMDL","SXDAMKSR","SXDAMCAD","SXDAMCDL","SXDAMACT"):
        
                if len(分割文字列) > 5:
                    ActSheet_x[7] = reformat_record(分割文字列[3])
                    ActSheet_x[8] = reformat_record(分割文字列[5])
                ActSheet_x[13] = JFE_CRUD判定
                ActSheet_x[14] = JFE_IO判定

    
    
            elif JFE_データ分類 == "独自DAM" and 関連資産 in ("XEDAERD","XEDAEWT","XEDARLX","XEDAOPN","XEDACLS","XEDCB","XODAOPN","XODACLS"):
                        
                ActSheet_x[7] = "調査保留"   ###調査可能か現時点では不明
                ActSheet_x[13] = JFE_CRUD判定
                ActSheet_x[14] = JFE_IO判定
    
            
            elif JFE_データ分類 == "独自DAM" and 関連資産 in ("XPDARED","XPDAWRT","XPDAOPN","XPDACLS","XPDAFRE"):
                        
                ActSheet_x[7] = "調査保留"   ###調査可能か現時点では不明
                ActSheet_x[13] = JFE_CRUD判定
                ActSheet_x[14] = JFE_IO判定
                        

            
            ###棒線系列一般 独自DAM
            elif JFE_データ分類 == "独自DAM" and 関連資産 == "RXDAMDL":
                        
                if len(分割文字列) > 6:
                    if 分割文字列[6] != ".":
                        ActSheet_x[7] = reformat_record(分割文字列[6])
                    else:
                        ActSheet_x[7] = "要再調査"
                else:
                    ActSheet_x[7] = "要再調査"
                ActSheet_x[13] = JFE_CRUD判定
                ActSheet_x[14] = JFE_IO判定

                        
            ###棒線系列一般 独自DAM
            elif JFE_データ分類 == "独自DAM" and 関連資産 in ("RXTFRD","RXTFAD","RXTFDL","RXTFMDF","RXTFMV"):
        
                if len(分割文字列) > 7:
                    ActSheet_x[7] = reformat_record(分割文字列[6])
                    if 分割文字列[7] != ".":
                        ActSheet_x[8] = reformat_record(分割文字列[7])
                elif len(分割文字列) > 6:
                    
                    if 分割文字列[6] != ".":
                        ActSheet_x[7] = reformat_record(分割文字列[6])
                    else:
                        ActSheet_x[7] = "要再調査"
                else:
                    ActSheet_x[7] = "要再調査"
                ActSheet_x[13] = JFE_CRUD判定
                ActSheet_x[14] = JFE_IO判定

                                                    
            else:
            
                if len(分割文字列) > JFE_レコード関連引数位置:
                    JFE_処理レコード = 分割文字列[JFE_レコード関連引数位置]
                    ActSheet_x[7] = reformat_record(JFE_処理レコード)
                    ActSheet_x[13] = JFE_CRUD判定
                    ActSheet_x[14] = JFE_IO判定
                 
            
            if ActSheet_x[7] == "":
                ActSheet_x[7] = "要再調査"
                
    return ActSheet_x

#'20240214 ADD qian.e.wang
def COBOL_EXEC命令解析(data):
    
    global JFE_DATA関連PGM判定_
    global 関連資産,JFE_データ分類,JFE_レコード関連引数位置,JFE_CRUD判定,JFE_IO判定
    global 資産ID,COBOL_ID,元資産行情報,PARM_CMD
    global ActSheet_x
    
    ActSheet_x = [""]*22
    資産ID = data["資産ID"]
    if data["PGM_NAME"] == "UTACH" or data["PGM_NAME"] == "ADM" or data["PGM_NAME"] == "JYAADP":
        COBOL_ID = data["SYSIN_PGM"]
    else:
        COBOL_ID = data["PGM_NAME"]
    元資産行情報 = data["元資産行情報"]
    PARM_CMD = data["PARM"]
    
    ActSheet_x[1] = 資産ID
    ActSheet_x[2] = COBOL_ID
    ActSheet_x[5] = 元資産行情報
    ActSheet_x[6] = PARM_CMD
    
    関連資産 = COBOL_ID
    if JFE_DATA関連PGM判定_.get() == False:
        ActSheet_x[3] = "対象外"
    else:
        # DEBUG
        # print("関連資産① :["+str(関連資産)+"] JFE_データ分類① :["+str(JFE_データ分類)+"]\r\n")
        ###日産ANPSS一般 ADABAS
        if JFE_データ分類 == "ADABAS":
            ActSheet_x[3] = 関連資産
            ActSheet_x[4] = JFE_データ分類
            
            JFE_処理レコード = 関連資産
            ActSheet_x[7] = reformat_record(JFE_処理レコード)
            ActSheet_x[13] = JFE_CRUD判定
            ActSheet_x[14] = JFE_IO判定
            
            
    if ActSheet_x[7] == "":
        ActSheet_x[7] = "要再調査"
    
    return ActSheet_x
#'ADD END
    
def analysis1(db_path,title):
    global JFE_DATA関連PGM判定_
    global ActSheet, ActSheet_x,DB自動登録時PARM
    start = time.time()

    if os.path.isdir(title) == False:
        os.makedirs(title)
        
    ### 既存DB削除
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    sql = "SELECT * FROM 顧客別_資産関連性情報 WHERE 登録分類 = '自動設定（JFE_DB特定）'"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("顧客別_資産関連性情報",values,keys)
        cursor.execute(sql,values)
 

    sql = "SELECT * FROM 顧客別_JCL_PGM_DSN WHERE 手動更新FLG = '' AND 自動更新FLG = '自動設定（JFE_DB特定）'"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("顧客別_JCL_PGM_DSN",values,keys)
        cursor.execute(sql,values)
        
    sql = "SELECT * FROM 顧客別_PGM_IO情報 WHERE 資産分類 = 'COBOL_自動'"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("顧客別_PGM_IO情報",values,keys)
        cursor.execute(sql,values)
    
    
    # sql,values = make_delete_sql("顧客別_JCL_PGM_DSN",["",DB自動登録時PARM],["手動更新FLG","自動更新FLG"])
    # cursor.execute(sql,values)
    # sql,values = make_delete_sql("顧客別_資産関連性情報",[DB自動登録時PARM],["登録分類"])
    # cursor.execute(sql,values)
    # sql,values = make_delete_sql("顧客別_PGM_IO情報",["COBOL_自動"],["資産分類"])
    # cursor.execute(sql,values)
    
    conn.commit()
    print("DB削除完了", time.time()-start)
    
#'20240214 ADD qian.e.wang
    JFE_DATA関連PGM判定_ = JFE_DATA関連PGM判定(conn,cursor)
    ActSheet = []
    
    
    ###日産ANPSS ADABAS向け
    sql =   """\
            SELECT tbl1.*, tbl2.SYSIN_PGM FROM 顧客別_JCL_CMD情報 tbl1 
            INNER JOIN (SELECT DISTINCT JCL_NAME, STEP_SEQ, PGM_NAME, SYSIN_PGM FROM 顧客別_JCL_PGM_DSN) AS tbl2 
            ON tbl1.資産ID = tbl2.JCL_NAME AND tbl1.STEP_SEQ = tbl2.STEP_SEQ AND tbl1.PGM_NAME = tbl2.PGM_NAME
            WHERE tbl1.PGM_NAME <> '' AND tbl1.CMD分類 = 'EXEC'
            """
            
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    df.sort_values(["資産ID","CMD_SEQ","元資産行情報"],inplace=True)
    
    for i in range(len(df)):
        data = df.iloc[i]
        ActSheet_x = COBOL_EXEC命令解析(data)
        ActSheet.append(ActSheet_x)
#'ADD END
    
    
    sql =   """\
            SELECT * FROM 顧客別_COBOL_CMD情報
            """
            
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    df.sort_values(["資産ID","CMD_SEQ","元資産行情報"],inplace=True)
    
#'20240214 DEL qian.e.wang
    #JFE_DATA関連PGM判定_ = JFE_DATA関連PGM判定(conn,cursor)
    #ActSheet = []
#'DEL END
    
    for i in range(len(df)):
        data = df.iloc[i]
        ActSheet_x = COBOL_CALL命令解析(data)
        ActSheet.append(ActSheet_x)
    ActSheet_all = [actSheet[1:] for actSheet in ActSheet]
    write_excel_multi_sheet("JFE-DB利用箇所特定1.xlsx",ActSheet_all,"JFE_DB利用個所特定",title,output_header)
    
    conn.close()


# analysis1(sys.argv[1],sys.argv[2])