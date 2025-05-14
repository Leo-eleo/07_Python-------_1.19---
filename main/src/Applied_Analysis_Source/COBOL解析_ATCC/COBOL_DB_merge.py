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
                    SELECT * FROM �ACOBOL_CMD��� WHERE CMD���� = 'CALL'
                    """
        else:
            sql = """\
                    SELECT * FROM �ACOBOL_CMD���
                    """

        df = pd.read_sql(sql, conn)
        df.fillna("", inplace=True)
        COBOL_CMD += df.values.tolist()
        COBOL_CMD_header = df.columns.tolist()

        sql = """\
                SELECT * FROM �ACOBOL_�֘A���Y
                """

        df = pd.read_sql(sql, conn)
        df.fillna("", inplace=True)
        COBOL_relate_asset += df.values.tolist()
        COBOL_relate_asset_header = df.columns.tolist()

        sql = """\
                SELECT * FROM �ACOBOL_��{���
                """

        df = pd.read_sql(sql, conn)
        df.fillna("", inplace=True)
        COBOL_basic_info += df.values.tolist()
        COBOL_basic_info_header = df.columns.tolist()

        sql = """\
                SELECT * FROM �ACOBOL_���o�͏��1
                """

        df = pd.read_sql(sql, conn)
        df.fillna("", inplace=True)
        COBOL_IO_1 += df.values.tolist()
        COBOL_IO_1_header = df.columns.tolist()

        sql = """\
                SELECT * FROM �ACOBOL_���o�͏��2
                """

        df = pd.read_sql(sql, conn)
        df.fillna("", inplace=True)
        COBOL_IO_2 += df.values.tolist()
        COBOL_IO_2_header = df.columns.tolist()

        sql = """\
                SELECT * FROM �ACOBOL_���o�͏��3
                """

        df = pd.read_sql(sql, conn)
        df.fillna("", inplace=True)
        COBOL_IO_3 += df.values.tolist()
        COBOL_IO_3_header = df.columns.tolist()

        sql = """\
                SELECT * FROM ����_PGM_IO���
                """

        df = pd.read_sql(sql, conn)
        df.fillna("", inplace=True)
        COMMON_PGM_IO += df.values.tolist()
        COMMON_PGM_IO_header = df.columns.tolist()

        sql = """\
                SELECT * FROM ����_���Y���_NG���
                """

        df = pd.read_sql(sql, conn)
        df.fillna("", inplace=True)
        COMMON_ANALYSIS_NG += df.values.tolist()
        COMMON_ANALYSIS_NG_header = df.columns.tolist()

        sql = """\
                SELECT * FROM ����_���Y���_�֘A���
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

    write_excel_multi_sheet("COBOL_CMD���_merge��.xlsx", COBOL_CMD,
                            "COBOL_CMD���", title, COBOL_CMD_header)
    write_excel_multi_sheet("COBOL_�֘A���Y_merge��.xlsx", COBOL_relate_asset,
                            "COBOL_�֘A���Y", title, COBOL_relate_asset_header)
    write_excel_multi_sheet("COBOL_��{���_merge��.xlsx", COBOL_basic_info,
                            "COBOL_��{���", title, COBOL_basic_info_header)
    write_excel_multi_sheet("COBOL_���o�͏��1_merge��.xlsx", COBOL_IO_1,
                            "COBOL_���o�͏��1", title, COBOL_IO_1_header)
    write_excel_multi_sheet("COBOL_���o�͏��2_merge��.xlsx", COBOL_IO_2,
                            "COBOL_���o�͏��2", title, COBOL_IO_2_header)
    write_excel_multi_sheet("COBOL_���o�͏��3_merge��.xlsx", COBOL_IO_3,
                            "COBOL_���o�͏��3", title, COBOL_IO_3_header)
    write_excel_multi_sheet("����_PGM_IO���_merge��.xlsx", COMMON_PGM_IO,
                            "����_PGM_IO���", title, COMMON_PGM_IO_header)
    write_excel_multi_sheet("����_���Y���_NG���_merge��.xlsx", COMMON_ANALYSIS_NG,
                            "����_���Y���_NG���", title, COMMON_ANALYSIS_NG_header)
    write_excel_multi_sheet("����_���Y���_�֘A���_merge��.xlsx", COMMON_ANALYSIS_relate,
                            "����_���Y���_�֘A���", title,
                            COMMON_ANALYSIS_relate_header)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])

    ### ����1 COBOL��͍�DB�̊i�[�t�H���_ ����2 �o�̓t�H���_