import glob
import os
from typing import Tuple
import pandas
import pyodbc
import shutil

from loguru import logger

SPLIT_CHAR = [
    " ",
    ";",
    "(",
    ")",
    "=",
    ",",
    ":",
    "+",
    "-",
    "*",
    "%",
    "/",
    "<",
    ">",
    "{",
    "}",
    "&",
    "|",
    "!",
    "^",
    "~",
    "?",
]

SPLIT_CHAR2 = ["{", "}", ";"]
# SPLIT_CHAR2 = ["{", ";"]

C_KEY_WORD = [
    "auto",
    "break",
    "case",
    "char",
    "const",
    "continue",
    "default",
    "do",
    "double",
    "else",
    "enum",
    "extern",
    "float",
    "for",
    "goto",
    "if",
    "int",
    "long",
    "register",
    "return",
    "short",
    "signed",
    "sizeof",
    "static",
    "struct",
    "switch",
    "typedef",
    "union",
    "unsigned",
    "void",
    "volatile",
    "while",
]

C_PRE_PROCESS = [
    "#define",
    "#include",
    "#undef",
    "#ifdef",
    "#ifndef",
    "#if",
    "#else",
    "#elif",
    "#endif",
    "#error",
    "#pragma",
]


class Setting_EXCEL:
    設定条件HIT情報出力 = False
    分析条件HIT情報出力 = False
    設計条件HIT情報出力 = False
    設定条件HIT_NG情報出力 = False
    PLI入出力情報出力 = False
    IsDelete = False
    言語解析_path = False
    字句解析_path = False
    トークン解析_path = False
    言語解析_out = False
    字句解析_out = False
    トークン解析_out = False


def make_insert_sql(DBNAME, value_iist, key_list) -> Tuple[str, tuple]:
    keys = "[" + "],[".join(key_list) + "]"
    values = []
    for v in value_iist:
        if v == None:
            v = ""
        values.append(str(v))
    values = tuple(values)
    value = "?," * (len(values) - 1) + "?"
    sql = "INSERT INTO " + DBNAME + "(" + keys + ")" + "VALUES (" + value + ")"
    return sql, values


def insert_COBOL_基本情報(
    cursor: pyodbc.Cursor, file_name: str, lib: str, gouki: str, member: str, length: int, file_io: str, have_sql: str
):
    key_list = [
        "資産ID",
        "LIBRARY_ID",
        "メンバ名",
        "モジュール名",
        "CMD行数",
        "解析結果",
        "ファイルIO有無",
        "PARM有無",
        "サブルーチン有無",
        "SQL有無",
        "画面有無",
    ]
    value_list = [
        file_name,
        lib,
        member,
        gouki,
        length,
        "NOT CHECK",
        file_io,
        "",
        "",
        have_sql,
        "",
    ]
    sql, val = make_insert_sql("②COBOL_基本情報", value_list, key_list)
    cursor.execute(sql, val)


def insert_COBOL_関連資産(cursor: pyodbc.Cursor, file_name: str, member: str, fn: str, target: str, args: str):
    key_list = ["資産ID", "COBOL_ID", "関連区分", "関連資産", "関連資産_TRANID"]
    value_list = [file_name, member, fn, target, args]
    sql, val = make_insert_sql("②COBOL_関連資産", value_list, key_list)
    cursor.execute(sql, val)


def insert_COBOL_CMD情報(
    cursor: pyodbc.Cursor, file_name: str, member: str, line_no: int, parm: str, cmd: int, cmd_type: str
):
    key_list = [
        "資産ID",
        "COBOL_ID",
        "CMD_SEQ",
        "元資産行情報",
        "記述領域",
        "段落",
        "分岐判定",
        "CMD分類",
        "PARM",
        "行CHK結果",
    ]
    value_list = [
        file_name,
        member,
        cmd,
        line_no,
        "-",
        "-",
        "-",
        cmd_type,
        parm,
        "-",
    ]
    sql, val = make_insert_sql("②COBOL_CMD情報", value_list, key_list)
    cursor.execute(sql, val)


def insert_共通_PGM_IO情報(cursor: pyodbc.Cursor, lib: str, file_name: str, io: str, file: str):
    key_list = ["資産分類", "LIBRARY_ID", "資産ID", "入出力区分", "ファイル名"]
    value_list = ["C", lib, file_name, io, file]
    sql, val = make_insert_sql("共通_PGM_IO情報", value_list, key_list)
    cursor.execute(sql, val)


def insert_COBOL_入出力情報1(
    cursor: pyodbc.Cursor, file_name: str, member: str, select_id: str, assign_id: str, line_no: int
):
    key_list = ["資産ID", "COBOL_ID", "SELECT_ID", "ASSIGN_ID", "LINE_INFO"]
    value_list = [file_name, member, select_id, assign_id, line_no]
    sql, val = make_insert_sql("②COBOL_入出力情報1", value_list, key_list)
    cursor.execute(sql, val)


def pre_process(setting_path: str) -> Setting_EXCEL:
    _set = Setting_EXCEL()
    condition_df = pandas.read_excel(setting_path, sheet_name="資産解析")
    for cond, val in zip(condition_df["項目"], condition_df["設定"]):
        if cond == "設定条件HIT関連情報出力（ｷｰID）":
            _set.設定条件HIT情報出力 = val == "出力する"
        if cond == "設定条件HIT関連情報出力（分析ID）":
            _set.分析条件HIT情報出力 = val == "出力する"
        if cond == "設定条件HIT関連情報出力（設計ID）":
            _set.設計条件HIT情報出力 = val == "出力する"
        if cond == "設定条件HIT-NG情報出力":
            _set.設定条件HIT_NG情報出力 = val == "出力する"
        if cond == "COBOL入出力関連情報出力":
            _set.PLI入出力情報出力 = val == "出力する"
        if cond == "DB更新制御":
            _set.IsDelete = val == "実行前に関連TABLEクリアする"
        if cond == "結果出力フォルダ1":
            _set.言語解析_path = val
        if cond == "結果出力フォルダ1":
            _set.字句解析_path = val
        if cond == "結果出力フォルダ1":
            _set.トークン解析_path = val
        if cond == "結果ファイル出力制御（ソースコード）":
            _set.言語解析_out = val == "出力する"
        if cond == "結果ファイル出力制御（字句解析用）":
            _set.字句解析_out = val == "出力する"
        if cond == "結果ファイル出力制御（ﾄｰｸﾝ再構成用）":
            _set.トークン解析_out = val == "出力する"
    return _set


def connect_accdb(db_path):
    assert os.path.isfile(db_path), "file path is invalid : " + db_path
    conn_str = r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" r"DBQ=" + db_path
    conn = pyodbc.connect(conn_str, autocommit=False)
    return conn


def clear_db(db_base_path: str) -> None:
    print("you chose to clear db, so clear the remaining data.")
    conn = connect_accdb(db_base_path)
    cursor = conn.cursor()
    sql = "DELETE FROM ②COBOL_入出力情報1"
    cursor.execute(sql)
    sql = "DELETE FROM ②COBOL_入出力情報2"
    cursor.execute(sql)
    sql = "DELETE FROM ②COBOL_入出力情報3"
    cursor.execute(sql)
    sql = "DELETE FROM ②COBOL_関連資産"
    cursor.execute(sql)
    sql = "DELETE FROM ②COBOL_CMD情報"
    cursor.execute(sql)
    sql = "DELETE FROM ②COBOL_基本情報"
    cursor.execute(sql)
    sql = "DELETE FROM 共通_PGM_IO情報"
    cursor.execute(sql)
    # HIT時関連情報削除
    sql = "DELETE FROM 共通_資産解析_関連情報"
    cursor.execute(sql)
    # HIT-NG時関連情報削除
    sql = "DELETE FROM 共通_資産解析_NG情報"
    cursor.execute(sql)
    conn.commit()
    conn.close()


def glob_files(path, glob_type="file", recursive=False) -> list[str] | None:
    assert os.path.exists(path), "file path is invalid : " + path
    files = glob.glob(path + "/**", recursive=recursive)
    if glob_type == "file":
        return [p for p in files if os.path.isfile(p)]
    elif glob_type == "folder":
        return [p for p in files if os.path.isdir(p)]


def gen_new_db(
    source: str, target: str, db_number: int, folder_name: str
) -> Tuple[pyodbc.Connection, pyodbc.Cursor, str]:
    target_db = os.path.join(target, f"言語解析DB_{folder_name}_{db_number}.accdb")
    shutil.copy2(source, target_db)
    logger.info(f"Create the new accdb file [{target_db}]")
    _conn = connect_accdb(target_db)
    _cursor = _conn.cursor()
    return _conn, _cursor, target_db


def check_db_size(target_db: str) -> bool:
    if os.path.getsize(target_db) > 1500000000:
        logger.warning("DB size too large!")
        return False
    else:
        return True


def get_lib_gouki_member(file_name: str) -> Tuple[str, str, str]:
    name, _ = os.path.splitext(file_name)
    split = name.split("%")
    if len(split) < 3:
        return "A", "A", name
    else:
        return split[0], split[1], split[2]


def read_excel(_path: str, _sheet: str, _header=0) -> Tuple[list[str], list[list[str]]]:
    read_sheet = pandas.read_excel(_path, sheet_name=_sheet, header=_header)
    read_sheet.fillna("", inplace=True)
    return read_sheet.columns.tolist(), read_sheet.values.tolist()


def gen_c_call_functions(setting: str) -> dict[str, list[str]]:
    res: dict[str, list[str]] = {}
    _, val = read_excel(setting, "組み込み関数_C")
    for row in val:
        res.setdefault(row[0], [])
        res[row[0]].append(row[1])
    return res
