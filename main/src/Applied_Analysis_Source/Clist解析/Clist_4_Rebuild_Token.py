import Clist_Analysis_common

Rwods = Clist_Analysis_common.get_4_RWords()


def Mid(string, start_index, length):
    if len(string) <= start_index:
        return ""
    return string[start_index:min(start_index + length, len(string))]

def 予約語判定_CLIST(str1):
    return str1 in Rwods

def ラベル判定_CLIST(str1, 検索列):
    # ラベルの場合は改行
    # if Mid(str1, len(str1), 1) == ":" and 検索列 == 3:
    if str1.rstrip()[-1] == ":" and 検索列 == 3:
        return True
    else:
        return False

def clist_4_rebuild_token(TokenSheet):
    TokenSheet2 = []
    i = 0
    TokenSheet2_GYO = [""] * 4
    while i < len(TokenSheet):
        検索列 = 3
        TokenSheet_GYO = TokenSheet[i]
        while 検索列 < len(TokenSheet_GYO):
            検索文字列 = TokenSheet_GYO[検索列]
            if not 検索列 + 1 >= len(TokenSheet_GYO):
                先読トークン = TokenSheet_GYO[検索列 + 1]
            else:
                先読トークン = ""
            if (検索文字列 == "+" or 検索文字列 == "-") and 先読トークン == "":
                # 検索列 = 3
                # i += 1
                # TokenSheet2_GYO.append(検索文字列)
                break
            elif (予約語判定_CLIST(検索文字列) or ラベル判定_CLIST(検索文字列, 検索列)) and len(TokenSheet2_GYO) > 4:
                TokenSheet2.append(TokenSheet2_GYO)
                TokenSheet2_GYO = [""] * 4
                TokenSheet2_GYO[1] = TokenSheet_GYO[1]
            if 検索文字列 != "":
                TokenSheet2_GYO.append(TokenSheet_GYO[検索列])
            検索列 += 1
        i += 1
    TokenSheet2.append(TokenSheet2_GYO)
    i = 0
    基準列2 = 4
    条件CNT = 0
    while i < len(TokenSheet2):
        if TokenSheet2[i][基準列2] == "IF":
            条件CNT = 条件CNT + 1
            if TokenSheet2[i + 1][基準列2] == "DO":
                TokenSheet2[i][基準列2-1] = "IF-DO"
            else:
                TokenSheet2[i][基準列2-1] = "IF"
        elif TokenSheet2[i][基準列2] == "ELSE":
            条件CNT = 条件CNT + 1
            TokenSheet2[i][基準列2-1] = "ELSE"
        elif TokenSheet2[i][基準列2] == "DO":
            条件CNT = 条件CNT + 1
            TokenSheet2[i][基準列2-1] = "DO"
        elif TokenSheet2[i][基準列2] == "END":
            条件CNT = 条件CNT - 1
            TokenSheet2[i][基準列2-1] = "END"
        elif ":" in TokenSheet2[i][基準列2-1] == "DO":
            TokenSheet2[i][基準列2-1] = "ラベル"
        i += 1
    return TokenSheet2


