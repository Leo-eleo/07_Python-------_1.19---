import glob
import logging
import os
import re
import sys

pin_point_pattern = r"(\d+)\.(\d+)"
ptn_init_pattern = r"(.*)( *INIT *)(.*)(\<.+\>)"

ptn_array_pattern = r"(\d+):(\d+)"
ptn_array1_pattern = r"(\d+)"

layout_define_pattern = r"\d{4} *(\d*)(( *)(\#[^ ]+)( *)\((.+)\))|(\d+X\)*)"
layout_redefine_pattern = r"\d{4} *(\d*)( +REDEFINE +)(\#*[^ ]+)*"
layout_reset_pattern = r"\d{4} *(\d*)( +RESET +)(\#*[^ ]+)"

layout_pattern = r"(#[^ ]+)\((\w)(.+?)\)"

layout_active_pattern = r" +\*+ACTIVE +([^ ]+)\."

logging.basicConfig(filename='layout_cobol_handler' + '.log',
                    format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]', level=logging.DEBUG, filemode='a',
                    datefmt='%Y-%m-%d%I:%M:%S %p')


def glob_files(file_path, recursive=True, type="file"):
    assert os.path.exists(file_path), "file path is invalid : " + file_path

    files = glob.glob(file_path + "/**", recursive=recursive)
    if type == "file":
        return [p for p in files if os.path.isfile(p)]

    elif type == "folder":
        return [p for p in files if os.path.isdir(p)]


def convertByType(resultLine, dataType, t, length, layoutPath, name):
    if t == "A":
        if int(length) >= 100:
            logging.warning("（A100以上）の場所\tSCMファイル名：{}\t対象の項目名：{}\t対象項目の実際の定義：{}".format(layoutPath, name, t + "(" + str(length) + ")"))

        resultLine = resultLine + dataType + "X(" + length.rjust(2, "0") + ")"
    elif t == "B" or t == "I":
        if length == "2":
            length = "4"
        elif length == "4":
            length = "9"
        elif length == "8":
            length = "18"
        resultLine = resultLine + dataType + "S9(" + length.rjust(2, "0") + ") COMP-4"
    elif t == "N":
        pinPointMatch = re.search(pin_point_pattern, length)
        if pinPointMatch:
            resultLine = resultLine + dataType + "S9(" + pinPointMatch.group(1).rjust(2, "0") + ")"
            if pinPointMatch.group(2) != "0":
                resultLine = resultLine + "V9(" + pinPointMatch.group(2).rjust(2, "0") + ")"
        else:
            resultLine = resultLine + dataType + "S9(" + length.rjust(2, "0") + ")"
    elif t == "P":
        resultLine = resultLine + dataType + "S9(" + length.rjust(2, "0") + ") COMP-3"
    elif t == "D" or t == "T":
        resultLine + dataType + "X(10)"
    else:
        logging.error("scm_file={}, name={}不具合".format(layoutPath, name))

    return resultLine


def convertLine(line, start, index, dataType, layoutPath, activeList=[]):
    rMatch = re.search(layout_pattern, line)
    if rMatch:
        rname = rMatch.group(1)
        rtype = rMatch.group(2)
        rLen = rMatch.group(3)
    else:
        rname = "FILLER"
        rtype = "A"
        rLen = line.replace(")", "").replace("X", "").replace("#", "")

    if len(activeList) > 0 and rname not in activeList:
        return "", rname

    resultLine = start + " " * int(index) + str(index).rjust(2, "0") + " " + rname.replace("#", "S-").ljust(20, " ")
    resultLine = convertByType(resultLine, dataType, rtype, rLen, layoutPath, rname)
    resultLine = resultLine + "."
    return resultLine, rname


def repalceBracket(s):
    return re.sub(r"/\*.+", " ", re.sub(r" +\)", ")", re.sub(r" +\(", "(", s)))


def convertRedefineLine(rname, redefineMap, start, dataType, filePath, lines, index):
    resultLine = start + " " * index + str(index).rjust(2,
                                                        "0") + " " + "FILLER REDEFINES" + " " + rname.replace(
        "#", "S-") + "."

    if str(index).rjust(2, "0") == "01":
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip().startswith("01") and lines[i].find(" " + rname.replace("#", "S-") + " ") > -1:
                lines[i] = start + " " * index + str(index).rjust(2, "0") + " " + rname.replace("#", "S-") + "."
                break
    else:
        lines.append(resultLine)

    for redefine in redefineMap[rname]:
        if redefine == "" or redefine.startswith(r"/*"):
            continue
        resultLine, rname = convertLine(redefine, start, index + 1, dataType, filePath)
        lines.append(resultLine)
        if rname in redefineMap:
            convertRedefineLine(rname, redefineMap, start, dataType, filePath, lines, index + 1)


def layoutCobolHandler(layoutPath, resultPath):
    layoutList = glob_files(layoutPath)

    start = " " * 6
    dataType = " PIC "
    for filePath in layoutList:
        rName = ""
        resetFlg = False
        redefineFlg = False
        resetList = []
        redefineList = []
        redefineMap = {}
        lines = []
        occursIndex = ""
        maxOccurs = 0
        with open(filePath, "r", errors="ignore") as ft:
            content = ft.read()

            activeList = []
            activeMatcher = re.search(layout_active_pattern, content)
            if activeMatcher:
                activeList = [am.strip() for am in activeMatcher.group(1).split(",")]

            for line in content.split("\n"):
                realLine = line[6::].strip()
                if re.search(layout_reset_pattern, line):
                    resetFlg = True
                    resetList.extend(re.split(" +", repalceBracket(realLine.replace("RESET ", ""))))
                elif resetFlg and re.search(layout_define_pattern, line) and line.find("REDEFINE") == -1:
                    resetList.extend(re.split(" +", repalceBracket(realLine)))
                elif re.search(layout_redefine_pattern, line) and resetFlg:
                    resetFlg = False
                    redefineFlg = True
                    redefineList.extend(re.split(" +", repalceBracket(realLine.replace("REDEFINE", ""))))
                elif redefineFlg and re.search(layout_define_pattern, line):
                    redefineList.extend(re.split(" +", repalceBracket(realLine)))
                else:
                    if redefineFlg:
                        redefineFlg = False
                        brackCount = 0
                        for redefine in redefineList:
                            if redefine == "" or redefine.startswith(r"/*"):
                                continue

                            if redefine.find("(") > -1:
                                brackCount = brackCount + len(re.findall(r"\(", redefine))
                                if rName == "":
                                    rNameMatch = re.search(r"(#[^ ]+?)\(", redefine)
                                    rName = rNameMatch.group(1)
                                    redefineMap[rName] = []
                                    redefine = redefine.replace(rName + r"(", "")

                                if redefine.find(")") > -1:
                                    brackCount = brackCount - len(re.findall(r"\)", redefine))
                                if rName != "":
                                    try:
                                        redefineMap[rName].append(redefine)
                                    except Exception as e:
                                        print(e)
                            else:
                                if redefine.find(")") > -1:
                                    brackCount = brackCount - len(re.findall(r"\)", redefine))
                                if rName != "":
                                    redefineMap[rName].append(redefine)

                            if brackCount == 0:
                                rName = ""

                        for reset in resetList:
                            if reset == "" or reset.startswith(r"/*"):
                                continue
                            resultLine, rname = convertLine(reset, start, "1", dataType, filePath, activeList)
                            if rname not in activeList:
                                continue
                            lines.append(resultLine)
                            if rname in redefineMap:
                                convertRedefineLine(rname, redefineMap, start, dataType, filePath, lines, 1)

                    else:
                        codes = [r for r in re.split(" +", line) if r != ""]
                        if len(codes) == 0:
                            continue
                        index = codes[0]

                        if index == "R":
                            index = codes[1]
                            name = codes[2]
                            resultLine = start + " " * int(index) + index.rjust(2,
                                                                                "0") + " " + "FILLER REDEFINES" + " " + name.replace(
                                "#", "S-") + "."
                            if str(index).rjust(2, "0") == "01":
                                for i in range(len(lines) - 1, -1, -1):
                                    if lines[i].strip().startswith("01") and lines[i].find(
                                            " " + name.replace("#", "S-") + " ") > -1:
                                        lines[i] = start + " " * int(index) + index.rjust(2, "0") + " " + name.replace(
                                            "#",
                                            "S-") + "."
                                        break
                            else:
                                lines.append(resultLine)
                            continue
                        elif index == "G" or index == "V" or index == "P":
                            codes.remove(codes[0])
                            index = codes[0]
                        elif index == "*":
                            continue
                        name = codes[1]
                        if len(codes) < 4:
                            resultLine = start + " " * int(index) + index.rjust(2,
                                                                                "0") + " " + name.replace("#",
                                                                                                          "S-") + "."
                            lines.append(resultLine)
                            continue
                        t = codes[2]
                        length = codes[3]
                        resultLine = start + " " * int(index) + index.rjust(2, "0") + " " + name.replace("#",
                                                                                                         "S-").ljust(20,
                                                                                                                     " ")
                        resultLine = convertByType(resultLine, dataType, t, length, filePath, name)

                        if occursIndex != "" and occursIndex != index and maxOccurs > 0:
                            for i in range(len(lines) - 1, -1, -1):
                                if lines[i].strip().startswith(str(int(occursIndex) - 1).rjust(2, "0")):
                                    lines[i] = lines[i].replace(".", " OCCURS " + str(maxOccurs) + ".")
                                    break
                            occursIndex = ""
                            maxOccurs = 0

                        if len(codes) > 4 and re.search(ptn_array_pattern, codes[4]):
                            occursIndex = index
                            maxOccurs = max(maxOccurs, int(codes[4].split(":")[-1].replace(")", "")))
                        elif len(codes) > 4 and re.search(ptn_array1_pattern, codes[4]):
                            occursIndex = index
                            maxOccurs = max(maxOccurs, int(codes[4].replace(")", "").replace("(", "")))
                        resultLine = resultLine + "."
                        lines.append(resultLine)

        resultList = []
        muchOneMatch = re.findall(r" +01 .+?\n", "\n".join(lines) + "\n")
        if muchOneMatch and len(muchOneMatch) > 1:
            for l in lines:
                index = re.match(r" +(\d+) +", l).group(1)
                resultList.append(l.replace(" " + index + " ", "  " + str(int(index) + 1).rjust(2, "0") + " "))
        else:
            resultList = lines

        fileName = os.path.basename(filePath)
        with open(os.path.join(resultPath, fileName), "w") as wt:
            wt.writelines([l.ljust(80, " ") + "\n" for l in resultList])


if __name__ == "__main__":
    layoutCobolHandler(sys.argv[1], sys.argv[2])
