def Mid(string, start_index, length):
    if len(string) <= start_index:
        return ""
    return string[start_index:min(start_index + length, len(string))]

# def Mid(s, start, length=0):
#     if length == 0:
#         length = len(s)
#     # 使用字符串切片操作获取需要的子字符串
#     return s[start - 1:start + length - 1]

def InStr(s, sub, start=0):
    position = s.find(str(sub), start)
    return position + 1 if position >= 0 else 0


def 分離文字判定_CLIST(str1, str2="", str3=""):
    if str1 == " ":
        return True
    else:
        return False


def clist_3_lexical(TmpSheet):
    TokenSheet = []
    出力行 = 1
    検索行 = 2
    for TmpSheet_GYO in TmpSheet:
        if TmpSheet_GYO[2].replace(" ", "") == "":
            検索行 += 1
            continue
        CMD_fld = TmpSheet_GYO[2]
        TokenSheet_GYO = [""] * 3
        # 行番号情報
        TokenSheet_GYO[1] = TmpSheet_GYO[5]
        # 行情報
        TokenSheet_GYO[2] = "通常行"
        i = 0
        while i < len(CMD_fld):
            判定対象文字 = Mid(CMD_fld, i, 1)
            判定対象文字2 = Mid(CMD_fld, i + 1, 1)
            判定対象文字3 = Mid(CMD_fld, i + 2, 1)
            判定対象文字_from = i
            判定対象文字_to = i
            if 判定対象文字 == "'":
                判定対象文字_to = InStr(Mid(CMD_fld, 判定対象文字_from + 1, 80), "'")
                if 判定対象文字_to < 1:
                    判定対象文字_to = 71
                対象文字数 = 判定対象文字_to + 1
                i = i + 対象文字数
                TokenSheet_GYO.append(Mid(CMD_fld, 判定対象文字_from, 対象文字数))
            elif 分離文字判定_CLIST(判定対象文字, 判定対象文字2, 判定対象文字3) == True:
                if 判定対象文字 == " ":
                    i = i + 1
                else:
                    i = i + 1
                    TokenSheet_GYO.append(判定対象文字)
            else:
                i2 = i
                while True:
                    i2 = i2 + 1
                    if 分離文字判定_CLIST(Mid(CMD_fld, i2, 1), Mid(CMD_fld, i2 + 1, 1), (CMD_fld, i2 + 2, 1)) or i2 > len(CMD_fld):
                        break
                if i2 > len(CMD_fld):
                    判定対象文字_to = 80
                    i = 80  # 後続検索終了
                    対象文字数 = 判定対象文字_to - 判定対象文字_from + 1
                    TokenSheet_GYO.append(Mid(CMD_fld, 判定対象文字_from, 対象文字数))
                else:
                    判定対象文字_to = i2 - 1
                    対象文字数 = 判定対象文字_to - 判定対象文字_from + 1
                    i = i + 対象文字数
                    TokenSheet_GYO.append(Mid(CMD_fld, 判定対象文字_from, 対象文字数))
        TokenSheet.append(TokenSheet_GYO)
    return TokenSheet
