import argparse
import os

import c_utiles
import c_parse_1_read_text
import c_parse_2_lexical
import c_parse_3_rebuild_token
import c_parse_4_structure
import c_io_info

from loguru import logger

logger.add("error_log.log", level="ERROR")


def arg_parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="C Parse Tool for Python")
    parser.add_argument("c_sources_folder", type=str, help="C sources folder")
    parser.add_argument("db_path", type=str, help="Parse result db (.accdb)")
    parser.add_argument("setting_path", type=str, help="Tool Config (Excel file)")
    parser.add_argument("result_folder", type=str, help="Parse result db output folder")
    parser.add_argument(
        "--remove_line72",
        "-R",
        action="store_true",
        help="If the file like cobol(72 - 80 is line no), then remove it",
    )
    return parser.parse_args()


def preparation(args: argparse.Namespace):
    logger.info("Start preparation for analysis.")
    _set = c_utiles.pre_process(args.setting_path)
    if _set.IsDelete:
        c_utiles.clear_db(args.db_path)
    if not os.path.exists(args.result_folder) or not os.path.isdir(args.result_folder):
        os.makedirs(args.result_folder)
    logger.info("Finish preparation and start analysis.")
    return


def pro_c_parse_file(file: str, file_name: str, cursor, c_call_fn, args: argparse.Namespace) -> None:
    lines = c_parse_1_read_text.read_text(file, args.remove_line72)
    tokens = c_parse_2_lexical.lexical(lines)
    rebuild_tokens, inner_fn, include, io_info = c_parse_3_rebuild_token.rebuild(tokens)
    c_parse_4_structure.structure(file_name, rebuild_tokens, inner_fn, cursor, c_call_fn, include, io_info)
    c_io_info.io_info_insert(cursor, file_name, io_info)


def pro_c_parse_foder(folder: str, args: argparse.Namespace, c_call_fn) -> None:
    folder_name = os.path.basename(folder)
    logger.info(f"Start analysis the folder of [{folder_name}]")
    files = c_utiles.glob_files(folder)
    if len(files) == 0:
        logger.warning(f"No file in folder: [{folder_name}]")
        return
    db_number = 1
    conn, cursor, target_db = c_utiles.gen_new_db(args.db_path, args.result_folder, db_number, folder_name)
    for i, file in enumerate(files):
        # Check DB Size
        if not c_utiles.check_db_size(target_db):
            # if db size too large, then generate a new access db
            db_number = db_number + 1
            conn, cursor, target_db = c_utiles.gen_new_db(args.db_path, args.result_folder, db_number, folder_name)
        file_name = os.path.splitext(os.path.basename(file))[0]
        # main process (for file)
        try:
            pro_c_parse_file(file, file_name, cursor, c_call_fn, args)
            conn.commit()
        except Exception:
            conn.rollback()
            logger.exception(f"Process Error! file -> [{file_name}]")
        logger.info(f"Process Finished [{i + 1} / {len(files)}], file -> [{file_name}]")
    logger.info(f"All analysis OK at folder: [{folder_name}]")
    conn.close()


def main(args: argparse.Namespace) -> None:
    # Pre Process
    preparation(args)
    C_Folders = c_utiles.glob_files(args.c_sources_folder, "folder", False)
    C_Folders.append(args.c_sources_folder)
    c_call_fn = c_utiles.gen_c_call_functions(args.setting_path)
    # Process all folders
    for C_Folder in C_Folders:
        pro_c_parse_foder(C_Folder, args, c_call_fn)
    logger.info("All folder analysis finished!")


if __name__ == "__main__":
    main(arg_parse())
