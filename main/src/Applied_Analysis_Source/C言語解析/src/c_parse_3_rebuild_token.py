import os

from typing import Tuple
from c_utiles import SPLIT_CHAR2, C_KEY_WORD, SPLIT_CHAR, C_PRE_PROCESS


def brackets_check(count: int, token: str) -> int:
    if token == "(":
        count = count + 1
    elif token == ")":
        count = count - 1
    return count


def find_fn(res: list[str]) -> dict[int, str]:
    fn: dict[int, str] = {}
    for tokens_index, tokens in enumerate(res):
        if tokens_index == 575:
            pass
        for i, token in enumerate(tokens):
            if (
                token == "("
                and tokens[i - 1] not in C_KEY_WORD
                and tokens[i - 1] not in SPLIT_CHAR
                and not type(tokens[i - 1]) == int
            ):
                fn[tokens_index] = tokens[i - 1]
    return fn


def rebuild_token(tokens_list: list[list[str]]) -> list[list[str]]:
    _res: list[list[str]] = []
    r_tokens: list[str] = [""] * 2
    brackets_count = 0
    for tokens in tokens_list:
        # line no
        line_no = tokens[1]
        r_tokens[1] = line_no
        for token in tokens[5:]:
            brackets_count = brackets_check(brackets_count, token)
            # r_tokens.append(token)
            # not in brackets
            if brackets_count == 0:
                if token in SPLIT_CHAR2:
                    r_tokens.append(token)
                    _res.append(r_tokens)
                    r_tokens = [""] * 2
                    r_tokens[1] = line_no
                elif token in C_PRE_PROCESS or token in C_KEY_WORD:
                    if len(r_tokens) > 3:
                        _res.append(r_tokens)
                        r_tokens = [""] * 2
                        r_tokens[1] = line_no
                        r_tokens.append(token)
                    else:
                        r_tokens.append(token)
                else:
                    r_tokens.append(token)
            else:
                r_tokens.append(token)
    return _res


def merge_right_braces(_res: list[list[str]]) -> list[list[str]]:
    res: list[list[str]] = []
    for row in _res:
        while True:
            if len(row) > 2:
                if row[2] == "}" or row[2] == ";":
                    res[-1].append(row[2])
                    row.pop(2)
                else:
                    res.append(row)
                    break
            else:
                break
    return res


def find_include(res: list[list[str]]) -> list[str]:
    include: list[str] = []
    for row in res:
        if row[1] == "#include":
            if row[2] == "<":
                include.append(os.path.splitext(row[3])[0])
            else:
                include.append(os.path.splitext(row[2].replace('"', "").replace("'", ""))[0])
    return include


def find_io_info(res: list[list[str]]) -> list[list[str]]:
    _res: list[list[str]] = []
    for row in res:
        if any([x == "fopen" for x in row]):
            _res.append(row)
    return _res


def rebuild(tokens_list: list[list[str]]) -> Tuple[list[list[str]], dict[int, str], list[str], list[list[str]]]:
    # rebuild token
    _res = rebuild_token(tokens_list)

    # Merge right braces
    res = merge_right_braces(_res)

    # Find inner function
    inner_fn = find_fn(res)

    # Find include file
    include = find_include(res)

    # Find io_info
    io_info = find_io_info(res)

    # Return
    return res, inner_fn, include, io_info
