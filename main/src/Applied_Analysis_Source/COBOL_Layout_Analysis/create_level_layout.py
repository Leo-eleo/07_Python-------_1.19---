#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


�t�@�C���� = ""
DD�� = ""
�t�@�C����� = ""
���R�[�h�� = ""
�t�@�C���A�� = 0
�X�L�[�}�� = ""
COPY���� = ""
�G���[MSG = ""
OutSheet = []    
OutPut_folder = ""
                  
class QRY_COBOL_���o�͏��:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "QRY_COBOL_���o�͏��B"
        self.keys = []
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        self.keys = df.columns.tolist()
        for i in range(len(df)):
            data = df.iloc[i]
            cobol_id = data["COBOL_ID"]
            if cobol_id not in self.dic:
                self.dic[cobol_id] = []
                
            dic = {key:data[key] for key in self.keys}
            self.dic[cobol_id].append(dic)    
            
        
    def get(self,COBOL_ID):
        if self.dic == None:
            self.setup()
            
        if COBOL_ID in self.dic:
            return self.dic[COBOL_ID]

        else:
            return []
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        

class ���x�����C�A�E�g�֘A���ݒ�:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "01���x�����C�A�E�g�֘A���ݒ�"
        self.keys = []
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
              
    def insert(self): 
        if self.dic == None:
            self.setup()
            
        global ���W���[����,DD��,�t�@�C���A��,�X�L�[�}��
            
        key_list = ["COBOL","DD��","�t�@�C���A��","���C�A�E�g��"]
        value_list = [���W���[����,DD��,�t�@�C���A��,�X�L�[�}��]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
   
   
def ���ʈꗗ�o��():
    global ���W���[����,DD��,�t�@�C���A��,�X�L�[�}��,�t�@�C����,�t�@�C�����,COPY����,�G���[MSG,���R�[�h��
    global OutSheet
    global ���x�����C�A�E�g�֘A���ݒ�_
    
    OutSheet_gyo = [""]*10
    
    OutSheet_gyo[1] = ���W���[����
    # 'OutSheet_gyo[1] = ���̓t�@�C����
    OutSheet_gyo[7] = �X�L�[�}��
    
    OutSheet_gyo[2] = �t�@�C����
    OutSheet_gyo[3] = DD��
    OutSheet_gyo[4] = �t�@�C�����
    OutSheet_gyo[5] = ���R�[�h��
    OutSheet_gyo[6] = �t�@�C���A��
    
    OutSheet_gyo[8] = COPY����
    OutSheet_gyo[9] = �G���[MSG
            
    OutSheet.append(OutSheet_gyo)
    #  '�f�[�^���YDB�Ɂu01���x�����C�A�E�g�֘A���ݒ�v�������o��
    ���x�����C�A�E�g�֘A���ݒ�_.insert()
    
def TEXT_READ����(file_path):
    TmpSheet = []
    with open(file_path,errors="ignore") as f:
        for line in f:
            line.rstrip()
            TmpSheet.append(line)
    return TmpSheet
 
def �L���s(�s���):

    if len(�s���) > 6 and �s���[6] == " ":
        return True
    else:
        return False


def �X�L�[�}���׍s�o��(tmp_layout):
    global OutPut_folder
    global ���W���[����,DD��,�t�@�C���A��,�X�L�[�}��,�t�@�C����,�t�@�C�����,COPY����,�G���[MSG,���R�[�h��
    
    if tmp_layout == []:
        return 
    
    OutPut_Path = OutPut_folder + "\\" + �X�L�[�}��
    with open(OutPut_Path,"w",newline='\n') as f:
        for line in tmp_layout:
            f.write(line)
    
    return 

def WORK_AREA_���C�A�E�g���o�͏���(TmpSheet):

    # 'WORK�̈�܂Ō����Ώۍs���X�L�b�v
    �����s = 0
    hit_flg = False
    while �����s < len(TmpSheet):
        �Ώۍs������ = TmpSheet[�����s]
        string_7_66 = Mid(�Ώۍs������,6,66)
        # 'if �A_�L���s(�Ώۍs������) and InStr(�Ώۍs������, "WORKING-STORAGE" in string_7_66:    '�K��HIT���邱�Ƃ�z��
        # '01���x���̈ڑ����A�ڑ��悪�K������WORK�̈���̒�`�ł͂Ȃ��ꍇ������A�t�@�C��SECTION����̌����Ɋg�傷��
        if �L���s(�Ώۍs������) and "FILE" in string_7_66 and "SECTION" in string_7_66:   #  '�K��HIT���邱�Ƃ�z��
           hit_flg = True
        
        �����s = �����s + 1
        if hit_flg or �����s >= len(TmpSheet):
            break

    if hit_flg:
        
        chk_end = False
        �Ώۃt�@�C���L = False  #'�����l�͖�
        chk_1st = True
        tmp_layout = []
        
        while �����s < len(TmpSheet):
            �Ώۍs������ = TmpSheet[�����s]
            string_7_66 = Mid(�Ώۍs������,6,66)
            if �L���s(�Ώۍs������):
                # '�u01�v���x���ƃ��R�[�h���̃L�[���[�h�͓���s�ɂ��邱�Ƃ�z��
                # ' �ϐ��̃��x���́u01�v�ł��邱�Ƃ�z��
                if " 01 " in string_7_66 and \
                   " " + ���R�[�h�� + "." in string_7_66 or " " + ���R�[�h�� + " " in string_7_66:
                    �Ώۃt�@�C���L = True
                #    Set TSO = myFSO.CreateTextFile(Filename:=�X�L�[�}�t�H���_ + "\\" + �X�L�[�}��, Overwrite:=True)
                    chk_end = False
                    while True:
                        if �L���s(�Ώۍs������):
                            if (" FD " in string_7_66) or (" SD " in string_7_66) or (" EJECT " in string_7_66): # 'QA�Ǘ��\��0011�Ǘ��ԍ���Ή� (��)
                                # '�X�L�[�}���I��
                                chk_end = True
                            elif " PROCEDURE " in string_7_66 and \
                                " DIVISION " in string_7_66:
                                # '�X�L�[�}���I��
                                chk_end = True
                            elif " SECTION" in string_7_66:
                                # '�X�L�[�}���I��
                                chk_end = True
                            elif" 01 " in  Mid(�Ώۍs������, 6, 6) and not (chk_1st):
                                # '�X�L�[�}���I��(�ʂ̕ϐ����o��������o�͏I��)
                                chk_end = True
                            else:
                                tmp_layout.append(�Ώۍs������)
                                # Call �A_�X�L�[�}���׍s�o��
                           
                        
                        �����s = �����s + 1
                        chk_1st = False
                        if �����s >= len(TmpSheet) or chk_end:
                            break
                    
                        �Ώۍs������ = TmpSheet[�����s]
                        string_7_66 = Mid(�Ώۍs������,6,66)
                
            
            
            �����s = �����s + 1
    #    'Loop Until InStr(Mid(�Ώۍs������, 7, 6), " 01 " in string_7_66 and InStr(Mid(�Ώۍs������, 7, 6), " 01 " in string_7_66 and �A_�L���s(�Ώۍs������)
            if �����s >= len(TmpSheet) or chk_end:
                break
        �X�L�[�}���׍s�o��(tmp_layout)

    if �Ώۃt�@�C���L:
        pass
    else:
       �G���[MSG = "WK���C�A�E�g����s�\"
    
def WORK-STORAGE_���C�A�E�g���o�͏���(TmpSheet):

    # 'WORK�̈�܂Ō����Ώۍs���X�L�b�v
    �����s = 0
    hit_flg = False
    while �����s < len(TmpSheet):
        �Ώۍs������ = TmpSheet[�����s]
        string_7_66 = Mid(�Ώۍs������,6,66)
        # 'if �A_�L���s(�Ώۍs������) and InStr(�Ώۍs������, "WORKING-STORAGE" in string_7_66:    '�K��HIT���邱�Ƃ�z��
        # '01���x���̈ڑ����A�ڑ��悪�K������WORK�̈���̒�`�ł͂Ȃ��ꍇ������A�t�@�C��SECTION����̌����Ɋg�傷��
        if �L���s(�Ώۍs������) and "WORKING-STORAGE" in string_7_66 and "SECTION" in string_7_66:
           #  '�K��HIT���邱�Ƃ�z��
           hit_flg = True
        
        �����s = �����s + 1
        if hit_flg or �����s >= len(TmpSheet):
            break

    if hit_flg:
        
        chk_end = False
        �Ώۃt�@�C���L = False  #'�����l�͖�
        chk_1st = True
        tmp_layout = []
        
        while �����s < len(TmpSheet):
            �Ώۍs������ = TmpSheet[�����s]
            string_7_66 = Mid(�Ώۍs������,6,66)
            if �L���s(�Ώۍs������):
                # '�u01�v���x���ƃ��R�[�h���̃L�[���[�h�͓���s�ɂ��邱�Ƃ�z��
                # ' �ϐ��̃��x���́u01�v�ł��邱�Ƃ�z��
                if " 01 " in string_7_66 and \
                   " " + ���R�[�h�� + "." in string_7_66 or " " + ���R�[�h�� + " " in string_7_66:
                    �Ώۃt�@�C���L = True
                #    Set TSO = myFSO.CreateTextFile(Filename:=�X�L�[�}�t�H���_ + "\\" + �X�L�[�}��, Overwrite:=True)
                    chk_end = False
                    while True:
                        if �L���s(�Ώۍs������):
                            if (" FD " in string_7_66) or (" SD " in string_7_66) or (" EJECT " in string_7_66): # 'QA�Ǘ��\��0011�Ǘ��ԍ���Ή� (��)
                                # '�X�L�[�}���I��
                                chk_end = True
                            elif " PROCEDURE " in string_7_66 and \
                                " DIVISION " in string_7_66:
                                # '�X�L�[�}���I��
                                chk_end = True
                            elif " SECTION" in string_7_66:
                                # '�X�L�[�}���I��
                                chk_end = True
                            elif" 01 " in  Mid(�Ώۍs������, 6, 6) and not (chk_1st):
                                # '�X�L�[�}���I��(�ʂ̕ϐ����o��������o�͏I��)
                                chk_end = True
                            else:
                                tmp_layout.append(�Ώۍs������)
                                # Call �A_�X�L�[�}���׍s�o��
                           
                        
                        �����s = �����s + 1
                        chk_1st = False
                        if �����s >= len(TmpSheet) or chk_end:
                            break
                    
                        �Ώۍs������ = TmpSheet[�����s]
                        string_7_66 = Mid(�Ώۍs������,6,66)
                
            
            
            �����s = �����s + 1
    #    'Loop Until InStr(Mid(�Ώۍs������, 7, 6), " 01 " in string_7_66 and InStr(Mid(�Ώۍs������, 7, 6), " 01 " in string_7_66 and �A_�L���s(�Ώۍs������)
            if �����s >= len(TmpSheet) or chk_end:
                break
        �X�L�[�}���׍s�o��(tmp_layout)

    if �Ώۃt�@�C���L:
        pass
    else:
       �G���[MSG = "WK���C�A�E�g����s�\"

def �X�L�[�}�t�@�C���o��(TmpSheet):
  
    global ���W���[����,DD��,�t�@�C���A��,�X�L�[�}��,�t�@�C����,�t�@�C�����,COPY����,�G���[MSG,���R�[�h��

    �Ώۃt�@�C���L = False  #'�����l�͖�
 
    �����s = 0
    chk_end = False
    chk_1st = True
    
    while �����s < len(TmpSheet):
        �Ώۍs������ = TmpSheet[�����s]
        # '�R�����g�s��SKIP (�V�[�g2��ڂ͏����σ`�F�b�N��)
        if �L���s(�Ώۍs������) == False:
            �����s += 1
            continue
        
        string_7_66 = Mid(�Ώۍs������,6,66)
        
        if (" FD " in string_7_66 or " SD " in string_7_66) and \
            " " + �t�@�C���� in string_7_66:
                
            #   '01���x���L�[���[�h���ł�܂Ō���
            while �����s < len(TmpSheet):
                �����s = �����s + 1     #'FD��Ɠ���s�ɂ�01���x���L�[���[�h�͔������Ȃ��O��
                �Ώۍs������ = TmpSheet[�����s]
                string_7_66 = Mid(�Ώۍs������,6,66)
                #'if " 01 " in string_7_66:
                if " 01 " in Mid(�Ώۍs������, 6, 6) or \
                    " 1 " in Mid(�Ώۍs������, 6, 6): # '�댟�m�h�~�Ή���01���x���� 7-10 ��ڂ���n�܂�͂� (RECORD CONTAIN����Ɂu01�v�L�[���[�h������ꍇ������)
                    �Ώۃt�@�C���L = True
                # ' V1.1.1 �Ή� START *** 01 ���x���L�[���[�h���Ȃ������ꍇ�̏��� ***
                elif (" FD " in string_7_66) or (" SD " in string_7_66) or (" EJECT " in string_7_66):  #'QA�Ǘ��\��0011�Ǘ��ԍ���Ή� (��)
                    break
                elif " SECTION" in string_7_66:
                    break
                elif " WORKING-STORAGE " in string_7_66:
                    break
                elif " PROCEDURE " in string_7_66:
                    break
                elif " DIVISION " in string_7_66:
                    break
                # ' V1.1.1 �Ή� END

                if " 01 " in Mid(�Ώۍs������, 6, 6) and �L���s(�Ώۍs������):
                    break
                
            if �Ώۃt�@�C���L:
                # Set TSO = myFSO.CreateTextFile(Filename:=�X�L�[�}�t�H���_ + "\" + �X�L�[�}��, Overwrite:=True)
                
                chk_end = False
                tmp_layout = []
                while True:
                    if �L���s(�Ώۍs������):
                    
                        if (" FD " in string_7_66) or (" SD " in string_7_66) or (" EJECT " in string_7_66):  #'QA�Ǘ��\��0011�Ǘ��ԍ���Ή� (��)
                            # '�X�L�[�}���I��
                            chk_end = True
                        elif " SECTION" in string_7_66:
                            # '�X�L�[�}���I��
                            chk_end = True
                        elif " WORKING-STORAGE " in string_7_66:
                            # '�X�L�[�}���I��
                            chk_end = True
                        elif " PROCEDURE " in string_7_66:
                            # '�X�L�[�}���I��
                            chk_end = True
                        elif " DIVISION " in string_7_66:
                            # '�X�L�[�}���I��
                            chk_end = True
                        # 'elif " 01 " in string_7_66 and \ot (chk_1st):
                        elif " 01 " in Mid(�Ώۍs������, 6, 6) and not (chk_1st):
                            # '����01���x���Ή�
                            # TSO.Close
                            # Set TSO = Nothing
                            ���ʈꗗ�o��()
                            �X�L�[�}���׍s�o��(tmp_layout)
                            tmp_layout = []
                            tmp_layout.append(�Ώۍs������)
                            �t�@�C���A�� = �t�@�C���A�� + 1
                            
                            ���R�[�h�� = Mid(�Ώۍs������, 7, 65).replace("01", "").replace(" ", "").replace(".", "")
                            # '�X�L�[�}�� = ���W���[���� + "_" + �t�@�C���� + "_" + Format(�t�@�C���A��, "00") + ".scm"
                            �X�L�[�}�� = ���W���[���� + "_" + DD�� + "_" + str(�t�@�C���A��).zfill(2) + ".scm"
                            # Set TSO = myFSO.CreateTextFile(Filename:=�X�L�[�}�t�H���_ + "\" + �X�L�[�}��, Overwrite:=True)
                           
                        else:
                            # '�X�L�[�}���p��
                            tmp_layout.append(�Ώۍs������)
         
                    �����s = �����s + 1
                    chk_1st = False
                    if �����s >= len(TmpSheet) or chk_end:
                        break
                    
                    �Ώۍs������ = TmpSheet[�����s]
                    string_7_66 = Mid(�Ώۍs������,6,66)
                
                �X�L�[�}���׍s�o��(tmp_layout)
                tmp_layout = []
                
            else:
                chk_end = True
     
        �����s = �����s + 1
        
        if chk_end:
            break
    
    if �Ώۃt�@�C���L:
        pass
    else:
       �G���[MSG = "���C�A�E�g����s�\"

    
def main(db_path, Folder_COBOL_path, Output_folder_path):

    global ���W���[����,DD��,�t�@�C���A��,�X�L�[�}��,�t�@�C����,�t�@�C�����,COPY����,�G���[MSG,���R�[�h��
    global ���x�����C�A�E�g�֘A���ݒ�_
    global OutPut_folder 
    print("start preparation for analysis.")
    
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    sql,_ = make_delete_sql("01���x�����C�A�E�g�֘A���ݒ�",[],[])
    cursor.execute(sql)
    
    QRY_COBOL_���o�͏��_ = QRY_COBOL_���o�͏��(conn,cursor)
    ���x�����C�A�E�g�֘A���ݒ�_ = ���x�����C�A�E�g�֘A���ݒ�(conn,cursor)
    COBOL_Files = glob_files(Folder_COBOL_path)
    OutPut_folder = Output_folder_path
    OutSheet = []

    for file_path in COBOL_Files:
        cobol_file = get_filename(file_path)
        cobol_file,_,_,���W���[���� = GetFileInfo(cobol_file)
        myRS = QRY_COBOL_���o�͏��_.get(���W���[����) 
        
        if myRS == []:
            �t�@�C���� = ""
            DD�� = ""
            �t�@�C����� = ""
            ���R�[�h�� = ""
            �t�@�C���A�� = 0
            �X�L�[�}�� = ""
            COPY���� = ""
            �G���[MSG = "COBOL��͏��"
            ���ʈꗗ�o��()

            continue
        
        TmpSheet = TEXT_READ����(file_path)
        
        for data in myRS:
            
            �t�@�C���� = data["SELECT_ID"]
            DD�� = data["ASSIGN_ID"]
            �t�@�C����� = data["LINE_INFO"]
            ���R�[�h�� = data["RECORD_ID"]
            COPY���� = data["COPY"]
            �G���[MSG = ""
            �t�@�C���A�� = 1
            
            if COPY���� != "WORK�̈�":
                # '�ʏ�̃��C�A�E�g�����o�͂���iFD��܂���SD��j
                # '�X�L�[�}�� = ���W���[���� + "_" + �t�@�C���� + "_" + Format(�t�@�C���A��, "00") + ".scm"
                �X�L�[�}�� = ���W���[���� + "_" + DD�� + "_" + str(�t�@�C���A��).zfill(2) + ".scm"
                �X�L�[�}�t�@�C���o��(TmpSheet)
                ���ʈꗗ�o��()
            else:
            # '�y�蓮�z�ŉ�͂���WORK�̈�̃��C�A�E�g�������E�o�͂���
            #     '���R�[�h�� = DD��
                if ���R�[�h�� != "":
                    # '�X�L�[�}�� = ���W���[���� + "_" + �t�@�C���� + "_WK_" + ���R�[�h�� + ".scm"
                    �X�L�[�}�� = ���W���[���� + "_" + DD�� + "_WK_" + ���R�[�h�� + ".scm"
                    WORK_AREA_���C�A�E�g���o�͏���(TmpSheet)
                    ���ʈꗗ�o��()
             
        # OutSheet = [outsheet[1:] for outsheet in OutSheet]
        # write_excel_multi_sheet("01���x�����C�A�E�g�o�͌���.xlsx",OutSheet,"01���x�����C�A�E�g�o�͌���","",["COBOL���Y","�t�@�C����","DD��","�t�@�C�����","���R�[�h��","�t�@�C���A��","�X�L�[�}��","COPY����","�G���[���"])
    
if __name__ == "__main__":     
    main(sys.argv[1],sys.argv[2],sys.argv[3])