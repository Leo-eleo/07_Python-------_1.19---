import pyodbc
import c_utiles


def func_call_check(fn: str, c_call_fn: dict[str, list[str]], include: list[str]) -> bool:
    if fn in c_call_fn:
        for define_file in c_call_fn[fn]:
            if define_file == "-":
                return True
            elif define_file in include:
                return True
    return False


def is_call_file_include(define_files: list[str], include: list[str]) -> str:
    for define_file in define_files:
        if define_file == "-":
            return "-"
        elif define_file in include:
            return define_file
    return ""


def get_fn_args(fn: str, line_no: int, tokens_list: list[list[str]]) -> str:
    arg: list[str] = []
    line = tokens_list[line_no]
    for token in line[line.index(fn) + 1 :]:
        arg.append(token)
        if token == ")":
            break
    return " ".join(arg)


def structure(
    file_name: str,
    tokens_list: list[list[str]],
    inner_fn: dict[int, str],
    cursor: pyodbc.Cursor,
    c_call_fn: dict[str, list[str]],
    include: list[str],
    io_info: list[list[str]],
):
    lib, gouki, member = c_utiles.get_lib_gouki_member(file_name)

    # 基本情報
    file_io = ""
    have_sql = ""
    if len(io_info) > 0:
        file_io = "●"

    # CMD情報 Insert
    cmd_count = 0
    for index, tokens in enumerate(tokens_list):
        cmd_count = cmd_count + 1
        # CALL Check
        if index in inner_fn:
            if func_call_check(inner_fn[index], c_call_fn, include):
                tokens[0] = "CALL"
        # EXEC Check
        if tokens[2] == "EXEC":
            tokens[0] = "EXEC"
            have_sql = "●"
        # CMD情報 Insert
        c_utiles.insert_COBOL_CMD情報(cursor, file_name, member, tokens[1], " ".join(tokens[2:]), cmd_count, tokens[0])

    # 関連資産 Insert
    for line_no, fn in inner_fn.items():
        # function in settings
        if fn in c_call_fn:
            # file is included
            call_file = is_call_file_include(c_call_fn[fn], include)
            if not call_file == "":
                args = get_fn_args(fn, line_no, tokens_list)
                c_utiles.insert_COBOL_関連資産(cursor, file_name, member, fn, call_file, args)

    # 基本情報 Insert
    c_utiles.insert_COBOL_基本情報(cursor, file_name, lib, gouki, member, len(tokens_list), file_io, have_sql)
