#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
import time
import bas_main
import traceback

import subprocess
import shutil

from analysis1_1_read_text_PLI import analysis1_1_read_text_PLI
from analysis1_2_lexical_PLI import analysis1_2_lexical_PLI
from analysis1_3_rebuild_Token_PLI import analysis1_3_rebuild_Token_PLI
from analysis1_4_structure_PLI import analysis1_4_structure_PLI
from PLI_IO_Info import PLI_IO_Info
from common_Regular_Expression import setting_re_pattern_sheet

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

def generate_pli_dict_from_sheet(sheet, key_index, value_index):
    return_dict = {}
    for item in sheet:
        return_dict[item[key_index]] = item[value_index]
    return return_dict

def connect_accdb(db_path):

    assert os.path.isfile(db_path), "file path is invalid : " + db_path

    conn_str = (
                r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                r'DBQ=' + db_path
                )

    conn = pyodbc.connect(conn_str,autocommit=False)
    return conn


def main_all_folder(db_base_path, Folder_PLI_path, PLI_setting_path, title):
    time_start = time.time()
    low_value_change = False
    low_value_replace = "20"
    print("Start preparation for analysis.")

    condition_df = pd.read_excel(PLI_setting_path, sheet_name="資産解析")
    for cond, val in zip(condition_df["項目"], condition_df["設定"]):
        if cond == "設定条件HIT関連情報出力（ｷｰID）":
            設定条件HIT情報出力 = val == "出力する"

        if cond == "設定条件HIT関連情報出力（分析ID）":
            分析条件HIT情報出力 = val == "出力する"

        if cond == "設定条件HIT関連情報出力（設計ID）":
            設計条件HIT情報出力 = val == "出力する"

        if cond == "設定条件HIT-NG情報出力":
            設定条件HIT_NG情報出力 = val == "出力する"

        if cond == "COBOL入出力関連情報出力":
            PLI入出力情報出力 = val == "出力する"

        if cond == "DB更新制御":
            IsDelete = val == "実行前に関連TABLEクリアする"

        if cond == "結果出力フォルダ1":
            言語解析_path = val

        if cond == "結果出力フォルダ1":
            字句解析_path = val

        if cond == "結果出力フォルダ1":
            トークン解析_path = val

        if cond == "結果ファイル出力制御（ソースコード）":
            言語解析_out = val == "出力する"

        if cond == "結果ファイル出力制御（字句解析用）":
            字句解析_out = val == "出力する"

        if cond == "結果ファイル出力制御（ﾄｰｸﾝ再構成用）":
            トークン解析_out = val == "出力する"

    if os.path.isdir(title) == False:
        os.makedirs(title)

    PLISheet = pd.read_excel(PLI_setting_path, sheet_name="PLI設定シート")
    PLISheet.fillna("", inplace=True)
    PLISheet = PLISheet.values.tolist()
    PLISheet = [[""] + sheet for sheet in PLISheet]
    PLISheet = setting_re_pattern_sheet(PLISheet)

    function_sheet = pd.read_excel(PLI_setting_path, sheet_name="組み込み関数")
    function_sheet = function_sheet.values.tolist()

    pli_keyword_dict = generate_pli_dict_from_sheet(PLISheet,
                                                    key_index=2,
                                                    value_index=7)
    pli_function_dict = generate_pli_dict_from_sheet(function_sheet,
                                                     key_index=0,
                                                     value_index=1)

    # 実行前にDBを削除するを選択した場合に削除する
    if IsDelete:
        print("you chose to clear db, so clear the remaining data.")

        conn = connect_accdb(db_base_path)

        cursor = conn.cursor()

        sql = "DELETE FROM ②COBOL_入出力情報1"
        cursor.execute(sql)
        sql = "DELETE FROM ②COBOL_入出力情報2"
        cursor.execute(sql)
        sql = "DELETE FROM ②COBOL_入出力情報3"
        cursor.execute(sql)
        sql = "DELETE FROM ②COBOL_関連資産"
        cursor.execute(sql)
        sql = "DELETE FROM ②COBOL_CMD情報"
        cursor.execute(sql)
        sql = "DELETE FROM ②COBOL_基本情報"
        cursor.execute(sql)
        sql = "DELETE FROM 共通_PGM_IO情報"
        cursor.execute(sql)

        # 'HIT時関連情報削除
        sql = "DELETE FROM 共通_資産解析_関連情報"
        cursor.execute(sql)
        # 'HIT-NG時関連情報削除
        sql = "DELETE FROM 共通_資産解析_NG情報"
        cursor.execute(sql)
        conn.commit()
        conn.close()

    print("Finish preparation and start analysis.")
    PLI_Folders = glob_files(Folder_PLI_path, recursive=False, type="folder")
    PLI_Folders.append(Folder_PLI_path)
    # PLI_Files = glob_files(Folder_PLI_path)

    for PLI_Folder in PLI_Folders:
        prepare_temp_path = title + "\\" + "TEMP"
        if not os.path.exists(prepare_temp_path):
            os.makedirs(prepare_temp_path)
        bas_main.bas_main(PLI_Folder, prepare_temp_path, low_value_change, low_value_replace)
        # if PLI_Folder == Folder_PLI_path:
        #     PLI_Files = glob_files(PLI_Folder, recursive=False, type="file")

        #     if len(PLI_Files) == 0:
        #         continue

        Folder_name = os.path.split(PLI_Folder)[-1]

        file_num = 1
        print("Start analysis the folder of ", Folder_name)

        db_path = title + "\\言語解析DB_" + Folder_name + "_" + str(
            file_num) + ".accdb"
        command = "copy " + db_base_path + " " + db_path
        subprocess.call(command, shell=True)
        print("Create the new accdb file ", db_path)

        PLI_Files = glob_files(prepare_temp_path, recursive=False, type="file")

        ld = len(PLI_Files)
        conn = connect_accdb(db_path)
        cursor = conn.cursor()

        for i, PLI_File in enumerate(PLI_Files):
            if os.path.getsize(db_path) >= 1500000000:
                conn.close()
                file_num += 1
                db_path = title + "\\言語解析DB_" + Folder_name + "_" + str(
                    file_num) + ".accdb"
                command = "copy " + db_base_path + " " + db_path
                subprocess.call(command, shell=True)
                print("Create the new accdb file ", db_path)
                conn = connect_accdb(db_path)
                cursor = conn.cursor()

            ファイル名 = get_filename(PLI_File)
            ファイル名2 = take_extensions(ファイル名)
            print(f"\rAnalysis: {i + 1} / {ld}, File = {ファイル名}", end="")

            try:
                TmpSheet = analysis1_1_read_text_PLI(PLI_File)
                if 言語解析_out == True:
                    ActSheet_all, output_header = make_output_list_val_length(
                        TmpSheet, [
                            "行情報", "標識", "領域Aあり", "領域Bのみ", "ｼｰｹﾝｽ域", "73-80",
                            "元資産行番号", "元資産行情報"
                        ])
                    # output_header = ["行情報","標識","領域Aあり","領域Bのみ","ｼｰｹﾝｽ域","73-80","元資産行番号","元資産行情報"]
                    write_excel_multi_sheet(
                        "言語解析結果_" + ファイル名2.replace("%", "_") + ".xlsx",
                        ActSheet_all, "言語解析", 言語解析_path, output_header)

                TokenSheet, call_table, filename_dd_io_table, filename_copy_relation_table, io_filename_table \
                    = analysis1_2_lexical_PLI(TmpSheet, pli_keyword_dict, pli_function_dict, function_sheet)
                if 字句解析_out == True:
                    ActSheet_all, output_header = make_output_list_val_length(
                        TokenSheet, ["行番号情報", "行情報", "記述領域", "階層情報", "TOKEN情報"])

                    # output_header = ["行番号情報","行情報","記述領域","階層情報","TOKEN情報"]
                    write_excel_multi_sheet(
                        "字句解析結果_" + ファイル名2.replace("%", "_") + ".xlsx",
                        ActSheet_all, "字句解析", 字句解析_path, output_header)

                TokenSheet2 = analysis1_3_rebuild_Token_PLI(
                    TokenSheet, pli_keyword_dict)
                if トークン解析_out == True:
                    ActSheet_all, output_header = make_output_list_val_length(
                        TokenSheet2, ["行番号情報", "行情報", "記述領域", "階層情報", "制御情報"])

                    # output_header = ["行番号情報","行情報","記述領域","階層情報","制御情報"]
                    write_excel_multi_sheet(
                        "トークン解析結果_" + ファイル名2.replace("%", "_") + ".xlsx",
                        ActSheet_all, "トークン解析", トークン解析_path, output_header)

                analysis1_4_structure_PLI(TokenSheet2, PLISheet, ファイル名, db_path,
                                        call_table, TmpSheet, pli_keyword_dict,
                                        pli_function_dict, 設定条件HIT情報出力,
                                        分析条件HIT情報出力, 設計条件HIT情報出力, 設定条件HIT_NG情報出力,
                                        conn, cursor)
                if PLI入出力情報出力:
                    PLI_IO_Info(TokenSheet2, ファイル名, db_path, conn, cursor,
                                filename_dd_io_table, filename_copy_relation_table,
                                io_filename_table)
                conn.commit()
            except Exception as e:
                conn.rollback()
                error_path = os.path.join(title, f"ErrorFile_{Folder_name}")
                if not os.path.exists(error_path):
                    os.makedirs(error_path)
                true_file_path = os.path.join(PLI_Folder, os.path.basename(PLI_File))
                shutil.move(true_file_path, error_path)
                print(f" Error!")
                with open(os.path.join(error_path, "00_Error_Info.txt"), "a", encoding="CP932") as ft:
                    ft.write(f"file_name: {os.path.basename(PLI_File)}\n")
                    ft.write(traceback.format_exc())
                    ft.write("\n")

        conn.close()
        print("\nClean Temp File...")
        shutil.rmtree(prepare_temp_path)
        time_end = time.time()
        time_sum = time_end - time_start
        print(f"Analysis finished, time is {time_sum} second")



if __name__ == "__main__":
    main_all_folder(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
