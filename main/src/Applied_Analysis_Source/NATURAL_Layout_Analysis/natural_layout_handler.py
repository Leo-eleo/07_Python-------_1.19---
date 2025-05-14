import glob
import os
import re
import sys

import chardet

jcl_find_pattern = r"CMWKF\d+ "
jcl_natural_pattern = r"R +([a-zA-Z0-9$#%]+) "
jcl_dsn_pattern = r"DSN=(.+?)[, ]"
jcl_vol_pattern = r"VOL=(.+?)[, ]"

layout_define_pattern = r"\d{4} *(\d*)(( *)(\#[^ ]+)( *)\((.+)\))|(\d+X\)*)"
layout_redefine_pattern = r"\d{4} *(\d*)( +REDEFINE +)(\#*[^ ]+)*"
layout_reset_pattern = r"\d{4} *(\d*)( +RESET +)(\#*[^ ]+)"

layout_define_data_start_pattern = r"\d{4} *(\d*)( +DEFINE +)( +DATA +)"
layout_define_data_pattern = r"( \w* [1-9] +[^ ]+ )|( [1-9] +[^ ]+ *\w +\d\.*\d*)"
layout_define_data_end_pattern = r"\d{4} *(\d*)( +END-DEFINE +)"

test_io_pattern = r"(WRITE|READ) +WORK +(FILE +)*{} +(.+?) +\n"


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


def parseJclStep(pgmLine):
    stepMap = {}
    stepName = ""
    for pl in pgmLine.split("\n"):
        if pl.startswith("//"):
            realLine = pl[2::]
        else:
            realLine = pl
        stepNameIndex = realLine.find(" ")
        if stepNameIndex == 0:
            stepMap[stepName].append(realLine)
        else:
            stepName = realLine[0:stepNameIndex]
            stepMap[stepName] = []
            stepMap[stepName].append(realLine)

    return stepMap


def parseJcl(jclPath):
    with open(jclPath, "r", errors="ignore", encoding=get_file_encoding(jclPath)) as ft:
        content = "".join([c for c in ft.readlines() if c[2:3] != "*"])

        match = re.search(jcl_find_pattern, content)
        naturalDdNameDsnMap = {}

        if match:

            pgmLines = re.split("EXEC +", content)[1::]
            for pgmLine in pgmLines:
                ddNameAndDsn = []
                matchAll = re.findall(jcl_find_pattern, pgmLine)
                if matchAll:
                    naturalNameMatch = re.search(jcl_natural_pattern, pgmLine)
                    if naturalNameMatch:
                        naturalName = naturalNameMatch.group(1)

                    stepMap = parseJclStep(pgmLine)

                    for m in matchAll:
                        ddName = m.strip()
                        dsnMatch = re.search(jcl_dsn_pattern, "\n".join(stepMap[ddName]))
                        volMatch = re.search(jcl_vol_pattern, "\n".join(stepMap[ddName]))
                        if dsnMatch:
                            if volMatch:
                                ddNameAndDsn.append(ddName + "," + dsnMatch.group(1) + "," + volMatch.group(1))
                            else:
                                ddNameAndDsn.append(ddName + "," + dsnMatch.group(1))
                        naturalDdNameDsnMap[naturalName] = ddNameAndDsn
            return True, naturalDdNameDsnMap
        else:
            return False, {}


def repalceBracket(s):
    return re.sub(r" +\)", ")", re.sub(r" +\(", "(", s))


def handler(jclPath, naturalPathMap, resultPath):
    haveFlg, naturalDdNameDsnMap = parseJcl(jclPath)

    if not haveFlg:
        return

    for naturalName in naturalDdNameDsnMap:
        ddNameDsnList = naturalDdNameDsnMap[naturalName]

        if naturalName not in naturalPathMap:
            continue
        naturalPath = naturalPathMap[naturalName]

        naturalContent = []
        resetFlg = False
        redefineFlg = False

        resetList = []
        redefineList = []
        layoutLineList = []
        nameLayoutMap = {}

        defineFlg = False
        defineLayoutMap = {}

        with open(naturalPath, "r", errors="ignore", encoding=get_file_encoding(naturalPath)) as ft:
            for line in ft.readlines():
                if line[0:7].find("*") > -1:
                    continue
                naturalContent.append(line)
                realLine = line[6::].strip()
                if re.search(layout_reset_pattern, line):
                    if len(resetList) > 0 and len(redefineList) > 0:
                        for resetName in resetList:
                            if resetName != "":
                                nameLayoutMap[re.sub("\(.+?\)", "", resetName)] = layoutLineList
                        layoutLineList = []
                        resetList = []
                        redefineList = []
                    resetFlg = True
                    layoutLineList.append(line)
                    resetList.extend(re.split(" +", repalceBracket(realLine.replace("RESET ", ""))))
                elif resetFlg and re.search(layout_define_pattern, line) and line.find("REDEFINE") == -1:
                    layoutLineList.append(line)
                    resetList.extend(re.split(" +", repalceBracket(realLine)))
                elif resetFlg and re.search(layout_redefine_pattern, line):
                    resetFlg = False
                    redefineFlg = True
                    redefineList.extend(re.split(" +", repalceBracket(realLine.replace("REDEFINE", ""))))
                    layoutLineList.append(line)
                elif redefineFlg and re.search(layout_define_pattern, line):
                    redefineList.extend(re.split(" +", repalceBracket(realLine.replace("REDEFINE", ""))))
                    layoutLineList.append(line)
                elif re.search(layout_define_data_start_pattern, line):
                    defineFlg = True
                elif defineFlg and re.search(layout_define_data_pattern, line):
                    realLine = line[5::].strip()
                    rs = re.split(" +", realLine)
                    if rs[0] == "1":
                        deFineName = rs[1]
                        if deFineName not in defineLayoutMap:
                            defineLayoutMap[deFineName] = []
                            defineLayoutMap[deFineName].append([])
                        else:
                            firstLine = defineLayoutMap[deFineName][0][0]
                            defineLayoutMap[deFineName].append([firstLine])
                    defineLayoutMap[deFineName][-1].append(line)
                elif re.search(layout_define_data_end_pattern, line):
                    defineFlg = False
                else:
                    if len(resetList) > 0 and len(redefineList) > 0:
                        for resetName in resetList:
                            if resetName != "":
                                nameLayoutMap[re.sub("\(.+?\)", "", resetName)] = layoutLineList

                    resetList = []
                    redefineList = []
                    layoutLineList = []
                    resetFlg = False
                    redefineFlg = False

        for ddNameDsn in ddNameDsnList:
            ddv = ddNameDsn.split(",")
            ddName = ddv[0]
            dsn = ddv[1]

            ddNameMatch = re.search(test_io_pattern.format(re.search(r"(\d+)", ddName).group()),
                                    "".join(naturalContent))

            if ddNameMatch:

                # fn = dsn + "_" + naturalName
                fn = naturalName + "_" + ddName

                if len(ddv) > 2:
                    fn = fn + "_" + ddv[2]

                resetNames = [r for r in re.split(" +", ddNameMatch.group(3).strip()) if not r.startswith(r"/*")]

                fileLinesMap = {}

                for resetName in resetNames:
                    if resetName in defineLayoutMap:
                        if len(defineLayoutMap[resetName]) > 1 and len(defineLayoutMap[resetName][0]) == 1:
                            defineLayoutMap[resetName].remove(defineLayoutMap[resetName][0])
                        for index, lines in enumerate(defineLayoutMap[resetName]):
                            fName = os.path.join(resultPath, fn + "_" + str(index + 1) + ".scm")
                            if fName not in fileLinesMap:
                                fileLinesMap[fName] = []
                            if not set(lines).issubset(set(fileLinesMap[fName])):
                                fileLinesMap[fName].extend(lines)

                    if resetName in nameLayoutMap:
                        fName = os.path.join(resultPath, fn + "_" + "1" + ".scm")
                        if fName not in fileLinesMap:
                            fileLinesMap[fName] = []
                        if not set(nameLayoutMap[resetName]).issubset(set(fileLinesMap[fName])):
                            fileLinesMap[fName].extend(nameLayoutMap[resetName])

                for f in fileLinesMap:
                    with open(f, "w") as wt:
                        rl = fileLinesMap[f]
                        c = "".join(rl)
                        if c.find("REDEFINE") > -1 and c.find("RESET") > -1:
                            rl.append("      **ACTIVE " + ",".join(resetNames) + ".")
                        wt.writelines(rl)


def naturalLayoutHandler(jclPath, naturalPath, resultPath):
    jclPathList = glob_files(jclPath)

    naturalPathList = glob_files(naturalPath)

    naturalPathMap = {os.path.splitext(os.path.basename(naturalPath))[0].split("%")[-1]: naturalPath for naturalPath in
                      naturalPathList}

    for jclPath in jclPathList:
        handler(jclPath, naturalPathMap, resultPath)


if __name__ == "__main__":
    naturalLayoutHandler(sys.argv[1], sys.argv[2], sys.argv[3])
