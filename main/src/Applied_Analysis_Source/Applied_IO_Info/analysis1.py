#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


応用_顧客別_JCL_PGM_DSN_ = None
入出力判定_IMSDB_ = None
#'20240214 ADD qian.e.wang
入出力判定_ADABAS_ = None
#'ADD END
GET_PROC_PGM_ = None
DATA_DSN別データ分類情報_ = None
変数値補正_ = None
Select_BMCP_PGM_ = None
入出力判定_ = None
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
L_SCHEMAKUBUN = ""
P_データ種別 = ""
#'20240614 DELETE jiaqi.chen
# P_入出力判定 = ""
#'20240614 DELETE 
TMP_DSN = ""
PGM_PROC = ""
BMCP_PGM = ""
parm = ""
vbCrLf = "\n"

class 応用_顧客別_JCL_PGM_DSN:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "顧客別_JCL_PGM_DSN"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        keys = df.columns.tolist()
        for i in range(len(df)):
            data = df.iloc[i]
            jcl,job,step = data["JCL_NAME"],data["JOB_SEQ"],data["STEP_SEQ"]
            dic = {key:data[key] for key in keys}
            
            if (jcl,job,step) not in self.dic:
                self.dic[(jcl,job,step)] = []
            self.dic[(jcl,job,step)].append(dic)
            
            if (jcl,job) not in self.dic:
                self.dic[(jcl,job)] = []
            self.dic[(jcl,job)].append(dic)
        
            

    def get(self,JCL_NAME,JOB_SEQ,STEP_SEQ=None):
        if self.dic == None:
            self.setup()
        
        
        if STEP_SEQ == None:
            if (JCL_NAME,JOB_SEQ) in self.dic:
                return self.dic[(JCL_NAME,JOB_SEQ)]
            else:
                return []
            
        if (JCL_NAME,JOB_SEQ,STEP_SEQ) in self.dic:
            return self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)]
        else:
            return []
        

class 入出力判定_IMSDB:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "QRY_JCL_PGM_DSN_IMSDB_SEG利用個所"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for jcl,job,step,sysin_pgm,dsn2,io in zip(df["JCL_NAME"],df["JOB_SEQ"],df["STEP_SEQ"],df["SYSIN_PGM"],df["DSN2"],df["入出力区分"]):
            if (jcl,job,step,sysin_pgm,dsn2) not in self.dic:
                self.dic[(jcl,job,step,sysin_pgm,dsn2)] = 0
            if io == "DLI_I-O":
                self.dic[(jcl,job,step,sysin_pgm,dsn2)] = 1
                


    def get(self,P_PGM, P_JCL, JOB_SEQ, STEP_SEQ, DSN):
        if self.dic == None:
            self.setup()
        
        
        if (P_JCL,JOB_SEQ,STEP_SEQ,P_PGM,DSN) in self.dic:
            update = self.dic[(P_JCL,JOB_SEQ,STEP_SEQ,P_PGM,DSN)]
            if update == 1:
                return "I-O" # SEGMENT利用有、SEGMENT更新処理有
            else:
                return "INPUT" # SEGMENT利用有、SEGMENT更新処理無
        else:
            return "未使用" # SEGMENT利用無
   
#'20240214 ADD qian.e.wang
class 入出力判定_ADABAS:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "【暫定】JFE_DATA関連性設定"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for sub,pgm,dsn,io in zip(df["データ分類"],df["データID"],df["DSN"],df["IO判定"]):
            self.dic[(sub,pgm,dsn)] = io

    def get(self,P_データ種別, P_PGM, DSN):
        if self.dic == None:
            self.setup()
        
        if (P_データ種別,P_PGM,DSN) in self.dic:
            update = self.dic[(P_データ種別,P_PGM,DSN)]
            if update == "":
                return "未設定"  # ADABAS利用有
            else:
                return update    # ADABAS利用有
        else:
            return "未使用"      # ADABAS利用無
#'ADD END
   
class GET_PROC_PGM:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "顧客別_JCL_STEP情報"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for jcl,job,step,pgm in zip(df["JCL_NAME"],df["JOB_SEQ"],df["STEP_SEQ"],df["PGM_NAME"]):
            if pgm != "":
                self.dic[(jcl,job,step)] = pgm
                


    def get(self,P_JCL,P_JOB_SEQ,P_STEP_SEQ):
        if self.dic == None:
            self.setup()
        
        if (P_JCL,P_JOB_SEQ,P_STEP_SEQ) in self.dic:
            return self.dic[(P_JCL,P_JOB_SEQ,P_STEP_SEQ)]
        else:
            return ""
    
    
class DATA_DSN別データ分類情報:
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
        
        for dsn,data,sub_info in zip(df["DSN"],df["データ分類"],df["補足"]):
            self.dic[dsn] = [data,sub_info]


    def get(self,P_DSN):
        if self.dic == None:
            self.setup()
        
        if P_DSN in self.dic:
            return self.dic[P_DSN] ### return データ分類,補足
        else:
            return "",""
    
    
class 変数値補正:
    def __init__(self,conn,cursor):
        self.dic = None
        self.dic2 = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "顧客別_JCL_STEP情報"
        self.dbname2 = "顧客別_PROC_PARM"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for jcl,job,step,var,value in zip(df["JCL_NAME"],df["JOB_SEQ"],df["STEP_SEQ"],df["PARM_VAR_LIST"],df["PARM_VALUE_LIST"]):
            if var != "":
                self.dic[(jcl,job,step)] = [var,value]
                
        
    def setup2(self):
        self.dic2 = {}
        sql = "SELECT * FROM "+self.dbname2
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for proc,var,value in zip(df["PROC_ID"],df["PARM_KEY"],df["PARM_VALUE"]):
            if proc not in self.dic2:
                self.dic2[proc] = []
            self.dic2[proc].append([var,value])
                

    def get(self,P_DSN, P_JCL, P_JOB_SEQ, P_STEP_SEQ, P_PROC):
        if self.dic == None:
            self.setup()
            
        global 分割文字列,分割文字列2
        
        if (P_JCL, P_JOB_SEQ, P_STEP_SEQ) in self.dic:
            var,value = self.dic[(P_JCL, P_JOB_SEQ, P_STEP_SEQ)]
            分割文字列 = ArrayEmptyDelete(var.split(" "))
            分割文字列2 = ArrayEmptyDelete(value.split(" "))
            for i in range(len(分割文字列)):
                L_tmp_str1 = "&" + 分割文字列[i]
                L_tmp_str2 = 分割文字列2[i]
            
                # 'P_DSN = Replace(P_DSN, "&" & 分割文字列(i) & ".", 分割文字列2(i))
                P_DSN = P_DSN.replace(L_tmp_str1, L_tmp_str2)
                
            return P_DSN.replace("\"","")
        
        
        if self.dic2 == None:
            self.setup2()
            
        if P_PROC in self.dic2:
            myRS3 = self.dic2[P_PROC]
            for var,value in myRS3:
                L_tmp_str1 = "&" + var
                L_tmp_str2 = value
                P_DSN = P_DSN.replace(L_tmp_str1, L_tmp_str2)
        
        return P_DSN.replace("\"","")
    
    
class Select_BMCP_PGM:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "BMCP_PGM情報"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for jcl,job,ste,pgm,sysin,bmcp in zip(df["JCL_NAME"], df["JOB_SEQ"], df["STEP_SEQ"], df["PGM_NAME"], df["SYSIN_PGM"],df["BMCP_PGM"]):
            if (jcl,job,ste,pgm,sysin) not in self.dic:
                self.dic[(jcl,job,ste,pgm,sysin)] = []
            self.dic[(jcl,job,ste,pgm,sysin)].append(bmcp)


    def get(self,JCL_NAME, JOB_SEQ, STEP_SEQ, PGM_NAME, SYSIN_PGM):
        if (isBMCP_PGM(PGM_NAME) or (PGM_NAME == "UTACH" and isBMCP_PGM(SYSIN_PGM))) == False:
            return ""
        
        if self.dic == None:
            self.setup()
        
        if (JCL_NAME, JOB_SEQ, STEP_SEQ, PGM_NAME, SYSIN_PGM) in self.dic:
            bmcp_name = self.dic[(JCL_NAME, JOB_SEQ, STEP_SEQ, PGM_NAME, SYSIN_PGM)]
            # if len(bmcp_name) > 1:
                # print("複数BMCP_PGMが存在?要確認" + 
                #           "JCL : " + str(JCL_NAME) + vbCrLf +
                #           "JOB_SEQ : " + str(JOB_SEQ) + vbCrLf +
                #           "STEP_SEQ : " + str(STEP_SEQ) + vbCrLf +
                #           "PGM_NAME : " + str(PGM_NAME) + vbCrLf +
                #           "SYSIN_PGM : " + str(SYSIN_PGM))
            return bmcp_name[0]
                
            
        else:
            return "" # 暫定として空文字列を返す
    
    
    
class 入出力判定:
    def __init__(self,conn,cursor):
        self.dic = None
        self.dic2 = None
        self.dic3 = None
        self.dic4 = None
        self.dic5 = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "UTL_Utility_IO情報"
        self.dbname2 = "入出力判定"
        self.dbname3 = "顧客別_PGM_IO情報"
        self.dbname4 = "UTL_STEP別_IO情報"
        self.dbname5 = "UTL_DD別_IO情報"
#'20240209 ADD qian.e.wang
        self.dic6 = None
        self.dbname6 = "【暫定】JFE_DATA関連性設定"
#'ADD END
        # self.db_path = db_path

    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        
    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname + " ORDER BY IO DESC"
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for util,dd,io in zip(df["Utility_ID"],df["DD名"],df["IO"]):
            if (util,dd) not in self.dic:
                self.dic[(util,dd)] = io
                

                
    def setup2(self):
        self.dic2 = {}

        sql = "SELECT * FROM "+self.dbname2 + " ORDER BY 入出力区分 DESC"
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for type,asset,assign,io in zip(df["資産分類"],df["COBOL_ID"],df["ASSIGN_ID"],df["入出力区分"]):
            if type != "COBOL":
                continue
            if (asset,assign) not in self.dic2:
                self.dic2[(asset,assign)] = io
 
        
    def setup3(self):
        self.dic3 = {}

        sql = "SELECT * FROM "+self.dbname3 + " ORDER BY 入出力区分 DESC"
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for asset,file,io in zip(df["資産ID"],df["ファイル名"],df["入出力区分"]):
            if (asset,file) in self.dic3:
                continue
            self.dic3[(asset,file)] = io
            
    def setup4(self):
        self.dic4 = {}

        sql = "SELECT * FROM "+self.dbname4 + " ORDER BY IO DESC"
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for jcl,job,step,dd,io in zip(df["JCL_NAME"],df["JOB_SEQ"],df["STEP_SEQ"], df["DD名"],df["IO"]):
            if (jcl,job,step,dd) not in self.dic4:
                self.dic4[(jcl,job,step,dd)] = io
            

        
    def setup5(self):
        self.dic5 = {}

        sql = "SELECT * FROM "+self.dbname5 + " ORDER BY IO DESC"
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for dd,io in zip(df["DD名"],df["IO"]):
            if dd not in self.dic5:
                self.dic5[dd] = io
            
#'20240209 ADD qian.e.wang
    def setup6(self):
        self.dic6 = {}

        sql = "SELECT * FROM "+self.dbname6
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for asset,file,io in zip(df["データID"],df["DSN"],df["IO判定"]):
            if (asset,file) in self.dic6:
                continue
            self.dic6[(asset,file)] = io
#'ADD END
            
    def 暫定判定(self, 入出力,P_PGM,PGM_SYSIN,P_DD,dsn):
        if 入出力 != "":
            return 入出力
        #Utility別固定処理
        if P_PGM == "KDJBR14" or P_PGM == "IEFBR14":
            入出力 = "対応不要"
        elif PGM_SYSIN == "DFSURRL0" or PGM_SYSIN == "DFSURRL0":
            入出力 = "廃止"
        #   'DD_NAMEが"SYSIN"且つ
        if P_DD == "SYSIN" and dsn != "":
            入出力 = "INPUT"
            
        return 入出力
        
                


    def get(self,P_PGM, P_DD, P_SYSIN, P_JCL, P_STEP, JOB_SEQ, STEP_SEQ, dsn, PGM名):    
        global 分割文字列,分割文字列2
        global PGM_SYSIN,L_DSN,P_データ種別
        
        if self.dic == None:
            self.setup()
        
        # 1UTL・ASM・PLI
        if (P_PGM,P_DD) in self.dic: 
            入出力 = self.dic[(P_PGM,P_DD)]
            return self.暫定判定(入出力,P_PGM,PGM_SYSIN,P_DD,dsn)
        
        #     2起動元Utility
        #     P_PGMはSYSIN_PGMが優先されるため、SYSIN_PGMでの利用ではなく起動元UtilityのDDの場合判定されない
        #     その為ここで起動元UtilityのDDのIO判定を行う。
        if (PGM名,P_DD) in self.dic:  
            入出力 = self.dic[(PGM名,P_DD)]
            return self.暫定判定(入出力,P_PGM,PGM_SYSIN,P_DD,dsn)
        
        
        
        # 3 メインCOBOL　サブCOBOL　EASYのサブルーチン対応
        #  入出力判定の元TABLEは「顧客別_PGM_IO情報」「顧客別_COBOL_入出力情報1_1」
        
        if self.dic2 == None:
            self.setup2()
        
        if (P_PGM,P_DD) in self.dic2:
            入出力 = self.dic2[(P_PGM,P_DD)]
            return self.暫定判定(入出力,P_PGM,PGM_SYSIN,P_DD,dsn)
        
        
        # 4 PGM資産と解析済DD
        ### sql の like 文の高速化は難しいので、ここだけ毎回 sqlを発行する
        Cmd_A = """SELECT 資産分類,資産ID,ASSIGN_ID,入出力区分 
                    FROM 入出力判定 WHERE 資産分類 = 'COBOL' AND 
                    資産ID LIKE '"""
        
        Cmd_B = """*' AND ASSIGN_ID = '"""
        tempPgmStr = P_PGM 
        sql = Cmd_A + tempPgmStr + Cmd_B + P_DD + """'"""
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        if len(df) > 0:
            入出力 = df.iloc[0]["入出力区分"]
            return self.暫定判定(入出力,P_PGM,PGM_SYSIN,P_DD,dsn)
            
        # 5 DB2,IMSDB対応
        if self.dic3 == None:
            self.setup3()
            
            
        if P_データ種別 == "DB2_TABLE" and "." in dsn:
            分割文字列 = dsn.split(".")
            L_DSN = 分割文字列[1]
        else:
            L_DSN = dsn
                 
        if (P_PGM,L_DSN) in self.dic3:
            入出力 = self.dic3[(P_PGM,L_DSN)]
            return self.暫定判定(入出力,P_PGM,PGM_SYSIN,P_DD,dsn)
        
        
        # 6 STEP別に設定されたDD
        if self.dic4 == None:
            self.setup4()
        
        if (P_JCL,JOB_SEQ,STEP_SEQ,P_DD) in self.dic4:
            入出力 = self.dic4[(P_JCL,JOB_SEQ,STEP_SEQ,P_DD)]
            return self.暫定判定(入出力,P_PGM,PGM_SYSIN,P_DD,dsn)
        
        
        # 7 DD別に設定されたIO
        if self.dic5 == None:
            self.setup5()
        
        if P_DD in self.dic5:
            入出力 = self.dic5[P_DD]
            return self.暫定判定(入出力,P_PGM,PGM_SYSIN,P_DD,dsn)
        
#'20240209 ADD qian.e.wang
        # 8 ADABAS対応
        if self.dic6 == None:
            self.setup6()
            
        # DEBUG
        # print("■③ データ種別 :["+str(P_データ種別)+"] DSN :["+str(L_DSN)+"]\r\n")
        if P_データ種別 == "ADABAS":
            入出力 = self.dic6[(P_PGM,L_DSN.replace("ADABAS:", "").replace("(設定無)", "").replace("(" + P_PGM + ")", ""))]
            return 入出力
#'ADD END
        
        return self.暫定判定("",P_PGM,PGM_SYSIN,P_DD,dsn)
        
    
def 入出力判定_DISP調整(P_INOUT, P_DISP):

    入出力判定_DISP = P_INOUT
    
    if P_INOUT == "BK-INPUT" or P_INOUT == "INPUT_判定除外":
       入出力判定_DISP = "INPUT"
    elif P_INOUT == "BK-OUTPUT":
       入出力判定_DISP = "OUTPUT"
    elif P_DISP == "M,D":
       入出力判定_DISP = "DELETE"
    elif P_DISP == "O,D":
       入出力判定_DISP = "INPUT-DELETE"
    elif P_INOUT == "廃止" or P_INOUT == "対応不要" or P_INOUT == "未使用":
       入出力判定_DISP = "判定対象外"
    elif P_DISP == ",K,D":
       入出力判定_DISP = "OUTPUT"
    elif P_DISP == ",P":
       入出力判定_DISP = "OUTPUT"
    elif P_DISP != "":
        分割文字列 = P_DISP.split(",")
        if 分割文字列[0] == "M" and P_INOUT == "OUTPUT":
            入出力判定_DISP = "I-O"
        elif 分割文字列[0] == "O" and P_INOUT == "OUTPUT":
            入出力判定_DISP = "I-O"
        elif 分割文字列[0] == "S" and P_INOUT == "OUTPUT":
            入出力判定_DISP = "I-O"
            
    return 入出力判定_DISP
 
     
def データ種別判定(P_DSN, P_GDG, P_SYSIN,P_SCHEMAKUBUN,P_PGM):
    global DATA_DSN別データ分類情報_
    global P_データ種別
    global ActSheet_x
    # '顧客毎にロジックを改修する（現在はLION暫定バージョン）
        
    if P_GDG != "":
        データ種別 = "GDG"
    elif P_SYSIN != "":
        # '福山通運 SYSIN名が存在する場合、データ種別判定 = "PAM" HP李 2013/11/26
        # 'データ種別判定 = "SYSIN"
        データ種別 = "PDS"
    else:

#'20240214 UPD qian.e.wang
        #data,sub_info = DATA_DSN別データ分類情報_.get(P_DSN)
        data,sub_info = DATA_DSN別データ分類情報_.get(P_DSN.replace("ADABAS:", "").replace("(設定無)", "").replace("(" + P_PGM + ")", ""))
        データ種別 = data
        # DEBUG
        # print("■① データ種別 :["+str(データ種別)+"] DSN :["+str(P_DSN)+"]\r\n")
#'UPD END

        # 'DSNは"DUMMY"の場合 データ種別判定 = "DUMMY"
        if データ種別 != "":
            if データ種別 == "IMSDB" or データ種別 == "IMSDB_未使用":
                ActSheet_x[17] = sub_info
                # 'ActSheet_x[14] = ActSheet_x[14] & " → " & myRS3!補足    'DSNにDB名も付与
        elif P_DSN == "DUMMY":
            データ種別 = "DUMMY"
        elif "&&" in P_DSN:
            データ種別 = "一時DSN"
        elif "IMSF." in P_DSN:
            データ種別 = "IMS関連"
        else:
            if P_SCHEMAKUBUN == "":
                データ種別 = "NON-VSAM"
            else:
                データ種別 = P_SCHEMAKUBUN
                
    if (データ種別 != "一時DSN") and ("&" in P_DSN) and ("変数" not in データ種別):
        if データ種別 != "NON-VSAM":
            データ種別 = データ種別 + "_変数"
        else:
            データ種別 = "変数"
 
    P_データ種別 = データ種別
    
    return データ種別

    
def DSN情報なし時処理(ActSheet_x,data):
    
    global JCL_NAME_WK,STEP_SEQ_SV,PROC_ID
    global ActSheet
    ### 基本的には、解析処理の最初に書き込まれていて不要
    
    if STEP_SEQ_SV > 0:
        ActSheet_x[11] = PROC_ID
    else:
        ActSheet_x[11] = data["PROC名"]

    ActSheet_x[35] = JCL_NAME_WK ### 間違い?
    ###MHI用暫定 終了
    
    ActSheet.append(ActSheet_x)
            
            
def DSN情報有り時処理(P_PARAM,data,data2):
    global ActSheet,ActSheet_x
    global JCL_NAME_WK,PGM_NAME,STEP_SEQ,JCL_NAME_SV,JOB_SEQ_SV,STEP_SEQ_SV,PROC_ID
    global PGM_SYSIN,L_GDG,L_DISP,L_SYSIN,L_SCHEMAKUBUN,P_データ種別,TMP_DSN,PGM_PROC,BMCP_PGM,parm
    global 分割文字列
    global 入出力判定_IMSDB_,GET_PROC_PGM_,変数値補正_,Select_BMCP_PGM_,入出力判定_
    #'20240614 ADD jiaqi.chen
    P_入出力判定 = ""
    #'ADD END

    #  'step_seq = step_seq + 1
    ActSheet_x = [""]*45
    
    
    # 'JCL-STEP情報も転記
    ActSheet_x[1] = data["TEST_ID"]
    ActSheet_x[2] = data["JCL_SEQ"]
    ActSheet_x[3] = data["JCL_ID"]
    ActSheet_x[4] = data["LIBRARY"]
    ActSheet_x[5] = data["JOB_SEQ"]
    ActSheet_x[6] = data["JOB_ID"]
    ActSheet_x[7] = data["STEP_SEQ"]
    
    ActSheet_x[10] = PGM_NAME              #     '2019/9/13　追加
    
    ActSheet_x[12] = data2["SYSIN_PGM"]
    
    #     '20220215列13-44の位置1づつ移動
    ActSheet_x[14] = data2["DD_NAME"]  #  '13⇒14 
    ActSheet_x[15] = data2["DSN"] #                      '14⇒15
    ActSheet_x[16] = data2["GDG"]#                      '15⇒16
    ActSheet_x[17] = data2["SYSIN"]#                    '16⇒17
    
    ActSheet_x[24] = data2["DISP"] #                    '20→23⇒24
    ActSheet_x[25] = data2["SYSOUT"]#                   '21→24⇒25
    ActSheet_x[26] = data2["WRITER"]#                   '22→25⇒26
    ActSheet_x[27] = data2["FORM"]#                     '23→26⇒27
    ActSheet_x[28] = data2["UNIT"]#                     '24→27⇒28
    ActSheet_x[29] = data2["VOL"]#   'VOL抽出追加       '25→28⇒29
    ActSheet_x[30] = data2["SPACE_Q"]#                  '26→29⇒30
    ActSheet_x[31] = data2["DCB_RECFM"]#                '27→30⇒31
    ActSheet_x[32] = data2["DCB_LRECL"]#                '28→31⇒32
    ActSheet_x[33] = data2["DCB_BLKSIZE"]#              '29→32⇒33
    ActSheet_x[34] = data2["LABEL"] #'LABEL抽出追加  '30→33⇒34
    
    #'MHI用暫定 開始
    ActSheet_x[35] = JCL_NAME_WK      #  '34⇒35
    # 'MHI用暫定 終了
    
    # '間隔があくが今後の案件で調整する
    ActSheet_x[41] = data2["PGM予備"]   #               '2020/4/30 ADD⇒41
    ActSheet_x[42] = data2["実行モード"] #              '2020/4/30 ADD⇒42
                
    PGM_SYSIN = data2["SYSIN_PGM"]#                                          '12
    L_GDG = data2["GDG"]
    L_SYSIN = data2["SYSIN"]
    L_DISP = data2["DISP"]
    
    # '★★★★　暫定調査ロジック　★★★★
    # 'if data2["DSN = "DUMMY":
    # '   err_msg = ""
    # 'End if
    # '★★★★　暫定調査ロジック　★★★★
    if data2["手動更新FLG"] == "DEFAULT":
        L_SCHEMAKUBUN = ""
    elif data2["手動更新FLG"].startswith("DAM"):
        L_SCHEMAKUBUN = "DAM"
    elif data2["手動更新FLG"].startswith("DB"):
        L_SCHEMAKUBUN = "NDB"
    elif data2["手動更新FLG"].startswith("AIM"):
        L_SCHEMAKUBUN = "AIM"
    elif data2["手動更新FLG"].startswith("VICS") or data2["手動更新FLG"].startswith("新VICS"):
        L_SCHEMAKUBUN = "VICS"
    elif data2["手動更新FLG"].startswith("その他環境"):
        L_SCHEMAKUBUN = "その他環境"
    else:
        L_SCHEMAKUBUN = ""
    

    if data2["DSN"] != "":
        ##'データ種別判定 & データ属性情報取得
        P_データ種別 = ""          #             '初期化
        if data2["DD_NAME"] == "_SYSI001":
            ActSheet_x[19] = "IMSDB_SEGMENT"   #     '18⇒19
            P_データ種別 = "IMSDB_SEGMENT"
        # 'elif data2["DD_NAME = "_SYSM001":             'データ種別判定の中でDBのセットも行っているので直接指定はしない
        # '   ActSheet_x[18] = "IMSDB"
        # '   P_データ種別 = "IMSDB"
        # '
        elif data2["DD_NAME"] == "_SYST001" or data2["DD_NAME"] == "_SYST002":
            ActSheet_x[19] = "DB2_TABLE"         #   '18⇒19
            if "." in data2["DSN"]:   # 'スキーマ付きの場合はスキーマは除去
                
                分割文字列 = data2["DSN"].split(".")
                ActSheet_x[15] = 分割文字列[1]    #   '14⇒15
            P_データ種別 = "DB2_TABLE"         #                      '入出力判定時に利用するので退避
        elif data2["DD_NAME"] == "STEPLIB":
            ActSheet_x[19] = "PDS"              #   '18⇒19
        else:
            ActSheet_x[19] = データ種別判定(data2["DSN"], L_GDG, L_SYSIN,L_SCHEMAKUBUN, data2["PGM_NAME"])

        # '変数値補正処理
        if "変数" in P_データ種別:
            ActSheet_x[40] = data2["DSN"] #  '元の値を退避（確認用）39⇒40
            TMP_DSN = 変数値補正_.get(data2["DSN"], data["JCL_ID"], data["JOB_SEQ"], data["STEP_SEQ"], data["PROC名"])# '引数にPROC_ID追加
            ActSheet_x[15] = TMP_DSN         #       '14⇒15
        
            #'データ種別再判定（内部判定）
            if "&" not in TMP_DSN: # '変数値がなくなっていた場合,再判定
                ActSheet_x[19] = データ種別判定(TMP_DSN, L_GDG, L_SYSIN,L_SCHEMAKUBUN, data2["PGM_NAME"])   #  '18⇒19

        #'PROC内PGM名補正処理
        if PGM_SYSIN == "" and data["PGM名"] == "":
            #'PGM_PROC = GET_PROC_PGM(data["JCL_ID, data["JOB_SEQ, data["STEP_SEQ)
            PGM_PROC = GET_PROC_PGM_.get(JCL_NAME_SV, JOB_SEQ_SV, STEP_SEQ_SV)
            ActSheet_x[11] = PGM_PROC   #  '★出力列のが変わった場合に注意すること
        else:
            ActSheet_x[11] = data["PGM名"]
            
        # '=========================================================
        # '20210607 Add Horiuchi
        # 'Batch Module Control Program対応
        # '=========================================================
        BMCP_PGM = Select_BMCP_PGM_.get(JCL_NAME_SV, JOB_SEQ_SV, STEP_SEQ_SV, data2["PGM_NAME"], PGM_SYSIN)
        
        if BMCP_PGM != "":
            ActSheet_x[13] = BMCP_PGM                        # '44⇒13
        else:
            pass
            #'ActSheet_x[13] = "特定に失敗"
            
        # 'End Add


        # '=========================================================
        # '20210607 Add Horiuchi
        # 'Batch Module Control Program対応
        # '=========================================================
        if BMCP_PGM != "":
            parm = BMCP_PGM
        #'入出力判定用PARM調整
        elif PGM_SYSIN != "":
            parm = PGM_SYSIN
        elif data["PGM名"] != "":
            parm = data["PGM名"]
        elif PGM_PROC != "":
            parm = PGM_PROC
        else:
            parm = data["PROC名"]
        
#'20240219 ADD qian.e.wang
        if "ADABAS:" in data2["DSN"]:
            P_データ種別 = "ADABAS"
        # DEBUG
        # print("■② データ種別 :["+str(P_データ種別)+"] 入出力判定用PARM :["+str(parm)+"] DSN :["+str(data2["DSN"])+"]\r\n")
        if P_データ種別 == "ADABAS":                
            # 'P_入出力判定
            P_入出力判定 = 入出力判定_ADABAS_.get(P_データ種別, parm, data2["DSN"].replace("ADABAS:", "").replace("(設定無)", "").replace("(" + parm + ")", ""))
            ActSheet_x[43] = "ADABAS有無判定"  #'コメント欄      '42⇒43
#'ADD END

        #'P_入出力判定 = 入出力判定(PARM, data2["DD_NAME, L_SYSIN, data["JCL_ID, data["STEP名, data["JOB_SEQ, data["STEP_SEQ, data2["DSN)
        if P_入出力判定 == "":
            P_入出力判定 = 入出力判定_.get(parm, data2["DD_NAME"], L_SYSIN, JCL_NAME_SV, data["STEP名"], JOB_SEQ_SV, STEP_SEQ_SV, data2["DSN"],data["PGM名"])

        # DEBUG
        # print(parm, data2["DD_NAME"], L_SYSIN, JCL_NAME_SV, data["STEP名"], JOB_SEQ_SV, STEP_SEQ_SV, data2["DSN"],data["PGM名"],P_入出力判定)

        # 'データ種別による入出力判定補正
        # 'if P_データ種別 = "IMSDB" and P_入出力判定 != "DELETE":     'DELETEする場合があるのでそれは例外にする
        if P_データ種別 == "IMSDB" and P_入出力判定 == "":
            # 'P_入出力判定 = "I-O"
            P_入出力判定 = 入出力判定_IMSDB_.get(PGM_SYSIN, JCL_NAME_SV, JOB_SEQ_SV, STEP_SEQ_SV, data2["DSN"])
            ActSheet_x[43] = "SEGMENT有無判定"  #'コメント欄      '42⇒43
        elif P_データ種別 == "IMSDB_INDEX" or P_データ種別 == "IMSDB_要確認":   #    'MHI案件のみの予定
            P_入出力判定 = "対応不要"                                            #                '判定しない
            
        ActSheet_x[21] = P_入出力判定                  #         '20⇒21
        
        # 'MHI暫定対応 「EASYTREV」「EZTPA00」の場合はDISPで判定する
        # 'if P_入出力判定 = "" and L_DISP != "" and (PGM_NAME = "EASYTREV" or PGM_NAME = "EZTPA00" or PGM_SYSIN = "EASYTREV" or PGM_SYSIN = "EZTPA00"):
        if P_入出力判定 == "": # '全ての条件で未判定の入出力判定をDISPで判定する。正し跡で識別できるようにDISP調整後の判定結果のみ設定する
            # ' 20220227 wangqian DISP全パターン対応 START
            # 'if L_DISP = "S" or L_DISP = "O":
            # '   'P_入出力判定 = "INPUT"
            # '   ActSheet_x[22] = "INPUT"                          '21⇒22
            # 'elif L_DISP = "S,D" or L_DISP = "O,D" or L_DISP = "M,D":
            # '   'P_入出力判定 = "DELETE"
            # '   ActSheet_x[22] = "DELETE"                         '21⇒22
            # 'elif InStr(L_DISP, "M") > 0:
            # '   'P_入出力判定 = "I-O"
            # '   ActSheet_x[22] = "I-O"                            '21⇒22
            # 'elif InStr(L_DISP, "N") > 0 or InStr(L_DISP, "C") > 0:
            # '   'P_入出力判定 = "OUTPUT"
            # '   ActSheet_x[22] = "OUTPUT"                         '21⇒22
            # 'elif InStr(L_DISP, "O") > 0 or InStr(L_DISP, "S") > 0:
            # '   ActSheet_x[22] = "INPUT"                          '21⇒22
            # 'End if
            # ' *******************************************************************
            # ' DISP=(aaa,bbb,ccc)
            # ' aaa…データセットの前処理
            # '        NEW or SHR or OLD or MOD
            # '        省略時解釈はNEWです｡
            # ' bbb…データセットの後処理（正常終了時）
            # '        DELETE or KEEP or PASS or CATLG or UNCALTG
            # '        省略時解釈はaaaがNEWの場合DELETE、aaaがOLD/SHR/MODの場合KEEPです。
            # ' ccc…データセットの後処理（異常終了時）
            # '        DELETE or KEEP or CALTG or UNCALTG
            # '        省略時解釈はaaaがNEWの場合DELETE、aaaがOLD/SHR/MODの場合KEEPです。
            # '
            # ' N：NEW 　 新規
            # ' O：OLD　  既存独占読取
            # ' S：SHR　  既存共有読取
            # ' M：MOD　  追加モード
            # ' K：KEEP   保存
            # ' D：DELETE 削除
            # ' C：CATLG  カタログ
            # ' U：UNCATLGアンカタログ※未対応 ⇒ 現時点はENDに変換
            # ' P：PASS　 後続利用
            # ' ＜JFE202112末全Gr資産にて纏めたパターン＞
            # ' INPUT   ⇒ "S","O"
            # '            "O,END","O,K","O,P","S,K","S,P","END"
            # ' DELETE  ⇒ "S,D","O,D",",D",",D,D",",K,D","M,D","N,D",",P,D"
            # ' I-O     ⇒ "M","M,C","M,K","M,P"
            # ' OUTPUT  ⇒ "N","N,C","N,K","N,P",",C",",C,D","O,C",",END",",K",",P",
            # '            "N,END"(//OUTDD    DD   DSN=ARCSBP&SL,UNIT=AFF=CMT,DISP=(NEW,&DSP)),
            # '            "END,END"(//KUTOUT   DD   DSN=_____,DISP=(___,____)),
            # '            "END,K"(//OLOG      DD   &OUT.UNIT=&U,VOL=SER=&V,DSN=&D,DISP=(&DP,KEEP))
            # ' *******************************************************************
            if L_DISP in  ("S", "O"):
                ActSheet_x[22] = "INPUT"
            elif L_DISP in ("S,D", "O,D", ",D", ",D,D", ",K,D", "M,D", "N,D", ",P,D","R,D"):
                ActSheet_x[22] = "DELETE"
            elif L_DISP in ("M", "M,C", "M,K", "M,P"):
                ActSheet_x[22] = "I-O"
            elif L_DISP in ("N", "N,C", "N,K", "N,P", "R", "R,C", "R,K", "R,P",",C", ",C,D", "O,C", ",END", ",K", ",P", "N,END", "END,END", "END,K","R,END"):
                ActSheet_x[22] = "OUTPUT"
            else:
                #' "O,END","O,K","O,P","S,K","S,P","END"
                ActSheet_x[22] = "INPUT"
            ##' 20220227 wangqian DISP全パターン対応 END
        
        
        if P_入出力判定 != "":
            ActSheet_x[22] = 入出力判定_DISP調整(P_入出力判定, L_DISP) #'21⇒22
        
        # 'データ種別2判定 ※テストツールで利用するための対応
        if P_データ種別 == "DB2_TABLE":
            ActSheet_x[20] = "DB2_TABLE" #                        '19⇒20
        elif P_データ種別 == "DUMMY":
            ActSheet_x[20] = ""           #                      '19⇒20
            ActSheet_x[22] = "判定対象外"  #                     '21⇒22
        elif P_データ種別 == "ENTRY-DATA":
            ActSheet_x[20] = "SAM"        #                      '19⇒20
        elif P_データ種別 == "IMSDB":
            ActSheet_x[20] = "IMSDB_TABLE"#                      '19⇒20
        elif P_データ種別 == "IMSDB_INDEX":
            ActSheet_x[20] = ""            #                     '19⇒20以下同
            ActSheet_x[22] = "判定対象外"   #                    '21⇒22以下同
        elif P_データ種別 == "IMSDB_未使用":
            ActSheet_x[20] = ""
            ActSheet_x[22] = "判定対象外"
        elif P_データ種別 == "IMSDB_SEGMENT":
            ActSheet_x[20] = "IMSDB_SEGMENT"
            # 'ActSheet_x[22] = "判定対象外"
        elif P_データ種別 == "IMSDB_要確認":
            ActSheet_x[20] = ""
        elif P_データ種別 == "IMS関連":
            ActSheet_x[20] = ""
        # '    ActSheet_x[22] = "判定保留"
        elif P_データ種別 == "NON-VSAM":
            ActSheet_x[20] = "SAM"
        elif P_データ種別 == "NON-VSAM(ユーザー用)":
            ActSheet_x[20] = "SAM"
        elif P_データ種別 == "PDS":
            ActSheet_x[20] = "PDS"
            ActSheet_x[22] = "判定対象外"
        elif P_データ種別 == "PDS_変数":
            ActSheet_x[20] = "PDS"
            ActSheet_x[22] = "判定対象外"
        elif P_データ種別 == "VSAM":
            ActSheet_x[20] = "VSAM"
        elif P_データ種別 == "ダンプファイル":
            ActSheet_x[20] = "SAM"
        elif P_データ種別 == "ファイル伝送用":
            ActSheet_x[20] = "SAM"
        elif P_データ種別 == "プリントデータ":
            ActSheet_x[20] = "SAM"
        elif P_データ種別 == "ユーザー用":
            ActSheet_x[20] = "SAM"
        elif P_データ種別 == "一時DSN":
            ActSheet_x[20] = ""
        elif P_データ種別 == "変数付DSN_要調査":
            ActSheet_x[20] = "要調査"
        elif P_データ種別 == "制御用ダミー":
            ActSheet_x[20] = "空ファイル"
            ActSheet_x[22] = "INPUT"
        else:
            ActSheet_x[20] = P_データ種別
        
        if data2["DD_NAME"] == "STEPLIB":
            ActSheet_x[22] = "判定対象外"
        
#'20240209 DEL qian.e.wang
        # ' 20220302 wangqian DSNによるデータ種別2判定の追加　START
        if data2["DSN"] == "変数値要確認":
            ActSheet_x[20] = "独自DAM"
        elif len(data2["DSN"].replace("(設定無)", "")) == 4:
            ActSheet_x[20] = "基準"
        # ' 20220302 wangqian DSNによるデータ種別2判定の追加　END
#' DEL END
    else:
        
        # 'PROC内PGM名補正処理　→　処理速度を考慮してDSNがNULLのものは対応する必要は無いが出力結果に違和感があるので実施する。（遅ければコメントアウトしてもよい）
        if PGM_SYSIN == "" and data["PGM名"] == "":
            # 'PGM_PROC = GET_PROC_PGM(data["JCL_ID, data["JOB_SEQ, data["STEP_SEQ)
            PGM_PROC = GET_PROC_PGM_.get(JCL_NAME_SV, JOB_SEQ_SV, STEP_SEQ_SV)
            ActSheet_x[10] = PGM_PROC    # '★出力列のが変わった場合に注意すること    '★9→10に変更（要確認）
        else:
            ActSheet_x[10] = data["PGM名"]
    
    
    # '========================================================================
    # 'JFE倉敷暫定対応
    if "NDB:" in data2["DSN"]:   # '14⇒15,17⇒18,19⇒20
        ActSheet_x[15] = ActSheet_x[15].replace("NDB:", "").replace("(設定無)", "")
        ActSheet_x[18] = "確認中"
        ActSheet_x[20] = "NDB"
    elif "DAM:" in data2["DSN"]:
        ActSheet_x[15] = ActSheet_x[15].replace("DAM:", "").replace("(設定無)", "")
        ActSheet_x[18] = "確認中"
        ActSheet_x[20] = "DAM"
    elif "基準:" in data2["DSN"]:
        ActSheet_x[15] = ActSheet_x[15].replace("基準:", "").replace("(設定無)", "")
        ActSheet_x[18] = "確認中"
        ActSheet_x[20] = "基準"
#'20240209 ADD qian.e.wang
    # '日産ANPSS暫定対応
    if "ADABAS:" in data2["DSN"]:   # '14⇒15,17⇒18,19⇒20
        ActSheet_x[15] = ActSheet_x[15].replace("ADABAS:", "").replace("(設定無)", "")
        ActSheet_x[18] = "確認中"
        ActSheet_x[19] = "ADABAS"
        ActSheet_x[20] = "ADABAS"
#' ADD END
    # '========================================================================
    
    
    
    if data2["STEP_SEQ"] != "" and P_PARAM == "PROC":
        ActSheet_x[8] = data2["STEP_SEQ"]
        ActSheet_x[9] = data2["STEP_NAME"]#  '20161021 Takei
        ActSheet_x[11] = PROC_ID
        ActSheet_x[39] = "①"           # '★38⇒39
    elif P_PARAM == "JCL" and STEP_SEQ_SV > 0:       #      '20161021 Takei
        # 'ActSheet_x[8] = data["STEP_SEQ2   '20161021 Takei　20190914変更
        ActSheet_x[8] = 0  # '20161021 Takei　20190914変更
        ActSheet_x[9] = data2["STEP_NAME"]#   '20161021 Takei
        ActSheet_x[11] = PROC_ID
        ActSheet_x[39] = "②"       #     '★38⇒39
    else:
        ActSheet_x[8] = data["STEP_SEQ2"]
        ActSheet_x[9] = data["STEP_NAME"]#   '20161021 Takei
        # 'ActSheet_x[10] = ""
        ActSheet_x[39] = "③"  #          '★38⇒39
    
    if data2["PGM_NAME"] == "UTACH" and data2["自動更新FLG"] == "自動設定（UTL解析）":
        ActSheet_x[8] = int(data2["手動更新FLG"])

#'20240219 ADD qian.e.wang
    if (data2["PGM_NAME"] == "ADM" or data2["PGM_NAME"] == "JYAADP") and (data2["自動更新FLG"] == "自動設定（UTL解析）" or data2["自動更新FLG"] == "手動補足（UTL解析）"):
        ActSheet_x[8] = int(data2["手動更新FLG"])
#'ADD END
    
    # 'ActSheet_x[8] = data["STEP_NAME     '20161021 Takei
    # 'ActSheet_x[9] = data["PGM_NAME  '上で補正しているのでここでは行わない
    
    # 'if P_PARAM = "PROC":
    # '
    # 'else
    #     'ActSheet_x[10] = data["PROC_NAME
    #     'ActSheet_x[10] = PROC_ID
    #     ' PROC_ID
    # 'End if
    
    ActSheet.append(ActSheet_x)


def 解析処理(data):
    global 応用_顧客別_JCL_PGM_DSN_
    
    global JCL_NAME_WK,PGM_NAME,STEP_SEQ,JCL_NAME_SV,JOB_SEQ_SV,STEP_SEQ_SV,PROC_ID
    ActSheet_x = [""]*45
    
    ActSheet_x[1] = data["TEST_ID"]
    ActSheet_x[2] = data["JCL_SEQ"]
    ActSheet_x[3] = data["JCL_ID"]
    ActSheet_x[4] = data["LIBRARY"]
    ActSheet_x[5] = data["JOB_SEQ"]
    ActSheet_x[6] = data["JOB_ID"]
    ActSheet_x[7] = data["STEP_SEQ"]
    ActSheet_x[8] = data["STEP_SEQ2"]#  'MHI案件で追加
    ActSheet_x[9] = data["STEP名"]
    ActSheet_x[10] = data["PGM名"]
    ActSheet_x[11] = data["PROC名"]
    #'ActSheet_x[12] = ""             'MHI案件で追加

    #'MHI用暫定 開始  JCLのメンバー名のみ必要
    
    分割文字列 = data["JCL_ID"].split("%")
    
    # '20220311 入出力情報出力のメンバー名取得見直しSTART
    if len(分割文字列) > 2:
        分割文字列2 = 分割文字列[2].split(".")
        if len(分割文字列2) > 0:
            JCL_NAME_WK = 分割文字列2[0]
        else:
            JCL_NAME_WK = 分割文字列[2]
    # 'If len(分割文字列) > 0:
    elif len(分割文字列) > 1:
    # '20220311 入出力情報出力のメンバー名取得見直しEND
        分割文字列2 = 分割文字列[1].split(".")
        if len(分割文字列2) > 0:
            JCL_NAME_WK = 分割文字列2[0]
        else:
            JCL_NAME_WK = 分割文字列[1]
    else:
        JCL_NAME_WK = data["JCL_ID"]
    ActSheet_x[35] = JCL_NAME_WK       #'34⇒35
    #'MHI用暫定 終了
    
    
    
    PGM_NAME = data["PGM名"] # 'PGM名退避　この値はPROC内のPGMを反映している

    #'ACOM版処理
    #'STEP情報のみ存在しない場合を想定（処理は続行）
    #    '実際に発生したら検討する

    
    STEP_SEQ = 0

    #'JCL_PGM_DSN呼出共通関数にセット　JCLｔｐPROCでパラメータを共通化
    if data["STEP_SEQ2"] > 0:     #'PROC呼出
        JCL_NAME_SV = data["PROC名"]      #        '呼出時にLIKE指定が必要
        JOB_SEQ_SV = 0
        STEP_SEQ_SV = data["STEP_SEQ2"]     #       '0以上の場合はPROC内処理 acom版より
    else:                        #'JCL呼出
        JCL_NAME_SV = data["JCL_ID"]       #        '
        JOB_SEQ_SV = data["JOB_SEQ"]
        STEP_SEQ_SV = data["STEP_SEQ"]      #       '

    # 'if data["PROC名"] != "":
    if data["STEP_SEQ2"] > 0:
        PROC_ID = data["PROC名"]
        #'STEP_SEQ_SV = data["STEP_SEQ"]
    
    #'①JCL内PROC（内部PROC）
    #'前提　内部PROCの「JCL_NAME」が「JCL_ID%PROC名」となる命名ルールを想定？

        myRS2 = 応用_顧客別_JCL_PGM_DSN_.get(data["JCL_ID"] + "%" + data["PROC名"],data["JOB_SEQ"])
        # DEBUG
        # print("■①JCL内PROC（内部PROC）\r\n")
        if myRS2 == []:
            #'②外部PROCを想定
            # 'myRS2.Source = Cmd1 + data["PROC_NAME"] + Cmd2 + data["STEP_SEQ2"] + Cmd3 + 0 + Cmd4
            # 'myRS2.Source = Cmd1x + data["PROC名"] + Cmd4x
            # 'myRS2.Source = Cmd1x + data["PROC名"] + Cmd2 + data["STEP_SEQ2"] + Cmd4
            # 'myRS2.Source = Cmd1x + JCL_NAME_SV + Cmd2x + STEP_SEQ_SV + Cmd3 + JOB_SEQ_SV + Cmd4
            myRS2 = 応用_顧客別_JCL_PGM_DSN_.get(JCL_NAME_SV,JOB_SEQ_SV,STEP_SEQ_SV)
            # DEBUG
            # print("■②外部PROC\r\n")

            # 'MsgBox (myRS2.Source)
            if myRS2 == []:
                DSN情報なし時処理(ActSheet_x,data)
            else:
            # '外部PROC明細出力
                for data2 in myRS2:
                    DSN情報有り時処理("PROC",data,data2)
        else:
            # '内部PROC明細出力
            for data2 in myRS2:
                DSN情報有り時処理("PROC",data,data2)
    else:
    # '③JCL内PGM
        PROC_ID = ""     #'不具合対応 2019/12/24
        # 'myRS2.Source = Cmd1 + data["JCL_ID"] + Cmd2 + data["STEP_SEQ"] + Cmd3 + data["JOB_SEQ"] + Cmd4
        
        # 'ActSheet_x, 35] = myRS2.Source   '★★★
        myRS2 = 応用_顧客別_JCL_PGM_DSN_.get(JCL_NAME_SV,JOB_SEQ_SV,STEP_SEQ_SV)
        # DEBUG
        # print("■③JCL内PGM\r\n")
        if myRS2 == []:
            DSN情報なし時処理(ActSheet_x,data)
        else:

            for data2 in myRS2:
                # DEBUG
                # print("■③JCL_NAME_SV :["+str(JCL_NAME_SV)+"] JOB_SEQ_SV :["+str(JOB_SEQ_SV)+"] STEP_SEQ_SV :["+str(STEP_SEQ_SV)+"]\r\n")
                DSN情報有り時処理("JCL",data,data2)



def analysis1(conn,cursor):
    global 応用_顧客別_JCL_PGM_DSN_,入出力判定_IMSDB_,GET_PROC_PGM_,DATA_DSN別データ分類情報_,変数値補正_,Select_BMCP_PGM_,入出力判定_
#'20240214 ADD qian.e.wang
    global 入出力判定_ADABAS_
#'ADD END
    
    sql =   """\
        
            SELECT * FROM TEST_JCL_PROC_PGM関連設定
            """
            
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    
    print(len(df),"解析1")
    応用_顧客別_JCL_PGM_DSN_ = 応用_顧客別_JCL_PGM_DSN(conn,cursor)
    入出力判定_IMSDB_ = 入出力判定_IMSDB(conn,cursor)
#'20240214 ADD qian.e.wang
    入出力判定_ADABAS_ = 入出力判定_ADABAS(conn,cursor)
#'ADD END
    GET_PROC_PGM_ = GET_PROC_PGM(conn,cursor)
    DATA_DSN別データ分類情報_ = DATA_DSN別データ分類情報(conn,cursor)
    変数値補正_ = 変数値補正(conn,cursor)
    Select_BMCP_PGM_ = Select_BMCP_PGM(conn,cursor)
    入出力判定_ = 入出力判定(conn,cursor)

    for i in range(len(df)):
        data = df.iloc[i]
        解析処理(data)
    
    global ActSheet
    
    return ActSheet