import os
import shutil
import sys
import pandas
import datetime
import time
import Clist_Analysis_common
import Clist_2_Read_text
import Clist_3_Lexical
import Clist_4_Rebuild_Token
import Clist_5_Structure


def main(db_path, setting_path, input_path, output_path):
    # ⑫_1_事前処理
    start_time_format = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    time_start = time.time()
    clist_sheet = Clist_Analysis_common.get_setting_excel(setting_path, "CLIST設定シート")
    # Base Setting
    設定条件HIT情報出力, 分析条件HIT情報出力, 設計条件HIT情報出力, 設定条件HIT_NG情報出力, IsDelete = Clist_Analysis_common.get_base_setting(setting_path)
    # フォルダリストの取得
    folder_list = Clist_Analysis_common.get_folder_list(input_path)
    if len(folder_list) == 0:
        folder_list.append(input_path)
    # すべてのフォルダーの取り扱い
    for folder in folder_list:
        # Create new accessdb file, and connect it
        db_new_path = os.path.join(output_path, f"{os.path.splitext(os.path.basename(folder))[0]}_{start_time_format}.accdb")
        shutil.copy(db_path, db_new_path)
        db_conn = Clist_Analysis_common.connect_accdb(db_new_path)
        # 実行時TABLE削除
        if IsDelete:
            Clist_Analysis_common.delete_db_table(db_conn)
        # ⑫_0_主処理
        print(f"\nStart process folder: {folder}")
        # Start process for one folder
        file_list = Clist_Analysis_common.get_file_list(folder)
        file_count = len(file_list)
        file_name_max_length = 0
        for i, file in enumerate(file_list):
            file_name_max_length = Clist_Analysis_common.print_process_log(i, file_count, file, file_name_max_length)
            try:
                TmpSheet = Clist_2_Read_text.clist_2_read_text(file)
                TokenSheet = Clist_3_Lexical.clist_3_lexical(TmpSheet)
                TokenSheet2 = Clist_4_Rebuild_Token.clist_4_rebuild_token(TokenSheet)
                Clist_5_Structure.clist_5_structure(TokenSheet2, db_conn, file, clist_sheet, 設定条件HIT情報出力, 分析条件HIT情報出力, 設計条件HIT情報出力, 設定条件HIT_NG情報出力)
                db_conn.commit()
            except Exception as e:
                print(" Status: Error!")
                db_conn.rollback()
    time_end = time.time()
    time_sum = time_end - time_start
    print(f"\nAnalysis finished, time is {time_sum} second")


if __name__ == "__main__":
    # # ! Debug
    # db_path = r"C:\Users\yi.a.qian\Desktop\Work\230725_CLIST_Vba_2_Python\db\言語解析DB_V1.29.00_empty.accdb"
    # setting_path = r"C:\Users\yi.a.qian\Desktop\Work\230725_CLIST_Vba_2_Python\Clist_Analysis\Clist_Setting.xlsx"
    # input_path = r"C:\Users\yi.a.qian\Desktop\Work\230725_CLIST_Vba_2_Python\CLIST"
    # output_path = r"C:\Users\yi.a.qian\Desktop\Work\230725_CLIST_Vba_2_Python\Res"
    # main(db_path, setting_path, input_path, output_path)
    main(sys.argv[1], sys.argv[3], sys.argv[2], sys.argv[4])