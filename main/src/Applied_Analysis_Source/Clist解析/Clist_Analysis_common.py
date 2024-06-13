import os
import pandas
import pyodbc
# import glob


def print_process_log(index, count, file, max):
    if len(os.path.basename(file)) > max:
        max = len(os.path.basename(file))
    print(f"\rAnalysis {index+1} / {count}, File: {os.path.basename(file).ljust(max, ' ')}", end="")
    return max


def get_base_setting(setting_path):
    condition_df = pandas.read_excel(setting_path, sheet_name="資産解析")
    # Get Base Setting
    for cond, val in zip(condition_df["項目"], condition_df["設定"]):
        if cond == "設定条件HIT関連情報出力（ｷｰID）":
            設定条件HIT情報出力 = val == "出力する"
        if cond == "設定条件HIT関連情報出力（分析ID）":
            分析条件HIT情報出力 = val == "出力する"
        if cond == "設定条件HIT関連情報出力（設計ID）":
            設計条件HIT情報出力 = val == "出力する"
        if cond == "設定条件HIT-NG情報出力":
            設定条件HIT_NG情報出力 = val == "出力する"
        if cond == "DB更新制御":
            IsDelete = val == "実行前に関連TABLEクリアする"
    return 設定条件HIT情報出力, 分析条件HIT情報出力, 設計条件HIT情報出力, 設定条件HIT_NG情報出力, IsDelete


def get_folder_list(folder):
    folder_list = []
    for root, dirs, files in os.walk(folder):
        for dir in dirs:
            if not dir == "":
                folder_list.append(os.path.join(root, dir))
    return folder_list

def get_file_list(folder):
    file_list = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if not file == "":
                file_list.append(os.path.join(root, file))
    return file_list

def get_setting_excel(excel_path, name):
    # name = "CLIST設定シート"
    sheet = pandas.read_excel(excel_path, sheet_name=name)
    sheet.fillna("", inplace = True)
    sheet = sheet.values.tolist()
    sheet = [[""] + row for row in sheet]
    return sheet


def connect_accdb(db_path_local):
    assert os.path.isfile(db_path_local), "file path is invalid : " + db_path_local
    conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                r'DBQ=' + db_path_local)
    conn = pyodbc.connect(conn_str, autocommit=False)
    return conn


def delete_db_table(conn):
    cmd1 = "DELETE FROM ⑪CLIST_関連資産"
    cmd2 = "DELETE FROM 共通_PGM_IO情報"
    cmd3 = "DELETE FROM 共通_資産解析_関連情報"
    cmd4 = "DELETE FROM 共通_PGM_IO情報"
    conn.execute(cmd1)
    conn.execute(cmd2)
    conn.execute(cmd3)
    conn.execute(cmd4)
    conn.commit()



def get_clist_call_key():
    key_list = [
        "SYSCALL",
        "EXEC",
        "CALL",
        "SUBMIT"
    ]
    return key_list

def get_4_RWords():
    RWords = [
        r"ATTN",
        r"CONTROL",
        r"DATA",
        r"ERROR",
        r"EXIT",
        r"GLOBAL",
        r"GOTO",
        r"NGLOBAL",
        r"PROC",
        r"RETURN",
        r"SYSCALL",
        r"SYSREF",
        r"TERMIN",
        r"WRITE",
        r"WRITENR",
        r"READ",
        r"READDVAL",
        r"SET",
        r"LISTDSI",
        r"DO",
        r"IF",
        r"SELECT",
        r"ELSE",
        r"END",
        r"CLOSFILE",
        r"GETFILE",
        r"OPENFILE",
        r"PUTFILE",
        r"EXEC",
        r"FREE",
        r"EXCEFI",
        r"AIMALLOC",
        r"AIMFREE",
        r"ALLOC",
        r"PRTFILE",
        r"DELETE",
        r"CALL",
        r"LIB",
        r"INDATA",
        r"SUBMIT",
        r"WRTMSG",
        r"CHKNMI",
        r"ALLOCATE",
        r"SEND",
        r"FIMPORT",
        r"FEXPORT",
        r"LPALLOC",
        r"EXCSCMD",
        r"ATTR",
        r"EVENT",
        r"DROP",
        r"INFDCT",
        r"WRITENR",
        r"DOCKF77",
        r"RESTART",
        r"JVEXMSP",
        r"%JVE0CHK1",
        r"%JVE0CHK3",
        r"%JVE0DLNL",
        r"COBOL",
        r"FORT77",
        r"CC",
        r"FCC",
        r"JYD2UTY1",
        r"JYD2UTY4",
        r"TSTYFRT",
        r"TESTCOB",
        r"TESTPLI",
        r"PUTPGMC",
        r"ADDPGMC"
    ]
    return RWords
