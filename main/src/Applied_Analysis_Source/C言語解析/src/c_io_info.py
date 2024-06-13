import pyodbc
import c_utiles


def replace_dd_2_empty(io_info: list[list[str]]):
    for row in io_info:
        for index, item in enumerate(row):
            if "dd:" in str(item) or "DD:" in str(item):
                row[index] = item.replace("dd:", "").replace("DD:", "")


def gen_io_info(io_info_list: list[list[str]]) -> list[dict[str, str]]:
    _res: list[dict[str, str]] = []
    for row in io_info_list:
        fopen_index = row.index("fopen")
        _res.append({"select_id": row[fopen_index - 2], "assign_id": row[fopen_index + 2], "line_no": row[1]})
    return _res


def io_info_insert(cursor: pyodbc.Cursor, file_name: str, io_info: list[list[str]]):
    lib, _, member = c_utiles.get_lib_gouki_member(file_name)

    # for SMBC, will replace "dd:" and "DD:" to ""
    replace_dd_2_empty(io_info)

    # get select_id and assign_id
    io_details = gen_io_info(io_info)

    # DB insert
    for item in io_details:
        # 共通_PGM_IO情報
        c_utiles.insert_共通_PGM_IO情報(cursor, lib, file_name, "IO", item["select_id"])
        # 入出力情報1
        c_utiles.insert_COBOL_入出力情報1(
            cursor, file_name, member, item["select_id"], item["assign_id"], item["line_no"]
        )
