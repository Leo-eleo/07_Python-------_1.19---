import os
import time
import pyodbc
import shutil
import pandas
import helper
import sys
import datetime

global error_msg
global start_time, exit_flag
global 複数ライブラリ処理, フォルダ_元資産, 出力フォルダ_資産分類結果, ライブラリ名判定方法
global 入力資産ファイル形式_拡張子有無, 入力資産ファイル形式_ライブラリ名有無, 入力資産ファイル形式_メンバーID有無
global 実行時TABLE削除, 資産分類結果クリア
global db_conn, db_path, setting_path

global モジュールID, ライブラリID, メンバーID, 拡張子

global 資産_資産行数, 資産_最少文字数, 資産_最大文字数, ALL_chk_ok, 資産_チェック, 資産_分類レベル
global JOB指定有無, macro指定有無, 資産_チェック_サマリ

global 資産分類条件Sheet, 資産_分類_判定, 資産_資産格納先, 資産_資産分類, 資産_格納資産名

global Folder, ファイル名
global folder_number, folder_number_max

分類レベル_dict = helper.資産_分類レベル_dict


def get_files(path):
    return [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def get_subfolders(folder_path):
    subfolders = []
    for sub_folder in os.listdir(folder_path):
        each_path = os.path.join(folder_path, sub_folder)
        if os.path.isdir(each_path):
            subfolders.append(each_path)
    return subfolders


def get_bool_from_param(parm):
    if parm == 1 or parm.upper() == "TRUE":
        return True
    else:
        return False


def get_資産分類条件Sheet(excel_path):
    global 資産分類条件Sheet
    資産分類条件Sheet = pandas.read_excel(excel_path, sheet_name="資産分類条件")
    資産分類条件Sheet.fillna("", inplace=True)
    資産分類条件Sheet = 資産分類条件Sheet.values.tolist()
    資産分類条件Sheet = [[""] + sheet for sheet in 資産分類条件Sheet]


def connect_accdb(db_path_local):
    assert os.path.isfile(db_path_local), "file path is invalid : " + db_path_local
    conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                r'DBQ=' + db_path_local)
    conn = pyodbc.connect(conn_str, autocommit=True)
    return conn


def 基本設定():
    global error_msg, db_path, setting_path
    global start_time, exit_flag
    global 複数ライブラリ処理, フォルダ_元資産, 出力フォルダ_資産分類結果, ライブラリ名判定方法
    global ライブラリID
    global 入力資産ファイル形式_拡張子有無, 入力資産ファイル形式_ライブラリ名有無, 入力資産ファイル形式_メンバーID有無
    global 実行時TABLE削除, 資産分類結果クリア
    # INIT
    start_time = time.time()
    exit_flag = False
    複数ライブラリ処理 = sys.argv[5] == "複数ライブラリ対応"
    フォルダ_元資産 = sys.argv[1]
    出力フォルダ_資産分類結果 = sys.argv[2]
    ライブラリ名判定方法 = sys.argv[6]
    if ライブラリ名判定方法 == "①直接指定する":
        ライブラリID = sys.argv[7]
        if ライブラリID == "":
            error_msg = "ライブラリ名を指定してください"
            exit_flag = True
    入力資産ファイル形式_拡張子有無 = sys.argv[8]
    入力資産ファイル形式_ライブラリ名有無 = sys.argv[9]
    入力資産ファイル形式_メンバーID有無 = sys.argv[10]
    実行時TABLE削除 = get_bool_from_param(sys.argv[11])
    資産分類結果クリア = get_bool_from_param(sys.argv[12])
    db_path = sys.argv[4]
    setting_path = sys.argv[3]
    # フォルダのクリーンアップ
    if 資産分類結果クリア:
        資産資産出力先フォルダクリア処理()


def 資産資産出力先フォルダクリア処理():
    # フォルダ以下のファイルおよびすべてのサブディレクトリを削除します。
    for root, dirs, files in os.walk(出力フォルダ_資産分類結果):
        for file_name in files:
            os.remove(os.path.join(root, file_name))
        for dir_name in dirs:
            shutil.rmtree(os.path.join(root, dir_name))


def 共通_ファイル名分割処理(file_name):
    global モジュールID, ライブラリID, メンバーID, 拡張子
    一時文字列 = file_name.split("%")
    if 入力資産ファイル形式_ライブラリ名有無 != "①なし":
        if ライブラリ名判定方法 == "③ファイル名から取得":
            ライブラリID = 一時文字列[0]
        if 入力資産ファイル形式_メンバーID有無 != "①なし":
            モジュールID = 一時文字列[1]
            if 入力資産ファイル形式_拡張子有無 != "①なし":
                一時文字列2 = 一時文字列[2].split(".")
                メンバーID = 一時文字列2[0]
                拡張子 = 一時文字列2[1]
            else:
                メンバーID = 一時文字列[2]
        else:
            if 入力資産ファイル形式_拡張子有無 != "①なし":
                一時文字列2 = 一時文字列[1].split(".")
                モジュールID = 一時文字列2[0]
                拡張子 = 一時文字列2[1]
            else:
                モジュールID = 一時文字列[1]
    else:
        if 入力資産ファイル形式_メンバーID有無 != "①なし":
            if 入力資産ファイル形式_拡張子有無 != "①なし":
                モジュールID = 一時文字列[0]
                一時文字列2 = 一時文字列[1].split(".")
                メンバーID = 一時文字列2[0]
                拡張子 = 一時文字列2[1]
            else:
                モジュールID = 一時文字列[0]
                メンバーID = 一時文字列[1]
        else:
            if 入力資産ファイル形式_拡張子有無 != "①なし":
                一時文字列2 = 一時文字列[0].split(".")
                モジュールID = 一時文字列2[0]
                拡張子 = 一時文字列2[1]
            else:
                モジュールID = 一時文字列[0]


def F_0_事前処理():
    global error_msg, exit_flag
    global db_conn
    if フォルダ_元資産 == "":
        error_msg = "資産分析対象フォルダ（分類前）が設定されていません。"
        exit_flag = True
        return
    elif 出力フォルダ_資産分類結果 == "":
        error_msg = "資産分類結果出力先フォルダが設定されていません。"
        exit_flag = True
        return
    # データベースを出力先アドレスにコピーする
    process_start_time = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    db_new_path = os.path.join(出力フォルダ_資産分類結果, f"{os.path.splitext(os.path.basename(db_path))[0]}_{process_start_time}.accdb")
    shutil.copy(db_path, db_new_path)
    db_conn = connect_accdb(db_new_path)
    if 実行時TABLE削除:
        sql = "DELETE FROM ④資産分類情報"
        db_conn.execute(sql)


def F_1_主処理(folder):
    global Folder, ファイル名
    Folder = folder
    # 検索文字 = "*"
    files = get_files(folder)
    file_number_max = len(files)
    for index, file in enumerate(files):
        ファイル名 = os.path.basename(file)
        F_2_テキストファイル読み込み(file)
        F_3_資産判定()
        F_3_資産判定_例外対応()
        F_4_資産分類条件取得()
        F_5_資産分類処理(folder)
        print(f"Processing: Folder {folder_number} / {folder_number_max}, File {index + 1} / {file_number_max}, Name = {ファイル名}")


def F_2_テキストファイル読み込み(file_path):
    global 資産_資産行数, 資産_最少文字数, 資産_最大文字数, ALL_chk_ok, 資産_チェック, 資産_分類レベル
    global JOB指定有無, macro指定有無, 資産_チェック_サマリ
    # 初期設定
    共通_ファイル名分割処理(os.path.basename(file_path))
    資産_資産行数 = 0
    資産_最少文字数 = 80
    資産_最大文字数 = 80
    ALL_chk_ok = True
    資産_チェック = [""] * 6
    資産_分類レベル = [0] * 21
    JOB指定有無 = False
    macro指定有無 = False
    # ファイルを読み込んで、正式に処理を開始する
    with open(file_path, "r", encoding="CP932") as f:
        while True:
            strREC = f.readline()
            if not strREC:
                break
            strREC = strREC.strip("\n")
            # テキスト長を取得する
            処理行文字数 = len(strREC.encode("CP932"))
            if 処理行文字数 > 資産_最大文字数:
                資産_最大文字数 = 処理行文字数
            if 処理行文字数 < 資産_最少文字数:
                資産_最少文字数 = 処理行文字数
            # エラーチェック（オンコーディング）
            if 資産_最大文字数 != 資産_最少文字数:
                ALL_chk_ok = False
            # SOとSIの有無チェック
            if chr(14) in strREC:
                資産_チェック[1] = "●"
            if chr(15) in strREC:
                資産_チェック[2] = "●"
            # エラーチェックサマリ
            if ALL_chk_ok:
                資産_チェック_サマリ = "OK"
            else:
                資産_チェック_サマリ = "NG"
            # 資産分類チェック（外部パラメータ設定）
            for item in 資産分類条件Sheet:
                資産_分類先 = item[2]
                資産_レベル = item[4]
                資産_分類_キーワード = item[5]
                if 資産_分類_キーワード in strREC:
                    資産_分類レベル[分類レベル_dict[資産_分類先]] = 資産_分類レベル[分類レベル_dict[資産_分類先]] + 資産_レベル
            # 例外キーワードチェック
            if strREC[:3] != "//*" and " JOB " in strREC:
                JOB指定有無 = True
            if strREC[:1] != "*" and " MACRO " in strREC:
                macro指定有無 = True
            # 処理行カウント
            資産_資産行数 = 資産_資産行数 + 1


def F_3_資産判定():
    global 資産_分類_判定
    資産_分類レベル_MAX = 0
    資産_分類_判定 = "⑳"
    for index, value in enumerate(資産_分類レベル):
        if value > 資産_分類レベル_MAX:
            資産_分類レベル_MAX = value
            資産_分類_判定 = 分類レベル_dict[index]


def F_3_資産判定_例外対応():
    global 資産_分類_判定
    if 資産_分類_判定 == "①":
        if not JOB指定有無:
            資産_分類_判定 = "⑤"
    # if 資産_分類_判定 == "⑦":
    #     if macro指定有無:
    #         資産_分類_判定 = "⑧"


def F_4_資産分類条件取得():
    global 資産_資産格納先, 資産_資産分類, 資産_格納資産名
    Cmd1 = "SELECT ④資産分類マスタ.ID, ④資産分類マスタ.資産分類, ④資産分類マスタ.資産名付与文字_前, " + \
           "④資産分類マスタ.資産名付与文字_後, ④資産分類マスタ.資産格納先 " + \
           "FROM ④資産分類マスタ WHERE ((④資産分類マスタ.ID)='"
    Cmd2 = "');"
    # データベースへの接続と分類データの取得
    cursor = db_conn.cursor()
    cursor.execute(f"{Cmd1}{資産_分類_判定}{Cmd2}")
    db_master_info = cursor.fetchone()
    # 変数の初期化
    資産_資産分類 = ""
    資産_資産名付与文字_前 = ""
    資産_資産名付与文字_後 = ""
    資産_資産格納先 = ""
    # データベースに分類条件がない場合、各変数を空にしておく。
    if db_master_info:
        if db_master_info[1]:
            資産_資産分類 = db_master_info[1]
        if db_master_info[2]:
            資産_資産名付与文字_前 = db_master_info[2]
        if db_master_info[3]:
            資産_資産名付与文字_後 = db_master_info[3]
        if db_master_info[4]:
            資産_資産格納先 = db_master_info[4]
    # 資産_格納資産名 = 資産_資産名付与文字_前 + モジュールID + 資産_資産名付与文字_後
    # 資産_格納資産名 = 資産_資産名付与文字_前 + ファイル名 + 資産_資産名付与文字_後
    資産_格納資産名 = f"{資産_資産名付与文字_前}{ライブラリID}%{モジュールID}%{メンバーID}{資産_資産名付与文字_後}"


def F_5_資産分類処理(入力フォルダPATH):
    Cmd1 = "INSERT INTO ④資産分類情報 (" + \
           "受領資産ライブラリ," + \
           "受領資産名," + \
           "受領資産パス," + \
           "資産分類," + \
           "分類資産名," + \
           "分類資産格納パス," + \
           "基本チェック結果," + \
           "資産行数," + \
           "最少文字数," + \
           "最大文字数," + \
           "チェック①," + \
           "チェック②," + \
           "チェック③," + \
           "チェック④," + \
           "チェック⑤,"
    Cmd2 = "資産分類要素①," + \
           "資産分類要素②," + \
           "資産分類要素③," + \
           "資産分類要素④," + \
           "資産分類要素⑤," + \
           "資産分類要素⑥," + \
           "資産分類要素⑦," + \
           "資産分類要素⑧," + \
           "資産分類要素⑨," + \
           "資産分類要素⑩," + \
           "資産分類要素⑪," + \
           "資産分類要素⑫," + \
           "資産分類要素⑬," + \
           "資産分類要素⑭," + \
           "資産分類要素⑮," + \
           "資産分類要素⑯," + \
           "資産分類要素⑰," + \
           "資産分類要素⑱," + \
           "資産分類要素⑲," + \
           "資産分類要素⑳" + \
           ") "
    Cmd3 = "VALUES(" + \
           "'" + ライブラリID + "'," + \
           "'" + ファイル名 + "'," + \
           "'" + Folder + "'," + \
           "'" + 資産_資産分類 + "'," + \
           "'" + 資産_格納資産名 + "'," + \
           "'" + 資産_資産格納先 + "'," + \
           "'" + 資産_チェック_サマリ + "'," + \
           str(資産_資産行数) + "," + \
           str(資産_最少文字数) + "," + \
           str(資産_最大文字数) + "," + \
           "'" + 資産_チェック[1] + "'," + \
           "'" + 資産_チェック[2] + "'," + \
           "'" + 資産_チェック[3] + "'," + \
           "'" + 資産_チェック[4] + "'," + \
           "'" + 資産_チェック[5] + "',"
    Cmd4 = str(資産_分類レベル[1]) + "," + \
           str(資産_分類レベル[2]) + "," + \
           str(資産_分類レベル[3]) + "," + \
           str(資産_分類レベル[4]) + "," + \
           str(資産_分類レベル[5]) + "," + \
           str(資産_分類レベル[6]) + "," + \
           str(資産_分類レベル[7]) + "," + \
           str(資産_分類レベル[8]) + "," + \
           str(資産_分類レベル[9]) + "," + \
           str(資産_分類レベル[10]) + "," + \
           str(資産_分類レベル[11]) + "," + \
           str(資産_分類レベル[12]) + "," + \
           str(資産_分類レベル[13]) + "," + \
           str(資産_分類レベル[14]) + "," + \
           str(資産_分類レベル[15]) + "," + \
           str(資産_分類レベル[16]) + "," + \
           str(資産_分類レベル[17]) + "," + \
           str(資産_分類レベル[18]) + "," + \
           str(資産_分類レベル[19]) + "," + \
           str(資産_分類レベル[20]) + ")"
    # データベースに挿入されたカテゴリー情報
    sql = Cmd1 + Cmd2 + Cmd3 + Cmd4
    db_conn.execute(sql)
    # ★★★★★★ファイルコピー機能
    if 資産_資産格納先 != "":
        入力ファイルPATH = os.path.join(入力フォルダPATH, ファイル名)
        出力ファイルPATH = os.path.join(資産_資産格納先, f"{資産_格納資産名}.{拡張子}")
        shutil.copy(入力ファイルPATH, 出力ファイルPATH)


def F_6_事後処理():
    db_conn.close()
    end_time = time.time()
    print(f"Process OK, Time is : {end_time - start_time}")


def main():
    global ライブラリID
    global folder_number, folder_number_max
    # 初期化されたフォルダの数
    folder_number = 1
    基本設定()
    F_0_事前処理()
    get_資産分類条件Sheet(setting_path)
    if exit_flag:
        print(error_msg)
        exit()
    # ! プロセスの開始
    # 複数ライブラリ
    if 複数ライブラリ処理:
        folders = get_subfolders(フォルダ_元資産)
        folder_number_max = len(folders)
        for sub_folder in folders:
            ライブラリID = sub_folder.replace(f"{フォルダ_元資産}{os.sep}", "")
            F_1_主処理(sub_folder)
            folder_number = folder_number + 1
    # 個別ライブラリ
    else:
        folder_number_max = 1
        F_1_主処理(フォルダ_元資産)
    F_6_事後処理()


if __name__ == "__main__":
    main()
