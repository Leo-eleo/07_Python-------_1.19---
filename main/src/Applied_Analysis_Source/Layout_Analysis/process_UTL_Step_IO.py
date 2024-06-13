#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

     
class UTL_STEP別_IO情報_DSNテーブル:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "UTL_STEP別_IO情報_DSNテーブル"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
        sql = "SELECT * FROM "+self.dbname + " ORDER BY JCL_NAME,JOB_SEQ,STEP_SEQ,IO DESC, DSN DESC"
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        keys = df.columns.tolist()
        
        for i in range(len(df)):
            data = df.iloc[i]
            
            jcl_name = data["JCL_NAME"]
            job_seq = data["JOB_SEQ"]
            job_id = data["JOB_ID"]
            step_seq = data["STEP_SEQ"]
            step_name = data["STEP名"]
            utility_id = data["Utility_ID"]
            
            if (jcl_name,job_seq,job_id,step_seq,step_name,utility_id) not in self.dic:
                self.dic[(jcl_name,job_seq,job_id,step_seq,step_name,utility_id)] = [[] for j in range(2)]
                
            dic = {key:data[key] for key in keys}
            if data["IO"] == "INPUT":
                self.dic[(jcl_name,job_seq,job_id,step_seq,step_name,utility_id)][0].append(dic)
            elif data["IO"] == "OUTPUT":
                self.dic[(jcl_name,job_seq,job_id,step_seq,step_name,utility_id)][1].append(dic)
        
        
    def get(self, jcl_name,job_seq,job_id,step_seq,step_name,utility_id):
        if self.dic == None:
            self.setup()
            
            
        if (jcl_name,job_seq,job_id,step_seq,step_name,utility_id) in self.dic:
            return self.dic[(jcl_name,job_seq,job_id,step_seq,step_name,utility_id)]
        else:
            return []
            
    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
     
 
def process_UTL_Step_IO_main(db_path,title):
    
    
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    
    #  Utility,ASM関連　同一レイアウト情報解析
    UTL_STEP別_IO情報_DSNテーブル_ = UTL_STEP別_IO情報_DSNテーブル(conn,cursor)
    
    sql = "SELECT DISTINCT JCL_NAME, JOB_SEQ, JOB_ID, STEP_SEQ, STEP名, Utility_ID,SYSIN FROM QRY_UTL_STEP別_IO情報_DSNテーブル"
    
    df = pd.read_sql(sql,conn)
    df.fillna("", inplace=True)
    
    ActSheet = []
    
    for i in range(len(df)):
        data = df.iloc[i]
        ActSheet_GYO = [""]*14
        out = [""]*3
        y = 0
        ActSheet_GYO[1] = data["JCL_NAME"]
        ActSheet_GYO[2] = data["JOB_SEQ"]
        ActSheet_GYO[3] = data["JOB_ID"]
        ActSheet_GYO[4] = data["STEP_SEQ"]
        ActSheet_GYO[5] = data["STEP名"]
        ActSheet_GYO[6] = data["Utility_ID"]
        
        myRS_all = UTL_STEP別_IO情報_DSNテーブル_.get(data["JCL_NAME"],data["JOB_SEQ"],data["JOB_ID"],data["STEP_SEQ"], data["STEP名"],data["Utility_ID"])
    
        if myRS_all == []:
            ActSheet_GYO[7] = "該当するデータは存在しません"
            ActSheet.append(ActSheet_GYO)
            continue
        
        ActSheet_GYO = [""]*14

        len_input = len(myRS_all[0])
        len_output = len(myRS_all[1])
        
        if len_input == 0 or len_output == 0:
            continue
        

        for myRS_in in myRS_all[0]:
            for myRS_out in myRS_all[1]:
                ActSheet_GYO = [""]*14
                ActSheet_GYO[1] = data["JCL_NAME"]
                ActSheet_GYO[2] = data["JOB_SEQ"]
                ActSheet_GYO[3] = data["JOB_ID"]
                ActSheet_GYO[4] = data["STEP_SEQ"]
                ActSheet_GYO[5] = data["STEP名"]
                ActSheet_GYO[6] = data["Utility_ID"]
                ActSheet_GYO[13] = data["SYSIN"]
                
                ActSheet_GYO[7] = myRS_in["DD名"]
                ActSheet_GYO[8] = myRS_in["IO"]
                # 'ActSheet_GYO[9] = ActSheet_GYO[9] & "_" & myRS["DSN"]
                ActSheet_GYO[9] = myRS_in["DSN"]
                
                ActSheet_GYO[10] = myRS_out["DD名"]
                ActSheet_GYO[11] = myRS_out["IO"]
                # 'ActSheet_GYO[12] = ActSheet_GYO[12] & "_" & myRS["DSN"]
                ActSheet_GYO[12] = myRS_out["DSN"]
                ActSheet.append(ActSheet_GYO)
                
            
        #     #'一旦解除
        #     #'DD連結（この場合のDD連結は複数のINPUTとOUTPUTが同じレイアウトである場合の対応なので対象PGMを限定する）　↓
        #     utility_id = data["Utility_ID"]
        #     if utility_id in  ("SORT","JSDGENER","XCPY0010"):
        #         y = y + 1

        #     if myRS["IO"] == "OUTPUT" and myRS["DD名"] != "":
        #         out[0] = myRS["DD名"]
        #         out[1] = myRS["IO"]
        #         out[2] = myRS["DSN"]
            
        #     if myRS["IO"] == "INPUT":
        #         if ActSheet_GYO[7] != "":
        #             ActSheet.append(ActSheet_GYO)
        #             ActSheet_GYO = [""]*14
        #             ActSheet_GYO[1] = data["JCL_NAME"]
        #             ActSheet_GYO[2] = data["JOB_SEQ"]
        #             ActSheet_GYO[3] = data["JOB_ID"]
        #             ActSheet_GYO[4] = data["STEP_SEQ"]
        #             ActSheet_GYO[5] = data["STEP名"]
        #             ActSheet_GYO[6] = data["Utility_ID"]
        #             # 'ActSheet_GYO[7] = ActSheet_GYO[7] & "_" & myRS["DD名"]
        #             ActSheet_GYO[7] = myRS["DD名"]
        #             ActSheet_GYO[8] = myRS["IO"]
        #             # 'ActSheet_GYO[9] = ActSheet_GYO[9] & "_" & myRS["DSN"]
        #             ActSheet_GYO[9] = myRS["DSN"]
                    
        #         else:
        #             ActSheet_GYO[7] = myRS["DD名"]
        #             ActSheet_GYO[8] = myRS["IO"]
        #             ActSheet_GYO[9] = myRS["DSN"]
                    
        #     elif myRS["IO"] == "OUTPUT":
            
        #         if ActSheet_GYO[10] != "":
        #             ActSheet.append(ActSheet_GYO)
        #             ActSheet_GYO = [""]*14
        #             ActSheet_GYO[1] = data["JCL_NAME"]
        #             ActSheet_GYO[2] = data["JOB_SEQ"]
        #             ActSheet_GYO[3] = data["JOB_ID"]
        #             ActSheet_GYO[4] = data["STEP_SEQ"]
        #             ActSheet_GYO[5] = data["STEP名"]
        #             ActSheet_GYO[6] = data["Utility_ID"]
                    
        #             # 'ActSheet_GYO[10] = ActSheet_GYO[10] & "_" & myRS["DD名"]
        #             ActSheet_GYO[10] = myRS["DD名"]
        #             ActSheet_GYO[11] = myRS["IO"]
        #             # 'ActSheet_GYO[12] = ActSheet_GYO[12] & "_" & myRS["DSN"]
        #             ActSheet_GYO[12] = myRS["DSN"]
        #         else:
        #             ActSheet_GYO[10] = myRS["DD名"]
        #             ActSheet_GYO[11] = myRS["IO"]
        #             ActSheet_GYO[12] = myRS["DSN"]
            
        #     # 'DD連結対応 ※2つ目以降のINPUTにSAVEしていたOUTPUT情報をセットする
        #     if utility_id in  ("SORT","JSDGENER","XCPY0010") and y > 2:
        #         ActSheet_GYO[10] = out[0]
        #         ActSheet_GYO[11] = out[1]
        #         ActSheet_GYO[12] = out[2]
                
        # ActSheet.append(ActSheet_GYO)
          
          
    # COBOL資産　同一レイアウト情報解析 
          
    sql = "SELECT DISTINCT JCL_NAME, JOB_SEQ, JOB_ID, STEP_SEQ, STEP_NAME, PGM_NAME,IN_DD,DSN1,OUT_DD,DSN2 FROM QRY_同一レイアウトモジュール_DSN②"
    
    df = pd.read_sql(sql,conn)
    df.fillna("", inplace=True)              
    print(len(df))
    for i in range(len(df)):
        data = df.iloc[i]
        ActSheet_GYO = [""]*14
        ActSheet_GYO[1] = data["JCL_NAME"]
        ActSheet_GYO[2] = data["JOB_SEQ"]
        ActSheet_GYO[3] = data["JOB_ID"]
        ActSheet_GYO[4] = data["STEP_SEQ"]
        ActSheet_GYO[5] = data["STEP_NAME"]
        ActSheet_GYO[6] = data["PGM_NAME"]
        ActSheet_GYO[7] = data["IN_DD"]
        ActSheet_GYO[8] = "INPUT"
        ActSheet_GYO[9] = data["DSN1"]
        ActSheet_GYO[10] = data["OUT_DD"]
        ActSheet_GYO[11] = "OUTPUT"
        ActSheet_GYO[12] = data["DSN2"]
        ActSheet.append(ActSheet_GYO)
        
    
        
            

    for i in range(len(ActSheet)):
        
        if ActSheet[i][13] == "":
            # 'IN-DSNとOUT-DSNの両方が空白だったら名寄せ対象外
            if ActSheet[i][9] == "" and ActSheet[i][12] == "":
                ActSheet[i][13] = "対象外：入出力DSN無"
                            
            # '入力DSNのみ空白
            elif ActSheet[i][9] == "":
                ActSheet[i][9] = "SYSIN"
                ActSheet[i][13] = "変更：入力DSN無→SYSIN"
            # '出力DSNのみ空白
            elif ActSheet[i][12] == "":
                ActSheet[i][13] = "対象外：出力DSN無(INTRDR または SYSOUT)"
                        
            # '入力DSN = 出力DSN
            elif ActSheet[i][9] == ActSheet[i][12]:
                ActSheet[i][13] = "対象外：入出力DSNが同じ"
        
            # '入力DSN = DUMMY
            elif ActSheet[i][9] == "DUMMY":
                ActSheet[i][13] = "対象外：入力DSNがDUMMY"
        
            # '通常パターン
            else:
                ActSheet[i][13] = "OK"
        
            
        else:
            ActSheet[i][13] = "対象外："+ LTrim(ActSheet[i][13])
            
            
    ActSheet_all = [actSheet[1:] for actSheet in ActSheet]
    print(len(ActSheet_all))
    output_header = ["JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP名","Utility_ID","INPUT_DD名","INPUT","INPUT_DSN","","","","除外STEP"]
    write_excel_multi_sheet("UTL_STEP別_IO情報(加工).xlsx",ActSheet_all,"UTL_STEP別_IO情報(加工)",title,output_header)
    
if __name__ == "__main__":
    process_UTL_Step_IO_main(sys.argv[1],sys.argv[2])