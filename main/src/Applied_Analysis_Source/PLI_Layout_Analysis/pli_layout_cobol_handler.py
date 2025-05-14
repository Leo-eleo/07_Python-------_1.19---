import glob
import logging
import os
import re
import sys

number_pattern = r"\((\d+)\)"
number1_pattern = r"\((\d+),(\d+)\)"

pic_pattern = r"\((\d+)\)\w"

logging.basicConfig(filename='pli_layout_cobol_handler' + '.log',
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
    lhMatch = re.search(number_pattern, length)

    lh = "0"
    if lhMatch:
        lh = lhMatch.group(1)
    else:
        lh1Match = re.search(number1_pattern, length)
        if lh1Match:
            lh = lh1Match.group(1)

    if t.upper() == "CHAR" or t.upper() == "CHARACTER":
        resultLine = resultLine + dataType + "X(" + lh.rjust(2, "0") + ")"
    elif t.upper() == "PIC" or t.upper() == "PICTURE":
        length = length.replace("V.", ".").replace("'", "").replace("\"", "")

        picLnMatcher = re.search(pic_pattern, length)
        if picLnMatcher:
            lsh = int(picLnMatcher.group(1)) + len(re.sub(pic_pattern, "", length))
            if lsh <= 18:
                resultLine = resultLine + dataType + "9(" + str(lsh).rjust(2, "0") + ")"
            else:
                resultLine = resultLine + dataType + "X(" + str(lsh).rjust(2, "0") + ")"
        else:
            resultLine = resultLine + dataType + length
    elif t.upper() == "BIT":
        resultLine = resultLine + dataType + "1(" + lh.rjust(2, "0") + ")" + " bit"
    elif t.upper() == "G":
        resultLine = resultLine + dataType + "X(" + str(int(lh) * 2).rjust(2, "0") + ")"
    elif t.upper() == "WIDECHAR":
        resultLine = resultLine + dataType + "X(" + str(int(lh) * 2).rjust(2, "0") + ")"
    elif t.upper() == "FIXED":
        if length.find("BIN") > -1 or length.find("bin") > -1:
            if int(lh) > 15:
                resultLine = resultLine + dataType + "s9(8) Comp"
            else:
                resultLine = resultLine + dataType + "s9(4) Comp"
        else:
            resultLine = resultLine + dataType + "s9(" + lh + ") Comp-3"
    elif t.upper() == "DEC":
        if length.find("FIXED") > -1 or length.find("fixed") > -1:
            resultLine = resultLine + dataType + "s9(" + lh + ") Comp-3"
        else:
            logging.warning("DEC layoutPath={}".format(layoutPath))
    elif t.upper() == "BIN":
        if length.find("FIXED") > -1 or length.find("fixed") > -1:
            if int(lh) > 15:
                resultLine = resultLine + dataType + "s9(8) Comp"
            else:
                resultLine = resultLine + dataType + "s9(4) Comp"
        else:
            logging.warning("BIN layoutPath={}".format(layoutPath))
    elif t.upper() == "FLOAT":
        if length.find("BIN") > -1 or length.find("bin") > -1:
            if int(lh) > 24:
                resultLine = resultLine + dataType + "USAGE IS Comp-2"
            else:
                resultLine = resultLine + dataType + "USAGE IS Comp-1"
        else:
            if int(lh) > 6:
                resultLine = resultLine + dataType + "USAGE IS Comp-2"
            else:
                resultLine = resultLine + dataType + "USAGE IS Comp-1"
    elif t.upper() == "NCHAR":
        resultLine = resultLine + dataType + "N(" + lh.rjust(2, "0") + ")"
    else:
        if t.find("BASED") == -1:
            logging.error("scm_file={}, name={}, value={}不具合".format(layoutPath, name, t))
    return resultLine


def layoutCobolHandler(layoutPath, resultPath):
    layoutList = glob_files(layoutPath)

    start = " " * 6
    dataType = " PIC "
    for filePath in layoutList:
        lines = []
        with open(filePath, "r", errors="ignore") as ft:
            content = ft.read()

            occursIndex = -1
            for l in content.split("\n"):
                if l.strip().startswith("INIT"):
                    continue
                line = l.replace("\x00", " ") + "\n"
                if line.startswith("0") or line.startswith("-"):
                    line = line[1::]
                line = re.sub(r"/\*.+?\*/", "", line)
                line = re.sub(r"\d{5} *\n", "", line)
                line = re.sub(r"^\d", "", line)
                if line.strip() == '':
                    continue
                commaIndex = line.rfind(";", 0, len(line))
                if commaIndex == -1:
                    commaIndex = line.rfind(",", 0, len(line))
                    if commaIndex == -1:
                        commaIndex = len(line)

                realLine = line[0: commaIndex].replace("/*", "")

                codes = [r for r in re.split(" +", realLine) if r != ""]
                if len(codes) == 0:
                    continue
                i = 0
                index = codes[i]

                name = codes[i + 1]

                if index.find("DCL") > -1:
                    index = "1"
                    if name == "1":
                        i = i + 1
                        name = codes[i + 1]

                if name == "DCL":
                    index = "1"
                    i = i + 1
                    name = codes[i + 1]
                    if name == "1":
                        i = i + 1
                        name = codes[i + 1]

                if re.search(r"^\d+$", index) is None:
                    codes.insert(0, "1")
                    name = index
                    index = "1"


                if name.endswith("("):
                    name = codes[i + 1].strip() + codes[i + 2].strip()
                    i = i + 1

                if occursIndex != -1 and occursIndex < int(index):
                    index = str(int(index) + 1)
                else:
                    occursIndex = -1

                numMatcher = re.search(number_pattern, name)
                if numMatcher:
                    name = re.sub(number_pattern, "", name) + " OCCURS " + str(
                        numMatcher.group(1))
                else:
                    num1Matcher = re.search(number1_pattern, name)
                    if num1Matcher:
                        name = re.sub(number1_pattern, "", name)
                        tempLine = start + " " * int(index) + index.rjust(2, "0") + " " + name + " OCCURS " + str(
                            num1Matcher.group(1)) + "."
                        lines.append(tempLine)
                        occursIndex = int(index)
                        index = str(int(index) + 1)
                        name = name + "-1" + " OCCURS " + str(num1Matcher.group(2))

                if len(codes) <= i + 2 or "".join(codes[i + 2]).find("BASED") > -1:
                    resultLine = start + " " * int(index) + index.rjust(2, "0") + " " + name + "."
                    lines.append(resultLine)
                    continue

                t = codes[i + 2]
                if t.upper() == "STATIC" or t.upper() == "UNAL":
                    i = i + 1
                    if i + 2 >= len(codes):
                        resultLine = start + " " * int(index) + index.rjust(2, "0") + " " + name + "."
                        lines.append(resultLine)
                        continue
                    t = codes[i + 2]
                elif t.upper() == "VAR":
                    tempLine = start + " " * int(index) + index.rjust(2, "0") + " " + name + "."
                    lines.append(tempLine)

                    index = str(int(index) + 1)

                    tempLine = start + " " * int(index) + index.rjust(2, "0") + " FILLER LEN USAGE IS Comp-5 " + "."
                    lines.append(tempLine)

                    i = i + 1
                    t = codes[i + 2]

                if re.fullmatch(number_pattern, t) or re.fullmatch(number1_pattern, t) or t == "(":
                    name = codes[i + 1].strip() + codes[i + 2].strip()
                    if t == "(":
                        name = name + codes[i + 3].strip()
                        i = i + 1
                    i = i + 1

                    numMatcher = re.search(number_pattern, name)
                    if numMatcher:
                        name = re.sub(number_pattern, "", name) + " OCCURS " + str(
                            numMatcher.group(1))
                    else:
                        num1Matcher = re.search(number1_pattern, name)
                        if num1Matcher:
                            name = re.sub(number1_pattern, "", name)
                            tempLine = start + " " * int(index) + index.rjust(2, "0") + " " + name + " OCCURS " + str(
                                num1Matcher.group(1)) + "."
                            lines.append(tempLine)
                            occursIndex = int(index)
                            index = str(int(index) + 1)
                            name = name + "-1" + " OCCURS " + str(num1Matcher.group(2))

                    if len(codes) <= i + 2 or "".join(codes[i + 2]).find("BASED(") > -1:
                        resultLine = start + " " * int(index) + index.rjust(2, "0") + " " + name + "."
                        lines.append(resultLine)
                        continue
                    else:
                        t = codes[i + 2]

                numberMatcher = re.search(number_pattern, t)
                if numberMatcher:
                    t = re.sub(number_pattern, "", t)
                    length = "(" + numberMatcher.group(1) + ")"
                else:
                    numberMatcher = re.search(number1_pattern, t)
                    if numberMatcher:
                        t = re.sub(number1_pattern, "", t)
                        length = "(" + numberMatcher.group(1) + ")"
                    else:
                        if t.find("(") > -1:
                            numberMatcher = re.search(number_pattern, "(" + "".join(codes[i + 3::]))
                            if numberMatcher:
                                length = "(" + numberMatcher.group(1) + ")"
                        else:
                            length = "".join(codes[i + 3::])

                        t = t.replace("(", "")

                if t.upper() == "DEF":
                    resultLine = start + " " * int(index) + index.rjust(2,
                                                                        "0") + " " + name + " REDEFINES " + length + "."
                    lines.append(resultLine)
                    continue

                if t.upper() == "CTL" or t.upper() == "MODE":
                    resultLine = start + " " * int(index) + index.rjust(2, "0") + " " + name + "."
                    lines.append(resultLine)
                    continue

                if t.find("PICTURE'") > -1 or t.find("PIC'") > -1:
                    length = t.replace("PICTURE'", "'").replace("PIC'", "'")
                    t = "PIC"

                if length.find("VAR") > -1:
                    tempLine = start + " " * int(index) + index.rjust(2, "0") + " " + name + "."
                    lines.append(tempLine)

                    index = str(int(index) + 1)

                    tempLine = start + " " * int(index) + index.rjust(2, "0") + " FILLER LEN USAGE IS Comp-5 " + "."
                    lines.append(tempLine)

                try:
                    resultLine = start + " " * int(index) + index.rjust(2, "0") + " " + name.ljust(20, " ")

                    resultLine = convertByType(resultLine, dataType, t, length, filePath, name)
                    resultLine = resultLine + "."
                    lines.append(resultLine)
                except Exception as e:
                    logging.error("エラー, message={}, scm_file={}".format(e, filePath))

        fileName = os.path.basename(filePath)
        with open(os.path.join(resultPath, fileName), "w") as wt:
            wt.writelines([l.ljust(80, " ") + "\n" for l in lines])


if __name__ == "__main__":
    layoutCobolHandler(sys.argv[1], sys.argv[2])
