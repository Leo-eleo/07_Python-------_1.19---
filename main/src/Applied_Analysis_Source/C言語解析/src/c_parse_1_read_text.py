# import re
from typing import Tuple


def get_after_char(line: str, index: int) -> str:
    if index + 1 >= len(line):
        return ""
    else:
        return line[index + 1]


def quotation_check(char: str, single_quotation: bool, double_quotation: bool, comment_flg: bool) -> Tuple[bool, bool]:
    if char == "'" and not double_quotation:
        single_quotation = not single_quotation
    if char == '"' and not single_quotation:
        double_quotation = not double_quotation
    if comment_flg:
        return False, False
    return single_quotation, double_quotation


def clear_comment(content: str) -> list[str]:
    # content = re.sub(r"/\*.*?\*/", "", content)
    single_quotation = double_quotation = comment_flg = False
    _content = ""
    # Multi Line Comment
    # replace /t to 4 space
    content = content.replace("\t", "    ")
    for i, char in enumerate(content):
        # quotation check
        single_quotation, double_quotation = quotation_check(char, single_quotation, double_quotation, comment_flg)
        # in quotation check
        if single_quotation or double_quotation:
            comment_flg = False
        else:
            # comment check
            if char == "/" and content[i + 1] == "*":
                comment_flg = True
            if char == "/" and content[i - 1] == "*":
                comment_flg = False
                continue
        # gen res
        if not comment_flg:
            _content = _content + char
    # Single Line Comment
    lines = _content.split("\n")
    for line_index, line in enumerate(lines):
        single_quotation = double_quotation = comment_flg = False
        _line = ""
        for char_index, char in enumerate(line):
            # quotation check
            single_quotation, double_quotation = quotation_check(char, single_quotation, double_quotation, comment_flg)
            # comment check
            if char == "/" and get_after_char(line, char_index) == "/":
                comment_flg = True
            # in quotation check
            if single_quotation or double_quotation:
                comment_flg = False
            if not comment_flg:
                _line = _line + char
            else:
                break
        lines[line_index] = _line
    return lines


# Warning! This function only work on SJIS
def remove_72_to_80(file: str) -> str:
    with open(file, "rb") as fr:
        crlf_flg = False
        file_bytes = fr.read()
        if b"\x0d\x0a" in file_bytes:
            crlf_flg = True
        split_bytes = b""
        if crlf_flg:
            # CRLF
            split_bytes = b"\x0d\x0a"
        else:
            # LF
            split_bytes = b"\x0a"
        lines_bytes = file_bytes.split(split_bytes)
        # remove 72 - 80
        # lines_bytes = [x[:72] for x in lines_bytes]
        lines = [x[:72].decode("CP932") + "\n" for x in lines_bytes]
        return "".join(lines)


def read_text(file: str, remove72: bool) -> list[list[str]]:
    res = []

    # Read
    content = ""
    if remove72:
        content = remove_72_to_80(file)
    else:
        with open(file, "r", encoding="CP932") as fr:
            content = fr.read()

    # Parse content
    lines = clear_comment(content)
    for i, line in enumerate(lines):
        tmp_sheet_gyo = [""] * 9
        if line.replace(" ", "") == "":
            行分類 = "空白行"
        else:
            行分類 = "通常行"
        # 行情報
        tmp_sheet_gyo[1] = 行分類
        # 行番号
        tmp_sheet_gyo[7] = i + 1
        # 行情報
        tmp_sheet_gyo[8] = line

        res.append(tmp_sheet_gyo)

    return res
