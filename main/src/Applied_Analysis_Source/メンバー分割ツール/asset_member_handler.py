import glob
import os
import sys


def assetDivisionHandler(sourcePath, resultPath):
    sources = glob_files(sourcePath)
    file_count = 1

    for file in sources:
        fileName = os.path.basename(file)
        with open(file, "r", errors="ignore") as ft:
            content = [tmp for tmp in ft.read().split("VMEMBER NAME") if tmp != ""]
            for mn in content:
                endIndex = mn.find("\n") + 1
                pattern = mn[0:endIndex].replace("\n", "").strip().replace("\\", "￥")\
                    .replace("<", "＜").replace(">", "＞").replace("|", "｜").replace(":", "：")\
                    .replace("*", "＊").replace("?", "？").replace("/", "・")

                # Windows ファイルに使えない文字、非表示文字を●に置き換え
                patternFile = pattern.replace('\\', '●').replace('/', '●').replace(':', '●').replace('*', '●')\
                    .replace('?', '●').replace('"', '●').replace("'", '●').replace('<', '●').replace('>', '●')\
                    .replace('|', '●').replace('(', '●').replace(')', '●').replace('[', '●').replace(']', '●')\
                    .replace('\t', '●').replace('\r', '●').replace('\n', '●').replace('\0', '●')\
                    .replace('^', '●').replace('･', '●')\
                    .replace('\x01', '●').replace('\x02', '●').replace('\x03', '●').replace('\x04', '●')\
                    .replace('\x05', '●').replace('\x06', '●').replace('\x07', '●').replace('\x08', '●')\
                    .replace('\x09', '●').replace('\x0a', '●').replace('\x0b', '●').replace('\x0c', '●')\
                    .replace('\x0d', '●').replace('\x0e', '●').replace('\x0f', '●').replace('\x10', '●')\
                    .replace('\x11', '●').replace('\x12', '●').replace('\x13', '●').replace('\x14', '●')\
                    .replace('\x15', '●').replace('\x16', '●').replace('\x17', '●').replace('\x18', '●')\
                    .replace('\x19', '●').replace('\x1a', '●').replace('\x1b', '●').replace('\x1c', '●')\
                    .replace('\x1d', '●').replace('\x1e', '●').replace('\x1f', '●').replace('\x7f', '●')\

                # 半角スペースを削除
                patternFile = patternFile.replace(' ', '')

                # patternとpatternFileが不一致の場合、_と4桁連番をpatternFileの後ろに付ける
                if pattern != patternFile:
                    patternFile = patternFile + "_化け文字" + str(file_count).zfill(4)
                    file_count += 1

                # 対象ファイル名出力
                print("⇒受領ファイル名: {}, 受領メンバー名: {}, 出力ファイル名: {}".format(fileName, pattern, patternFile))

                mn = mn[endIndex::]
                mn = mn.replace("++ID TSO", "++ID *TSO").replace("\nV", "\n")
                if mn.startswith("V"):
                    mn = mn[1::]
                outputPath = os.path.join(resultPath, fileName + "%A%" + patternFile + ".txt")
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
