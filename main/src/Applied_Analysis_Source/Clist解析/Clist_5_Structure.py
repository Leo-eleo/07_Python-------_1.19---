import os
import re
import Clist_Analysis_common

# CLIST共通正規表現設定
CLIST基本ID = r"[A-Z0-9\.<\(\+\|&\*\)\;\^\-/\,%>\?:#@'=\\']+"
単項演算子 = r"((\s\()*((\s(\+|\-))?\s[0-9\.]+|\sCLIST基本ID|\sZERO)(\s\))*|((\s(\+|\-))?\s[0-9\.]+|\sCLIST基本ID|\sZERO))".replace(
    "CLIST基本ID", CLIST基本ID)
指数演算子 = r"(\s\(単項演算子(\s\*\*単項演算子)*\s\)|単項演算子(\s\*\*単項演算子)*)".replace("単項演算子", 単項演算子)
乗除演算子 = r"(\s\(指数演算子(\s(\*|\/)指数演算子)*\s\)|指数演算子(\s(\*|\/)指数演算子)*)".replace("指数演算子", 指数演算子)
加減演算子 = r"(\s\(乗除演算子(\s(\+|\-)乗除演算子)*\s\)|乗除演算子(\s(\+|\-)乗除演算子)*)".replace("乗除演算子", 乗除演算子)
算術式 = 加減演算子
call_key = Clist_Analysis_common.get_clist_call_key()


def make_insert_sql(DBNAME, value_list, key_list):
    keys = "[" + "],[".join(key_list) + "]"
    values = []
    for v in value_list:
        if v == None:
            v = ""
        values.append(str(v))
    values = tuple(values)
    value = "?," * (len(values) - 1) + "?"
    sql = "INSERT INTO " + DBNAME + "(" + keys + ")" + "VALUES (" + value + ")"
    return sql, values


def SUB_SQL生成_共通_1(info1, lib2, id3, row4, key5, hit6, cursor):
    db_name = "共通_資産解析_関連情報"
    key_list = ["分類キー", "LIBRARY_ID", "資産ID", "最終行番号", "設定情報キー", "資産行情報"]
    value_list = [info1, lib2, id3, row4, key5, hit6]
    cmd, value = make_insert_sql(db_name, value_list, key_list)
    cursor.execute(cmd, value)


def SUB_SQL生成_共通_2(info1, lib2, id3, row4, str5, cursor):
    db_name = "共通_資産解析_NG情報"
    key_list = ["実行分類", "LIBRARY_ID", "資産ID", "最終行番号", "資産行情報"]
    value_list = [info1, lib2, id3, row4, str5]
    cmd, value = make_insert_sql(db_name, value_list, key_list)
    cursor.execute(cmd, value)


def SUB_SQL生成_CLIST_1(ライブラリID, CLIST_ID, CMD分類, CLIST_呼出資産, CLIST_呼出PARM, cursor):
    db_name = "⑪CLIST_関連資産"
    key_list = ["LIBRARY_ID", "CLIST_ID", "関連区分", "関連資産", "呼出時PARM"]
    value_list = [ライブラリID, CLIST_ID, CMD分類, CLIST_呼出資産, CLIST_呼出PARM]
    cmd, value = make_insert_sql(db_name, value_list, key_list)
    cursor.execute(cmd, value)


def 検索行文字列生成処理(TokenSheet_str):
    TokenSheet_str = [str(s) for s in TokenSheet_str]
    検索行文字列 = " ".join(TokenSheet_str)
    return 検索行文字列


def Mid(string, start_index, length):
    if len(string) <= start_index:
        return ""
    return string[start_index:min(start_index + length, len(string))]


def 例外キー_CLIST(key):
    return key == "ラベル"


def 設定値タイプチェック_CLIST(code_val):
    if "'" in code_val or "==" in code_val:
        return "定数"
    elif ":" in code_val:
        return "ラベル"
    else:
        return "変数"


def 設定値parmチェック_CLIST(code_val):
    matchs = re.search(CLIST基本ID, code_val)
    if matchs:
        return True
    else:
        return False


def 設定値数値チェック_CLIST(code_val):
    return code_val.isnumeric()


def 設定値一致チェック_CLIST(parm_val, code_val):
    # ラベル
    if "ラベル" in parm_val and 設定値タイプチェック_CLIST(code_val) == "ラベル":
        return True
    # パラメータ
    elif "PARM" in parm_val and 設定値parmチェック_CLIST(code_val):
        return True
    # 変数
    elif "変数" in parm_val and 設定値タイプチェック_CLIST(code_val) == "変数":
        return True
    # 定数
    elif "定数" in parm_val and 設定値タイプチェック_CLIST(code_val) == "定数":
        return True
    # 数値
    elif "数値" in parm_val and 設定値数値チェック_CLIST(code_val) == "数値":
        return True
    # 予約語（上記条件以外）
    elif parm_val == code_val:
        return True
    else:
        return False


def clist_5_structure(TokenSheet2,
                      conn,
                      file,
                      clist_sheet,
                      設定条件HIT情報出力=False,
                      分析条件HIT情報出力=False,
                      設計条件HIT情報出力=False,
                      設定条件HIT_NG情報出力=False):
    ALL_chk_ok = True
    ライブラリID, _,  _ = os.path.basename(file).split("%")
    CLIST_ID = os.path.basename(file)
    FILE_SEQ = 0
    cursor = conn.cursor()

    検索行 = 0      # TokenSheet2　行ポインタ
    分析行TYPE = ""
    while 検索行 < len(TokenSheet2):
        TokenSheet2_GYO = TokenSheet2[検索行]
        検索列 = 4
        while 検索列 < len(TokenSheet2_GYO):
            PARM行 = 0
            parm_hit = False
            while PARM行 < len(clist_sheet):
                if parm_hit:
                    break
                PARM列 = 5
                hit_flg = True
                parm_cnt = 0
                re_flg = False
                # 先頭のトークン比較(最初が違う場合は列のカウントアップ不要)
                if TokenSheet2_GYO[検索列] == clist_sheet[PARM行][PARM列] or 例外キー_CLIST(clist_sheet[PARM行][PARM列]):
                    while PARM列 < len(clist_sheet[PARM行]) or hit_flg:
                        if PARM列 < len(clist_sheet[PARM行]):
                            if clist_sheet[PARM行][PARM列] == "":
                                break
                            parm_cnt += 1
                        parm_val = str(clist_sheet[PARM行][5 + parm_cnt - 1])
                        code_val = str(TokenSheet2_GYO[検索列 + parm_cnt - 1])
                        if not 設定値一致チェック_CLIST(parm_val, code_val):
                            hit_flg = False
                        PARM列 = PARM列 + 1
                # 先頭トークンが正規表現の場合
                elif "正規表現_" in clist_sheet[PARM行][PARM列]:
                    # 検索対象文字列再構成
                    tokenstr = ""
                    tokencnt = 検索列
                    re_flg = True
                    while tokencnt < len(TokenSheet2_GYO):
                        tokenstr = tokenstr + TokenSheet2_GYO[tokencnt] + " "
                        tokencnt = tokencnt + 1
                    # 正規表現再設定
                    re_pattern = clist_sheet[PARM行][PARM列].replace("正規表現_", "")
                    matchs = re.search(re_pattern, tokenstr)
                    if matchs:
                        matchstr = matchs.group()
                        # 先頭の文字列から一致している場合のみ(先頭の文字列の一部が正規表現にHITしているものは対象外)
                        if Mid(tokenstr, 0, len(matchstr)) == matchstr and len(TokenSheet2_GYO[検索列]) <= len(matchstr):
                            tokencnt = 検索列
                            re_exit = False
                            while matchstr.replace(" ", "") != "" and not re_exit:
                                if tokencnt >= len(TokenSheet2_GYO):
                                    break
                                if TokenSheet2_GYO[tokencnt] in matchstr:
                                    matchstr = matchstr.replace(
                                        TokenSheet2_GYO[tokencnt], "")
                                    tokencnt = tokencnt + 1
                                    parm_cnt = parm_cnt + 1
                                else:
                                    re_exit = True
                        else:
                            hit_flg = False
                    else:
                        hit_flg = False
                else:
                    hit_flg = False
                # 'チェック結果
                if hit_flg:
                    parm_hit = True
                    # 検索行文字列作成
                    検索行文字列 = 検索行文字列生成処理(TokenSheet2_GYO[4:])
                    # 関連情報出力
                    if 設定条件HIT情報出力:
                        SUB_SQL生成_共通_1("キーID", ライブラリID, CLIST_ID, 検索行, clist_sheet[PARM行][1], 検索行文字列, cursor)
                    if 分析条件HIT情報出力 and clist_sheet[PARM行][2] != "":
                        SUB_SQL生成_共通_1("分析ID", ライブラリID, CLIST_ID, 検索行, clist_sheet[PARM行][2], 検索行文字列, cursor)
                    if 設計条件HIT情報出力 and clist_sheet[PARM行][3] != "":
                        SUB_SQL生成_共通_1("設計ID", ライブラリID, CLIST_ID, 検索行, clist_sheet[PARM行][3], 検索行文字列, cursor)
                        CMD分類 = clist_sheet[PARM行][3]
                        if CMD分類 in call_key:
                            CLIST_呼出資産 = TokenSheet2_GYO[4+1]
                            CLIST_呼出PARM = 検索行文字列.replace(f"{CMD分類} ", "")
                            CLIST_呼出PARM = CLIST_呼出PARM.replace(CLIST_呼出資産, "")
                            CLIST_呼出資産 = TokenSheet2_GYO[4+1].replace("'", "")
                            SUB_SQL生成_CLIST_1(ライブラリID, CLIST_ID, CMD分類, CLIST_呼出資産, CLIST_呼出PARM, cursor)
                else:
                    PARM行 = PARM行 + 1
            # 検索列更新
            if parm_hit:
                re_flg = False
                検索列 = 検索列 + parm_cnt
            else:
                ALL_chk_ok = False
                if 設定条件HIT_NG情報出力:
                    検索行文字列 = 検索行文字列生成処理(TokenSheet2_GYO[4:])
                    # NG時関連情報出力
                    SUB_SQL生成_共通_2("CL", ライブラリID, CLIST_ID, 検索行, 検索行文字列, cursor)
                    検索列 = 検索列 + 1
        検索行 = 検索行 + 1
