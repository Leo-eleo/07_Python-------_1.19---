#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

from reserved_word_table_PLI import reserved_word_table_PLI

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

Rwords = reserved_word_table_PLI()


def �\��ꔻ��_PLI(STR):
    if STR in Rwords:
        return True
    else:
        return False


def ���s����_PLI():
    global ���O�g�[�N��, ���O�g�[�N��2, ���s����FLG, ����������
    # '���s����t���O
    # 'EXEC SQL �` END-EXEC �Ȃǂ̓r���ɉ��s�L�[���[�h�����Ă����s�����Ȃ��悤�ɐ��䂷��
    if ���s����FLG:
        if ���������� == "END-EXEC":
            ���s����FLG = False
            return True  # '���ۂɉ��s�ɂȂ�̂͌��������񂪗\�������𖞂����ꍇ
    else:

        if ���O�g�[�N��2 == "EXEC" and ���O�g�[�N�� == "SQL":
            ���s����FLG = True
            return False

        # '        elif ���O�g�[�N��2 = "CURSOR" and ���O�g�[�N�� = "FOR": # '���s����t���O�̒ǉ��ɂ�肱�̏ꍇ�͋N���Ȃ�
        # '            return False
        elif ���O�g�[�N��2 == "EXEC" and ���O�g�[�N�� == "CICS":
            return False
        else:
            return True
    return False


def �g�[�N���o��_PLI(P_STR):
    global ���O�g�[�N��, ���O�g�[�N��2

    ���O�g�[�N��2 = ���O�g�[�N��  # '���̃g�[�N���̉��s����ɗ��p
    ���O�g�[�N�� = P_STR  # '���̃g�[�N���̉��s����ɗ��p


def analysis1_3_rebuild_Token_PLI(TokenSheet, pli_keyword_dict):
    global ���O�g�[�N��, ���O�g�[�N��2, ���s����FLG, ����������

    ��� = 5  # 'TokenSheet�@��|�C���^
    ���2 = 6  # 'TokenSheet2 ��|�C���^
    �����s = 0  # 'TokenSheet�@�s�|�C���^
    ���O�g�[�N�� = ""
    ���O�g�[�N��2 = ""
    �o�͍s = 1
    ���s����FLG = False
    ���������� = ""
    TokenSheet2 = []
    TokenSheet2_GYO = [""] * 6
    hit_flg = False
    while �����s < len(TokenSheet):
        TokenSheet_GYO = TokenSheet[�����s]

        if TokenSheet_GYO[4] != "�w�b�_�[":  # '�w�b�_�[�͏������Ȃ�
            # '�ŏ��̏����s�̏����o��
            if TokenSheet2_GYO != [""] * 6:
                TokenSheet2.append(TokenSheet2_GYO)
            TokenSheet2_GYO = [""] * 6
            �o�͍s = �o�͍s + 1
            TokenSheet2_GYO[1] = TokenSheet_GYO[1]  # '�����Y�s�ԍ�
            TokenSheet2_GYO[2] = TokenSheet_GYO[2]  # '�s���
            TokenSheet2_GYO[3] = TokenSheet_GYO[3]  # '�L�q�̈�
            TokenSheet2_GYO[4] = TokenSheet_GYO[4]  # '�K�w���

            # '�o�͗� = 5
            �o�͗� = ���2
            hit_flg = False

            while True:

                # '������ = 4
                ������ = ���

                while True:
                    ���������� = TokenSheet_GYO[������]

                    #   if �\��ꔻ��_PLI(����������) and ���s����_PLI()and �o�͗� > ���2:

                    # if ���s����_PLI() and �\��ꔻ��_PLI(����������) and �o�͗� > ���2:
                    #
                    #     if TokenSheet2_GYO != [""] * 6:
                    #         TokenSheet2.append(TokenSheet2_GYO)
                    #     TokenSheet2_GYO = [""] * 6
                    #
                    #     �o�͍s = �o�͍s + 1
                    #     TokenSheet2_GYO[1] = TokenSheet_GYO[1]
                    #     TokenSheet2_GYO[2] = TokenSheet_GYO[2]
                    #     TokenSheet2_GYO[3] = TokenSheet_GYO[3]
                    #     TokenSheet2_GYO[4] = TokenSheet_GYO[4]
                    #     # '�o�͗� = 5
                    #     �o�͗� = ���2
                    #     ���O�g�[�N�� = ""
                    #     ���O�g�[�N��2 = ""

                    # '�Ώۃg�[�N���o�͂���щߋ�2�񕪂̃g�[�N����ޔ�����
                    �g�[�N���o��_PLI(����������)
                    TokenSheet2_GYO.append(����������)

                    #                 'Call �g�[�N���o��_PLI(TokenSheet_GYO[������])

                    #                 '�g�[�N���č\�z�̍s�I�������𖞂�����
                    # 'MERGER FROM Ver1.13.1
                    #                 '�܂�ɂP�s�ɕ����̏I���������܂ނ΂�������
                    # '                if (TokenSheet_GYO[������] = "." or \
                    # '                    TokenSheet_GYO[������] = ";" or \
                    # '                    TokenSheet_GYO[������] = ",") and \
                    # '                   TokenSheet_GYO[������ + 1] = "":
                    # '                   hit_flg = True
                    # '                End if
                    if (TokenSheet_GYO[������] == ":"
                        or TokenSheet_GYO[������] == ";"
                        or pli_keyword_dict.get(TokenSheet_GYO[������]) == "THEN"
                        or pli_keyword_dict.get(TokenSheet_GYO[������]) == "ELSE"
                        or pli_keyword_dict.get(TokenSheet_GYO[������]) == "OTHER"
                        or pli_keyword_dict.get(TokenSheet_GYO[������]) == "OTHERWISE") and \
                            ������ + 1 >= len(TokenSheet_GYO):
                        hit_flg = True

                    # # '***** ADD START *****
                    # #                 'EJECT�ASKIP�̔���
                    # if (TokenSheet_GYO[������] == "EJECT" or
                    #     TokenSheet_GYO[������] == "SKIP1" or
                    #     TokenSheet_GYO[������] == "SKIP2" or
                    #     TokenSheet_GYO[������] == "SKIP3") and \
                    #         ������ + 1 >= len(TokenSheet_GYO):
                    #     hit_flg = True
                    # # '***** ADD END   *****

                    ������ = ������ + 1
                    �o�͗� = �o�͗� + 1
                    if ������ >= len(TokenSheet_GYO) or hit_flg:
                        break
                �����s = �����s + 1
                if �����s >= len(TokenSheet) or hit_flg:
                    break
                TokenSheet_GYO = TokenSheet[�����s]

        #   '�o�͍s = �o�͍s + 1  '�o�͎��ɃJ�E���g�A�b�v�ɕύX

        #   '�w�b�_�[�s�̏ꍇ�̓��[�h�X�L�b�v
        else:
            �����s = �����s + 1

        if �����s >= len(TokenSheet):
            break

    if TokenSheet2_GYO != [""] * 6:
        TokenSheet2.append(TokenSheet2_GYO)
    #    '���䏈���s�Ƀ}�[�N
    #         'ELSE END-** �̔���Łu-1�v�𐧌䂷�锻��ňꕔ�s�����A����̉ۑ�iTAKEI�j
    �����s = 2  # 'TokenSheet2�@�s�|�C���^
    ����CNT = 0

    for i in range(len(TokenSheet2)):
        # '������ = 5
        ������ = ���2
        hit_flg = False
        while ������ < len(TokenSheet2[i]) and hit_flg == False:
            if pli_keyword_dict.get(TokenSheet2[i][������]) == "IF":
                ����CNT = ����CNT + 1
                TokenSheet2[i][���2 - 1] = "IF-" + str(����CNT)
                hit_flg = True
            elif pli_keyword_dict.get(TokenSheet2[i][������]) == "ELSE":
                ����CNT = ����CNT + 1
                TokenSheet2[i][���2 - 1] = "ELSE-" + str(����CNT)
                hit_flg = True
            elif TokenSheet2[i][������] == ";":
                ����CNT = 0

            ������ = ������ + 1

    return TokenSheet2
