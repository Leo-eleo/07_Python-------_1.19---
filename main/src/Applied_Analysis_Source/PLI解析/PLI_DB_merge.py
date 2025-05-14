#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


def main(Folder_PLI_path, title, Limit_Call_Order="True", rem_extensions=True):

    if type(Limit_Call_Order) != bool:
        Limit_Call_Order = Limit_Call_Order == "True"

    if os.path.isdir(title) == False:
        os.makedirs(title)

    PLI_Files = glob_files(Folder_PLI_path)
    PLI_CMD = []
    PLI_relate_asset = []
    PLI_basic_info = []
    PLI_IO_1 = []
    PLI_IO_2 = []
    PLI_IO_3 = []
    COMMON_PGM_IO = []
    COMMON_ANALYSIS_NG = []
    COMMON_ANALYSIS_relate = []

    PLI_CMD_header = []
    PLI_relate_asset_header = []
    PLI_basic_info_header = []
    PLI_IO_1_header = []
    PLI_IO_2_header = []
    PLI_IO_3_header = []
    COMMON_PGM_IO_header = []
    COMMON_ANALYSIS_NG_header = []
    COMMON_ANALYSIS_relate_header = []

    print("start to merge DB data")
    for PLI_File in PLI_Files:
        conn = connect_accdb(PLI_File)

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
        PLI_CMD += df.values.tolist()
        PLI_CMD_header = df.columns.tolist()

        sql = """\
                SELECT * FROM �ACOBOL_�֘A���Y
                """

        df = pd.read_sql(sql, conn)
        df.fillna("", inplace=True)
        PLI_relate_asset += df.values.tolist()
        PLI_relate_asset_header = df.columns.tolist()

        sql = """\
                SELECT * FROM �ACOBOL_��{���
                """

        df = pd.read_sql(sql, conn)
        df.fillna("", inplace=True)
        PLI_basic_info += df.values.tolist()
        PLI_basic_info_header = df.columns.tolist()

        sql = """\
                SELECT * FROM �ACOBOL_���o�͏��1
                """

        df = pd.read_sql(sql, conn)
        df.fillna("", inplace=True)
        PLI_IO_1 += df.values.tolist()
        PLI_IO_1_header = df.columns.tolist()

        sql = """\
                SELECT * FROM �ACOBOL_���o�͏��2
                """

        df = pd.read_sql(sql, conn)
        df.fillna("", inplace=True)
        PLI_IO_2 += df.values.tolist()
        PLI_IO_2_header = df.columns.tolist()

        sql = """\
                SELECT * FROM �ACOBOL_���o�͏��3
                """

        df = pd.read_sql(sql, conn)
        df.fillna("", inplace=True)
        PLI_IO_3 += df.values.tolist()
        PLI_IO_3_header = df.columns.tolist()

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
        PLI_CMD = take_all_extensions(PLI_CMD)
        PLI_relate_asset = take_all_extensions(PLI_relate_asset)
        PLI_basic_info = take_all_extensions(PLI_basic_info)
        PLI_IO_1 = take_all_extensions(PLI_IO_1)
        PLI_IO_2 = take_all_extensions(PLI_IO_2)
        PLI_IO_3 = take_all_extensions(PLI_IO_3)
        COMMON_PGM_IO = take_all_extensions(COMMON_PGM_IO)
        COMMON_ANALYSIS_NG = take_all_extensions(COMMON_ANALYSIS_NG)
        COMMON_ANALYSIS_relate = take_all_extensions(COMMON_ANALYSIS_relate)

    write_excel_multi_sheet("PLI_CMD���_merge��.xlsx", PLI_CMD, "PLI_CMD���",
                            title, PLI_CMD_header)
    write_excel_multi_sheet("PLI_�֘A���Y_merge��.xlsx", PLI_relate_asset,
                            "PLI_�֘A���Y", title, PLI_relate_asset_header)
    write_excel_multi_sheet("PLI_��{���_merge��.xlsx", PLI_basic_info, "PLI_��{���",
                            title, PLI_basic_info_header)
    write_excel_multi_sheet("PLI_���o�͏��1_merge��.xlsx", PLI_IO_1, "PLI_���o�͏��1",
                            title, PLI_IO_1_header)
    write_excel_multi_sheet("PLI_���o�͏��2_merge��.xlsx", PLI_IO_2, "PLI_���o�͏��2",
                            title, PLI_IO_2_header)
    write_excel_multi_sheet("PLI_���o�͏��3_merge��.xlsx", PLI_IO_3, "PLI_���o�͏��3",
                            title, PLI_IO_3_header)
    write_excel_multi_sheet("����_PGM_IO���_merge��.xlsx", COMMON_PGM_IO,
                            "����_PGM_IO���", title, COMMON_PGM_IO_header)
    write_excel_multi_sheet("����_���Y���_NG���_merge��.xlsx", COMMON_ANALYSIS_NG,
                            "����_���Y���_NG���", title, COMMON_ANALYSIS_NG_header)
    write_excel_multi_sheet("����_���Y���_�֘A���_merge��.xlsx", COMMON_ANALYSIS_relate,
                            "����_���Y���_�֘A���", title,
                            COMMON_ANALYSIS_relate_header)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])

    ### ����1 PLI��͍�DB�̊i�[�t�H���_ ����2 �o�̓t�H���_