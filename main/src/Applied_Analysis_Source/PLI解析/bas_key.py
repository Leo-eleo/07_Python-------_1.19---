def fn_get_key_word():
    key_word_list = [
        r"%ACTIVATE",
        r"ALLOCATE",
        r"BEGIN",
        r"CALL",
        r"CLOSE",
        r"%DEACTIVATE",
        r"DECLARE",
        r"%DECLARE",
        r"DEFAULT",
        r"DELAY",
        r"DELETE",
        r"DISPLAY",
        r"DO",
        r"%DO",
        r"END",
        r"%END",
        r"ENTRY",
        r"ELSE",
        r"EXIT",
        r"FETCH",
        r"FORMAT",
        r"FREE",
        r"GET",
        r"GOTO",
        r"GO",
        r"%GO",
        r"IF",
        r"%IF",
        r"%INCLUDE",
        r"LEAVE",
        r"LOCATE",
        r"%NOPRINT",
        r"%NOTE",
        r"ON",
        r"OPEN",
        r"%PAGE",
        r"%PRINT",
        r"PROCEDURE",
        r"%PROCEDURE",
        r"%PROCESS",
        r"PUT",
        r"READ",
        r"RELEASE",
        r"RETURN",
        r"REVERT",
        r"REWRITE",
        r"SELECT",
        r"SIGNAL",
        r"%SKIP",
        r"STOP",
        r"THEN",
        r"UNLOCK",
        r"WAIT",
        r"WHEN",
        r"WRITE"
    ]
    return key_word_list

def fn_get_div_after_key_word():
    div_after_key_word = [
        "THEN",
        "ELSE",
        "OTHER",
        "OTHERWISE"
    ]
    return div_after_key_word

def fn_get_forbidden_word_label():
    forbidden_word_label = [
        "'",
        "(",
        ")",
        "="
    ]
    return forbidden_word_label

def fn_get_literal():
    literal = [
        "'",
        '"'
    ]
    return literal