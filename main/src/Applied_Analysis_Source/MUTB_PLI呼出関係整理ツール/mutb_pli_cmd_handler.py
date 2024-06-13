import os
import re
import sys

import pandas as pd


def getParam(name, param):
    rs = re.findall(name.replace("\\", "\\\\") + r"\S*\(.+?\)", param)
    if len(rs) > 0:
        return rs[0].replace(name, "").strip()[1:-1].strip().replace("'", "").replace("\"", "")
    return ""


def mutbPLICmdHandler(sourcePath, resultPath):
    sourceDf = pd.read_excel(sourcePath, sheet_name="COBOL_CMD情報")

    segmData = {"呼出元": [], "呼出方法": [], "呼出マクロ": [], "呼出先": [], "呼出MODE": [], "呼出FILE": [], "呼出DELETE": [],
                "呼出TYPE": [], "呼出AREA": [], "呼出OPER": [], "呼出KEY": [], "呼出PTR": [], "呼出CURPTR": []}
    ccallData = {"呼出元": [], "呼出方法": [], "呼出SEG": [], "呼出MOD": [], "呼出LOAD": [], "呼出PARM": []}
    crendoData = {"呼出元": [], "呼出方法": [], "呼出APPLID": [], "呼出TYPE": [], "呼出APCBPTR": [], "呼出KEY": []}
    asbctxedData = {"呼出元": [], "呼出方法": [], "呼出先": [], "呼出先パラメータ": []}

    for index in sourceDf.index:
        param = str(sourceDf.loc[index]['PARM'])
        cobolId = sourceDf.loc[index]['COBOL_ID']
        # SEGM
        if re.search(r"CDB\w+\s+", param):
            segmData["呼出元"].append(cobolId)
            segmData["呼出方法"].append("SEGM呼出")
            rs = re.findall(r"CDB\w+\s+", param)
            segmData["呼出マクロ"].append(rs[0].strip())
            segmData["呼出先"].append(getParam("SEGM", param))
            segmData["呼出MODE"].append(getParam("MODE", param))
            segmData["呼出FILE"].append(getParam("FILE", param))
            segmData["呼出DELETE"].append(getParam("DELETE", param))
            segmData["呼出TYPE"].append(getParam("TYPE", param))
            segmData["呼出AREA"].append(getParam("AREA", param))
            segmData["呼出OPER"].append(getParam("OPER", param))
            segmData["呼出KEY"].append(getParam("KEY", param))
            segmData["呼出PTR"].append(getParam("PTR", param))
            segmData["呼出CURPTR"].append(getParam("CURPTR", param))
        elif re.search(r"CCALL\s+", param):
            ccallData["呼出元"].append(cobolId)
            ccallData["呼出方法"].append("PGM呼出")
            ccallData["呼出SEG"].append(getParam("SEG", param))
            ccallData["呼出MOD"].append(getParam("MOD", param))
            ccallData["呼出LOAD"].append(getParam("LOAD", param))
            ccallData["呼出PARM"].append(getParam("PARM", param))
        elif re.search(r"CRENDO\s+", param):
            crendoData["呼出元"].append(cobolId)
            crendoData["呼出方法"].append("PGM呼出")
            crendoData["呼出APPLID"].append(getParam("APPLID", param))
            crendoData["呼出TYPE"].append(getParam("TYPE", param))
            crendoData["呼出APCBPTR"].append(getParam("APCBPTR", param))
            crendoData["呼出KEY"].append(getParam("KEY", param))
        elif re.search(r"^[^A-Z0-9]{0,}CALL\s+", param):
            asbctxedData["呼出元"].append(cobolId)
            asbctxedData["呼出方法"].append("CALL呼出")
            rs = re.findall(r"^[^A-Z0-9]{0,}CALL\s+.+?\(", param)
            if rs:
                callname = rs[0].replace("CALL ", "").strip()[0:-1]
                asbctxedData["呼出先"].append(callname)
                asbctxedData["呼出先パラメータ"].append(getParam(callname, param))
            else:
                rs = param.split(" ")
                print("■CALL　param=" + param)
                if len(rs) > 1:
                    callname = rs[1]
                    print("⇒CALL　callname=" + callname)
                    asbctxedData["呼出先"].append(callname)
                    asbctxedData["呼出先パラメータ"].append("")
                else:
                    asbctxedData["呼出先"].append("")
                    asbctxedData["呼出先パラメータ"].append("")

    writer = pd.ExcelWriter(os.path.join(resultPath, "【CoE】PLI呼出関係整理.xlsx"))  # 重点1：writer不能在下面的for循环中
    data = pd.DataFrame(segmData)
    data.to_excel(writer, "SEGM呼出", engine='xlsxwriter', encoding="cp932")
    data1 = pd.DataFrame(ccallData)
    data1.to_excel(writer, "CCALL呼出", engine='xlsxwriter', encoding="cp932")
    data2 = pd.DataFrame(crendoData)
    data2.to_excel(writer, "CRENDO呼出", engine='xlsxwriter', encoding="cp932")
    data3 = pd.DataFrame(asbctxedData)
    data3.to_excel(writer, "CALL呼出", engine='xlsxwriter', encoding="cp932")
    writer._save()


if __name__ == "__main__":
    mutbPLICmdHandler(sys.argv[1], sys.argv[2])
