#!/usr/bin/env python
# -*- coding: cp932 -*-

def analysis0():
    
    
#'20250129 UPD qian.e.wang ���쌧�M�e�X�gIO�o�͑Ή�
    # '�w�b�_�[�s�쐬
    output_header = [""]*46
    output_header[1] = "No"

    output_header[2] = "TEST_ID"
    output_header[3] = "���s����"
    output_header[4] = "JCL_ID"
    output_header[5] = "LIBRARY"
    output_header[6] = "JOB_SEQ"  # '���R�ʉ^�Č��Œǉ�
    output_header[7] = "JOB_ID"
    output_header[8] = "STEP_SEQ"

    output_header[9] = "STEP_SEQ2"   #  '��MHI�Č��Œǉ��i�\���j

    output_header[10] = "STEP_NAME"
    output_header[11] = "PGM_NAME"
    output_header[12] = "PROC_NAME"

    output_header[13] = "PGM_SYSIN"  #  '��MHI�Č��Œǉ�
    output_header[14] = "BMCP_PGM"    # '�ǉ� 2021/06/08 Add Horiuchi�@��20220215��13-44�̈ʒu1�Âړ�

    output_header[15] = "DD_NAME"
    output_header[16] = "DSN"
    output_header[17] = "GDG"
    output_header[18] = "SYSIN"
        
    # '===�@���ڒǉ� ===
    output_header[19] = "DBNAME"           #        '���ǉ�
        
    # '���H���
    output_header[20] = "�f�[�^���"            #   '���ύX17��18
    output_header[21] = "�f�[�^���2"            #  '���ǉ�
    output_header[22] = "���o�͏��"              # '���ύX18��20
    output_header[23] = "���o�͏��(DISP������)"   #'���ړ�31��21
    output_header[24] = "��̔���"                 #'���ύX19��22
    output_header[25] = "DISP"                     #'���ύX20��23
    output_header[26] = "SYSOUT"                   #'���ύX21��24
    output_header[27] = "WRITER"                   #'���ύX22��25
    output_header[28] = "FORM"                     #'���ύX23��26
    output_header[29] = "UNIT"                     #'���ύX24��27
    output_header[30] = "VOL"   #'VOL���o�ǉ�       '���ύX25��28
    output_header[31] = "SPACE"  #                  '���ύX26��29
    output_header[32] = "RECFM"   #                 '���ύX27��30
    output_header[33] = "LRECL"    #                '���ύX28��31
    output_header[34] = "BLKSIZE"   #               '���ύX29��32
    output_header[35] = "LABEL" #'LABEL���o�ǉ�     '���ύX30��33

    # '�ǉ����iMHI�p�j
    output_header[36] = "JCL_MBR"       #           '�ǉ� 2019/10/29
    output_header[37] = "���R�[�h��"     #          '�ǉ� 2019/10/29
    output_header[38] = "�e�X�g�p��̔���"#         '�ǉ� 2019/10/29

    # '�⑫�̈�i�Q�l�l�j
    output_header[39] = "������"           #        '���ύX34��37
    output_header[40] = "�������W�b�N"      #       '���ύX35��38
    output_header[41] = "���ϐ��l"           #      '���ύX36��39

    # '�ǉ����@������̈Č��ŏo�͈ʒu�𒲐�����
    output_header[42] = "PGM�\��"             #     '�ǉ� 2020/04/30
    output_header[43] = "���s���[�h"           #    '�ǉ� 2020/04/30

    # '�㑱�����Œǉ�
    output_header[44] = "�R�����g"            #    '
    output_header[45] = "������"               #   '

    # 'output_header[32] = "���o�͏��(DISP������)"  '���ړ�31��21
    # 'output_header[33] = "�ڍs�Ώ۔���"            '���p�~�i���p���Ă��Ȃ��j
# UPD END
    return output_header