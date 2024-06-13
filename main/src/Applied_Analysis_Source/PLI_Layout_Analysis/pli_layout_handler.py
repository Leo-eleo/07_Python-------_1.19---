import glob
import logging
import os
import re
import sys

import chardet
import pandas as pd

pli_find_patterns = [
    r"( ([^ ]+) +FILE +RECORD[ ,;])",
    r"( ([^ ]+) +FILE +INPUT +RECORD[ ,;])",
    r"( ([^ ]+) +FILE +OUTPUT +RECORD[ ,;])"
]

jcl_dsn_pattern = r"DSN *= *(.+?)[, ]"

layout_define_data_start_pattern = r"[ 0]+DCL +[1-9]* +([^ ]+).*?[,;]"
layout_define_data_refine_pattern = r" +([1-9]*) +([^ ]+) +(DEF) +(.+?),"
layout_define_data_pattern = r" +([1-9]*) +([^ ]+) +(DEF)* +(.+?),"
layout_define_data_end_pattern = r" +([1-9]*) +([^ ]+) .+?;"

test_io_pattern = r"(WRITE|READ) +FILE\({}\) (INTO|FROM)\(([^ ]+)\)"

like_pattern = "([^ ]+) +LIKE +([^ ]+).*?[,;]"

logging.basicConfig(filename='pli_layout_handler' + '.log',
                    format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]', level=logging.INFO, filemode='a',
                    datefmt='%Y-%m-%d%I:%M:%S %p')


def get_file_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def glob_files(file_path, recursive=True, type="file"):
    assert os.path.exists(file_path), "file path is invalid : " + file_path

    files = glob.glob(file_path + "/**", recursive=recursive)
    if type == "file":
        return [p for p in files if os.path.isfile(p)]

    elif type == "folder":
        return [p for p in files if os.path.isdir(p)]


def handler(jclDdnames, pliName, content, pliDdnameScmMap, resultPath):
    pliContent = []
    defineFlg = False
    defineLayoutMap = {}

    deFineName = ""

    reDefineMap = {}

    for i, line in enumerate(content):
        if line.strip().startswith(r"/*"):
            continue
        if line[0:5].find("*") > -1:
            continue
        pliContent.append(line)
        defineStartMatch = re.search(layout_define_data_start_pattern, line)
        redefineStartMathch = re.search(layout_define_data_refine_pattern, line)
        defineMatch = re.search(layout_define_data_pattern, line)
        defineEndMatch = re.search(layout_define_data_end_pattern, line)
        if defineStartMatch:
            if redefineStartMathch:
                ix = redefineStartMathch.group(1)
                if ix == "":
                    ix = "1"
                if ix == "1":
                    reDefineName = redefineStartMathch.group(2).strip()
                    deFineName = redefineStartMathch.group(4).strip()
                    reDefineMap[reDefineName] = deFineName
                    if deFineName not in defineLayoutMap:
                        defineLayoutMap[deFineName] = []
                        defineLayoutMap[deFineName].append([])
                    else:
                        firstLine = defineLayoutMap[deFineName][0][0]
                        defineLayoutMap[deFineName].append([firstLine])
            else:
                deFineName = defineStartMatch.group(1)
                if deFineName not in defineLayoutMap:
                    defineLayoutMap[deFineName] = []
                    defineLayoutMap[deFineName].append([])
                else:
                    firstLine = defineLayoutMap[deFineName][0][0]
                    defineLayoutMap[deFineName].append([firstLine])

            if deFineName in defineLayoutMap:
                defineLayoutMap[deFineName][-1].append(line)

            if line.find(";") == -1:
                defineFlg = True
        elif defineFlg and defineMatch:
            ix = defineMatch.group(1)
            if ix == "1":
                if redefineStartMathch:
                    reDefineName = redefineStartMathch.group(2).strip()
                    deFineName = redefineStartMathch.group(4).strip()
                    reDefineMap[reDefineName] = deFineName
                    if deFineName not in defineLayoutMap:
                        defineLayoutMap[deFineName] = []
                        defineLayoutMap[deFineName].append([])
                    else:
                        firstLine = defineLayoutMap[deFineName][0][0]
                        defineLayoutMap[deFineName].append([firstLine])
            if deFineName in defineLayoutMap:
                defineLayoutMap[deFineName][-1].append(line)
            if defineEndMatch:
                defineFlg = False
        elif defineFlg and defineEndMatch:
            if line.strip().startswith("INIT"):
                defineFlg = False
                continue
            if deFineName in defineLayoutMap:
                defineLayoutMap[deFineName][-1].append(line)
            defineFlg = False
        else:
            if i + 1 < len(content) and content[i + 1].strip().startswith("INIT") and defineFlg:
                if deFineName in defineLayoutMap:
                    defineLayoutMap[deFineName][-1].append(line)
            if defineFlg and re.search(".+?;", line):
                if deFineName in defineLayoutMap:
                    defineLayoutMap[deFineName][-1].append(line)
                defineFlg = False

    for ddNameDsn in jclDdnames:
        ddv = ddNameDsn.split(",")
        jclPath = ddv[0]
        ddName = ddv[1]

        ddNameMatch = re.search(test_io_pattern.format(ddName.replace("\\", "\\\\")), "".join(pliContent))

        if ddNameMatch:

            # fn = ddName + "_" + pliName
            fn = pliName + "_" + ddName

            if fn not in pliDdnameScmMap:
                pliDdnameScmMap[fn] = []

            resetNames = [r for r in re.split(" +", ddNameMatch.group(3).strip())]

            fileLinesMap = {}

            for resetName in resetNames:
                if resetName in defineLayoutMap:
                    if len(defineLayoutMap[resetName]) > 1 and len(defineLayoutMap[resetName][0]) == 1:
                        defineLayoutMap[resetName].remove(defineLayoutMap[resetName][0])

                    for index, lines in enumerate(defineLayoutMap[resetName]):
                        fName = os.path.join(resultPath, fn + "_" + str(index + 1) + ".scm")
                        pliDdnameScmMap[fn].append(os.path.basename(fName))
                        if fName not in fileLinesMap:
                            fileLinesMap[fName] = []

                        if "".join(lines).find(" LIKE ") > -1:
                            try:
                                likeMatcher = re.search(like_pattern, "".join(lines))
                                if likeMatcher:
                                    sourceName = likeMatcher.group(1)
                                    likeName = likeMatcher.group(2)

                                    if likeName in reDefineMap:
                                        likeName = reDefineMap[likeName]

                                    if likeName in defineLayoutMap:
                                        lines.pop()
                                        if len(defineLayoutMap[likeName]) > 1 and len(
                                                defineLayoutMap[likeName][0]) == 1:
                                            defineLayoutMap[likeName].remove(defineLayoutMap[likeName][0])
                                        for likeLines in defineLayoutMap[likeName]:
                                            ll = [lns.replace(" " + likeName + " ", " " + sourceName + " ").replace(
                                                " " + likeName + ",", " " + sourceName + ",") for lns
                                                in likeLines]
                                            if not set(ll).issubset(set(fileLinesMap[fName])):
                                                lines.extend(ll)
                                                fileLinesMap[fName].extend(lines)
                                    else:
                                        if not set(lines).issubset(set(fileLinesMap[fName])):
                                            fileLinesMap[fName].extend(lines)
                                else:
                                    if not set(lines).issubset(set(fileLinesMap[fName])):
                                        fileLinesMap[fName].extend(lines)
                            except Exception as e:
                                logging.error(
                                    "エラー, message={}, jclPath={}, pliPath={}, resetName={}".format(e, jclPath, pliName,
                                                                                                   resetName))
                        else:
                            if not set(lines).issubset(set(fileLinesMap[fName])):
                                fileLinesMap[fName].extend(lines)

            for f in fileLinesMap:
                try:
                    with open(f, "w", errors="ignore") as wt:
                        wt.writelines(fileLinesMap[f])
                except Exception as e:
                    logging.error("エラー, message={}, jclPath={}".format(e, jclPath))


def pliLayoutHandler(pliPath, settingPath, resultPath):
    sourceJclDf = pd.read_excel(settingPath, sheet_name="JCL_CMD情報")
    sourceJclDf.fillna("", inplace=True)

    pliDdnameMap = {}
    pliDdnameScmMap = {}

    for index in sourceJclDf.index:
        key = sourceJclDf.loc[index, "PGM_NAME"] + "_" + sourceJclDf.loc[index, "DD_NAME"]
        value = sourceJclDf.loc[index]
        if key not in pliDdnameMap:
            pliDdnameMap[key] = []
        pliDdnameMap[key].append(value)

    pliPathList = glob_files(pliPath)
    ddNameDsns = {}
    for pliPath in pliPathList:
        pliName = os.path.splitext(os.path.basename(pliPath))[0].split("%")[-1]
        jclDdnames = []
        try:
            with open(pliPath, "r", errors="ignore", encoding="cp932") as ft:
                content = ft.readlines()
                for pli_find_pattern in pli_find_patterns:
                    pliSearchList = re.findall(pli_find_pattern, "".join(content))
                    if pliSearchList:
                        ddNames = list(set(ps[-1] for ps in pliSearchList))
                        for ddName in ddNames:
                            if pliName + "_" + ddName in pliDdnameMap:
                                for jclInfo in pliDdnameMap[pliName + "_" + ddName]:
                                    dsnMatcher = re.search(jcl_dsn_pattern, jclInfo["PARM"])
                                    if dsnMatcher:
                                        jclDdnames.append(jclInfo["資産ID"] + "," + ddName)

                                        key = pliName + "," + jclInfo["資産ID"] + "," + ddName
                                        if key not in ddNameDsns:
                                            ddNameDsns[key] = []
                                        ddNameDsns[key].append(dsnMatcher.group(1))
        except Exception as e:
            logging.error("エラー, message={}, pliPath={}".format(e, pliPath))

        if len(jclDdnames) > 0:
            handler(jclDdnames, pliName, content, pliDdnameScmMap, resultPath)

    resultList = {"PLI_NAME": [], "JCL_NAME": [], "DD_NAME": [], "DSN_NAME": [], "SCM_NAME": []}

    for key in list(set(ddNameDsns.keys())):
        pliName = key.split(",")[0]
        jclName = key.split(",")[1]
        ddName = key.split(",")[2]

        # fn = ddName + "_" + pliName
        fn = pliName + "_" + ddName

        for dsnName in list(set(ddNameDsns[key])):
            if fn in pliDdnameScmMap:
                for scm in list(set(pliDdnameScmMap[fn])):
                    resultList["PLI_NAME"].append(pliName)
                    resultList["JCL_NAME"].append(jclName)
                    resultList["DD_NAME"].append(ddName)
                    resultList["DSN_NAME"].append(dsnName)
                    resultList["SCM_NAME"].append(scm)
    data = pd.DataFrame(resultList)
    data.to_excel(os.path.join(resultPath, "PLI-DSNマッピング.xlsx"), sheet_name="マッピング", encoding="cp932",
                  index=False)


if __name__ == "__main__":
    pliLayoutHandler(sys.argv[1], sys.argv[2], sys.argv[3])
