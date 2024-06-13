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

    condition_df = pd.read_excel(PLI_setting_path, sheet_name="���Y���")
    for cond, val in zip(condition_df["����"], condition_df["�ݒ�"]):
        if cond == "�ݒ����HIT�֘A���o�́i��ID�j":
            �ݒ����HIT���o�� = val == "�o�͂���"

        if cond == "�ݒ����HIT�֘A���o�́i����ID�j":
            ���͏���HIT���o�� = val == "�o�͂���"

        if cond == "�ݒ����HIT�֘A���o�́i�݌vID�j":
            �݌v����HIT���o�� = val == "�o�͂���"

        if cond == "�ݒ����HIT-NG���o��":
            �ݒ����HIT_NG���o�� = val == "�o�͂���"

        if cond == "COBOL���o�͊֘A���o��":
            PLI���o�͏��o�� = val == "�o�͂���"

        if cond == "DB�X�V����":
            IsDelete = val == "���s�O�Ɋ֘ATABLE�N���A����"

        if cond == "���ʏo�̓t�H���_1":
            ������_path = val

        if cond == "���ʏo�̓t�H���_1":
            ������_path = val

        if cond == "���ʏo�̓t�H���_1":
            �g�[�N�����_path = val

        if cond == "���ʃt�@�C���o�͐���i�\�[�X�R�[�h�j":
            ������_out = val == "�o�͂���"

        if cond == "���ʃt�@�C���o�͐���i�����͗p�j":
            ������_out = val == "�o�͂���"

        if cond == "���ʃt�@�C���o�͐���iİ�ݍč\���p�j":
            �g�[�N�����_out = val == "�o�͂���"

    if os.path.isdir(title) == False:
        os.makedirs(title)

    PLISheet = pd.read_excel(PLI_setting_path, sheet_name="PLI�ݒ�V�[�g")
    PLISheet.fillna("", inplace=True)
    PLISheet = PLISheet.values.tolist()
    PLISheet = [[""] + sheet for sheet in PLISheet]
    PLISheet = setting_re_pattern_sheet(PLISheet)

    function_sheet = pd.read_excel(PLI_setting_path, sheet_name="�g�ݍ��݊֐�")
    function_sheet = function_sheet.values.tolist()

    pli_keyword_dict = generate_pli_dict_from_sheet(PLISheet,
                                                    key_index=2,
                                                    value_index=7)
    pli_function_dict = generate_pli_dict_from_sheet(function_sheet,
                                                     key_index=0,
                                                     value_index=1)

    # ���s�O��DB���폜�����I�������ꍇ�ɍ폜����
    if IsDelete:
        print("you chose to clear db, so clear the remaining data.")

        conn = connect_accdb(db_base_path)

        cursor = conn.cursor()

        sql = "DELETE FROM �ACOBOL_���o�͏��1"
        cursor.execute(sql)
        sql = "DELETE FROM �ACOBOL_���o�͏��2"
        cursor.execute(sql)
        sql = "DELETE FROM �ACOBOL_���o�͏��3"
        cursor.execute(sql)
        sql = "DELETE FROM �ACOBOL_�֘A���Y"
        cursor.execute(sql)
        sql = "DELETE FROM �ACOBOL_CMD���"
        cursor.execute(sql)
        sql = "DELETE FROM �ACOBOL_��{���"
        cursor.execute(sql)
        sql = "DELETE FROM ����_PGM_IO���"
        cursor.execute(sql)

        # 'HIT���֘A���폜
        sql = "DELETE FROM ����_���Y���_�֘A���"
        cursor.execute(sql)
        # 'HIT-NG���֘A���폜
        sql = "DELETE FROM ����_���Y���_NG���"
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

        db_path = title + "\\������DB_" + Folder_name + "_" + str(
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
                db_path = title + "\\������DB_" + Folder_name + "_" + str(
                    file_num) + ".accdb"
                command = "copy " + db_base_path + " " + db_path
                subprocess.call(command, shell=True)
                print("Create the new accdb file ", db_path)
                conn = connect_accdb(db_path)
                cursor = conn.cursor()

            �t�@�C���� = get_filename(PLI_File)
            �t�@�C����2 = take_extensions(�t�@�C����)
            print(f"\rAnalysis: {i + 1} / {ld}, File = {�t�@�C����}", end="")

            try:
                TmpSheet = analysis1_1_read_text_PLI(PLI_File)
                if ������_out == True:
                    ActSheet_all, output_header = make_output_list_val_length(
                        TmpSheet, [
                            "�s���", "�W��", "�̈�A����", "�̈�B�̂�", "���ݽ��", "73-80",
                            "�����Y�s�ԍ�", "�����Y�s���"
                        ])
                    # output_header = ["�s���","�W��","�̈�A����","�̈�B�̂�","���ݽ��","73-80","�����Y�s�ԍ�","�����Y�s���"]
                    write_excel_multi_sheet(
                        "�����͌���_" + �t�@�C����2.replace("%", "_") + ".xlsx",
                        ActSheet_all, "������", ������_path, output_header)

                TokenSheet, call_table, filename_dd_io_table, filename_copy_relation_table, io_filename_table \
                    = analysis1_2_lexical_PLI(TmpSheet, pli_keyword_dict, pli_function_dict, function_sheet)
                if ������_out == True:
                    ActSheet_all, output_header = make_output_list_val_length(
                        TokenSheet, ["�s�ԍ����", "�s���", "�L�q�̈�", "�K�w���", "TOKEN���"])

                    # output_header = ["�s�ԍ����","�s���","�L�q�̈�","�K�w���","TOKEN���"]
                    write_excel_multi_sheet(
                        "�����͌���_" + �t�@�C����2.replace("%", "_") + ".xlsx",
                        ActSheet_all, "������", ������_path, output_header)

                TokenSheet2 = analysis1_3_rebuild_Token_PLI(
                    TokenSheet, pli_keyword_dict)
                if �g�[�N�����_out == True:
                    ActSheet_all, output_header = make_output_list_val_length(
                        TokenSheet2, ["�s�ԍ����", "�s���", "�L�q�̈�", "�K�w���", "������"])

                    # output_header = ["�s�ԍ����","�s���","�L�q�̈�","�K�w���","������"]
                    write_excel_multi_sheet(
                        "�g�[�N����͌���_" + �t�@�C����2.replace("%", "_") + ".xlsx",
                        ActSheet_all, "�g�[�N�����", �g�[�N�����_path, output_header)

                analysis1_4_structure_PLI(TokenSheet2, PLISheet, �t�@�C����, db_path,
                                        call_table, TmpSheet, pli_keyword_dict,
                                        pli_function_dict, �ݒ����HIT���o��,
                                        ���͏���HIT���o��, �݌v����HIT���o��, �ݒ����HIT_NG���o��,
                                        conn, cursor)
                if PLI���o�͏��o��:
                    PLI_IO_Info(TokenSheet2, �t�@�C����, db_path, conn, cursor,
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
