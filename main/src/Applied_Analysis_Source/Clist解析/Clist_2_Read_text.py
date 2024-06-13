def delete_comment(strREC):
    result = ""
    comments = []
    i = 0
    while i < len(strREC):
        if strREC[i:i+2] == "/*":
            i += 2
            comment_start = i
            while i < len(strREC) - 1 and (strREC[i] != "*" or strREC[i+1] != "/"):
                i += 1
            comments.append(strREC[comment_start:i])
            i += 2
        else:
            result += strREC[i]
            i += 1
    return result, comments


# ⑫_2_テキストファイル読み込み_CLIST
def clist_2_read_text(file_name):
    # 行情報 有効情報 コメント 元資産行情報 元資産行番号
    TmpSheet = []
    CL行分類 = "通常行"
    C継続 = False
    GYO = 1
    with open(file_name, "r", encoding="CP932", errors="ignore") as ft:
        while True:
            strREC = ft.readline()
            if not strREC:
                break
            strREC = strREC.strip("\n")
            TmpSheet_GYO = [""] * 6
            str_encode = strREC.encode("CP932")
            str_encode = str_encode[:72]
            CL有効情報 = str_encode.decode("CP932", errors="ignore")
            CL有効情報, CLコメント = delete_comment(CL有効情報)
            CLコメント = ""
            CLコメント_TEMP = ""
            hit_flg = False
            # 行分類
            TmpSheet_GYO[1] = CL行分類
            # 有効行情報
            TmpSheet_GYO[2] = CL有効情報
            # コメント情報
            TmpSheet_GYO[3] = "_".join(CLコメント)
            # 元資産行情報
            TmpSheet_GYO[4] = strREC
            # 元資産行番号
            TmpSheet_GYO[5] = GYO
            TmpSheet.append(TmpSheet_GYO)
            GYO += 1
    return TmpSheet
