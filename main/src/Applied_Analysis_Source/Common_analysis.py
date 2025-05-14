#!/usr/bin/env python
# -*- coding: cp932 -*-

import glob
import os
import subprocess

import pandas as pd
import pyodbc

output_header = []


### take suffix from string if the string match
### ex) xxx.txt and take_suffix(xxx.txt,".txt")  ->   xxx
def take_suffix(string,suffix):
    l = len(suffix)
    string = str(string)
    if len(string) < l:
        return string
    
    if string[-l:] == suffix:
        string = string[:-l]
    return string

### take prefix from string if the string match
### ex) xxx.txt and take_prefix(xxx.txt,"xxx")  ->   .txt
def take_prefix(string,prefix):
    l = len(prefix)
    string = str(string)
    if len(string) < l:
        return string
    
    if string[:l] == prefix:
        string = string[l:]
    return string



### in this program, source code extension is assumed .txt or .cbl or .ET and get rid of those
def take_extensions(string):
    string = take_suffix(string,".txt")
    string = take_suffix(string,".TXT")
    string = take_suffix(string,".cbl")
    string = take_suffix(string,".cob")
    string = take_suffix(string,".ET")
    string = take_suffix(string,".jcl")
    return string

### take prefix and suffix ftom string if the string match
### ex)  "aaa.txt" and take_prefix_and_suffix("aaa.txt", "\"") -> aaa.txt
### in python  if you want to set single " , you need to set \" 
def take_prefix_and_suffix(string,presuffix):
    l = len(presuffix)
    string = str(string)
    if len(string) < l:
        return string
    if string[:l] == presuffix:
        string = string[l:]
        
    if string[-l:] == presuffix:
        string = string[:-l]
    return string


def get_filename(file_name):
    file_name = os.path.split(file_name)[-1]
    # file_name = take_extensions(file_name)
    # name = file_name.split("%")[-1]
    return file_name #, name

def get_filenames(file_name):
    file_name = os.path.split(file_name)[-1]
    file_name = take_extensions(file_name)
    name = file_name.split("%")[-1]
    return file_name, name

def GetFileInfo(FileName):
    """ return FileName, library, gouki, and module name

    Args:
        FileName (_string_): _FileName is consider the case like U.ADL.SOU#B%B%ACS3 _

    Returns:
        _type_: _FileName, library, gouki, and module name_
    """
    BaseName = take_extensions(FileName)
    if BaseName.find("%") == -1:
        return "A", "B", "C", BaseName
    tmp_list = BaseName.split("%")
    
    assert len(tmp_list) == 3, "Filename format is invalid : " + FileName
      
    library,gouki,module = tmp_list
    return FileName,library,"%"+gouki,module

### get the files from file_path directory, so path should be directory
def glob_files(file_path,recursive=True,type="file"):
    """ get the files from file_path directory, so path should be directory

    Args:
        file_path (_string_): _the path to the file saved directory_

    Returns:
        _list of file path in the directory_: _return the list of path in the directory, child directory is also valid_
    """
    if file_path == "":
        return []
    
    assert os.path.exists(file_path), "file path is invalid : " + file_path  
    
    
    files = glob.glob(file_path+"/**",recursive=recursive)
    if type == "file":
        return [p for p in files if os.path.isfile(p)]
    
    elif type == "folder":
        return [p for p in files if os.path.isdir(p)]
    

def make_output_list_val_length(output_list,output_header):
    m = len(output_header)
    
    for i in output_list:
        m = max(m,len(i)-1)
        
    output_list_after = []
    for i in output_list:
        dif = m - (len(i)-1)
        output_list_after.append(i[1:]+[""]*dif)

    output_header = output_header + [""]*(m-len(output_header))
    
    return output_list_after,output_header

def write_excel_multi_sheet(filename,df,sheet_name,path,output_header=output_header):
    
    Sheet_lim = 10**6
    writer = pd.ExcelWriter(path+"/"+filename,engine='xlsxwriter')
    writer.book.use_zip64()
    sheet_name_list = []
    
    M = len(df)
    df_list = []
    for i in range(M//Sheet_lim+1):
        df_list.append(df[i*Sheet_lim:min(M,(i+1)*Sheet_lim)])
    for i in range(len(df_list)):
        if i == 0:
            sheet_name_list.append(sheet_name)
        else:
            sheet_name_list.append(sheet_name +"_" + str(i+1))
            
    for list,sheet_name in zip(df_list,sheet_name_list):
        df = pd.DataFrame(list,columns=output_header)
        df.to_excel(writer, sheet_name=sheet_name,index=False)
        
    #writer._save()
    writer.close()
    
def write_excel_multi_sheet2(filename,dfs,sheet_names,path,output_headers=output_header):
    
    Sheet_lim = 10**6
    writer = pd.ExcelWriter(path+"/"+filename,engine='xlsxwriter')
    writer.book.use_zip64()
    sheet_name_list = ["サマリ"]
    
    df_list = [[]]
    output_header_list = [["シート名","件数"]]
    for df,header,sheet_name in zip(dfs,output_headers,sheet_names):
        M = len(df)
        df_list[0].append([sheet_name,M])
        for i in range(M//Sheet_lim+1):
            df_list.append(df[i*Sheet_lim:min(M,(i+1)*Sheet_lim)])
            output_header_list.append(header)
            if i == 0:
                sheet_name_list.append(sheet_name)
            else:
                sheet_name_list.append(sheet_name +"_" + str(i+1))
            
    for list,sheet_name,header in zip(df_list,sheet_name_list,output_header_list):
        df = pd.DataFrame(list,columns=header)
        df.to_excel(writer, sheet_name=sheet_name,index=False)
        
    #writer._save()
    writer.close()
      
      
def write_excel_multi_sheet3(filename,df_list,sheet_name_list,path,output_headers):
    writer = pd.ExcelWriter(path+"/"+filename,engine='xlsxwriter')
    writer.book.use_zip64()
    for list,sheet_name,output_header in zip(df_list,sheet_name_list,output_headers):
        df = pd.DataFrame(list,columns=output_header)
        df.to_excel(writer, sheet_name=sheet_name,index=False)
        
    #writer._save()
    writer.close()
    

def write_excel_multi_sheet4(filename,df_list,sheet_name_list,path,output_header=output_header):
    Sheet_lim = 10**6
    
    writer = pd.ExcelWriter(path+"/"+filename,engine='xlsxwriter')
    writer.book.use_zip64()
    df_list_all = []
    sheet_name_list_all = []
    
    for data_list,sheet_name in zip(df_list,sheet_name_list):
        M = len(data_list)
        data_list = list(data_list)
        for i in range(M//Sheet_lim+1):
            df_list_all.append(data_list[i*Sheet_lim:min(M,(i+1)*Sheet_lim)])
            if i == 0:
                sheet_name_list_all.append(sheet_name)
            else:
                sheet_name_list_all.append(sheet_name +"_" + str(i+1))
     
    for data_list,sheet_name in zip(df_list_all,sheet_name_list_all):
        df = pd.DataFrame(data_list,columns=output_header)
        df.to_excel(writer, sheet_name=sheet_name,index=False)
        
    #writer._save()
    writer.close()
    
def write_excel_multi_sheet5(filename,dfs,sheet_names,path,output_headers):
    
    Sheet_lim = 10**6
    writer = pd.ExcelWriter(path+"/"+filename,engine='xlsxwriter')
    writer.book.use_zip64()
    sheet_name_list = []
    
    df_list = []
    output_header_list = []
    for df,header,sheet_name in zip(dfs,output_headers,sheet_names):
        M = len(df)
        for i in range(M//Sheet_lim+1):
            df_list.append(df[i*Sheet_lim:min(M,(i+1)*Sheet_lim)])
            output_header_list.append(header)
            if i == 0:
                sheet_name_list.append(sheet_name)
            else:
                sheet_name_list.append(sheet_name +"_" + str(i+1))
            
    for list,sheet_name,header in zip(df_list,sheet_name_list,output_header_list):
        df = pd.DataFrame(list,columns=header)
        df.to_excel(writer, sheet_name=sheet_name,index=False)
        
    #writer._save()
    writer.close()
    
def connect_accdb(db_path):

    assert os.path.isfile(db_path), "file path is invalid : " + db_path
    
    conn_str = (
                r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                r'DBQ=' + db_path
                )

    conn = pyodbc.connect(conn_str,autocommit=True)
    return conn


def compact_accdb(db_path = None):
    """
    accdbの最適化を実行する SQLの処理を大量に行う際に最適化を行わないとファイル容量の制限を超えてしまう
    
    """
    
    assert os.path.isfile(db_path), "file path is invalid : " + db_path
    
    command = db_path + " /compact"
    subprocess.run(command,shell=True)
    


def ArrayEmptyDelete(split_string_list):
    """ArrayEmptyDeleteと同じような関数, listから空文字を除く

    Args:
        split_string_list (list): list of string
    """
    
    split_string_list_empty_delete = []
    for string in split_string_list:
        if string == "" or string == "\n" or string == " ":
            continue
        split_string_list_empty_delete.append(string)
    return split_string_list_empty_delete



def make_insert_sql(DBNAME,value_iist,key_list):
    
    keys = "[" + "],[".join(key_list) + "]"
    values = []
    for v in value_iist:
        if v == None:
            v = ""
        values.append(str(v))
        
    values = tuple(values)
    
    value = "?,"*(len(values)-1)+"?"
    sql = "INSERT INTO "+DBNAME+"(" + keys + ")" + "VALUES (" + value + ")"
    return sql,values


def make_update_sql(DBNAME,set_value_iist,set_key_list,where_value_list,where_key_list):
    
    set_keys = "[" + "]=?,[".join(set_key_list) + "]=?"
    where_keys = "[" + "]=? AND [".join(where_key_list) + "]=?"
    values = []
    for v in set_value_iist:
        if v == None:
            v = ""
        values.append(str(v))
    for v in where_value_list:
        if v == None:
            v = ""
        values.append(str(v))
        
    values = tuple(values)
 
    sql = "UPDATE "+DBNAME+" SET " + set_keys + " WHERE " + where_keys
    return sql,values


def make_delete_sql(DBNAME,where_value_list,where_key_list):
    
    where_keys = "[" + "]=? AND [".join(where_key_list) + "]=?"
    values = []

    for v in where_value_list:
        if v == None:
            v = ""
        values.append(str(v))
        
    values = tuple(values)

    ### where_key_list が空なら where句指定なし = DB全データ削除のSQLを返す
    if len(where_key_list) == 0:    
        sql = "DELETE FROM "+DBNAME
        
    ### where句にマッチしたデータを削除
    else:
        sql = "DELETE FROM "+DBNAME+" WHERE " + where_keys
    
    
    return sql,values



def isBMCP_PGM(pgm_name):
    """_check if pgm_name is BMCP or not_
        if "SUB" in pgm_name and pgm_name endswith "M", then BMCP and return True
        else return False

    Args:
        pgm_name (_string_): _string of pgm_name you want to check _

    Returns:
        _type_: _description_
    """
    pgm_name = str(pgm_name)
    
    if "SUB" in pgm_name and pgm_name.endswith("M"):
        return True

    return False


def Mid(string,start_index,length):
    """ same type of function of Mid of VBA language

    Args:
        string (_str_): string you want to get the middle of it, be careful, string length is enough 
        start_index (_int_): start index you want to take, count from 0 
        length (_int_): length of string you want to take

    Returns:
        string of midlle: if the string length is not enough, return the string until end
    """
    
    
    if len(string) <= start_index:
        return ""
    return string[start_index:min(start_index+length,len(string))]


def LTrim(string):
    """ same type of function of LTrim of VBA language

    Args:
        string (_string_): target string, which you want to trim space from head

    Returns:
        string : string after trim the space from head
    """
    
    for i in range(len(string)):
        if string[i] != " ":
            return string[i:]
    return ""

def RTrim(string):
    """ same type of function of RTrim of VBA language

    Args:
        string (_string_): target string, which you want to trim space from end
    Returns:
        string : string after trim the space from end
    """
    
    for i in range(len(string)-1,-1,-1):
        if string[i] != " ":
            return string[:i+1]
    return ""

def Trim(string):
    """ same type of function of Trim of VBA language

    Args:
        string (_string_): target string, which you want to trim space from head and end
    Returns:
        string : string after trim the space from head and end
    """
    
    
    return LTrim(RTrim(string))


def  DB文字(P_STR):
    
    DB文字_rtn = P_STR.replace("'", "\"").replace(",", " ")
    # 'TODO SQL構文不正エラー対応
    DB文字_rtn = DB文字_rtn.replace(chr(0), " ")
    
    return DB文字_rtn


def IsNumeric(parm_str):
    parm_str = str(parm_str)
    
    nums = [str(i) for i in range(10)]
    for s in parm_str:
        if s in nums or s in "+-":
            continue
        return False
    
    return True


def take_all_extensions(lis):
    if lis == []:
        return lis
    
    m = max(4,len(lis[0]))
    for i in range(len(lis)):
        for j in range(m):
            if type(lis[i][j]) == str:
                lis[i][j] = take_extensions(lis[i][j])
    return lis

def join_file_name_xlsx(date,file_name):
    return file_name + "_" + date + ".xlsx"



### check the string is comment line or not.
### return -1 if comment line
###        1 if not
def comment_line_check(string,language_type):
    if len(string) == 0:
        return -1
    
    if string[0] == "*":
        return -1
       
    assert language_type in ["COBOL","FORTRAN","JCL","PROC","COMMON","ASM"], "at Function comment_line_check, language_type is invalid"
    
    if language_type == "COMMON":
        return 1
    
    if language_type == "COBOL":
        if len(string) < 7:
            return -1
        if string[6] == "*":
            return -1
        return 1
    
    if language_type == "FORTRAN":
        if string[0] == "C" or string[0] == "c":
            return -1
        if len(string) >= 16 and string[15] == "*":
            return -1
        return 1
    
    if language_type == "JCL" or language_type == "PROC":
        if len(string) < 3:
            return -1
        if string[2] == "*" or string[1] == "*":
            return -1
        return 1
    
    if language_type == "ASM":
        return 1


### for the JCL and PROC source code
### if string is "//               "(only double slash and space) compile is end at this string and after the string is not consider
def end_line_check(string, language_type):
    assert language_type in ["COBOL","FORTRAN","JCL","PROC","COMMON"], "at Function end_line_check, language_type is invalid"
    
    if language_type == "JCL" or language_type == "PROC":
        if len(string) >= 72 and string[:72] == "//"+" "*70:
            return -1
        
    if language_type == "JCL" or language_type == "PROC":
        if string.startswith("//") and string[2] != "*" and " JOB " in string:
            return 2
        
    return 1



### grep the filename and line just find the matching keywords 
### keywords = ["CALL"] then " aaa CALL 11111", "aaaCALLxxxx 1111" match
### so if you want to get the single word "CALL"  keywords = [" CALL "]
### some source code have multi line sentense and in that case, this function probably not doing well.
def grep_keywords(files=[], keywords=[], returnpath=False):
    
    grep_list = []
    
    for file in files:
        file_name = os.path.split(file)[-1]
        with open(file,errors="ignore") as f:

            for line in f:
                for keyword in keywords:
                    if keyword in line:
                        if returnpath == True:
                            grep_list.append([file,line])
                        else:
                            grep_list.append([file_name,line])
    return grep_list


### grep only filename just find the matching keywords 
### for some kind of relation, it is difficult to get accurate information from normal pattern
### keywords = ["CALL"] then " aaa CALL 11111", "aaaCALLxxxx 1111" match
### so if you want to get the single word "CALL"  keywords = [" CALL "]
### some source code have multi line sentense and in that case, this function probably not doing well.
def grep_files(files, keywords, returnpath=False):
    
    grep_file = [[] for i in range(len(keywords))]
    
    for file in files:
        file_name = os.path.split(file)[-1]
        with open(file,errors="ignore") as f:
            for line in f:
                for i,keyword in enumerate(keywords):
                    if keyword in line:
                        if returnpath == True:
                            grep_file[i].append(file)
                        else:
                            grep_file[i].append(file_name)
                
    return grep_file


### grep the filename and line just find the matching keywords 
### list is separated by keywords, keywords = ["CALL","ENTRY"] then list:grep_file[0] has "CALL" matched filename and line 
### keywords = ["CALL"] then " aaa CALL 11111", "aaaCALLxxxx 1111" match
### so if you want to get the single word "CALL"  keywords = [" CALL "]
### some source code have multi line sentense and in that case, this function probably not doing well.
def grep_file_and_string(files=[], keywords=[], returnpath=False, language_type="COMMON"):
    
    grep_file = [[] for i in range(len(keywords))]
    
    for file in files:
        file_name = os.path.split(file)[-1]
        end_flag = False
        with open(file,errors="ignore") as f:
            for line in f:
                if comment_line_check(string=line, language_type=language_type) == -1:
                    continue
                # if end_line_check(string=line,language_type=language_type)== -1:
                #     break
                if end_flag:
                    if end_line_check(string=line,language_type=language_type) == 2:
                        end_flag = False
                        
                if end_line_check(string=line,language_type=language_type) == -1:
                    end_flag = True
                
                if end_flag:
                    continue
                
                for i,keyword in enumerate(keywords):
                    if keyword in line:
                        if returnpath == True:
                            grep_file[i].append([file,line])
                        else:
                            grep_file[i].append([file_name,line])
 
    return grep_file

def generate_pli_dict_from_sheet(sheet, key_index, value_index):
    return_dict = {}
    for item in sheet:
        return_dict[item[key_index]] = item[value_index]
    return return_dict
