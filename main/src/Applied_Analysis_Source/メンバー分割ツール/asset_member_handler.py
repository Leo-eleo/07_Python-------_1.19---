import glob
import os
import sys


def assetDivisionHandler(sourcePath, resultPath):
    sources = glob_files(sourcePath)

    for file in sources:
        fileName = os.path.basename(file)
        with open(file, "r", errors="ignore") as ft:
            content = [tmp for tmp in ft.read().split("VMEMBER NAME") if tmp != ""]
            for mn in content:
                endIndex = mn.find("\n") + 1
                pattern = mn[0:endIndex].replace("\n", "").strip().replace("\\", "￥")\
                    .replace("<", "＜").replace(">", "＞").replace("|", "｜").replace(":", "：")\
                    .replace("*", "＊").replace("?", "？").replace("/", "・")
                mn = mn[endIndex::]
                mn = mn.replace("++ID TSO", "++ID *TSO").replace("\nV", "\n")
                if mn.startswith("V"):
                    mn = mn[1::]
                outputPath = os.path.join(resultPath, fileName + "%A%" + pattern + ".txt")
                with open(outputPath, "w") as outFile:
                    outFile.write(mn)
    change_dos_to_unix(resultPath)


def glob_files(file_path, recursive=True, type="file"):
    assert os.path.exists(file_path), "file path is invalid : " + file_path

    files = glob.glob(file_path + "/**", recursive=recursive)
    if type == "file":
        return [p for p in files if os.path.isfile(p)]

    elif type == "folder":
        return [p for p in files if os.path.isdir(p)]


def change_dos_to_unix(path):
    for item in os.listdir(path):
        with open(os.path.join(path, item), "rb+") as file_handle:
            all_text = file_handle.read()
            all_change_text = all_text.replace(b"\r\n", b"\n")
            file_handle.seek(0, 0)
            file_handle.truncate()
            file_handle.write(all_change_text)


if __name__ == "__main__":
    assetDivisionHandler(sys.argv[1], sys.argv[2])
