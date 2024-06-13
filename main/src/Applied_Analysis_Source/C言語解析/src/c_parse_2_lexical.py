from typing import Tuple
from c_utiles import SPLIT_CHAR


def split_char_check(char1: str, char2: str, char3: str) -> bool:
    if char1 in SPLIT_CHAR:
        return True


def quotation_check(char: str, single_quotation: bool, double_quotation: bool) -> Tuple[bool, bool]:
    if char == "'" and not double_quotation:
        single_quotation = not single_quotation
    if char == '"' and not single_quotation:
        double_quotation = not double_quotation
    return single_quotation, double_quotation


def get_char123(text: str, index: int) -> Tuple[str, str, str]:
    _char = text[index]
    if not index + 1 >= len(text):
        _char2 = text[index + 1]
    else:
        _char2 = ""
    if not index + 2 >= len(text):
        _char3 = text[index + 2]
    else:
        _char3 = ""
    return _char, _char2, _char3


def lexical(tmp_sheet: list[list[str]]) -> list[list[str]]:
    token_sheet = []
    token_sheet_gyo = [""] * 5
    for tmp_sheet_gyo in tmp_sheet:
        行分類 = tmp_sheet_gyo[1]
        領域分類 = "C"
        # the string of line
        text = tmp_sheet_gyo[8]
        # continue space line
        if text.replace(" ", "") == "":
            continue
        #
        if not token_sheet_gyo == [""] * 5 and len(token_sheet_gyo) > 5:
            token_sheet.append(token_sheet_gyo)
        # Init
        token_sheet_gyo = [""] * 5
        # 元資産行番号
        token_sheet_gyo[1] = tmp_sheet_gyo[7]
        # 行情報
        token_sheet_gyo[2] = 行分類
        # 記述領域
        token_sheet_gyo[3] = 領域分類
        # 階層情報
        token_sheet_gyo[4] = ""
        # コマンド情報分解
        i = 0
        # For each line
        while i < len(text):
            char, char2, char3 = get_char123(text, i)
            char_start = i
            char_end = i
            # quotation
            if char == "'" or char == '"':
                char_start = i
                single_flg = double_flg = False
                for j, jchar in enumerate(text[i:]):
                    single_flg, double_flg = quotation_check(jchar, single_flg, double_flg)
                    if single_flg or double_flg:
                        continue
                    else:
                        break
                i = i + j + 1
                char_end = i
                token_sheet_gyo.append(text[char_start:char_end])
            # append split char
            elif split_char_check(char, char2, char3):
                if char == " ":
                    i = i + 1
                else:
                    i = i + 1
                    token_sheet_gyo.append(char)
            else:
                j = i
                while True:
                    # break condition
                    j = j + 1
                    if j >= len(text) or split_char_check(*get_char123(text, j)):
                        break
                # over line
                if j >= len(text):
                    i = j
                    char_end = len(text)
                    token_sheet_gyo.append(text[char_start:char_end])
                # find split char
                else:
                    i = j
                    char_end = j
                    token_sheet_gyo.append(text[char_start:char_end])
    token_sheet.append(token_sheet_gyo)
    return token_sheet
