#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


def main(Folder_COBOL_path,
         title,
         Limit_Call_Order="True",
         rem_extensions=True):

    if type(Limit_Call_Order) != bool:
        Limit_Call_Order = Limit_Call_Order == "True"

    if os.path.isdir(title) == False:
        os.makedirs(title)

    COBOL_Files = glob_files(Folder_COBOL_path)
    COBOL_CMD = []
    COBOL_relate_asset = []
    COBOL_basic_info = []
    COBOL_IO_1 = []
    COBOL_IO_2 = []
    COBOL_IO_3 = []
    COMMON_PGM_IO = []
    COMMON_ANALYSIS_NG = []
    COMMON_ANALYSIS_relate = []

    COBOL_CMD_header = []
    COBOL_relate_asset_header = []
    COBOL_basic_info_header = []
    COBOL_IO_1_header = []
    COBOL_IO_2_header = []
    COBOL_IO_3_header = []
    COMMON_PGM_IO_header = []
    COMMON_ANALYSIS_NG_header = []
    COMMON_ANALYSIS_relate_header = []

    print("start to merge DB data")
    for COBOL_File in COBOL_Files:
        conn = connect_accdb(COBOL_File)

        if Limit_Call_Order == True:
            sql = """\
                    SELECT * FROM ②COBOL_CMD情報 WHERE CMD分類 = 'CALL'
                    """
        else:
            sql = """\
                    SELECT * FROM ②COBOL_CMD情報
                    """

        df = pd.read_sql(sql, conn)
        df.fillna("", inplace=True)
        COBOL_CMD += df.values.tolist()
        COBOL_CMD_header = df.columns.tolist()

        sql = """\
                SELECT * FROM ②COBOL_関連資産
                """

        df = pd.read_sql(sql, conn)
        df.fillna("", inplace=True)
        COBOL_relate_asset += df.values.tolist()
        COBOL_relate_asset_header = df.columns.tolist()

        sql = """\
                SELECT * FROM ②COBOL_基本情報
                """

        df = pd.read_sql(sql, conn)
        df.fillna("", inplace=True)
        COBOL_basic_info += df.values.tolist()
        COBOL_basic_info_header = df.columns.tolist()

        sql = """\
                SELECT * FROM ②COBOL_入出力情報1
                """

        df = pd.read_sql(sql, conn)
        df.fillna("", inplace=True)
        COBOL_IO_1 += df.values.tolist()
        COBOL_IO_1_header = df.columns.tolist()

        sql = """\
                SELECT * FROM ②COBOL_入出力情報2
                """

        df = pd.read_sql(sql, conn)
        df.fillna("", inplace=True)
        COBOL_IO_2 += df.values.tolist()
        COBOL_IO_2_header = df.columns.tolist()

        sql = """\
                SELECT * FROM ②COBOL_入出力情報3
                """

        df = pd.read_sql(sql, conn)
        df.fillna("", inplace=True)
        COBOL_IO_3 += df.values.tolist()
        COBOL_IO_3_header = df.columns.tolist()

        sql = """\
                SELECT * FROM 共通_PGM_IO情報
                """

        df = pd.read_sql(sql, conn)
        df.fillna("", inplace=True)
        COMMON_PGM_IO += df.values.tolist()
        COMMON_PGM_IO_header = df.columns.tolist()

        sql = """\
                SELECT * FROM 共通_資産解析_NG情報
                """

        df = pd.read_sql(sql, conn)
        df.fillna("", inplace=True)
        COMMON_ANALYSIS_NG += df.values.tolist()
        COMMON_ANALYSIS_NG_header = df.columns.tolist()

        sql = """\
                SELECT * FROM 共通_資産解析_関連情報
                """

        df = pd.read_sql(sql, conn)
        df.fillna("", inplace=True)
        COMMON_ANALYSIS_relate += df.values.tolist()
        COMMON_ANALYSIS_relate_header = df.columns.tolist()

    if rem_extensions:
        COBOL_CMD = take_all_extensions(COBOL_CMD)
        COBOL_relate_asset = take_all_extensions(COBOL_relate_asset)
        COBOL_basic_info = take_all_extensions(COBOL_basic_info)
        COBOL_IO_1 = take_all_extensions(COBOL_IO_1)
        COBOL_IO_2 = take_all_extensions(COBOL_IO_2)
        COBOL_IO_3 = take_all_extensions(COBOL_IO_3)
        COMMON_PGM_IO = take_all_extensions(COMMON_PGM_IO)
        COMMON_ANALYSIS_NG = take_all_extensions(COMMON_ANALYSIS_NG)
        COMMON_ANALYSIS_relate = take_all_extensions(COMMON_ANALYSIS_relate)

    write_excel_multi_sheet("COBOL_CMD情報_merge版.xlsx", COBOL_CMD,
                            "COBOL_CMD情報", title, COBOL_CMD_header)
    write_excel_multi_sheet("COBOL_関連資産_merge版.xlsx", COBOL_relate_asset,
                            "COBOL_関連資産", title, COBOL_relate_asset_header)
    write_excel_multi_sheet("COBOL_基本情報_merge版.xlsx", COBOL_basic_info,
                            "COBOL_基本情報", title, COBOL_basic_info_header)
    write_excel_multi_sheet("COBOL_入出力情報1_merge版.xlsx", COBOL_IO_1,
                            "COBOL_入出力情報1", title, COBOL_IO_1_header)
    write_excel_multi_sheet("COBOL_入出力情報2_merge版.xlsx", COBOL_IO_2,
                            "COBOL_入出力情報2", title, COBOL_IO_2_header)
    write_excel_multi_sheet("COBOL_入出力情報3_merge版.xlsx", COBOL_IO_3,
                            "COBOL_入出力情報3", title, COBOL_IO_3_header)
    write_excel_multi_sheet("共通_PGM_IO情報_merge版.xlsx", COMMON_PGM_IO,
                            "共通_PGM_IO情報", title, COMMON_PGM_IO_header)
    write_excel_multi_sheet("共通_資産解析_NG情報_merge版.xlsx", COMMON_ANALYSIS_NG,
                            "共通_資産解析_NG情報", title, COMMON_ANALYSIS_NG_header)
    write_excel_multi_sheet("共通_資産解析_関連情報_merge版.xlsx", COMMON_ANALYSIS_relate,
                            "共通_資産解析_関連情報", title,
                            COMMON_ANALYSIS_relate_header)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])

    ### 引数1 COBOL解析済DBの格納フォルダ 引数2 出力フォルダ