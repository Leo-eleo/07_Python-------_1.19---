import glob
import os
import re
import sys


def nativePLISourceHandler(sourcePath, resultPath):
    sources = glob_files(sourcePath)
    file_len = len(sources)

    for i, file in enumerate(sources):
        result = []
        with open(file, "r", errors="ignore") as ft:
            # content = ft.read()
            startFlg = False
            endFlg = False
            # for line in content.splitlines():
            while True:
                line = ft.readline()
                if not line:
                    break
                line = line.strip("\n")
                if not startFlg:
                    startFlg = re.search(r"SOURCE +<START> +ECRUOS", line)
                    continue
                if not endFlg:
                    endFlg = re.search(r"SOURCE +<FINIS> +ECRUOS", line)

                if startFlg and not endFlg and not (line.replace(" ", "") == "" or re.search(r"1PL/I +OPTIMIZING +COMPILER", line)
                        or re.search(r"- +STMT +LEV +NT", line)):
                    byteLen = len(line.encode("CP932"))
                    if byteLen > 120:
                        line = re.sub(r"INIT\(.*\)", r"INIT('超長リテラル')", line)
                        line = re.sub(r"/\*.*?\*/", r"", line)
                    if byteLen > 97:
                        line = line[17: 97]
                    else:
                        line = line[17::]
                    result.append(line + "\n")
        outputPath = os.path.join(resultPath, os.path.basename(file))
        with open(outputPath, "w", encoding="cp932") as outFile:
            outFile.writelines(result)
        print(f"\rFinished: {i + 1} / {file_len}", end="")


def glob_files(file_path, recursive=True, type="file"):
    assert os.path.exists(file_path), "file path is invalid : " + file_path

    files = glob.glob(file_path + "/**", recursive=recursive)
    if type == "file":
        return [p for p in files if os.path.isfile(p)]

    elif type == "folder":
        return [p for p in files if os.path.isdir(p)]


if __name__ == "__main__":
    nativePLISourceHandler(sys.argv[1], sys.argv[2])
