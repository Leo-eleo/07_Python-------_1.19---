#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


ファイル名 = ""
DD名 = ""
ファイル情報 = ""
レコード名 = ""
ファイル連番 = 0
スキーマ名 = ""
COPY句情報 = ""
エラーMSG = ""
OutSheet = []    
OutPut_folder = ""
                  
class QRY_COBOL_入出力情報:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "QRY_COBOL_入出力情報③"
        self.keys = []
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        self.keys = df.columns.tolist()
        for i in range(len(df)):
            data = df.iloc[i]
            cobol_id = data["COBOL_ID"]
            if cobol_id not in self.dic:
                self.dic[cobol_id] = []
                
            dic = {key:data[key] for key in self.keys}
            self.dic[cobol_id].append(dic)    
            
        
    def get(self,COBOL_ID):
        if self.dic == None:
            self.setup()
            
        if COBOL_ID in self.dic:
            return self.dic[COBOL_ID]

        else:
            return []
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        

class レベルレイアウト関連性設定:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "01レベルレイアウト関連性設定"
        self.keys = []
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
              
    def insert(self): 
        if self.dic == None:
            self.setup()
            
        global モジュール名,DD名,ファイル連番,スキーマ名
            
        key_list = ["COBOL","DD名","ファイル連番","レイアウト名"]
        value_list = [モジュール名,DD名,ファイル連番,スキーマ名]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
   
   
def 結果一覧出力():
    global モジュール名,DD名,ファイル連番,スキーマ名,ファイル名,ファイル情報,COPY句情報,エラーMSG,レコード名
    global OutSheet
    global レベルレイアウト関連性設定_
    
    OutSheet_gyo = [""]*10
    
    OutSheet_gyo[1] = モジュール名
    # 'OutSheet_gyo[1] = 入力ファイル名
    OutSheet_gyo[7] = スキーマ名
    
    OutSheet_gyo[2] = ファイル名
    OutSheet_gyo[3] = DD名
    OutSheet_gyo[4] = ファイル情報
    OutSheet_gyo[5] = レコード名
    OutSheet_gyo[6] = ファイル連番
    
    OutSheet_gyo[8] = COPY句情報
    OutSheet_gyo[9] = エラーMSG
            
    OutSheet.append(OutSheet_gyo)
    #  'データ資産DBに「01レベルレイアウト関連性設定」を自動出力
    レベルレイアウト関連性設定_.insert()
    
def TEXT_READ処理(file_path):
    TmpSheet = []
    with open(file_path,errors="ignore") as f:
        for line in f:
            line.rstrip()
            TmpSheet.append(line)
    return TmpSheet
 
def 有効行(行情報):

    if len(行情報) > 6 and 行情報[6] == " ":
        return True
    else:
        return False


def スキーマ明細行出力(tmp_layout):
    global OutPut_folder
    global モジュール名,DD名,ファイル連番,スキーマ名,ファイル名,ファイル情報,COPY句情報,エラーMSG,レコード名
    
    if tmp_layout == []:
        return 
    
    OutPut_Path = OutPut_folder + "\\" + スキーマ名
    with open(OutPut_Path,"w",newline='\n') as f:
        for line in tmp_layout:
            f.write(line)
    
    return 

def WORK_AREA_レイアウト情報出力処理(TmpSheet):

    # 'WORK領域まで検索対象行をスキップ
    検索行 = 0
    hit_flg = False
    while 検索行 < len(TmpSheet):
        対象行文字列 = TmpSheet[検索行]
        string_7_66 = Mid(対象行文字列,6,66)
        # 'if ②_有効行(対象行文字列) and InStr(対象行文字列, "WORKING-STORAGE" in string_7_66:    '必ずHITすることを想定
        # '01レベルの移送元、移送先が必ずしもWORK領域内の定義ではない場合があり、ファイルSECTIONからの検索に拡大する
        if 有効行(対象行文字列) and "FILE" in string_7_66 and "SECTION" in string_7_66:   #  '必ずHITすることを想定
           hit_flg = True
        
        検索行 = 検索行 + 1
        if hit_flg or 検索行 >= len(TmpSheet):
            break

    if hit_flg:
        
        chk_end = False
        対象ファイル有 = False  #'初期値は無
        chk_1st = True
        tmp_layout = []
        
        while 検索行 < len(TmpSheet):
            対象行文字列 = TmpSheet[検索行]
            string_7_66 = Mid(対象行文字列,6,66)
            if 有効行(対象行文字列):
                # '「01」ラベルとレコード名のキーワードは同一行にあることを想定
                # ' 変数のラベルは「01」であることを想定
                if " 01 " in string_7_66 and \
                   " " + レコード名 + "." in string_7_66 or " " + レコード名 + " " in string_7_66:
                    対象ファイル有 = True
                #    Set TSO = myFSO.CreateTextFile(Filename:=スキーマフォルダ + "\\" + スキーマ名, Overwrite:=True)
                    chk_end = False
                    while True:
                        if 有効行(対象行文字列):
                            if (" FD " in string_7_66) or (" SD " in string_7_66) or (" EJECT " in string_7_66): # 'QA管理表の0011管理番号を対応 (李)
                                # 'スキーマ情報終了
                                chk_end = True
                            elif " PROCEDURE " in string_7_66 and \
                                " DIVISION " in string_7_66:
                                # 'スキーマ情報終了
                                chk_end = True
                            elif " SECTION" in string_7_66:
                                # 'スキーマ情報終了
                                chk_end = True
                            elif" 01 " in  Mid(対象行文字列, 6, 6) and not (chk_1st):
                                # 'スキーマ情報終了(別の変数が出現したら出力終了)
                                chk_end = True
                            else:
                                tmp_layout.append(対象行文字列)
                                # Call ②_スキーマ明細行出力
                           
                        
                        検索行 = 検索行 + 1
                        chk_1st = False
                        if 検索行 >= len(TmpSheet) or chk_end:
                            break
                    
                        対象行文字列 = TmpSheet[検索行]
                        string_7_66 = Mid(対象行文字列,6,66)
                
            
            
            検索行 = 検索行 + 1
    #    'Loop Until InStr(Mid(対象行文字列, 7, 6), " 01 " in string_7_66 and InStr(Mid(対象行文字列, 7, 6), " 01 " in string_7_66 and ②_有効行(対象行文字列)
            if 検索行 >= len(TmpSheet) or chk_end:
                break
        スキーマ明細行出力(tmp_layout)

    if 対象ファイル有:
        pass
    else:
       エラーMSG = "WKレイアウト特定不能"
    
def WORK-STORAGE_レイアウト情報出力処理(TmpSheet):

    # 'WORK領域まで検索対象行をスキップ
    検索行 = 0
    hit_flg = False
    while 検索行 < len(TmpSheet):
        対象行文字列 = TmpSheet[検索行]
        string_7_66 = Mid(対象行文字列,6,66)
        # 'if ②_有効行(対象行文字列) and InStr(対象行文字列, "WORKING-STORAGE" in string_7_66:    '必ずHITすることを想定
        # '01レベルの移送元、移送先が必ずしもWORK領域内の定義ではない場合があり、ファイルSECTIONからの検索に拡大する
        if 有効行(対象行文字列) and "WORKING-STORAGE" in string_7_66 and "SECTION" in string_7_66:
           #  '必ずHITすることを想定
           hit_flg = True
        
        検索行 = 検索行 + 1
        if hit_flg or 検索行 >= len(TmpSheet):
            break

    if hit_flg:
        
        chk_end = False
        対象ファイル有 = False  #'初期値は無
        chk_1st = True
        tmp_layout = []
        
        while 検索行 < len(TmpSheet):
            対象行文字列 = TmpSheet[検索行]
            string_7_66 = Mid(対象行文字列,6,66)
            if 有効行(対象行文字列):
                # '「01」ラベルとレコード名のキーワードは同一行にあることを想定
                # ' 変数のラベルは「01」であることを想定
                if " 01 " in string_7_66 and \
                   " " + レコード名 + "." in string_7_66 or " " + レコード名 + " " in string_7_66:
                    対象ファイル有 = True
                #    Set TSO = myFSO.CreateTextFile(Filename:=スキーマフォルダ + "\\" + スキーマ名, Overwrite:=True)
                    chk_end = False
                    while True:
                        if 有効行(対象行文字列):
                            if (" FD " in string_7_66) or (" SD " in string_7_66) or (" EJECT " in string_7_66): # 'QA管理表の0011管理番号を対応 (李)
                                # 'スキーマ情報終了
                                chk_end = True
                            elif " PROCEDURE " in string_7_66 and \
                                " DIVISION " in string_7_66:
                                # 'スキーマ情報終了
                                chk_end = True
                            elif " SECTION" in string_7_66:
                                # 'スキーマ情報終了
                                chk_end = True
                            elif" 01 " in  Mid(対象行文字列, 6, 6) and not (chk_1st):
                                # 'スキーマ情報終了(別の変数が出現したら出力終了)
                                chk_end = True
                            else:
                                tmp_layout.append(対象行文字列)
                                # Call ②_スキーマ明細行出力
                           
                        
                        検索行 = 検索行 + 1
                        chk_1st = False
                        if 検索行 >= len(TmpSheet) or chk_end:
                            break
                    
                        対象行文字列 = TmpSheet[検索行]
                        string_7_66 = Mid(対象行文字列,6,66)
                
            
            
            検索行 = 検索行 + 1
    #    'Loop Until InStr(Mid(対象行文字列, 7, 6), " 01 " in string_7_66 and InStr(Mid(対象行文字列, 7, 6), " 01 " in string_7_66 and ②_有効行(対象行文字列)
            if 検索行 >= len(TmpSheet) or chk_end:
                break
        スキーマ明細行出力(tmp_layout)

    if 対象ファイル有:
        pass
    else:
       エラーMSG = "WKレイアウト特定不能"

def スキーマファイル出力(TmpSheet):
  
    global モジュール名,DD名,ファイル連番,スキーマ名,ファイル名,ファイル情報,COPY句情報,エラーMSG,レコード名

    対象ファイル有 = False  #'初期値は無
 
    検索行 = 0
    chk_end = False
    chk_1st = True
    
    while 検索行 < len(TmpSheet):
        対象行文字列 = TmpSheet[検索行]
        # 'コメント行はSKIP (シート2列目は処理済チェック欄)
        if 有効行(対象行文字列) == False:
            検索行 += 1
            continue
        
        string_7_66 = Mid(対象行文字列,6,66)
        
        if (" FD " in string_7_66 or " SD " in string_7_66) and \
            " " + ファイル名 in string_7_66:
                
            #   '01レベルキーワードがでるまで検索
            while 検索行 < len(TmpSheet):
                検索行 = 検索行 + 1     #'FD句と同一行には01レベルキーワードは発生しない前提
                対象行文字列 = TmpSheet[検索行]
                string_7_66 = Mid(対象行文字列,6,66)
                #'if " 01 " in string_7_66:
                if " 01 " in Mid(対象行文字列, 6, 6) or \
                    " 1 " in Mid(対象行文字列, 6, 6): # '誤検知防止対応→01レベルは 7-10 列目から始まるはず (RECORD CONTAIN句内に「01」キーワードがある場合がある)
                    対象ファイル有 = True
                # ' V1.1.1 対応 START *** 01 レベルキーワードがなかった場合の処理 ***
                elif (" FD " in string_7_66) or (" SD " in string_7_66) or (" EJECT " in string_7_66):  #'QA管理表の0011管理番号を対応 (李)
                    break
                elif " SECTION" in string_7_66:
                    break
                elif " WORKING-STORAGE " in string_7_66:
                    break
                elif " PROCEDURE " in string_7_66:
                    break
                elif " DIVISION " in string_7_66:
                    break
                # ' V1.1.1 対応 END

                if " 01 " in Mid(対象行文字列, 6, 6) and 有効行(対象行文字列):
                    break
                
            if 対象ファイル有:
                # Set TSO = myFSO.CreateTextFile(Filename:=スキーマフォルダ + "\" + スキーマ名, Overwrite:=True)
                
                chk_end = False
                tmp_layout = []
                while True:
                    if 有効行(対象行文字列):
                    
                        if (" FD " in string_7_66) or (" SD " in string_7_66) or (" EJECT " in string_7_66):  #'QA管理表の0011管理番号を対応 (李)
                            # 'スキーマ情報終了
                            chk_end = True
                        elif " SECTION" in string_7_66:
                            # 'スキーマ情報終了
                            chk_end = True
                        elif " WORKING-STORAGE " in string_7_66:
                            # 'スキーマ情報終了
                            chk_end = True
                        elif " PROCEDURE " in string_7_66:
                            # 'スキーマ情報終了
                            chk_end = True
                        elif " DIVISION " in string_7_66:
                            # 'スキーマ情報終了
                            chk_end = True
                        # 'elif " 01 " in string_7_66 and \ot (chk_1st):
                        elif " 01 " in Mid(対象行文字列, 6, 6) and not (chk_1st):
                            # '複数01レベル対応
                            # TSO.Close
                            # Set TSO = Nothing
                            結果一覧出力()
                            スキーマ明細行出力(tmp_layout)
                            tmp_layout = []
                            tmp_layout.append(対象行文字列)
                            ファイル連番 = ファイル連番 + 1
                            
                            レコード名 = Mid(対象行文字列, 7, 65).replace("01", "").replace(" ", "").replace(".", "")
                            # 'スキーマ名 = モジュール名 + "_" + ファイル名 + "_" + Format(ファイル連番, "00") + ".scm"
                            スキーマ名 = モジュール名 + "_" + DD名 + "_" + str(ファイル連番).zfill(2) + ".scm"
                            # Set TSO = myFSO.CreateTextFile(Filename:=スキーマフォルダ + "\" + スキーマ名, Overwrite:=True)
                           
                        else:
                            # 'スキーマ情報継続
                            tmp_layout.append(対象行文字列)
         
                    検索行 = 検索行 + 1
                    chk_1st = False
                    if 検索行 >= len(TmpSheet) or chk_end:
                        break
                    
                    対象行文字列 = TmpSheet[検索行]
                    string_7_66 = Mid(対象行文字列,6,66)
                
                スキーマ明細行出力(tmp_layout)
                tmp_layout = []
                
            else:
                chk_end = True
     
        検索行 = 検索行 + 1
        
        if chk_end:
            break
    
    if 対象ファイル有:
        pass
    else:
       エラーMSG = "レイアウト特定不能"

    
def main(db_path, Folder_COBOL_path, Output_folder_path):

    global モジュール名,DD名,ファイル連番,スキーマ名,ファイル名,ファイル情報,COPY句情報,エラーMSG,レコード名
    global レベルレイアウト関連性設定_
    global OutPut_folder 
    print("start preparation for analysis.")
    
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    sql,_ = make_delete_sql("01レベルレイアウト関連性設定",[],[])
    cursor.execute(sql)
    
    QRY_COBOL_入出力情報_ = QRY_COBOL_入出力情報(conn,cursor)
    レベルレイアウト関連性設定_ = レベルレイアウト関連性設定(conn,cursor)
    COBOL_Files = glob_files(Folder_COBOL_path)
    OutPut_folder = Output_folder_path
    OutSheet = []

    for file_path in COBOL_Files:
        cobol_file = get_filename(file_path)
        cobol_file,_,_,モジュール名 = GetFileInfo(cobol_file)
        myRS = QRY_COBOL_入出力情報_.get(モジュール名) 
        
        if myRS == []:
            ファイル名 = ""
            DD名 = ""
            ファイル情報 = ""
            レコード名 = ""
            ファイル連番 = 0
            スキーマ名 = ""
            COPY句情報 = ""
            エラーMSG = "COBOL解析情報無"
            結果一覧出力()

            continue
        
        TmpSheet = TEXT_READ処理(file_path)
        
        for data in myRS:
            
            ファイル名 = data["SELECT_ID"]
            DD名 = data["ASSIGN_ID"]
            ファイル情報 = data["LINE_INFO"]
            レコード名 = data["RECORD_ID"]
            COPY句情報 = data["COPY"]
            エラーMSG = ""
            ファイル連番 = 1
            
            if COPY句情報 != "WORK領域":
                # '通常のレイアウト情報を出力する（FD句またはSD句）
                # 'スキーマ名 = モジュール名 + "_" + ファイル名 + "_" + Format(ファイル連番, "00") + ".scm"
                スキーマ名 = モジュール名 + "_" + DD名 + "_" + str(ファイル連番).zfill(2) + ".scm"
                スキーマファイル出力(TmpSheet)
                結果一覧出力()
            else:
            # '【手動】で解析したWORK領域のレイアウトを検索・出力する
            #     'レコード名 = DD名
                if レコード名 != "":
                    # 'スキーマ名 = モジュール名 + "_" + ファイル名 + "_WK_" + レコード名 + ".scm"
                    スキーマ名 = モジュール名 + "_" + DD名 + "_WK_" + レコード名 + ".scm"
                    WORK_AREA_レイアウト情報出力処理(TmpSheet)
                    結果一覧出力()
             
        # OutSheet = [outsheet[1:] for outsheet in OutSheet]
        # write_excel_multi_sheet("01レベルレイアウト出力結果.xlsx",OutSheet,"01レベルレイアウト出力結果","",["COBOL資産","ファイル名","DD名","ファイル情報","レコード名","ファイル連番","スキーマ名","COPY句情報","エラー情報"])
    
if __name__ == "__main__":     
    main(sys.argv[1],sys.argv[2],sys.argv[3])