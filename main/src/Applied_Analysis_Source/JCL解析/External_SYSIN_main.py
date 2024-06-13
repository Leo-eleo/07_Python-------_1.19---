#!/usr/bin/env python
# -*- coding: cp932 -*-

import numpy as np
from analysis_0 import analysis_0
from make_JCL_relations import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

def main(db_path,Folder_SYSIN_path,excel_path):
    
    
    print("start preparation for analysis.")
    
    condition_df = pd.read_excel(excel_path,sheet_name="資産解析")
    for cond,val in zip(condition_df["項目"],condition_df["設定"]):
        if cond == "DB更新制御":
            IsDelete = val == "実行前に関連TABLEクリアする"
            
        if cond == "解析結果エクセル出力先":
            title = val
            
    if os.path.isdir(title) == False:
        os.makedirs(title)
    
    SYSIN_Files = glob_files(Folder_SYSIN_path)
    SYSIN_FILE_dic = {}
    for SYSIN_File in SYSIN_Files:
        fileName = get_filename(SYSIN_File)
        SYSIN_FILE_dic[fileName] = SYSIN_File
    
    df_sheet_all = pd.read_excel(excel_path, sheet_name=None)
    df_sheet_list = df_sheet_all.keys()

    ### get the list of members
    sheet_members = df_sheet_all["settings"]["メンバ一覧"]
    for sheet in sheet_members:
        if sheet not in df_sheet_list:
            continue
        
        df_member = df_sheet_all[sheet]
        update_member_list(df_member)

    for sheet in df_sheet_list:
        if "資産分類不足情報" not in sheet:
            continue
        df = df_sheet_all[sheet]

        update_member_list2(df)
        
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    df_sheet_list = []
    # データベースに含まれるテーブルを取得します
    for table_info in cursor.tables(tableType='TABLE'):
        df_sheet_list.append(table_info.table_name)
    

    ### get the list of which source is proc_parm
    sheet_proc_parm = df_sheet_all["settings"]["PROC_PARM"]
    for sheet in sheet_proc_parm:
        if sheet not in df_sheet_list:
            continue
        
        sql = "SELECT * FROM "+sheet
        df = pd.read_sql(sql,conn)
        df.replace("", np.nan,inplace=True)
        update_proc_parm_dic(df)            
            
            
            
    ### get the list of which source is internal proc
    sheet_basic_info = df_sheet_all["settings"]["JCL_基本情報"]
    for sheet in sheet_basic_info:
        if sheet not in df_sheet_list:
            continue

        sql = "SELECT * FROM "+sheet
        df = pd.read_sql(sql,conn)
        df.replace("", np.nan,inplace=True)
        
        update_internal_proc_list(df[df.JCL分類 == "内部PROC"])
        
    
    ### get the list of which source is jcl cmd info
    sheet_cmd_info = df_sheet_all["settings"]["JCL_CMD情報"]
    for sheet in sheet_cmd_info:
        if sheet not in df_sheet_list:
            continue

        sql = "SELECT * FROM "+sheet
        df = pd.read_sql(sql,conn)
        df.replace("", np.nan,inplace=True)
        update_jobproc_list(df[df.DD_NAME == "JOBPROC"])

    
    has_relation_proc_set = set()
    ### get the list of jcl step info
    sheet_step = df_sheet_all["settings"]["JCL_STEP情報"]
    for sheet in sheet_step:
        if sheet not in df_sheet_list:
            continue
        
        sql = "SELECT * FROM "+sheet
        df = pd.read_sql(sql,conn)
        df.replace("", np.nan,inplace=True)
        has_relation_proc_set = update_step_info(df,has_relation_proc_set)


    
    if IsDelete == True:
        print("you chose to clear db, so clear the remaining data.")
        sql,values = make_delete_sql("①JCL_STEP_SYSIN2",[],[])
        cursor.execute(sql,values)
        conn.commit()
    
    print("finish preparation and start analysis.")
    
    sql = "SELECT * FROM ①JCL_PGM_DSN WHERE SYSIN <> ''"
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    
    
    ActSheet = []
    ld = len(df)
    for i in range(len(df)):
        print("\r","analysis finished",i,"/",ld,end="")
        data = df.iloc[i]
        SYSINSheet_GYO = [""]*15
        SYSINSheet_GYO[1] = data["LIBRARY_ID"]
        SYSINSheet_GYO[2] = data["JCL_NAME"]
        SYSINSheet_GYO[3] = data["JOB_SEQ"]
        SYSINSheet_GYO[4] = data["JOB_ID"]
        SYSINSheet_GYO[5] = data["STEP_SEQ"]
        SYSINSheet_GYO[6] = data["STEP_NAME"] 
        SYSINSheet_GYO[7] = data["PGM_NAME"]
        SYSINSheet_GYO[8] = data["PROC_NAME"]
        SYSINSheet_GYO[9] = data["SYSIN_PGM"] 
        SYSINSheet_GYO[10] = data["DD_NAME"]
        SYSINSheet_GYO[14] = "OK"
        

        
        # ' 20220109 ADD 外部SYSIN号機情報追加START
        Str_号機 = ""
        JCL_NAME = data["JCL_NAME"]
        JCL_NAME = take_extensions(JCL_NAME)
        JCL_NAME_Split = JCL_NAME.split("%")
        # ' JCL_NAMEより号機情報取得
        if len(JCL_NAME_Split) > 2:
            Str_号機 = JCL_NAME_Split[1]
        # ' 号機情報判定の優先順
        # ' 1.実行JCLと同じ号機
        # ' 2.系統が同じ号機⇒例)Aなら(A,B) Vなら(V,X,Y)
    
        dsn = data["DSN"]
        sysin = data["SYSIN"]
        
        dsn_list = get_variable2(JCL_NAME,dsn)
        sysin_list = get_variable2(JCL_NAME,sysin)
        

        for dsn,dsn_source in dsn_list:
            for sysin,sysin_source in sysin_list:
                if dsn_source != "" and sysin_source != "" and dsn_source != sysin_source:
                    continue
        
                SYSIN文字列 = dsn + "%" + Str_号機 + "%" + sysin + ".txt"
                L_ファイル名 = SYSIN_FILE_dic.get(SYSIN文字列,"")   #  '指定されたフォルダー名を取り出す
                if L_ファイル名 == "":
                    SYSIN文字列 = dsn + "%" + Str_号機 + "%" + sysin + ".TXT"
                    # SYSIN文字列 = sysin + ".TXT"
                    L_ファイル名 = SYSIN_FILE_dic.get(SYSIN文字列,"") 
                # if Str_号機 == "A":
                #     if L_ファイル名 == "":
                #         SYSIN文字列 =dsn + "%" + "B" + "%" + sysin + ".txt"
                #         L_ファイル名 = SYSIN_FILE_dic.get(SYSIN文字列,"")   # '指定されたフォルダー名を取り出す
                # if Str_号機 == "V":
                #     if L_ファイル名 == "":
                #         SYSIN文字列 =dsn + "%" + "X" + "%" + sysin + ".txt"
                #         L_ファイル名 = SYSIN_FILE_dic.get(SYSIN文字列,"")   # '指定されたフォルダー名を取り出す
                #         if L_ファイル名 == "":
                #             SYSIN文字列 =dsn + "%" + "Y" + "%" + sysin + ".txt"
                #             L_ファイル名 = SYSIN_FILE_dic.get(SYSIN文字列,"")   # '指定されたフォルダー名を取り出す
                
                #' 20220412 完全一致のみにするためそれ以外はなし
                
                SYSINSheet_GYO_TEMP = SYSINSheet_GYO[:]
                SYSINSheet_GYO_TEMP[11] = dsn
                SYSINSheet_GYO_TEMP[13] = sysin
                if L_ファイル名 != "":
                    SYSINSheet_GYO_TEMP = analysis_0(SYSINSheet_GYO_TEMP,L_ファイル名,conn,cursor)
                else:
                    SYSINSheet_GYO_TEMP[14] = "対象ファイル無" + "(" +  SYSIN文字列 + ")"
                ActSheet.append(SYSINSheet_GYO_TEMP) 
            
            
    ActSheet_all = [actSheet[1:] for actSheet in ActSheet]
    output_header = ["LIBRARY_ID","JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","SYSIN_PGM","DD_NAME","DSN","GDG","SYSIN","処理結果"]
    write_excel_multi_sheet("外部SYSIN取り込み.xlsx",ActSheet_all,"取り込みSYSIN",title,output_header)


if __name__ == "__main__":    
    main(sys.argv[1],sys.argv[2],sys.argv[3])