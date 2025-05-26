#!/usr/bin/env python
# -*- coding: cp932 -*-

def analysis0():
    
    
#'20250129 UPD qian.e.wang 長野県信テストIO出力対応
    # 'ヘッダー行作成
    output_header = [""]*46
    output_header[1] = "No"

    output_header[2] = "TEST_ID"
    output_header[3] = "実行順序"
    output_header[4] = "JCL_ID"
    output_header[5] = "LIBRARY"
    output_header[6] = "JOB_SEQ"  # '福山通運案件で追加
    output_header[7] = "JOB_ID"
    output_header[8] = "STEP_SEQ"

    output_header[9] = "STEP_SEQ2"   #  '★MHI案件で追加（予備）

    output_header[10] = "STEP_NAME"
    output_header[11] = "PGM_NAME"
    output_header[12] = "PROC_NAME"

    output_header[13] = "PGM_SYSIN"  #  '★MHI案件で追加
    output_header[14] = "BMCP_PGM"    # '追加 2021/06/08 Add Horiuchi　⇒20220215列13-44の位置1づつ移動

    output_header[15] = "DD_NAME"
    output_header[16] = "DSN"
    output_header[17] = "GDG"
    output_header[18] = "SYSIN"
        
    # '===　項目追加 ===
    output_header[19] = "DBNAME"           #        '★追加
        
    # '加工情報
    output_header[20] = "データ種別"            #   '★変更17→18
    output_header[21] = "データ種別2"            #  '★追加
    output_header[22] = "入出力情報"              # '★変更18→20
    output_header[23] = "入出力情報(DISP調整後)"   #'★移動31→21
    output_header[24] = "受領判定"                 #'★変更19→22
    output_header[25] = "DISP"                     #'★変更20→23
    output_header[26] = "SYSOUT"                   #'★変更21→24
    output_header[27] = "WRITER"                   #'★変更22→25
    output_header[28] = "FORM"                     #'★変更23→26
    output_header[29] = "UNIT"                     #'★変更24→27
    output_header[30] = "VOL"   #'VOL抽出追加       '★変更25→28
    output_header[31] = "SPACE"  #                  '★変更26→29
    output_header[32] = "RECFM"   #                 '★変更27→30
    output_header[33] = "LRECL"    #                '★変更28→31
    output_header[34] = "BLKSIZE"   #               '★変更29→32
    output_header[35] = "LABEL" #'LABEL抽出追加     '★変更30→33

    # '追加情報（MHI用）
    output_header[36] = "JCL_MBR"       #           '追加 2019/10/29
    output_header[37] = "レコード長"     #          '追加 2019/10/29
    output_header[38] = "テスト用受領判定"#         '追加 2019/10/29

    # '補足領域（参考値）
    output_header[39] = "発生順"           #        '★変更34→37
    output_header[40] = "内部ロジック"      #       '★変更35→38
    output_header[41] = "元変数値"           #      '★変更36→39

    # '追加情報　※今後の案件で出力位置を調整する
    output_header[42] = "PGM予備"             #     '追加 2020/04/30
    output_header[43] = "実行モード"           #    '追加 2020/04/30

    # '後続処理で追加
    output_header[44] = "コメント"            #    '
    output_header[45] = "元順序"               #   '

    # 'output_header[32] = "入出力情報(DISP調整後)"  '★移動31→21
    # 'output_header[33] = "移行対象判定"            '★廃止（利用していない）
# UPD END
    return output_header