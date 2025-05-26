#!/usr/bin/env python
# -*- coding: shift-jis -*-

import pandas as pd
import re
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

has_relation_proc_set = set()

internal_proc_dic = {}
jcl_to_internal_proc_dic = {}
jobproc_dic = {}
catapro_dic = {}
catapro_unit_dic = {}
jcl_dic = {}
jcl_invalid_dic = {}
easy_dic = {}
asset_dic = {}
module_dic = {}

proc_parm_dic = {}
proc_variable_dic = {}

valid_member_dic = {}
invalid_member_dic = {}

need_search_and_check_list = set()


check_list = set()


### relation of focus ex , candidate pgm-name list
focus_name_list = ["Q#FOCUS","U#FOCUS","R#FOCUS"]
    
## priority list
priority_list = ["", "SYS1.PROCLIB", "SYS1.IBM.PROCLIB", "SYS1.IOE.SIOEPROC", "SYS1.OSPROC", "SYS1.USERPROC", "BEST.PROCLIB", "$IMS.PROCLIB", "COM_PROCLIB", "SI95_SYS1_PROCLIB", "SI95_SYS1_USER_PROCLIB", "SI77_ISPF_BANK_PROCLIB", "SI77_SYS1_PROCLIB", "SI77_SYS1_USER_PROCLIB", "SI77_SYS2_PROCLIB", "NKN.PROCLIB", "NKNB.PROCLIB", "ANP.XDM.JCL", "USRA.PROCLIB", "SYS1.OSPROC", "カタプロ", "VOS.PLIB", "VOS.DSPLIB", "SYSOPN.PROCLIB","SYSJOB.PROCLIB","SYSSTC.PROCLIB","SYS2.PROCLIB","PP1.PROCLIB", "AIM1.PROCLIB", "JS.SYSJOBS", "JS.JCLIB", "JS.FXIPF.PROCLIB", "JS.TESTJCL", "D", "HULFT.FTPM.JCL", "J", "JS.AIM.SYMFOSRC", "JS.SP.JCL", "OWFT.FTPM.JCL", "P", "TSO.TEST.PROCLIB", "PJI2.ISPPO.REPLI.ATLS.PROCLIB", "PJI2.ISPPO.REPLI.NPLN.PROCLIB", "PJI2.ISPPO.REPLI.TOMS.PROCLIB", "SSL.PROCLIB", "SYS1.KKR.PROCLIB", "TSSD12.JCL", "TSSD12.JCL2", "TSSD21.SNT.JCL", "TSSD21.SUBMIT.JCL", "TSSD22.HJN.JCL", "TSSDENT.SUBMIT.JCL", "TSSP.HJN.JCL", "TSSP.JCL"] 
    
     
### valid string of 5,6 of pgm screen 
pgm_screen_valid_list = ["EW","FC","FI","FN","FW","FY","FZ"]

### cobol variable list no need to search
cobol_no_need_variable_list = ["DLKENT","PRG"]

### cobol group list which need to consider as the different file even though, file name is same
cobol_group_list = ["コイルOC","スラブOC","形鋼CC","形鋼OC","材試OC_材試CC","熱仕OC","熱延CC","計画CC"]


def no_matched_member(member_name):
    return str(member_name)+"_未受領PROC"

def no_mached_variable(variable_name):
    return str(variable_name)+"_変数元不明"

def invalid_variable(variable_name):
    return str(variable_name)+"_移行対象外"

def judge_screen(cand):
    
    if "-" in cand or "=" in cand or " " in cand:
        return -1
    if len(cand) != 8:
        return -1
    if cand[4:6] not in pgm_screen_valid_list:
        return -1
    
    return cand


### in the case of cobol folder, probably have the sub folder like ???OC, ???OC ... , and in that sub folder,
### even if, filename is same, treat as different file by adding info to subinfo like ":???OC","?????:???OC"
### so, this function check the file full path and if cobol_group in cobol_group_list found in the path, return that cobol_group name string or empty string
def get_cobol_group_info(filepath):
    sub = ""
    if "CC" or "OC" in filepath:
        for cobol_group in cobol_group_list:
            if cobol_group in filepath:
                sub = ":"+cobol_group
                break
            
    return sub


def check_priority_number(library_name):
    """return priority of library number

    Args:
        library_name [string]: Library name like  "SYS1.PROCLIB", "SYS1.IBM.PROCLIB", "SYS1.IOE.SIOEPROC", "SYS1.OSPROC", "SYS1.USERPROC", "BEST.PROCLIB", "$IMS.PROCLIB", "COM_PROCLIB", "SI95_SYS1_PROCLIB", "SI95_SYS1_USER_PROCLIB", "SI77_ISPF_BANK_PROCLIB", "SI77_SYS1_PROCLIB", "SI77_SYS1_USER_PROCLIB", "SI77_SYS2_PROCLIB", "NKN.PROCLIB", "NKNB.PROCLIB", "ANP.XDM.JCL", "USRA.PROCLIB", "SYS1.OSPROC", "カタプロ", "VOS.PLIB", "VOS.DSPLIB", "SYSOPN.PROCLIB","SYSJOB.PROCLIB","SYSSTC.PROCLIB","SYS2.PROCLIB","PP1.PROCLIB", "AIM1.PROCLIB", "JS.SYSJOBS", "JS.JCLIB", "JS.FXIPF.PROCLIB", "JS.TESTJCL", "D", "HULFT.FTPM.JCL", "J", "JS.AIM.SYMFOSRC", "JS.SP.JCL", "OWFT.FTPM.JCL", "P", "TSO.TEST.PROCLIB", "PJI2.ISPPO.REPLI.ATLS.PROCLIB", "PJI2.ISPPO.REPLI.NPLN.PROCLIB", "PJI2.ISPPO.REPLI.TOMS.PROCLIB", "SSL.PROCLIB", "SYS1.KKR.PROCLIB", "TSSD12.JCL", "TSSD12.JCL2", "TSSD21.SNT.JCL", "TSSD21.SUBMIT.JCL", "TSSD22.HJN.JCL", "TSSDENT.SUBMIT.JCL", "TSSP.HJN.JCL", "TSSP.JCL"

    Returns:
        int : return priority number 0 - 5 (o is high priority)
    """
    
   
    ### return 0 index number
    for i in range(1,len(priority_list)):
        if library_name == priority_list[i]:
            return i
    return 0


def check_string_only_number(string):
    """check string is only characters of  numbers and (, ), -, 

    Args:
        string [string]: any type is ok

    Returns:
        int : return  1 -> only number, return -1 -> has other character 
    """
    
    nums = [str(i) for i in range(10)]
    string = str(string)
    for s in string:
        if s in nums or s in " (-),#" :
            continue
        return -1
    return 1


def check_string_only_number_and_return_string(string):
    """check string only number and if not return string

    Args:
        string ([string]): [string you want to check]

    Returns:
        [str or int]: return string if it is not number
                      return -1 if is only number
    """
    if check_string_only_number(string) == 1:
        return -1
    # return string.replace("\\","$")
    return string


def check_cobol_call_valid(string):
    """get name from COBOL source code, "CALL" order
       if name has any symbol, that name is probably invalid

    Args:
        string [string]: any type is ok

    Returns:
        int : return 1 -> valid name
                    -1 -> invalid
    """
    nums = [str(i) for i in range(10)]
    alpha = [chr(ord("a")+i) for i in range(26)]
    ALPHA = [chr(ord("A")+i) for i in range(26)]
    string = str(string)
    for s in string:
        if s in nums or s in alpha or s in ALPHA or s in "-":
            continue
        return -1
    return 1
    
    
### Warning and no matched member message
def many_jobproc_order_warning(sisan_id,jobproc_order_library_list):
    message = "[Warning] "+str(sisan_id) + " found more than 1 jobproc order and the candidate is"
    print(message)
    for jobproc in jobproc_order_library_list:
        print(jobproc)


### asset_dic is dictionary of [asset name]:[classification]
### like "R.LB.PRC%A%U#LIKED":"JCL"
### so, if in asset_dic (have information in Member List) return classification
###     else (don't received the asset or get rid of)return -1 
def return_asset_classification(asset):
    """ return asset classification or -1

    Args:
        asset [string]: asset is like "R.LB.PRC%A%U#LIKED"

    Returns:
        string or int: if in asset_dic (have information in Member List) return classification
                        else (don't received the asset or get rid of)return -1 
    """
    return asset_dic.get(asset,-1)


### module_dic is dictionary of [module name]:[classification1,classification2] (list)
### like "U#LIKED":["JCL","カタプロ"]
### so, if in module_dic (have information in Member List) return classification list
###     else (don't received the module or get rid of)return [] (empty list)
def return_module_classification(module):
    """ return list of module classification or []

    Args:
        module [string]: asset is like "#LIKED"

    Returns:
        set or list: if in module_dic (have information in Member List) return classification list
                        else (don't received the asset or get rid of)return [] (empty list)
    """
    return module_dic.get(module,[])


### not used for now
def return_valid_classification(module):
    if module in valid_member_dic:
        return valid_member_dic[module],1
    if module in valid_member_dic:
        return invalid_member_dic[module],-1
    return -1,-1
       
       
        
def clean_proc_name(proc_name):
    if "%" in proc_name:
        proc_name = proc_name.split("%")[-1]
            
    proc_name = take_suffix(proc_name,"_未受領PROC")
    proc_name = take_suffix(proc_name,"_PROC")
    proc_name = take_suffix(proc_name,"_未受領")
    proc_name = proc_name.replace("\\","$")
    return proc_name




def grep_and_make_list(files, keywords, type, returnpath=False, language_type="COMMON"):
    """grep keywords from all file in files list and also get the information by "take_data_from_string" function of type

    Args:
        files ([list]): [list of full path source code files]
        keywords ([list of string]): [list of string you want to grep] like ["CALL", "ENTRY"]
        type ([string]): [string of type you want to do "take_data_from_string"] like "CALL-VARIABLE"
        returnpath (bool, optional): [if you want to return full path of source code, switch to True, in case you want to additional search in greped file]. Defaults to False.
        language_type (str, optional): [you want to get rid of information written in comment line, write the source code type like "COBOL"]. Defaults to "COMMON".

    Returns:
        [set of (file_name, greped information)]: []
    """
    grep_list = set()
                
    for file in files:
        file_name,_ = get_filenames(file)
        with open(file,errors="ignore") as f:

            for line in f:
                if comment_line_check(string=line,language_type=language_type) == -1:
                    continue
                
                for keyword in keywords:
                    if keyword not in line:
                        continue
                    member = take_data_from_string(string=line,type=type,language_type=language_type)

                    if member == -1:
                        continue
                    if returnpath == True:
                        grep_list.add((file,member))
                    else:
                        grep_list.add((file_name,member))

    return grep_list


def grep_and_make_list_cobol(files=[],keywords=[],type="",returnpath=False, language_type="COBOL"):
    
    grep_list = set()
                
    for file in files:
        file_name,_ = get_filenames(file)
        with open(file,errors="ignore") as f:
            
            data= []
            for line in f:
                if comment_line_check(string=line,language_type=language_type) == -1:
                    continue
                data.append(line[6:72])

            data1 = re.split(';|\\.\s|\*', ' '.join(data))
            
            for line in data1:
                for keyword in keywords:
                    if keyword not in line:
                        continue
                    member = take_data_from_string(string=line,type=type)

                    if member == -1:
                        continue
                    if returnpath == True:
                        grep_list.add((file,member))
                    else:
                        grep_list.add((file_name,member))

    return grep_list





### functions, based on JCL analysis result excel or db #######################


def take_data_from_jcl_analysis_result(string,type):
    string = str(string)
    
    
    ### consider the text like ) DD DSN = R.LB.PRC   DISP = SHR 
    ### get the string DSN = [xxx] in this case R.LB.PRC
    if type == "JOBPROC":
        if "DSN" not in string:
            return -1
        
        dsn_index = string.find("DSN ")
        string_after = string[dsn_index:]
        slist = string_after.split(" ")
        for s in slist[1:]:
            if s == "" or s == "=" or s == "\'" or s == "\"":
                continue
            s = take_prefix_and_suffix(s,"\"")
            return check_string_only_number_and_return_string(s)
                
        return -1
    
    ### consider the text like )   EX  RFB1       00006700 
    ### get the string EX [xxx] in this case RFB1
    if type == "FOCUS-EX":
        if "EX" not in string:
            return -1
        
        ex_index = string.find("EX ")
        string_after = string[ex_index:]
        slist = string_after.split(" ")
        for s in slist[1:]:
            if s == "" or s == "=" or s == "\'" or s == "\"":
                continue
            s = take_prefix_and_suffix(s,"\"")
            return check_string_only_number_and_return_string(s)
                
        return -1
    
    ### consider the text like )      TA PGM=UCARD                   00002200
    ### get the string PGM=[xxx] in this case UCARD
    if type == "UTACH":
        if "PGM=" not in string:
            return -1
        pgm_index = string.find("PGM=")
        string_after = string[pgm_index:]
        slist = string_after.split(" ")
        s = slist[0][slist[0].find("=")+1:] ### slist[0] = PGM=UCARD
        s = take_prefix_and_suffix(s,"\"")
        return check_string_only_number_and_return_string(s)

    
    
    ### consider the text like )        TA PGM=RVSUB61M PARM=04=RV61                  00004000
    ### if PGM name contain SUB and endwith M
    ### get the string PARM=number=[xxx] in this case RV61
    if type == "UTACH-BMCP":
        if "PGM=" not in string or "PARM" not in string:
            return -1
        
        pgm_index = string.find("PGM=")
        string_after = string[pgm_index:]
        slist = string_after.split(" ")

        cand_string = slist[0][slist[0].find("=")+1:]
        if "SUB" not in cand_string or  cand_string[-1] != "M":
            return -1
        
        
        parm_index = string.find("PARM")
        
        string_after = string[parm_index:]
        slist = string_after.split("=")

        for cand in slist[1:]:
            if check_string_only_number(cand) == 1:
                continue
            
            s = cand.split(" ")[0]
            s = take_prefix_and_suffix(s,"\"")
            return check_string_only_number_and_return_string(s)

       
        return -1
    
    ### consider the text like )        TTA PGM=UFTPSUPD PARM=08=00 QGT01                          
    ### if PGM name is UFTPSUPD
    ### get the string PARM=number=number [xxx] in this case QGT01
    if type == "OWFT-JCL-UTACH":
        if "UFTPSUPD" not in string or "PARM" not in string:
            return -1
        parm_index = string.find("PARM")

        string_after = string[parm_index:]
        slist = string_after.split("=")
        for cand in slist[1:]:
            if check_string_only_number(cand) == 1:
                continue
            
            slist = cand.split(" ")
        
            if len(slist) < 2:
                return -1
            s = take_prefix_and_suffix(slist[1],"\"")
            return check_string_only_number_and_return_string(s)
        return -1
    
    ### consider the text like )   1 DLA7 JYO004JYO004 A 23 J 8                              
    ### if PGM name is DXLIFTIN
    ### get the string number [xxxx] in this case DLA7 and should be 4 letters
    if type == "OWFT-DXLIFTIN":
        
        slist = string.split(" ")

        for s in slist[1:]:
            if s == "" or s == " ":
                continue
            if len(s) != 4:
                return -1
            return "DFT"+s
        
        return -1
    
    
    ### consider the text like )  BC11OBJ SD01OBJ CJEAOBJ"                              
    ### if PGM name is UXCMDCLR
    ### get the string list, in this case ["BC11OBJ", "SD01OBJ", "CJEAOBJ"]
    if type == "OBJ-UXCMDCLR":
        members = []
        slist = re.split("[\" ]",string)
        for s in slist:
            if s == "" or s == "\'" or s == "\"" or s == "(" or s == ")":
                continue
            if check_string_only_number(s) == 1:
                continue
            members.append(s)
        return members
    
    ### consider the text like )  00 RLA40VB"
    ### if PGM name is UFTPSUPD
    ### get the string number[xxx] in this case RLA40VB
    if type == "OWFT-JCL":
        slist = re.split("[\" ]",string)
        for s in slist[1:]:
            if s == "" or s == "\'" or s == "\"" or s == "(" or s == ")":
                continue
            
            if check_string_only_number(s) == 1:
                continue
            return s
        return -1
    
    
    ### consider the text like )  &FID"
    ### if PGM name is UFTPQUES or UFTPENDC
    ### get the string [xxx] in this case &FID
    if type == "OWFT":
        if string == "":
            return -1
        slist = string.split(" ")
        member = take_prefix_and_suffix(slist[0],"\"")
        return check_string_only_number_and_return_string(member)



def take_data_from_key_val(key,value,type):
    
    key = str(key)
    value = str(value)
    
    ### in jcl step information PARM_VAR_LIST and PARM_VALUE_LIST
    ### if the two string like
    ### PARM REGION
    ### R1H2 1024K
    ### then matched index of PARM value is returned, in this case R1H2 
    if type == "BMCP":
        key_list = key.split(" ")
        value_list = re.split("[\" ]",value)
        if "PARM" not in key_list:
            return -1
        
        for i,v in enumerate(key_list):
            if v == "" or v == " ":
                continue
            if v == "PARM":
                ind = i
                break

        count = 0
        for i,v in enumerate(value_list):
            if v == "" or v == " ":
                continue
            if ind == count:
                v = take_prefix_and_suffix(v,"\"")
                return v
            count += 1
        return -1
    
    last = []
    bracket = 0
    if type == "PROC-PGM-VARIABLE":
        key_list = re.split("[\" ]",key)
        value_list = re.split("[\" ]",value)
        keys = []
        values = []
        for k in key_list:
            if k == "" or k == " ":
                continue
            keys.append(k)
            
        for v in value_list:
            if v == "" or v == " ":
                continue
            if "(" in v or ")" in v:
                bracket += v.count("(") - v.count(")")
            if bracket:
                last.append(v)
            else:
                last.append(v)
                values.append(" ".join(last))
                last = []
            
        return keys,values
    
    # if type == "PROC-PGM-VARIABLE":
    #     key_list = re.split("[\" ]",key)
    #     value_list = re.split("[\" ]",value)
    #     keys = []
    #     values = []
    #     for k in key_list:
    #         if k == "" or k == " ":
    #             continue
    #         keys.append(k)
            
    #     for v in value_list:
    #         if v == "" or v == " ":
    #             continue
    #         values.append(v)
            
    #     return keys,values
    

### Check the internal proc and make dictionary
def update_internal_proc_list(internal_proc_list):
    
    for jcl_name,member in zip(internal_proc_list["JCL名"],internal_proc_list["PROC_ID"]):
        jcl_name = take_extensions(jcl_name)
        member = str(member).replace("\\","$")
        internal_proc_dic[(jcl_name,member)] = 1
        jcl_to_internal_proc_dic[jcl_name] = member
        

### Check the jobproc order and make dictionary of orders
### format is list of [sisan_id, library_name]
def update_jobproc_list(jobproc_list):
    
    ### make dictionary
    for jcl_name,parm in zip(jobproc_list["資産ID"],jobproc_list["PARM"]):
        jcl_name = take_extensions(jcl_name)
        
        parm = take_data_from_jcl_analysis_result(parm,"JOBPROC")
        if parm == -1 or parm == "":
            continue
        
        parm = parm.replace("\\","$")
        if jcl_name not in jobproc_dic:
            jobproc_dic[jcl_name] = []
            
        jobproc_dic[jcl_name].append(parm)
        
        # if jcl_name not in jobproc_dic:
        #     jobproc_dic[jcl_name] = set()
            
        # jobproc_dic[jcl_name].add(parm)
            

### make dictionary of received catalog procedure
def update_catapro_dic(catapro_data):
    
    ### dictionary format
    ### key = member id 
    ### value is list of list differed by the priority number of library [[],[],[],[],[],[],]
    member_id = catapro_data[0]
    library = catapro_data[1]
    unit = take_prefix(catapro_data[2],"#")

    priority = check_priority_number(library_name=library)
    
    if member_id not in catapro_dic:
        catapro_dic[member_id] = [[] for i in range(len(priority_list))]
        
    catapro_dic[member_id][priority].append(library)
        
    if (member_id,library) not in catapro_unit_dic:
        catapro_unit_dic[(member_id,library)] = []
        
    catapro_unit_dic[(member_id,library)].append(unit)
 
 
 ### make dictionary of received jcl list
def update_jcl_dic(jcl_list,valid):
    
    ### dictionary format
    ### key = member id ,i.e. module
    ### value is list of asset name, ex) key= SORT, value= [H.HON.SOU%B%SORT, R.HON.SOU%A%SORT]
    
    module,key = jcl_list
    if valid == "○":
        if module not in jcl_dic:
            jcl_dic[module] = []
        
        jcl_dic[module].append(key) 
    else:
        if module not in jcl_invalid_dic:
            jcl_invalid_dic[module] = []
        
        jcl_invalid_dic[module].append(key)      
        
        
def update_easy_dic(easy_list):
    
    ### dictionary format
    ### key = member id ,i.e. module
    ### value is list of asset name, ex) key= SORT, value= [H.HON.SOU%B%SORT, R.HON.SOU%A%SORT]
    
    module,key = easy_list
    if module not in easy_dic:
        easy_dic[module] = []
        
    easy_dic[module].append(key)


### make dictionary of proc_parm key value information
def update_proc_parm_dic(df_proc_parm):
    
    for jcl_name,parm_key,parm_val in zip(df_proc_parm["資産ID"],df_proc_parm["PARM_KEY"],df_proc_parm["PARM_VALUE"]):
        jcl_name = take_extensions(jcl_name)
        if pd.isna(parm_val):
            continue
        parm_key = str(parm_key)
        parm_val = str(parm_val)
        if parm_val == "" or parm_val == " ":
            continue
        parm_val = parm_val.replace("\\","$")
        proc_parm_dic[(jcl_name,parm_key)] = parm_val
   
### make some dictionnary used after from Member List         
def update_member_list2(df):

    for asset,classification in zip(df["ファイル名"],df["格納フォルダ"]):
        asset = take_extensions(asset)
        library,unit,module = asset.split("%")
        unit = "#" + unit
        valid = "○"
        
        if asset in asset_dic:# and asset_dic[asset] == classification:
            continue
        
        
        print(asset,classification)
        asset_dic[asset] = classification
        if module not in module_dic:
            module_dic[module] = set()
        module_dic[module].add(classification)
        
        if valid == "○":
            valid_member_dic[module] = classification
        else:
            invalid_member_dic[module] = classification
            
        if classification == "カタプロ" or classification == "COPY-INCLUDE":
            update_catapro_dic([module,library,unit]) 
        
        if classification == "JCL":
            update_jcl_dic([module,asset],valid)
            
        if classification == "Easyパラメタ":
            update_easy_dic([module,asset])

        
### make some dictionnary used after from Member List         
def update_member_list(df):

    for asset,module, library, unit, classification, valid in zip(df["KEY2"],df["モジュールID"],df["ライブラリ"],df["ソース管理号機"],df["資産分類(ACN)"], df["JSI資産有効判定"]):
        asset = take_extensions(asset)

        asset_dic[asset] = classification
        if module not in module_dic:
            module_dic[module] = set()
        module_dic[module].add(classification)
        
        if valid == "○":
            valid_member_dic[module] = classification
        else:
            invalid_member_dic[module] = classification
            
        if classification == "カタプロ" or classification == "COPY-INCLUDE":
            update_catapro_dic([module,library,unit]) 
        
        if classification == "JCL":
            update_jcl_dic([module,asset],valid)
            
        if classification == "Easyパラメタ":
            update_easy_dic([module,asset])


### in jcl step information PARM_VAR_LIST and PARM_VALUE_LIST
### if the two string like
### M GEM
### #JIKURL1 R.DEB.SOU"
### then in proc_name M=#JIKURL1 and GEM=R.DEB.SOU 
### if the word numbers of two string is not same, consider invailid information and don't take any word
def update_proc_variable_dic(jcl_name,proc_name,keys,values):
    proc_name = update_proc_library(jcl_name,proc_name)

    dic = {key:value for key,value in zip(keys,values)}
    if proc_name not in proc_variable_dic:
        proc_variable_dic[proc_name] = []
    proc_variable_dic[proc_name].append((dic,jcl_name))
    
    # if len(keys) != len(values):
    #     return     
    
    # for key,value in zip(keys,values):
    #     if key == "nan" or value == "nan":
    #         continue
        
    #     if (proc_name,key) not in proc_variable_dic:
    #         proc_variable_dic[(proc_name,key)] = set()
    #     value = value.replace("\\","$")
    #     proc_variable_dic[(proc_name,key)].add((value,jcl_name))
    
   
def update_proc_library(jcl_name,proc_name):
    
    proc_name = clean_proc_name(proc_name)
    
    sisan_id = jcl_name
    member_id = proc_name 
    
    unit_index = sisan_id.index("%")+1 ### sisan_id format is libraryname%unit%xxxxxx and take the index of unit
    unit = sisan_id[unit_index]
    
    ### the number 1000 don't have any mean, just as the enough big number
    ### and after this function, update this number 
    ### 0 is best matched and 1000 is not match any information 
    matching_number = 1000
    cand_member_id = member_id
    
    
    ### firstly check the internal proc 
    if (sisan_id,member_id) in internal_proc_dic:
        cand_member_id = sisan_id+"%"+member_id
        return cand_member_id
        
    
    ### secondary check the jobproc order
    if sisan_id in jobproc_dic:
        ### if jobproc order have
        order_list = jobproc_dic[sisan_id] ### list of libraryname
        for order_library in order_list:
            ### catapro_unit_dic is dictionary (member_id,librart): ["A","X"] (list of unit)
            ### if (member_id,order_library) not in, it means not have asset of [order_library]%[any unit]%[module]
            if (member_id,order_library) not in catapro_unit_dic:
                continue
            
            ### if same unit of jcl_name is in, that is best matched library and unit
            ### so get matching_number of 0
            if unit in catapro_unit_dic[(member_id,order_library)]:
                matching_number = 0
                cand_member_id = order_library+"%"+unit+"%"+member_id
                
#' 20240205 DEL qian.e.wang
            ### if same unit not in, 
            ### ("A","B","D") is treat as same group and ("X","Y","V") is also same group
            ### and if group is different, that library and unit is not matched
            #else:
            #    if unit in ("A","B","D"):
            #        
            #        for cand_unit in ("A","B","D"):
            #            if cand_unit in catapro_unit_dic[(member_id,order_library)]:
            #                if matching_number > 1:
            #                    matching_number = 1
            #                    cand_member_id = order_library+"%"+cand_unit+"%"+member_id
            #                    
            #                    
            #    elif unit in ("X","Y","V"):
            #        for cand_unit in ("X","Y","V"):
            #            if cand_unit in catapro_unit_dic[(member_id,order_library)]:
            #                if matching_number > 1:
            #                    matching_number = 1
            #                    cand_member_id = order_library+"%"+cand_unit+"%"+member_id
            #                    
#' DEL END
    
    ### if decide by jobproc ordered library 
    if matching_number < 1000:
        return cand_member_id
    
    
    ### search library of other 
    if member_id not in catapro_dic:
        return no_matched_member(member_name=member_id)
  
    
    ### if not matched in internal proc or jobproc, but have other candidate
    ### in the "for" loop, loop is [1,2,3,4,5] and lower matching number (means desirable) get first by 3*i
    ### if i==1, 3*i+x is 3<= <5, and i==2, 6<= <8, so doing well
    for i in range(1,len(priority_list)):
        catapro_list = catapro_dic[member_id][i]
        
        if unit in ("X","Y","V") and i == 1:
            continue
        
        for catapro in catapro_list:
            if unit in catapro_unit_dic[(member_id,catapro)]:
                if matching_number > 3*i:
                    matching_number = 3*i 
                    cand_member_id = catapro+"%"+unit+"%"+member_id
                
#' 20240205 DEL qian.e.wang
            #else:
            #    if unit in ("A","B","D"):
            #        
            #        for cand_unit in ("A","B","D"):
            #            if cand_unit in catapro_unit_dic[(member_id,catapro)]:
            #                if matching_number > 3*i+1:
            #                    matching_number = 3*i+1
            #                    cand_member_id = catapro+"%"+cand_unit+"%"+member_id
            #                    
            #    elif unit in ("X","Y","V"):
            #        for cand_unit in ("X","Y","V"):
            #            if cand_unit in catapro_unit_dic[(member_id,catapro)]:
            #                if matching_number > 3*i+1:
            #                    matching_number = 3*i+1
            #                    cand_member_id = catapro+"%"+cand_unit+"%"+member_id
#' DEL END
                                
    if matching_number == 1000:
        return no_matched_member(member_name=member_id)
    else:              
        return cand_member_id




def update_step_sysin(df_step_sysin,focus_ex_list,utach_list,owft_jcl_utach_list,bmcp_list,owft_dxliftin_list):
    
    ### utach candidate is pgm_name = UTACH and [TA ],[PGM=] is in SYSIN sentense
    df_utach = df_step_sysin[((df_step_sysin.PGM_NAME == "UTACH")) & (df_step_sysin["SYSIN"].str.contains("TA ",na=False)) & (df_step_sysin["SYSIN"].str.contains("PGM=",na=False))]
    
    
    ### owft jcl utach candidate is pgm_name = [UTACH] and [UFTPSUPD] is in SYSIN sentense
    df_owft_jcl_utach = df_step_sysin[((df_step_sysin.PGM_NAME == "UTACH")) & (df_step_sysin["SYSIN"].str.contains("UFTPSUPD",na=False))]
    
    ### owft dxliftin candidate is pgm_name = [DXLIFTIN] 
    df_owft_dxliftin = df_step_sysin[(df_step_sysin.PGM_NAME == "DXLIFTIN")]
    
    
    ### focus-ex candidate is proc_name is in (U#FOCUS, Q#FOCUS, R#FOCUS) or pgm_name = FOCUS
    ### and [EX ] in SYSIN sentense
    ### if proc_name is endwith #FOCUS, then need to check the source code and #FOCUS is valid
    for jcl_name,pgm_name,proc_name,sysin in zip(df_step_sysin["JCL_NAME"],df_step_sysin["PGM_NAME"],df_step_sysin["PROC_NAME"],df_step_sysin["SYSIN"]):
        jcl_name = take_extensions(jcl_name)
        if pd.isna(proc_name) == False:
            proc_name = clean_proc_name(proc_name)
        else:
            proc_name = ""
            
        if pd.isna(sysin) == True or "EX " not in str(sysin):
            continue
        
        if (pgm_name == "FOCUS") or (proc_name in focus_name_list):
            member = take_data_from_jcl_analysis_result(string=sysin,type="FOCUS-EX")
            if member != -1:
                member = member.replace("\\","$")
                focus_ex_list.add((jcl_name,jcl_name,"FOCUS-EX",member,""))
        
        elif proc_name.endswith("#FOCUS"):
            member = take_data_from_jcl_analysis_result(string=sysin,type="FOCUS-EX")
            if member != -1:
                member = member.replace("\\","$")
                # focus_ex_list.add((jcl_name,jcl_name,"FOCUS-EX",member,"調査対象" + proc_name))
                need_search_and_check_list.add((jcl_name,jcl_name,"FOCUS-EX",member,"調査対象" + proc_name))
        

    for jcl_name,sysin in zip(df_utach["JCL_NAME"],df_utach["SYSIN"]):
        jcl_name = take_extensions(jcl_name)
            
        member = take_data_from_jcl_analysis_result(string=sysin,type="UTACH")
        if member == -1:
            continue
        member = member.replace("\\","$")
        classification = return_asset_classification(jcl_name)
        if classification == "JCL":
            utach_list.add((jcl_name,jcl_name,"JCL-UTACH",member,""))
        elif classification == "カタプロ":
            utach_list.add((jcl_name,jcl_name,"PROC-UTACH",member,""))
        else:
            utach_list.add((jcl_name,jcl_name,"JCL-UTACH",member,""))
            print(jcl_name,jcl_name,"不明-UTACH",member,"")



        member = take_data_from_jcl_analysis_result(string=sysin,type="UTACH-BMCP")
        if member == -1:
            continue
        member = member.replace("\\","$")
        classification = return_asset_classification(jcl_name)
        if classification == "JCL":
            bmcp_list.add((jcl_name,jcl_name,"JCL-UTACH-BMCP",member,""))
        elif classification == "カタプロ":
            bmcp_list.add((jcl_name,jcl_name,"PROC-UTACH-BMCP",member,""))
        else:
            bmcp_list.add((jcl_name,jcl_name,"JCL-UTACH-BMCP",member,""))
            print(jcl_name,jcl_name,"不明-UTACH-BMCP",member,"")
            

    for jcl_name,sysin in zip(df_owft_jcl_utach["JCL_NAME"],df_owft_jcl_utach["SYSIN"]):
        jcl_name = take_extensions(jcl_name)
        
        member = take_data_from_jcl_analysis_result(string=sysin,type="OWFT-JCL-UTACH")
        if member == -1:
            continue
        member = member.replace("\\","$")
        if return_module_classification(member) == []:
            continue
        
        owft_jcl_utach_list.add((jcl_name,jcl_name,"OWFT-JCL-UTACH",member,""))
      
      
    for jcl_name,sysin in zip(df_owft_dxliftin["JCL_NAME"],df_owft_dxliftin["SYSIN"]):
        jcl_name = take_extensions(jcl_name)
        member = take_data_from_jcl_analysis_result(sysin,"OWFT-DXLIFTIN")
        if member == -1:
            # owft_dxliftin_list.add((jcl_name,jcl_name,"OWFT-DXLIFTIN","呼び出し先不明","個別調査対象"))
            need_search_and_check_list.add((jcl_name,jcl_name,"OWFT-DXLIFTIN","呼び出し先不明","個別調査対象"))
        else:
            member = member.replace("\\","$")
            unit = jcl_name.split("%")[1]
            owft_dxliftin_list.add((jcl_name,jcl_name,"OWFT-DXLIFTIN",member+unit+"_F_S",""))
            
    return focus_ex_list,utach_list,owft_jcl_utach_list,bmcp_list,owft_dxliftin_list




def update_step_info(df_step_info,jcl_pgm_list, proc_pgm_list, jcl_proc_list, proc_proc_list, bmcp_list, \
                    obj_ujobkic_list, obj_upjobkic_list, obj_upbkic_list, obj_uxcmdclr_list, \
                    owft_jcl_list, owft_jcl_proc_cand_list, owft_uftpendc_list, owft_uftpques_list, \
                    jcl_pgm_search_list, proc_pgm_search_list,bmcp_search_list):

    
    ### jcl_pgm or proc_pgm candidate is PGM_NAME is not blank
    df_pgm = df_step_info.dropna(subset=["PGM_NAME"])
    
    ### jcl_proc or proc_proc candidate is PROC_NAME is not blank
    df_proc = df_step_info.dropna(subset=["PROC_NAME"])
    
    ### bmcp candidate is PGM_NAME contains [SUB] and PGM_NAME is end with M ex) xxSUBxxM
    df_bmcp = df_pgm[(df_pgm["PGM_NAME"].str.contains("SUB",na=False)) & (df_pgm["PGM_NAME"].str.endswith("M",na=False))]
    
    ### obj opjobkic candidate is PGM_NAME = [UPJOBKIC]
    df_obj_upjobkic = df_pgm[df_pgm.PGM_NAME == "UPJOBKIC"]
    
    ### obj opbkic candidate is PGM_NAME = [UPBKIC]
    df_obj_upbkic = df_pgm[df_pgm.PGM_NAME == "UPBKIC"]
    
    ### obj ojobkic candidate is PGM_NAME = [UJOBKIC]
    df_obj_ujobkic = df_proc[df_proc.PROC_NAME == "UJOBKIC"]
    
    ### obj oxcmdclr candidate is PGM_NAME = [UXCMDCLR] and PARM_VALUE_LIST is not blank
    df_obj_uxcmdclr = df_pgm[df_pgm.PGM_NAME == "UXCMDCLR"].dropna(subset=["PARM_VALUE_LIST"])
    
    ### owft_jcl or owft_jcl_proc candidate is PGM_NAME = [UFTPSUPD]
    df_owft_jcl = df_pgm[df_pgm.PGM_NAME == "UFTPSUPD"]
    

    
    ### owft_uftpques candidate is PGM_NAME = [UFTPQUES]
    df_owft_uftpques = df_pgm[df_pgm.PGM_NAME == "UFTPQUES"]
    
    ### owft_uftpendc candidate is PGM_NAME = [UFTPENDC]
    df_owft_uftpendc = df_pgm[df_pgm.PGM_NAME == "UFTPENDC"]
    
    
    
    for jcl_name,proc_name,param_key,param_val in zip(df_proc["JCL_NAME"],df_proc["PROC_NAME"],df_proc["PARM_VAR_LIST"],df_proc["PARM_VALUE_LIST"]):
        jcl_name = take_extensions(jcl_name)
        
        keys,values = take_data_from_key_val(param_key,param_val,"PROC-PGM-VARIABLE")
        update_proc_variable_dic(jcl_name,proc_name,keys,values)
               
            
    for jcl_name,proc_name in zip(df_proc["JCL_NAME"],df_proc["PROC_NAME"]):
        jcl_name = take_extensions(jcl_name)
            
        classification = return_asset_classification(jcl_name)
        
        ### this is the error case of jcl analysis tool 
        if proc_name in ["REGION","T","TIME","COND","PARM"]:
            continue
        
        proc_name = update_proc_library(jcl_name,proc_name)
        
        if classification == "JCL":
            jcl_proc_list.add((jcl_name,jcl_name,"JCL-PROC",proc_name,""))
            
            has_relation_proc_set.add(proc_name)
            
        elif classification == "カタプロ":
            proc_proc_list.add((jcl_name,jcl_name,"PROC-PROC",proc_name,""))
        else:
            print(jcl_name,jcl_name,"不明-PROC",proc_name,"")
            jcl_proc_list.add((jcl_name,jcl_name,"JCL-PROC",proc_name,""))
            
            has_relation_proc_set.add(proc_name)
    
    for jcl_name,pgm_name in zip(df_pgm["JCL_NAME"],df_pgm["PGM_NAME"]):
        jcl_name = take_extensions(jcl_name)
        
        classification = return_asset_classification(jcl_name)
        pgm_name = pgm_name.replace("\\","$")
        if "&" in str(pgm_name):
            if classification == "JCL":
                jcl_pgm_search_list.add((jcl_name,pgm_name))
            elif classification == "カタプロ":
                proc_pgm_search_list.add((jcl_name,pgm_name))
            continue
            
        if classification == "JCL":        
            jcl_pgm_list.add((jcl_name,jcl_name,"JCL-PGM",pgm_name,""))
        elif classification == "カタプロ":
            proc_pgm_list.add((jcl_name,jcl_name,"PROC-PGM",pgm_name,""))
        else:
            print(jcl_name,jcl_name,"不明-PGM",pgm_name,"")
            jcl_pgm_list.add((jcl_name,jcl_name,"JCL-PGM",pgm_name,""))


    for jcl_name,param_key,param_val in zip(df_bmcp["JCL_NAME"],df_bmcp["PARM_VAR_LIST"],df_bmcp["PARM_VALUE_LIST"]):
        jcl_name = take_extensions(jcl_name)
        classification = return_asset_classification(jcl_name)
        member = take_data_from_key_val(key=param_key,value=param_val,type="BMCP")
        if member == -1:
            continue
        member = member.replace("\\","$")
        if "&" in member:
            bmcp_search_list.add((jcl_name,member))
            continue
            
        if classification == "JCL":
            bmcp_list.add((jcl_name,jcl_name,"JCL-BMCP",member,""))
        elif classification == "カタプロ":
            bmcp_list.add((jcl_name,jcl_name,"PROC-BMCP",member,""))
        else:
            print(jcl_name,jcl_name,"不明-BMCP",member,"")
            bmcp_list.add((jcl_name,jcl_name,"JCL-BMCP",member,""))

                
    for df, relation, obj_list in zip([df_obj_upjobkic,df_obj_upbkic,df_obj_ujobkic],["OBJ-UPJOBKIC","OBJ-UPBKIC","OBJ-UJOBKIC"],[obj_upjobkic_list,obj_upbkic_list,obj_ujobkic_list]):
        
        for jcl_name,param_val in zip(df["JCL_NAME"],df["PARM_VALUE_LIST"]):
            jcl_name = take_extensions(jcl_name)
            if pd.isna(param_val):
                need_search_and_check_list.add((jcl_name,jcl_name,relation,"呼び出し先不明","個別調査対象"))
                continue
                
            param_val = take_prefix_and_suffix(param_val,"\"")
            param_val = param_val.replace("\\","$")
            if param_val == "":
                need_search_and_check_list.add((jcl_name,jcl_name,relation,"呼び出し先不明","個別調査対象"))
                continue
            
            obj_list.add((jcl_name,jcl_name,relation,param_val,""))

        
    for jcl_name,param_key, param_val in zip(df_obj_uxcmdclr["JCL_NAME"],df_obj_uxcmdclr["PARM_VAR_LIST"],df_obj_uxcmdclr["PARM_VALUE_LIST"]):
        jcl_name = take_extensions(jcl_name)
        param_key = str(param_key)
        members = take_data_from_jcl_analysis_result(param_val,"OBJ-UXCMDCLR")
        
        if members == [] or "PARM" not in param_key:
            need_search_and_check_list.add((jcl_name,jcl_name,"OBJ-UXCMDCLR","呼び出し先不明","個別調査対象"))
            continue
        
        for member in members:
            member = member.replace("\\","$")
            obj_uxcmdclr_list.add((jcl_name,jcl_name,"OBJ-UXCMDCLR",member,""))
            
            
            
    for jcl_name,param_val in zip(df_owft_jcl["JCL_NAME"],df_owft_jcl["PARM_VALUE_LIST"]):
        jcl_name = take_extensions(jcl_name)
        member = take_data_from_jcl_analysis_result(param_val,"OWFT-JCL")
        classification = return_asset_classification(jcl_name)
        
        if member == -1:
            if classification == "JCL":        
                # owft_jcl_list.add((jcl_name,jcl_name,"OWFT-JCL","呼び出し先不明","個別調査対象"))
                need_search_and_check_list.add((jcl_name,jcl_name,"OWFT-JCL","呼び出し先不明","個別調査対象"))
            elif classification == "カタプロ":
                # owft_jcl_proc_cand_list.add((jcl_name,jcl_name,"OWFT-JCL-PROC","呼び出し先不明","個別調査対象"))
                need_search_and_check_list.add((jcl_name,jcl_name,"OWFT-JCL-PROC","呼び出し先不明","個別調査対象"))
            else:
                print(jcl_name,jcl_name,"OWFT-JCL-不明","呼び出し先不明","個別調査対象")
                need_search_and_check_list.add((jcl_name,jcl_name,"OWFT-JCL","呼び出し先不明","個別調査対象"))
                
        else:
            member = member.replace("\\","$")
            if classification == "JCL":        
                owft_jcl_list.add((jcl_name,jcl_name,"OWFT-JCL",member+"_F_S",""))
            elif classification == "カタプロ":
                owft_jcl_proc_cand_list.add((jcl_name,jcl_name,"OWFT-JCL-PROC",member+"_F_S",""))
            else:
                print(jcl_name,jcl_name,"OWFT-JCL",member+"_F_S","")
                owft_jcl_list.add((jcl_name,jcl_name,"OWFT-JCL",member+"_F_S",""))
                
                
                
                
    for df, relation, owft_list in zip([df_owft_uftpendc,df_owft_uftpques],["OWFT-UFTPENDC","OWFT-UFTPQUES"],[owft_uftpendc_list,owft_uftpques_list]):    
            
        for jcl_name,param_val in zip(df["JCL_NAME"],df["PARM_VALUE_LIST"]):
            jcl_name = take_extensions(jcl_name)
            member = take_data_from_jcl_analysis_result(param_val,"OWFT")

            if member == -1 or "&" in member:
                if member == -1:
                    member = "呼び出し先不明"
                # owft_list.add((jcl_name,jcl_name,relation,member,"個別調査対象"))
                member = member.replace("\\","$")
                need_search_and_check_list.add((jcl_name,jcl_name,relation,member,"個別調査対象"))
            else:
                member = member.replace("\\","$")
                owft_list.add((jcl_name,jcl_name,relation,member+"_F_S",""))

        
    return jcl_pgm_list, proc_pgm_list, jcl_proc_list, proc_proc_list, bmcp_list, \
            obj_ujobkic_list, obj_upjobkic_list, obj_upbkic_list, obj_uxcmdclr_list, \
            owft_jcl_list, owft_jcl_proc_cand_list, owft_uftpendc_list, owft_uftpques_list,jcl_pgm_search_list, proc_pgm_search_list, bmcp_search_list
            
  
  
def update_pgm_dsn(df_pgm_dsn,jcl_easy_list):
    
    ### jcl_easy or proc_easy candidate is SYSIN is not blank
    df_easy = df_pgm_dsn.dropna(subset=["SYSIN"])
    
    for jcl_name,sysin in zip(df_easy["JCL_NAME"],df_easy["SYSIN"]):
        jcl_name = take_extensions(jcl_name)
        classification = return_asset_classification(jcl_name)
        sysin = sysin.replace("\\","$")
        if sysin not in easy_dic:
            continue
        
        for source in easy_dic[sysin]:
            if classification == "JCL":        
                jcl_easy_list.add((jcl_name,jcl_name,"JCL-EASY",source,"外部定義EASY"))
            elif classification == "カタプロ":
                jcl_easy_list.add((jcl_name,jcl_name,"PROC-EASY",source,"外部定義EASY"))
            else:
                print(jcl_name,jcl_name,"JCL-EASY",source,"外部定義EASY")
                jcl_easy_list.add((jcl_name,jcl_name,"JCL-EASY",source,"外部定義EASY"))
    
    return jcl_easy_list
  
  
def get_variable(jcl_name,pgm_name):
    
    val_list = []

    i = 0
    last = ""
    while i < len(pgm_name):
        if pgm_name[i] == "&":
            if last:
                val_list.append(last)
            last = "&"
            i += 1
            while i < len(pgm_name) and pgm_name[i] != "." and pgm_name[i] != "&":
                last += pgm_name[i]
                i += 1
            val_list.append(last)
            last = ""
            if i < len(pgm_name) and pgm_name[i] == "&":
                i -= 1
                print("この変数定義は文法的に誤りの可能性があります。",pgm_name,jcl_name)
            
        else:
            last += pgm_name[i]
        i += 1
    if last:
        val_list.append(last)
  

    ans_list = set()
    vals = []
    for v in val_list:
        if "&" in v:
            vals.append(v.replace("&",""))
            
    find = 0
    if jcl_name in proc_variable_dic:
        for dic,source in proc_variable_dic[jcl_name]:
            ok = 1
            for v in vals:
                if v not in dic:
                    ok = 0
                    break
            
            if ok:
                find = 1
                convert = []
                for v in val_list:
                    if "&" in v:
                        convert.append(dic[v.replace("&","")])
                    else:
                        convert.append(v)
                convert_string = "".join(convert)
                ans_list.add((convert_string,source))
                
    if find:
        return ans_list
    
    convert = []
    ok = 1
    for v in val_list:
        if "&" in v:
            v = v.replace("&","")
            if (jcl_name,v) in proc_parm_dic:
                convert.append(proc_parm_dic[(jcl_name,v)])
            else:
                ok = 0
                break
        else:
            convert.append(v)
            
    if ok:
        convert_string = "".join(convert)
        ans_list.add((convert_string,jcl_name))
        return ans_list
    
    print("PROC-変数 変数元不明",jcl_name,pgm_name)
    return [(pgm_name,jcl_name+" 変数調査対象")]

  


### in the case JCL-PGM and has variable like &PGM
### it means the jcl_source has internal proc, so check internal proc list and search the variable
def update_jcl_pgm_variable_list(jcl_pgm_list, jcl_pgm_search_list):
    
    for jcl_name, pgm_name in jcl_pgm_search_list:
        if jcl_name in jcl_to_internal_proc_dic:   
            internal_proc_name = jcl_name + "%" + jcl_to_internal_proc_dic[jcl_name]

            if internal_proc_name in proc_variable_dic:
                for dic,nsource in proc_variable_dic[internal_proc_name]:
                    if pgm_name in dic:
                        s = dic[pgm_name]
                        jcl_pgm_list.add((jcl_name,jcl_name,"JCL-PGM",s,"PGM変数 内部PROC利用"))
            
            else:
                # jcl_pgm_list.add((jcl_name,jcl_name,"JCL-PGM",pgm_name,"PGM変数不明 調査対象"))
                need_search_and_check_list.add((jcl_name,jcl_name,"JCL-PGM",pgm_name,"PGM変数不明 調査対象"))

        else:
            # jcl_pgm_list.add((jcl_name,jcl_name,"JCL-PGM",pgm_name,"PGM変数不明 調査対象"))
            need_search_and_check_list.add((jcl_name,jcl_name,"JCL-PGM",pgm_name,"PGM変数不明 調査対象"))
                    
    return jcl_pgm_list
             
### three function [make_proc_pgm_variable_list,make_bmcp_variable_list,make_bmcp_variable_list] is close 
### get the variable case and return set of information
def make_proc_pgm_variable_list(proc_pgm_search_list):
    
    proc_pgm_variable_list = set()
    
    for jcl_name,pgm_name in proc_pgm_search_list:
        
        if jcl_name not in has_relation_proc_set:
            continue

        member_list = get_variable(jcl_name,pgm_name)

        for member, sub_info in member_list:
            if "&" in member:
                need_search_and_check_list.add((sub_info,sub_info,"PROC-変数呼出",member,jcl_name))
                continue
            proc_pgm_variable_list.add((sub_info,sub_info,"PROC-変数呼出",member,jcl_name))
  
    return proc_pgm_variable_list

def make_bmcp_variable_list(bmcp_search_list):
    
    bmcp_variable_list = set()
    
    for jcl_name,pgm_name in bmcp_search_list:
        
        if jcl_name not in has_relation_proc_set:
            continue

        member_list = get_variable(jcl_name,pgm_name)
 
        for member, sub_info in member_list:
            if "&" in member:
                need_search_and_check_list.add((sub_info,sub_info,"BMCP-変数",member,jcl_name))
                continue
            bmcp_variable_list.add((sub_info,sub_info,"BMCP-変数",member,jcl_name))
  
    return bmcp_variable_list


def make_owft_jcl_proc_list(owft_jcl_proc_cand_list):
    owft_jcl_proc_list = set()
    for list in owft_jcl_proc_cand_list:
        source,member = list[1],list[3]
        if source not in has_relation_proc_set:
            continue
        if "&" not in member:
            owft_jcl_proc_list.add(list)
            continue
        
        member_list = get_variable(source,take_suffix(member,"_F_S"))
        for member, sub_info in member_list:
            if "&" in member:
                need_search_and_check_list.add((sub_info,sub_info,"OWFT-JCL-PROC-変数",member,source))
                continue
            owft_jcl_proc_list.add((sub_info,sub_info,"OWFT-JCL-PROC-変数",member+"_F_S","変数ケース: "+source))
                
    return owft_jcl_proc_list


#################################################################################################################



### functions mainly based on original source code ##############################################################
def take_data_from_string(string,type,take_string="",language_type="COMMON"):
    string = str(string)

     
    
    ### INCLUDE, ex) /\      INCLUDE  &CPYINC              
    ### and, in this case, get &CPYINC (variable case)  
    if type == "INCLUDE":
        if comment_line_check(string=string,language_type="JCL") == -1:
            return -1
        
        slist = string.split(" ")
        
        ### start is 1 in the case, string like //HANTEI     INCLUDE  &CPYINC   and slist is ["//HANTEI","INCLUDE","&CPYINC"]
        ### start is 0 in the case, string like              INCLUDE  &CPYINC   and slist is ["INCLUDE","&CPYINC"]
        ### it means, the first order written in the sentense should be INCLUDE
        start = 0
        if string[0] != " ":
            start += 1
            
        include = False
        
        for s in slist[start:]:
            if s == "" or s == "\'" or s == "\"":
                continue
            
            if include == True:
# DEL 20240201 qian.e.wang
                #if "(" in s:
                #    return -1
# DEL END
                s = take_prefix_and_suffix(s,"\"")
                return s
            
            if include == False:
                if s == "INCLUDE":
                    include = True
                
                else:
                    return -1
        return -1
    
    ### EXPAND, ex) //        EXPAND  R#LIB02                        
    ### and, in this case, get R#LIB02
    if type == "EXPAND":
        if comment_line_check(string=string,language_type="JCL") == -1:
            return -1
        
        slist = string.split(" ")
        
        ### start is 1 in the case, string like //        EXPAND  R#LIB02   and slist is ["//","EXPAND","R#LIB02"]
        ### start is 0 in the case, string like           EXPAND  R#LIB02   and slist is ["EXPAND","R#LIB02"]
        ### it means, the first order written in the sentense should be EXPAND
        start = 0
        if string[0] != " ":
            start += 1
            
        include = False
        
        for s in slist[start:]:
            if s == "" or s == "\'" or s == "\"":
                continue
            
            if include == True:
                s = take_prefix_and_suffix(s,"\"")
                return s
            
            if include == False:
                if s == "EXPAND":
                    include = True
                
                else:
                    return -1
        return -1
    
    ### in ASSEMBLY-CALL, get CALL order
    ### ex)          CALL  XZDUMP2,(WTASK,HEAD1,HEAD2,KEYHAD,WINAREA,WRECSI,       C00040700
    ### in this case, get XZDUMP2
    if type == "ASSEMBLY-CALL":
        if comment_line_check(string,"ASM") == -1:
            return -1
        
        string = string[8:72]
        call_flag = False
        slist = re.split("[ .,\'\"]",string)
        for s in slist:
            if s == " " or s == "\n" or s == "":
                continue
            if call_flag == True:
                
                if check_string_only_number(s) == 1:
                    return -1
                
                if s[0] == "(" or s[-1] == ")":
                    return -1
                return s
            
            if s != "CALL":
                return -1
            call_flag = True
            
        return -1
                
    ### in ASSEMBLY-ENTRY, get ENTRY order 
    ### ex)          ENTRY CTRTK               *                                    00003400
    ### in this case CTRTK
    if type == "ASSEMBLY-ENTRY":
        if comment_line_check(string,"ASM") == -1:
            return -1
        
        string = string[8:72]
        members = []
        entry_flag = False
        slist = re.split("[ .,\'\"]",string)
        for s in slist:
            if s == " " or s == "\n" or s == "":
                continue
            if s[0] == "*":
                break
            if entry_flag == True and check_string_only_number(s) == -1:
                members.append(s)
            
            if s != "ENTRY" and entry_flag == False:
                return members
            entry_flag = True
        return members
    
    ### in EASY-CALL, get CALL order in EASY source code
    ### ex)    CALL  XADATE  WPARA  WCOMPYMD                                        00003200
    ### in this case , get XADATE 
    if type == "EASY-CALL":
        slist = string.split(" ")

        call_find = False
        for s in slist:
            if s == "" or s == " " or s == "\n":
                continue
            
            if call_find == True:
                s = take_prefix_and_suffix(s,"\'")
                s = take_prefix_and_suffix(s,"\"")
                return s
            
            if s != "CALL":
                return -1
            call_find = True
        return -1
                

    
    # if type == "PROC-PGM":
    #     if "PGM=" not in string:
    #         return -1 
    #     if str(string).startswith("//*"):
    #         return -1
        
    #     pgm_index = string.find("PGM=")
    #     string_after = string[pgm_index:]
    #     slist = re.split("[=, ]",string_after)
    #     for s in slist[1:]:
    #         if s == "" or s == "\'" or s == "\"":
    #             continue
    #         s = take_prefix_and_suffix(s,"\"")
    #         return s
    #     return -1
    
    # if type == "PROC-PROC":
    #     if "PGM=" in string:
    #         return -1 
    #     if str(string).startswith("//*"):
    #         return -1
        
    #     pgm_index = string.find("EXEC")
    #     string_after = string[pgm_index:]
    #     slist = re.split("[, ]",string_after)
    #     for s in slist[1:]:
    #         if s == "" or s == "\'" or s == "\"":
    #             continue
    #         s = take_prefix_and_suffix(s,"\"")
    #         return s
    #     return -1
    
    if language_type == "FORTRAN":
        if comment_line_check(string=string, language_type=language_type) == -1:
            return -1

        ### if FORTRAN-CALL, search CALL order 
        ### ex)    1 CALL    GKHF01( HF, INWC, SHIMA, NSTP )                           00007400
        ### in this case get GKHF01, and if GKHF01 in Member List, it's ok and add to relation list
        ###  else GKHF01 is SUBROUTINE of missing asset, so add to subroutine_dic and search after
        if type == "FORTRAN-CALL":
            call_index = string.find("CALL ")
            slist = re.split("[, ()]",string[call_index:])
            
            for s in slist[1:]:
                if s:
                    return s
                
            return -1
        
        ### if, FORTRAN-SUBROUTINE, search SUBROUTINE definition
        ### ex)      SUBROUTINE  GKHR02( INHS, INWC, INLS, HF, BAR, IR1PS, HR )        00000900"
        ### in this case get GKHR02
        if type == "FORTRAN-SUBROUTINE":
            subroutine_index = string.find("SUBROUTINE ")
            slist = re.split("[, ()]",string[subroutine_index:])
            
            for s in slist[1:]:
                if s:
                    return s
                
            return -1
        
        ### if FORTRAN-FUNCTION, search FUNCTION definition
        ### ex)       FUNCTION      ZIKAN( A, B, C )                                    00000800
        ### in this case, get ZIKAN
        if type == "FORTRAN-FUNCTION":           
            function_index = string.find("FUNCTION ")
            slist = re.split("[, ()]",string[function_index:])
            
            for s in slist[1:]:
                if s:
                    return s
                
            return -1
        
        ### if FUNCTION, check if searched FUNCTION is used 
        ### ex)          TH9DC = ZIKAN(VFSH9(NSTP),ALF01,LLH9DC)                        00026700
        ### in this string, ZIKAN is used as function, (in FORTRAN-FUNCTION, ZIKAN is defined in upper string)
        if type == "FUNCTION":
            take_string = " "+take_string+"("
            
            key_index = string.find(take_string)
            if key_index == -1 or "FUNCTION " in string[:key_index]:
                return -1
            return 1
        
   
    if type == "CALL-VARIABLE":
        if comment_line_check(string,"COBOL") == -1:
            return -1
        # ADD 20241008 yi.a.qian
        elif any([x in take_string for x in ["*", "+", "?", "(", ")"]]):
            return -1
        # ADD END

        #re_pattern = '\s*'+take_string+'\s+?PIC\s+?.+?\s+?VALUE\s+?\'\s*(?P<value_name>\S*)\s*\''
        re_pattern = '\s*'+take_string+'\s+?PIC\s+?.+?\s+?VALUE\s+?[\'\"]\s*(?P<value_name>\S*)\s*[\'\"]'
        re_pattern = re.compile(re_pattern)
         
        search = re_pattern.search(string)    

        if search:
            s = search.group("value_name")
            return check_string_only_number_and_return_string(s)
        
                    
        #re_pattern = '\s*MOVE\s+?\'\s*(?P<value_name>\S*)\s*\'\s+?TO\s+?.*'+take_string
        re_pattern = '\s*MOVE\s+?[\'\"]\s*(?P<value_name>\S*)\s*[\'\"]\s+?TO\s+?.*'+take_string
        re_pattern = re.compile(re_pattern)
        
        search = re_pattern.search(string)    
        if search:
            s = search.group("value_name")
            return check_string_only_number_and_return_string(s)

        return -1
   
    if type == "SCREEN-FMID":
        if comment_line_check(string,"COBOL") == -1:
            return -1
        
        ### in SCREEN-FMID, search the name move to FMID
        ### ex) 018800     MOVE  'NX99FWBN'          TO  FMID  OF SYNC-DCOM.           
        ### in this case NX99FWBN, and if NX99FWBN is like screen name, add relation
        
        #re_pattern = '\s*MOVE\s+?\'\s*(?P<value_name>\S*)\s*\'\s+?TO\s+?.*FMID'
        re_pattern = '\s*MOVE\s+?[\'\"]\s*(?P<value_name>\S*)\s*[\'\"]\s+?TO\s+?.*FMID'
        re_pattern = re.compile(re_pattern)
         
        search = re_pattern.search(string)    
        if search:
            
            s = search.group("value_name")
            if check_string_only_number(s) == 1:
                return -1
            if judge_screen(s) == -1:
                return -1
            
            return "'"+s+"'"
        
        ### if string is like 063000     MOVE W-FMTID TO FMID OF ASYNC-DCOM.                            
        ### get W-FMTID, but this is variable and need to search W-FMTID 
        re_pattern = '\s*MOVE\s+?(?P<value_name>\S*)\s+?TO\s+?.*FMID'
        re_pattern = re.compile(re_pattern)
         
        search = re_pattern.search(string)    
        if search:
            
            s = search.group("value_name")
            if check_string_only_number(s) == 1:
                return -1
            return s
        
        return -1
                
    
    if type == "SCREEN-VALUE":
        if comment_line_check(string,"COBOL") == -1:
            return -1
        
        ### if CALL-VARIABLE, get the info from MOVE order or VALUE order
        ### 083600     MOVE 'N2VJEW01' TO W-FMTID.           and N2VJEW01
        ### get N2VJEW01
        #re_pattern = '\s+?VALUE\s+?\'\s*(?P<value_name>\S*)\s*\''
        re_pattern = '\s+?VALUE\s+?[\'\"]\s*(?P<value_name>\S*)\s*[\'\"]'
        re_pattern = re.compile(re_pattern)
        search = re_pattern.search(string)    
        if search:
            s = search.group("value_name")
            if check_string_only_number(s) == 1:
                return -1
            return judge_screen(s)
        return -1
    
    ### in OBJ-XPOBAPI, for now, take the value in KSJOBNM   
    ### ex) 026700        MOVE  'DCD0OBJ'  TO  KSJOBNM OF W-UXPOBAPI-DT            
    ### in this case 'DCD0OBJ' and add relation
    ### if get value is variable like  MOVE  W-FMTID  TO  KSJOBNM OF W-UXPOBAPI-DT 
    ### get W-FMTID
    
    ### return two item, (get value or -1), (-1 if variable case, else 1) 
    if type == "XPOBAPI":
        if comment_line_check(string, "COBOL") == -1:
            return -1,-1
        
        ### case of ex) 026700        MOVE  'DCD0OBJ'  TO  KSJOBNM OF W-UXPOBAPI-DT
        #re_pattern = '\s*MOVE\s+?\'\s*(?P<value_name>\S*)\s*\'\s+?TO\s+?.*KSJOBNM'
        re_pattern = '\s*MOVE\s+?[\'\"]\s*(?P<value_name>\S*)\s*[\'\"]\s+?TO\s+?.*KSJOBNM'
        re_pattern = re.compile(re_pattern)
         
        search = re_pattern.search(string)    
        if search:
            
            s = search.group("value_name")
            if check_string_only_number(s) == 1:
                return -1,-1
            return s,1
        
        ### case of variable ex) MOVE  W-FMTID  TO  KSJOBNM OF W-UXPOBAPI-DT 
        re_pattern = '\s*MOVE\s+?\s*(?P<value_name>\S*)\s*\s+?TO\s+?.*KSJOBNM'
        re_pattern = re.compile(re_pattern)
         
        search = re_pattern.search(string)    
        if search:
            
            s = search.group("value_name")
            if check_string_only_number(s) == 1:
                return -1,-1
            return s,-1
            
        
        return -1,-1

    
    
    
    ### in COBOL-SUBSCHEMA, get the SUBSCHEMA order
    ### ex) 002900 SUBSCHEMA-NAME.  'UGSUB01'.                   
    ### in this case, get UGSUB01 
    if type == "COBOL-SUBSCHEMA":
        if comment_line_check(string,"COBOL") == -1:
            return -1
        
        string = string[6:]
        slist = re.split("[, \'\"]",string)
        subschema_flag = False
        for s in slist:
            if s == " " or s == "" or s == "\n":
                continue
            
            if subschema_flag == True:
                
                return check_string_only_number_and_return_string(s)
            if "SUBSCHEMA-NAME-" in s:
                return -1
            
            if "SUBSCHEMA-NAME" not in s:
                return -1
            subschema_flag = True
 
        return -1
    
    ### in COBOL-ENTRY, get the ENTRY order
    ### ex) 006400     ENTRY  'NOR4DLK'                          
    ### in this case, get NOR4DLK
    if type == "COBOL-ENTRY":
        if comment_line_check(string,"COBOL") == -1:
            return -1

        string = string[6:]
        slist = re.split("[, \'\"]",string)
        entry_flag = False
        for s in slist:
            if s == " " or s == "" or s == "\n":
                continue
            if entry_flag == True:
                return check_string_only_number_and_return_string(s)
            if s != "ENTRY":
                return -1
            entry_flag = True

        return -1
    
    
    ### in COBOL-CALL, get the CALL order
    ### ex) 008500     CALL  'XKDATE'  USING  XKDATEP.       
    ### in this case, get XKDATE, and add relation
    
    ### if the variable case like  008500     CALL  W-XKDATE  USING  XKDATEP. 
    if type == "COBOL-CALL":
        if comment_line_check(string,"COBOL") == -1:
            return -1
        # ダブルコーテーションでのCOBOL-CALL対応
        #re_pattern = '\s+?CALL\s+?\'\s*(?P<value_name>\S*)\s*\''
        re_pattern = '\s+?CALL\s+?[\'\"]\s*(?P<value_name>\S*)\s*[\'\"]'
        re_pattern = re.compile(re_pattern)
        search = re_pattern.search(string)    
        if search:
            s = search.group("value_name")
            if check_string_only_number(s) == 1:
                return -1
            return "'"+s+"'"
        
        re_pattern = '\s+?CALL\s+?\s*(?P<value_name>\S*)\s*'
        re_pattern = re.compile(re_pattern)
        search = re_pattern.search(string)    
        if search:
            s = search.group("value_name")
            # if check_string_only_number(s) == 1 or check_cobol_call_valid(s) == -1:
            if check_string_only_number(s) == 1:
                return -1
            
            s = take_prefix_and_suffix(s,"\"")
            return take_prefix_and_suffix(s,"\'")
        return -1
    
    
    ### in OWFT-COBOL, get the variable used to UFTPSUPD order
    ### ex) 037000        CALL  'UFTPSUPD'  USING  FTP-PARAM1.                      191212AD
    ### in this case FTP-PARAM1
    if type == "OWFT-COBOL":
        if comment_line_check(string,"COBOL") == -1:
            return -1
        #re_pattern = '\s*CALL\s+?\'\s*UFTPSUPD\s*\'\s+?USING\s+?.'
        re_pattern = '\s*CALL\s+?[\'\"]\s*UFTPSUPD\s*[\'\"]\s+?USING\s+?.'
        if re.search(re_pattern,string):
            using_index = string.find("USING")
            slist = re.split("[ .,\'\"]",string[using_index:])
            for s in slist[1:]:
                if s == " " or s == "" or s == "\n":
                    continue
                return s
        return -1
    
    
    if type == "OWFT-CALL-VARIABLE":
        if comment_line_check(string,"COBOL") == -1:
            return -1

        ### in the case of CALL-VARIABLE, get value
        s = take_data_from_string(string, "CALL-VARIABLE")
        if s == "CR":
            return -1
        if s != -1:
            return s

        ### in the case of  ex) 005100     02  FILLER              PIC X(8) VALUE 'MBMK600H'.           191212AD
        #re_pattern = '\s+?FILLER\s+?PIC\s+?.+?\s+?VALUE\s+?\'\s*(?P<value_name>\S*)\s*\''    
        re_pattern = '\s+?FILLER\s+?PIC\s+?.+?\s+?VALUE\s+?[\'\"]\s*(?P<value_name>\S*)\s*[\'\"]'    
        re_pattern = re.compile(re_pattern)
         
        search = re_pattern.search(string)    

        if search:
            s = search.group("value_name")
            if check_string_only_number(s) == 1 or s == "CR":
                return -1
            return s
            
        return -1  
    
    
    
    
    
    ###in SCREEN-SCHEDULE
    ### ex)    SCHEDULE  FID=KF00FN21,ALTPGM=KV89                             00005000
    ### need to have the command of FID=xxxx and (PGM=xxxx or ALTPGM=xxxx)
    ### and both found, return FID and PGM, in this case KF00FN21,KV89
    if type == "SCREEN-SCHEDULE":
        schedule_index = string.find("SCHEDULE")
        slist = re.split("[, ]",string[schedule_index:])
        fid_name = ""
        pgm_name = ""
        
        for s in slist[1:]:
            if s == " " or s == "" or s == "\n":
                continue
                
            if fid_name == "":
                if "FID=" not in s:
                    return -1,-1 
                fid_name = s.split("=")[1]
                
            elif pgm_name == "":
                if "PGM=" not in s:
                    return fid_name,-1
                pgm_name = s.split("=")[1]
                
                return fid_name,pgm_name
        return -1,-1
    
    ###in SCREEN-UKEY
    ### ex)           UKEY      KEY=(10,8,'FN21E000'),PGM=KFK0                    00005100
    ### need to have the command of PGM=xxxx 
    ### and it found, return PGM, in this case KFK0
    if type == "SCREEN-UKEY":
        if "PGM=" not in string:
            return -1
        pgm_index = string.find("PGM=")
        slist = re.split("[, ]",string[pgm_index:])
        
        pgm_name = ""
        
        for s in slist:
            if s == " " or s == "" or s == "\n":
                continue    
            if pgm_name == "":
                if "PGM=" not in s:
                    return -1
                pgm_name = s.split("=")[1]
                
                return pgm_name
            
    ### in SCREEN-DIST
    ### ex) SAID      DIST   PARM='P.BHB2'                                          00000300 
    ### if found DIST and PARM=, get after [.] in this case, BHB2
    ### if only found DIST, return 1, because, PARM will be defined later
    if type == "SCREEN-DIST":
        
        if " DIST " not in string:
            return -1
           
            
        if "PARM=" in string:
            slist = re.split("[, ()]",string)
            for s in slist:
                if s == " " or s == "" or s == "\n":
                    continue 
                if "PARM=" in s:
                    s = s.split("=")[1]
                    s = take_prefix_and_suffix(s,"\'")
                    s = take_prefix_and_suffix(s,"\"")
                    if "." not in s:
                        continue
                    
                    return s.split(".")[1]
    ### CALLのパターン
    ### ex) SAID      DIST   CALL='P.E3349'
    ### if found DIST and PARM=, get after [.] in this case, E3349
    ### if only found DIST, return 1, because, PARM will be defined later
        if "CALL=" in string:
            slist = re.split("[, ()]",string)
            for s in slist:
                if s == " " or s == "" or s == "\n":
                    continue 
                if "CALL=" in s:
                    s = s.split("=")[1]
                    s = take_prefix_and_suffix(s,"\'")
                    s = take_prefix_and_suffix(s,"\"")
                    if "." not in s:
                        continue
                    
                    return s.split(".")[1]

        return 1
  
    ### in SCREEN-PARM
    ### case 1
    ### ex)       PARM='P.BBBC'                                           00000400
    ### in this case, get after [.], in this case BBBC
    
    ### case 2
    ### ex) KZ113     DIST  DATA=('1','2','3','4',                                  00000300
    ###                   'A','B','Z',' ',ELSE)                             00000400
    ###             PARM=('P.BBY1','P.BEE7','P.BBY7','P.BBY4',              00000500
    ###                   'P.BBF1','P.BBL5','P.BBTA',                       00000600
    ###                   'P.BBTA','P.BXDSTER')                             00000700
    ### in this case, need to get some PGM and it is possible to have 
    ### PARM= case, )   PARM=('P.BBY1','P.BEE7','P.BBY7','P.BBY4',              00000500
    ### and in this case, get [BBY1,BEE7,BBY7,BBY4]
    
    ### or 
    
    ### other case, )   'P.BBF1','P.BBL5','P.BBTA',                       00000600
    ### and in this case, get [BBF1, BBL5, BBTA]
    
    ### so, in slist, split the string by bracket[()] and comma[,] 
    ### and check each word
    if type == "SCREEN-PARM":
        slist = re.split("[, ()]",string)
        
        pgm_list = []
        
        for s in slist:
            if s == " " or s == "" or s == "\n":
                continue 
            ### case 1
            if "PARM=" in s:
                s = s.split("=")[1]
                s = take_prefix_and_suffix(s,"\'")
                s = take_prefix_and_suffix(s,"\"")
                if "." not in s:
               
                    continue
                pgm_list.append(s.split(".")[1])
                
                continue
            
            ### case 2
            if s[0] == "\'" and s[-1] == "\'":
                s = take_prefix_and_suffix(s,"\'")
                if "." not in s:
                    continue
                pgm_list.append(s.split(".")[1])
            if s[0] == "\"" and s[-1] == "\"":
                s = take_prefix_and_suffix(s,"\"")
                if "." not in s:
                    continue
                pgm_list.append(s.split(".")[1])
            
        return pgm_list
    
    ### TODO　CALLパターン
    ### in SCREEN-CALL
    ### case 1
    ### ex)       CALL='P.BBBC'                                           00000400
    ### in this case, get after [.], in this case BBBC
    
    ### case 2
    ### ex)         CALL=('P.BBY1','P.BEE7','P.BBY7','P.BBY4',              00000500
    ###                   'P.BBF1','P.BBL5','P.BBTA',                       00000600
    ###                   'P.BBTA','P.BXDSTER')                             00000700
    ### in this case, need to get some PGM and it is possible to have 
    ### CALL= case, )   CALL=('P.BBY1','P.BEE7','P.BBY7','P.BBY4',              00000500
    ### and in this case, get [BBY1,BEE7,BBY7,BBY4]
    
    ### or 
    
    ### other case, )   'P.BBF1','P.BBL5','P.BBTA',                       00000600
    ### and in this case, get [BBF1, BBL5, BBTA]
    
    ### so, in slist, split the string by bracket[()] and comma[,] 
    ### and check each word
    if type == "SCREEN-CALL":
        slist = re.split("[, ()]",string)
        
        pgm_list = []
        
        for s in slist:
            if s == " " or s == "" or s == "\n":
                continue 
            ### case 1
            if "CALL=" in s:
                s = s.split("=")[1]
                s = take_prefix_and_suffix(s,"\'")
                s = take_prefix_and_suffix(s,"\"")
                if "." not in s:
               
                    continue
                pgm_list.append(s.split(".")[1])
                
                continue
            
            ### case 2
            if s[0] == "\'" and s[-1] == "\'":
                s = take_prefix_and_suffix(s,"\'")
                if "." not in s:
                    continue
                pgm_list.append(s.split(".")[1])
            if s[0] == "\"" and s[-1] == "\"":
                s = take_prefix_and_suffix(s,"\"")
                if "." not in s:
                    continue
                pgm_list.append(s.split(".")[1])
            
        return pgm_list
    
    if type=="ACSAPI-ACSEXT":
        if comment_line_check(string,"COBOL") == -1:
            return -1
        
        #re_pattern = '\s*CALL\s+?\'\s*ACSAPI\s*\'\s+?.*ACSEXT\s+?'
        re_pattern = '\s*CALL\s+?[\'\"]\s*ACSAPI\s*[\'\"]\s+?.*ACSEXT\s+?'
        
        if re.search(re_pattern,string):

            slist = re.split("[ .,\'\"]",string[string.find("ACSEXT"):])

            for s in slist[1:]:
                if s == " " or s == "\n" or s == "":
                    continue
                return s
            return -1
        
        #re_pattern = '\s*CALL\s+?\'\s*XPAPI\s*\'\s+?.*ACSEXT\s+?'
        re_pattern = '\s*CALL\s+?[\'\"]\s*XPAPI\s*[\'\"]\s+?.*ACSEXT\s+?'
        
        if re.search(re_pattern,string):

            slist = re.split("[ .,\'\"]",string[string.find("ACSEXT"):])
            for s in slist[1:]:
                if s == " " or s == "\n" or s == "":
                    continue
                return s
            
            return -1
        return -1
        
    if type == "CALL-VARIABLE-ACSAPI-ACSEXT":
        if comment_line_check(string,"COBOL") == -1:
            return -1
        
        #re_pattern = '\s*MOVE\s+?\'\s*(?P<value_name>\S*)\s*\'\s+?TO\s+?.*SNAME\s+?.*\s+?'+take_string
        re_pattern = '\s*MOVE\s+?[\'\"]\s*(?P<value_name>\S*)\s*[\'\"]\s+?TO\s+?.*SNAME\s+?.*\s+?'+take_string
        re_pattern = re.compile(re_pattern)
        
        search = re_pattern.search(string)    
        if search:
            s = search.group("value_name")
            return check_string_only_number_and_return_string(s)

        
        #re_pattern = '\s*'+take_string+'\s+?PIC\s+?.+?\s+?VALUE\s+?\'\s*(?P<value_name>\S*)\s*\''
        re_pattern = '\s*'+take_string+'\s+?PIC\s+?.+?\s+?VALUE\s+?[\'\"]\s*(?P<value_name>\S*)\s*[\'\"]'
        re_pattern = re.compile(re_pattern)
         
        search = re_pattern.search(string)    

        if search:
            s = search.group("value_name")
            return check_string_only_number_and_return_string(s)
        
        return -1
        
                    
        
     
    if type == "CALL-VARIABLE-ACSAPI-SWITCH":
        if comment_line_check(string,"COBOL") == -1:
            return -1,-1
        
        #re_pattern = '\s*MOVE\s+?\'.*\'\s+?TO\s+?.*SNAME\s+?.*\s+?'+take_string
        re_pattern = '\s*MOVE\s+?[\'\"].*[\'\"]\s+?TO\s+?.*SNAME\s+?.*\s+?'+take_string
        if re.search(re_pattern,string):
            value_index = string.find("MOVE")
            slist = re.split("[ .,\'\"]",string[value_index:])
            for s in slist[1:]:
                if s == " " or s == "" or s == "\n":
                    continue
                return s,1
            return -1,1
        
        re_pattern = '\s*'+take_string+'\s+?PIC\s+?.+?\s+?VALUE\s+?.'
        
        if re.search(re_pattern,string):
            value_index = string.find("VALUE")
            slist = re.split("[ .,\'\"]",string[value_index:])
            for s in slist[1:]:
                if s == " " or s == "\n" or s == "":
                    continue
                return s,1
            return -1,1
    
        #re_pattern = '\s*MOVE\s+?\'.*\'\s+?TO\s+?.*NAME\s+?.*\s+?'+take_string
        re_pattern = '\s*MOVE\s+?[\'\"].*[\'\"]\s+?TO\s+?.*NAME\s+?.*\s+?'+take_string
        if re.search(re_pattern,string):
            value_index = string.find("MOVE")
            slist = re.split("[ .,\'\"]",string[value_index:])
            for s in slist[1:]:
                if s == " " or s == "" or s == "\n":
                    continue
                return s,1
            return -1,1
        
        
        re_pattern = '\s*MOVE\s+?.*\s+?TO\s+?.*SNAME\s+?.*\s+?'+take_string
        if re.search(re_pattern,string):
            value_index = string.find("MOVE")
            slist = re.split("[ .,\'\"]",string[value_index:])
            for s in slist[1:]:
                if s == " " or s == "" or s == "\n":
                    continue
                return s,2
            return -1,1
            
        re_pattern = '\s*MOVE\s+?.*\s+?TO\s+?.*NAME\s+?.*\s+?'+take_string
        if re.search(re_pattern,string):
            value_index = string.find("MOVE")
            slist = re.split("[ .,\'\"]",string[value_index:])
            for s in slist[1:]:
                if s == " " or s == "" or s == "\n":
                    continue
                return s,2
            return -1,1
    
        return -1,1 
    
        
        
        
    if type=="ACSAPI-SWITCH":

        for cand_string in take_string:  
    
            #re_pattern = '\s*CALL\s+?\'\s*ACSAPI\s*\'\s+?USING\s+?'+cand_string+'\s+?'
            re_pattern = '\s*CALL\s+?[\'\"]\s*ACSAPI\s*[\'\"]\s+?USING\s+?'+cand_string+'\s+?'
    
            if re.search(re_pattern,string):
                string = string[string.find(cand_string):]

                slist = re.split("[ .,\'\"]",string[string.find(cand_string+" "):])
       
                for s in slist[1:]:
                    if s == " " or s == "\n" or s == "":
                        continue
                    if "DCOM" in s:
                        return s
                return -1
            
            #re_pattern = '\s*CALL\s+?\'\s*XPAPI\s*\'\s+?USING\s+?'+cand_string+'\s+?'
            re_pattern = '\s*CALL\s+?[\'\"]\s*XPAPI\s*[\'\"]\s+?USING\s+?'+cand_string+'\s+?'
            
            if re.search(re_pattern,string):

                string = string[string.find(cand_string):]
                slist = re.split("[ .,\'\"]",string[string.find(cand_string+" "):])
       
                for s in slist[1:]:
                    if s == " " or s == "\n" or s == "":
                        continue
                    if "DCOM" in s:
                        return s
                return -1
        return -1
    
    if type=="DEFINE-SWITCH":

        #re_pattern = '\s+?PIC\s+?.+?\s+?VALUE\s+?\'\s*SWITCH\s*\''
        re_pattern = '\s+?PIC\s+?.+?\s+?VALUE\s+?[\'\"]\s*SWITCH\s*[\'\"]'

        if re.search(re_pattern,string):

            slist = re.split("[ .,\'\"]",string)
            last = ""
            for s in slist:
                if s == " " or s == "\n" or s == "":
                    continue
                if s == "PIC":
                    return last
                
                last = s
      
        return -1
    
    # if type=="DEFINE-VARIABLE":
    
    #     re_pattern = '\s+?PIC\s+?.+?\s+?VALUE\s+?\'\s*SWITCH\s*\''

    #     if re.search(re_pattern,string):

    #         slist = re.split("[ .,\'\"]",string)
    #         last = ""
    #         for s in slist:
    #             if s == " " or s == "\n" or s == "":
    #                 continue
    #             if s == "PIC":
    #                 return last
                
    #             last = s
                
    #     re_pattern = '\s*MOVE\s+?\'.*\'\s+?TO\s+?'+take_string+'\s+?'
    #     if re.search(re_pattern,string):
    #         value_index = string.find("MOVE")
    #         slist = re.split("[ .,\'\"]",string[value_index:])
    #         for s in slist[1:]:
    #             if s == " " or s == "" or s == "\n":
    #                 continue
    #             return s
    #         return -1
      
    #     return -1
        
        
        
    

### add library to list[3] member information
def add_library_proc(list):
    sisan_id = list[1]
    member_id = list[3]
    member_id = update_proc_library(sisan_id,member_id)         
    list[3] = member_id
            
    return list
            
            
def check_proc(lis):
    jcl_name = lis[0]
    proc_name = lis[3]
    proc_name = clean_proc_name(proc_name)
    
    jobproc = ""
    if jcl_name in jobproc_dic:
        for library in jobproc_dic[jcl_name]:
            jobproc += library + ",\n"
    cand = ""
    if proc_name in catapro_dic:
        for i in range(6):
            for catapro in catapro_dic[proc_name][i]:
                for unit in catapro_unit_dic[(proc_name,catapro)]:
                    cand_member_id = catapro+"%"+unit+"%"+proc_name
                    cand += cand_member_id + ",\n"
    
    check_list.add((jcl_name,jcl_name,lis[2],proc_name,jobproc,cand))
    
### make member with library list 
### base list format is list of [sisan_id, sisan_id, relation-type( ex. jcl-proc), member_id]
def make_member_with_library_list(base_list):
    member_with_library_list = []
    
    for now_list in base_list:
        now_list = add_library_proc(list(now_list))
        if str(now_list[3]).endswith("_未受領PROC"):
            check_proc(now_list)
        member_with_library_list.append(now_list)
                
    return member_with_library_list
        


def make_member_with_library_list_onbatch(base_list):
    member_with_library_list = []
    
    for now_list in base_list:
        now_list = list(now_list)
        member_id = now_list[3]
        source = now_list[1]
        if "%" not in source:
            source = now_list[0]
        unit = source.split("%")[1]
        find_xdsrf = 0
                
        member_id_before = member_id
        if member_id in jcl_dic:
            # if len(jcl_dic[member_id]) == 1:
            #     member_id = jcl_dic[member_id][0]
            # else:
            
            string = "調査対象: 複数候補: "
            find_match = 0
            for member in jcl_dic[member_id]:
                member_unit = member.split("%")[1]
                if str(member).startswith("X.DSRF"):
                    find_xdsrf = 1
                    find_match = 2
                    member_id = member
                    
                elif find_match != 2:
                    if unit == member_unit:
                        find_match = 2
                        member_id = member
                    # else:
                    #     if unit in "AB" and member_unit in "AB":
                    #         member_id = member
                    #         find_match = 1
                    #     elif unit in "XYV" and member_unit in "XYV":
                    #         member_id = member
                    #         find_match = 1
                
                string += member + ", "
            if len(jcl_dic[member_id_before]) > 1:
                now_list[4] = string
                
            if find_match == 0:
                member_id = member_id + "_未受領"
                
        else:
            # cand = ""
            # if member_id in jcl_invalid_dic:
            #     for key in jcl_invalid_dic[member_id]:
            #         cand += key + ",\n"
            # check_list.add((source,source,now_list[2],member_id,"",cand))
            member_id = member_id + "_未受領"
            
            
        now_list[3] = member_id
        member_with_library_list.append(now_list)
        
    return member_with_library_list



def make_fortran_list(files):
    
    fortran_list = set()
    fortran = "FORTRAN"
    
    ### if FORTRAN-CALL, search CALL order 
    ### ex)    1 CALL    GKHF01( HF, INWC, SHIMA, NSTP )                           00007400
    ### in this case get GKHF01, and if GKHF01 in Member List, it's ok and add to relation list
    ###  else GKHF01 is SUBROUTINE of missing asset, so add to subroutine_dic and search after
    grep_call_list = grep_and_make_list(files=files,keywords=["CALL "],type="FORTRAN-CALL",returnpath=False,language_type=fortran)
    subroutine_dic = {}

    for file_name, member in grep_call_list:
        classification = return_module_classification(member)
        file_name, name = get_filenames(file_name)
        
        if classification != []:
            for clas in classification:
                fortran_list.add((file_name,name,"FORTRAN-CALL",member,clas))    
        else:
            if member not in subroutine_dic:
                subroutine_dic[member] = []
            subroutine_dic[member].append(file_name)

    ### if, FORTRAN-SUBROUTINE, search SUBROUTINE definition
    ### ex)      SUBROUTINE  GKHR02( INHS, INWC, INLS, HF, BAR, IR1PS, HR )        00000900"
    ### in this case get GKHR02
    ### if GKHR02 in subroutine_dic, the relation is [GKHR02 written source code] -> [CALL GKHR02 written source code]
    ### and after make relations, delete GKHR02 data from subroutine_dic
    grep_subroutine_list = grep_and_make_list(files=files,keywords=["SUBROUTINE "],type="FORTRAN-SUBROUTINE",returnpath=False,language_type=fortran)
    
    for file_name, member in grep_subroutine_list:
        file_name, name = get_filenames(file_name)
        
        if member in subroutine_dic:
            for file in subroutine_dic[member]:
                file_member = file.split("%")[-1]
                fortran_list.add((file,file_member,"FORTRAN-CALL",name,"FORTRAN SUBROUTINE ⇒ "+member+" "+file_name))
            del subroutine_dic[member]
            
            
    ### if it is not find in SUBROUTINE and Member List, that asset is missing and need to check
    for key,value in subroutine_dic.items():
        for file in value:
            file_member = file.split("%")[-1]
            # fortran_list.add((file,file_member,"FORTRAN-CALL","呼び出し先未受領","個別調査対象: FORTRAN SUBROUTINE ⇒ "+key))
            need_search_and_check_list.add((file,file_member,"FORTRAN-CALL","呼び出し先未受領","個別調査対象: FORTRAN SUBROUTINE ⇒ "+key))
            
            
    ### if FORTRAN-FUNCTION, search FUNCTION definition
    ### ex)       FUNCTION      ZIKAN( A, B, C )                                    00000800
    ### in this case, get ZIKAN  
    grep_function_list = grep_and_make_list(files=files,keywords=["FUNCTION "],type="FORTRAN-FUNCTION",returnpath=True,language_type=fortran)

    ### keywords is list of FUNCTION like ["ZIKAN","XXX"]
    keywords = [keyword for _,keyword in grep_function_list]
    
    ### grep_each_list get the list of each files found keyword
    ### if keywords is ["ZIKAN","XXX"]
    ### grep_each_list is [[some [file_name and string found "ZIKAN"]], [some[file_name and string found "XXX"]]] (list of 2 list)
    grep_each_list = grep_file_and_string(files=files,keywords=keywords)
    
     
    
    ### grep_function_list is list of [["ZIKAN" defined source_code, "ZIKAN"],["XXX" defined source_code, "XXX"]]
    ### grep_each_list is list of [[some [file_name and string found "ZIKAN"]], [some[file_name and string found "XXX"]]]
    ### so in this "for" loop 
    ### grep_function is ["ZIKAN" defined source_code, "ZIKAN"]
    ### grep_word_list is [[file_name, found "ZIKAN" string], [other_file_name, found "ZIKAN" string]]
    ### and in found "ZIKAN" string , if "ZIKAN" is used as FUNCTION, the relation file_name -> "ZIKAN" defined source_code is add.
    for grep_function, grep_word_list in zip(grep_function_list,grep_each_list):
        file,keyword = grep_function
        file, file_member = get_filenames(file)

        for file_name, string in grep_word_list:
            member = take_data_from_string(string=string,type="FUNCTION",take_string=keyword,language_type=fortran)
            file_name, name = get_filenames(file_name)
            
            if member == -1:
                continue
            fortran_list.add((file,file_member,"FORTRAN-FUNCTION",name,"FORTRAN FUNCTION ⇒ "+keyword+" "+file_name))

            
    return fortran_list
            
    
    
def make_cobol_list(files):
    
    cobol = "COBOL"
    
    cobol_call_list = set()
    cobol_call_variable_list = set()
    cobol_entry_list = set()
    cobol_subchema_list = set()
    
    cobol_entry_set = set()
    
    owft_cobol_list = set()
    
    ### in COBOL-ENTRY, get the ENTRY order
    ### ex) 006400     ENTRY  'NOR4DLK'                          
    ### in this case, get NOR4DLK, add relation and add to cobol_entry_set
    cobol_entry_grep_list = grep_and_make_list(files=files, keywords=[" ENTRY "], type="COBOL-ENTRY", returnpath=True, language_type=cobol)
    for file,member in cobol_entry_grep_list:
        file_name, name = get_filenames(file)
        sub = get_cobol_group_info(file)

        cobol_entry_list.add(("",member,"COBOL-ENTRY",name,file_name+sub))
        cobol_entry_set.add(name)
        
    ### in COBOL-SUBSCHEMA, get the SUBSCHEMA order
    ### ex) 002900 SUBSCHEMA-NAME.  'UGSUB01'.                   
    ### in this case, get UGSUB01, and add relation
    cobol_subchema_grep_list = grep_and_make_list(files=files,keywords=["SUBSCHEMA"],type="COBOL-SUBSCHEMA", returnpath=True, language_type=cobol)
    
    for file,member in cobol_subchema_grep_list:
        file_name, name = get_filenames(file)
        sub = get_cobol_group_info(file)
        
        cobol_subchema_list.add((file_name,name,"COBOL-SUB",member,sub))
        
     

    ### in COBOL-CALL, get the CALL order
    ### ex) 008500     CALL  'XKDATE'  USING  XKDATEP.       
    ### in this case, get XKDATE, and add relation
    
    ### if the variable case like  008500     CALL  W-XKDATE  USING  XKDATEP. 
    ### it add to cobol_call_search_list and search after   
    cobol_call_search_list = []
    cobol_call_grep_list = grep_and_make_list(files=files,keywords=[" CALL "],type="COBOL-CALL",returnpath=True, language_type=cobol)
    
    for file,member in cobol_call_grep_list:
        file_name, name = get_filenames(file)
        sub = get_cobol_group_info(file)
                
        if member[0] == "\'" or member[-1] == "\'" or member[0] == "\"" or member[-1] == "\"":
            member = take_prefix_and_suffix(member,"\'")
            member = take_prefix_and_suffix(member,"\"")
            if member[0] == "\'" or member[-1] == "\'" or member[0] == "\"" or member[-1] == "\"":
                continue
            
            classification = return_module_classification(member)
            if classification == []:
                if member in cobol_entry_set:
                    classification = ["ENTRY 移行対象外"]
                else:
                    classification = ["メンバ一覧記載なし"]
            for clas in classification:
                cobol_call_list.add((file_name,name,"COBOL-CALL",member,clas+sub))
            
        else:
            if member in cobol_no_need_variable_list:
                cobol_call_variable_list.add((file_name,name,"COBOL-CALL-変数",member,"調査不要CALL変数"+sub))
                continue
            
            cobol_call_search_list.append([file,member])
          
    ### if CALL-VARIABLE, get the info from MOVE order or VALUE order
    ### if, 083600     MOVE 'N2VJEW01' TO W-XKDATE.    
    ### get N2VJEW01
    for file, member in cobol_call_search_list:
        find = False
        file_name, name = get_filenames(file)
        sub = get_cobol_group_info(file)
        
        with open(file,errors="ignore") as f:
            for line in f:
                if comment_line_check(string=line,language_type=cobol) == -1 or member not in line:
                    continue
                
                get_val = take_data_from_string(line,"CALL-VARIABLE",member)
                if get_val == -1:
                    continue
                
                find = True
                cobol_call_variable_list.add((file_name,name,"COBOL-CALL-変数",get_val,member+sub))
                
        if find == False:
            # cobol_call_variable_list.add((file_name,name,"COBOL-CALL-変数","変数元不明","個別調査対象: "+member+sub))
            need_search_and_check_list.add((file_name,name,"COBOL-CALL-変数","変数元不明","個別調査対象: "+member+sub))
    
      
    ### in OWFT-COBOL, get the variable used to UFTPSUPD order
    ### ex) 037000        CALL  'UFTPSUPD'  USING  FTP-PARAM1.                      191212AD
    ### in this case FTP-PARAM1, and search the definition of FTP-PARAM1 after
    owft_cobol_grep_list = grep_and_make_list(files=files,keywords=["UFTPSUPD"],type="OWFT-COBOL",returnpath=True,language_type="COBOL")
    
    
    ### in the case of UFTPSUPD variable
    ### in addtion to MOVE order or VALUE order like CALL-VARIABLE
    
    ### the case like under and is exist and need to get MBMK600H
    ### 004700 01  FTP-PARAM1.                                                  191212AD
    ### 004800     02  FILLER              PIC 9(4) BINARY VALUE 11.            191212AD
    ### 004900     02  HENKO-CD            PIC X(2) VALUE '00'.                 191212AD
    ### 005000     02  FILLER              PIC X(1) VALUE ','.                  191212AD
    ### 005100     02  FILLER              PIC X(8) VALUE 'MBMK600H'.           191212AD
    
    ### after else: program, consider this case

    for file, member in owft_cobol_grep_list:

        find = False
        file_name, name = get_filenames(file)
        sub = get_cobol_group_info(file)
                
        value_flag = False
        with open(file,errors="ignore") as f:
            for line in f:
                if comment_line_check(line,"COBOL") == -1:
                    continue
                
                if member not in line and value_flag == False:
                    continue
                get_val = take_data_from_string(line,"OWFT-CALL-VARIABLE",member)
       
                if get_val != -1:
                    find = True
                    owft_cobol_list.add((file_name,name,"OWFT-COBOL",get_val+"_F_S",sub))
                    
                else:
                    if value_flag == False:
                        
                        ### if the current line is like
                        ### 004700 01  FTP-PARAM1.                                                  191212AD
                        ### there is a probability to define FTP-PARAM1 in the line like ) 005100     02  FILLER              PIC X(8) VALUE 'MBMK600H'.           191212AD
                        ### but, basically, we assume FTP-PARAM1 and defined value in the same line, so add value_flag and if value_flag == True, check all line, even if FTP-PARAM1 is not found.
                        re_pattern = '\s+?01\s+?'+member
        
                        if re.search(re_pattern,line):
                            value_flag = True
                         
                    ### if the statement of other value start
                    ### ex) ### 005300 01  FTP-PARAM2.                                                  191212AD
                    ### value_flag is return to False
                    else:
                        re_pattern = '01\s+?'
                        if re.search(re_pattern,line):
                            value_flag = False
 
        if find == False:
            # owft_cobol_list.add((file_name,name,"OWFT-COBOL",member+"_F_S","個別調査対象"+sub))
            need_search_and_check_list.add((file_name,name,"OWFT-COBOL",member+"_F_S","個別調査対象"+sub))
    
    
    return cobol_call_list,cobol_call_variable_list,cobol_entry_list,cobol_subchema_list,owft_cobol_list
    
    
    
def make_assembly_list(asm_files):
    
    assembly_list = set()
    
    
    ### in ASSEMBLY-CALL, get CALL order
    ### ex)          CALL  XZDUMP2,(WTASK,HEAD1,HEAD2,KEYHAD,WINAREA,WRECSI,       C00040700
    ### in this case, get XZDUMP2
    ### and get relation
    asm_call_grep_list = grep_and_make_list(asm_files,[" CALL "], "ASSEMBLY-CALL")
    for file_name, member in asm_call_grep_list:
        file_name,name = get_filenames(file_name)

        assembly_list.add((file_name,name,"ASM-CALL",member,""))
        
    
    ### in ASSEMBLY-ENTRY, get ENTRY order 
    ### ex)          ENTRY CTRTK               *                                    00003400
    ### in this case CTRTK
    ### and get relation CTRTK -> written source code
    for filepath in asm_files:
        file_name,name = get_filenames(filepath)
        
        with open(filepath, errors="ignore") as tf:
            
            for line in tf:
                if comment_line_check(line,"ASM") == -1:
                    continue
                    
                if " ENTRY " in line:
                    members = take_data_from_string(line,"ASSEMBLY-ENTRY")
                    if members == []:
                        continue

                    for member in members: 
                        if member != -1 and member != name:
                            assembly_list.add((member,member,"ASM-ENTRY",name,file_name))
                        
    return assembly_list


def update_easy_list(easy_files,easy_parm_files,jcl_easy_list,easy_call_list):
    
    
    for filepath in easy_files:
        file_name,_ = get_filenames(filepath)

        match=re.match("^(.+)E\d\d\d$",file_name)
        if match:
            name = match.group(1)
            jcl_easy_list.add((name,name,"JCL-EASY",file_name,"EASYパラメタに記載"))
        # rev_name = file_name[::-1]
        # rev_name = take_prefix(rev_name,rev_name[:rev_name.find("E")+1])
        # name = rev_name[::-1]
            
        

    ### in EASY-CALL, get CALL order in EASY source code
    ### ex)    CALL  XADATE  WPARA  WCOMPYMD                                        00003200
    ### in this case , get XADATE and add relation
    easy_parm_grep_list = grep_and_make_list(files=easy_parm_files+easy_files, keywords=" CALL", type="EASY-CALL")
    for file_name, member in easy_parm_grep_list:
        file_name = take_extensions(file_name)
        easy_call_list.add((file_name,file_name,"EASY-CALL",member,""))
                        
    return jcl_easy_list, easy_call_list


def make_include_expand_list(jcl_files,proc_files):
    
    include_expand_list = set()
    include_expand_proc_list = set()

    ### EXPAND, ex) //        EXPAND  R#LIB02                        
    ### and, in this case, get R#LIB02
    
    ### INCLUDE, ex) /\      INCLUDE  &CPYINC              
    ### and, in this case, get &CPYINC (variable case)        
    include_expand_grep_list = grep_file_and_string(files=jcl_files+proc_files,keywords=["INCLUDE","EXPAND"], returnpath=False, language_type="JCL")

    for grep_files, keyword in zip(include_expand_grep_list,["INCLUDE","EXPAND"]):
        
        for jcl_name, string in grep_files:
            jcl_name = take_extensions(jcl_name)

#' 20240206 DEL qian.e.wang
            ### if the source code is proc and not has JCL-PROC relations, this proc source is not valid, so pass the process
            #if return_asset_classification(jcl_name) == "カタプロ" and jcl_name not in has_relation_proc_set:
            #    continue
#' DEL END
            
            member = take_data_from_string(string=string, type=keyword)

            if member == -1:
                continue
          
            
            relation_type = "JCL-"+keyword
            sub_info = ""
            
            if "カタプロ" in return_module_classification(member):
                member = update_proc_library(jcl_name,member)
                include_expand_proc_list.add((jcl_name,jcl_name,relation_type,member,sub_info))
                continue
            if "COPY-INCLUDE" in return_module_classification(member):
                member = update_proc_library(jcl_name,member)
                include_expand_proc_list.add((jcl_name,jcl_name,relation_type,member,"COPY-INCLUDE"))
                continue
                
                
                
            # if "COPY-INCLUDE" in return_module_classification(member):
            #     sub_info = "COPY-INCLUDE"
                
                
            ### if member not contain "&", relation is valid and add to list
            if "&" not in member:
                include_expand_list.add((jcl_name,jcl_name,relation_type,member,sub_info))
                continue


            ### variable case
            member_list = get_variable(jcl_name,member)
            
            for member, sub_info in member_list:
                add_info = ""
                if "&" in member:
                    need_search_and_check_list.add((jcl_name,jcl_name,relation_type,member,"変数調査対象"))    
                    continue
                
                if "カタプロ" in return_module_classification(member) or "COPY-INCLUDE" in return_module_classification(member):
                    if "COPY-INCLUDE" in return_module_classification(member):
                        add_info = " COPY-INCLUDE"
                    member = update_proc_library(jcl_name,member)
                    if "COPY-INCLUDE" in add_info and str(member).endswith("PROC"):
                        member = take_suffix(member,"PROC")
                include_expand_list.add((sub_info,sub_info,relation_type+"-変数",member,jcl_name+add_info))

    return include_expand_list,include_expand_proc_list




def make_pgm_screen_list(cobol_files):
    
    pgm_screen_move_list = set()
    pgm_screen_value_list = set()
    
    ### in SCREEN-FMID, search the name move to FMID
    ### ex) 018800     MOVE  'NX99FWBN'          TO  FMID  OF SYNC-DCOM.           
    ### in this case NX99FWBN, and if NX99FWBN is like screen name, add relation
    
    ### if string is like 063000     MOVE W-FMTID TO FMID OF ASYNC-DCOM.                            
    ### get W-FMTID, but this is variable and need to search W-FMTID 
    ### so if retured member is not surround with ', it consider as variable and add pgm_fmid_search_list
    pgm_fmid_grep_list = grep_and_make_list(files=cobol_files, keywords=["FMID"], type="SCREEN-FMID", returnpath=True, language_type="COBOL")
    pgm_fmid_search_list = []
 
    for file,member in pgm_fmid_grep_list:
        file_name, name = get_filenames(file)
        sub = get_cobol_group_info(file)
        
        if member[0] == "\'" or member[-1] == "\'" or member[0] == "\"" or member[-1] == "\"":
            member = take_prefix_and_suffix(member,"\'")
            member = take_prefix_and_suffix(member,"\"")
            pgm_screen_move_list.add((file_name,name,"PGM-画面",member,"FMID設定値解析"+sub))
            
        else:
            pgm_fmid_search_list.append([file,member])
          
    ### if CALL-VARIABLE, get the info from MOVE order or VALUE order
    ### 083600     MOVE 'N2VJEW01' TO W-FMTID.           and N2VJEW01
    ### get N2VJEW01
    for file, member in pgm_fmid_search_list:
        # find = False
        file_name, name = get_filenames(file)
        sub = get_cobol_group_info(file)
                
        with open(file,errors="ignore") as f:
            for line in f:
                if comment_line_check(string=line,language_type="COBOL") == -1 or member not in line:
                    continue
                
                get_val = take_data_from_string(line,"CALL-VARIABLE",member)
                if get_val == -1:
                    continue
                # find = True
                if judge_screen(get_val) != -1:
                    pgm_screen_move_list.add((file_name,name,"PGM-画面",get_val,"FMID設定値解析-変数"+sub))
                    
        # if find == False:
        #     pgm_screen_move_list.add((file_name,name,"PGM-画面","変数不明","FMID設定値解析-変数: "+member))
        #     need_search_and_check_list.add((file_name,name,"PGM-画面","変数不明","FMID設定値解析-変数: "+member))
    
   
    ### in SCREEN-VALUE, it search VALUE order and get screen like information
    ### ex) 006400       03  WXCOMM-EFID1      PIC X(008)      VALUE 'KJ27FW01'.    *CNVT*  
    ### in this case, get KJ27FW01
    pgm_screen_values = grep_and_make_list(files=cobol_files,keywords=[" VALUE "],type="SCREEN-VALUE", returnpath=True)
    
    for file, member in pgm_screen_values:
        jcl_name, name = get_filenames(file)
        sub = get_cobol_group_info(file)
        
        pgm_screen_value_list.add((jcl_name,name,"PGM-画面",member,"VALUE値解析"+sub))
        
    return pgm_screen_move_list, pgm_screen_value_list


def make_obj_list(cobol_files):
    
    obj_xpobapi_list = set()
    obj_xpobapi_variable_list = set()
    
    ### in OBJ-XPBKIC, get by tool is difficult, so just get the source code, which written "XPBKIC"   
    obj_xpbkic_file_list,obj_xpobapi_file_list = grep_files(files=cobol_files,keywords=["XPBKIC","XPOBAPI"],returnpath=True)
    obj_xpbkic_file_list = [[take_extensions(os.path.split(file)[-1]),"","OBJ-XPBKIC","","個別調査対象"] for file in set(obj_xpbkic_file_list)]
    
    for info in obj_xpbkic_file_list:
        need_search_and_check_list.add(tuple(info))
     
    ### in OBJ-XPOBAPI, for now, take the value in KSJOBNM   
    ### ex) 026700        MOVE  'DCD0OBJ'  TO  KSJOBNM OF W-UXPOBAPI-DT            
    ### in this case 'DCD0OBJ' and add relation
    ### if get value is variable like  MOVE  W-FMTID  TO  KSJOBNM OF W-UXPOBAPI-DT    
    ### OBJ-XPOBAPI-変数 and check after 
    for filepath in obj_xpobapi_file_list:
        file_name, name = get_filenames(filepath)
        sub = get_cobol_group_info(filepath)
        find = False
        xpobapi = False
        with open(filepath, errors="ignore") as tf:
            
            for line in tf:
                if comment_line_check(line,"COBOL") == -1:
                    continue
                l = re.split("[ .,\'\"]",line)
                if "XPOBAPI" in l:
                    xpobapi = True
                
                if "KSJOBNM" not in line:
                    continue
                member,valid = take_data_from_string(string=line, type="XPOBAPI")
                
                if member == -1:
                    continue
                
                find = True
                if valid == -1:
                    # obj_xpobapi_variable_list.add((file_name,file_name,"OBJ-XPOBAPI-変数",member,"変数調査対象"+sub))
                    need_search_and_check_list.add((file_name,name,"OBJ-XPOBAPI-変数",member,"変数調査対象"+sub))
                else:
                    obj_xpobapi_list.add((file_name,name,"OBJ-XPOBAPI",member,""))


        if find == False:
            need_search_and_check_list.add((file_name,name,"OBJ-XPOBAPI-変数","KSJOBNMなし"+str(xpobapi),"変数調査対象"+sub))
    
    return obj_xpbkic_file_list, obj_xpobapi_list, obj_xpobapi_variable_list


def make_screen_definition_list(mcp_files, screen_files):
    
    screen_definition_list = set()

    ### in screen definition and FID pattern
    ### get the FID and PGM
    
    ### case 1, single line case
    ### ex)        SCHEDULE  FID=KU01FW01,PGM=UPACSCMD                            00003900
    ### in this case, make relation FID -> PGM, in this case KU01FW01 -> UPASCMD
    
    ### case 2, multi line case, 
    ### ex)     SCHEDULE  FID=KF00FN21,ALTPGM=KV89                             00005000
    ###         UKEY      KEY=(10,8,'FN21E000'),PGM=KFK0                    00005100 
    ### in this case, firstly make relation FID -> PGM, in this case KF00FN21 -> KV89 
    ### and also, keep fid_name =  KF00FN21
    ### and then, in UKEY definition, get PGM and make relation, in this case KF00FN21 -> KFK0
    for file in mcp_files:
        file_name,_ = get_filenames(file)

        with open(file) as f:
            schedule_flag = False ### if current line is SCHEDULE definition or continuous UKEY definition, flag is True
            fid_name = ""
            for line in f:
                if line[0] == "*":
                    continue
                
                
                if " SCHEDULE " in line:
                    fid_name,pgm_name = take_data_from_string(line,"SCREEN-SCHEDULE")
                    
                    if fid_name == -1:
                        fid_name = ""
                        continue
                    schedule_flag = True
                    
                    if pgm_name == -1:
                        continue
                    
                    screen_definition_list.add((file_name,"",fid_name,"画面→PGM呼出",pgm_name,"パターン1 FID"))
                
                
                elif " UKEY " in line and schedule_flag == True:
                    pgm_name = take_data_from_string(line,"SCREEN-UKEY")
                    
                    if pgm_name == -1:
                        schedule_flag = False
                        continue
                    screen_definition_list.add((file_name,"",fid_name,"画面→PGM呼出",pgm_name,"パターン1 FID"))
                    
                else:
                    schedule_flag = False
                    

    ### in FMID pattern
    ### get PGM in each files
    
    ### case1 
    ### ex) SAID      DIST  DATA=ELSE                                               00004600
    ###                     PARM='P.BBQI'                                           00004700
    ### in this case, don't have bracket and get BBQI by SCEERN-PARM
    
    ### case2
    ### ex) KZ113     DIST  DATA=('1','2','3','4',                                  00000300
    ###                           'A','B','Z',' ',ELSE)                             00000400
    ###                     PARM=('P.BBY1','P.BEE7','P.BBY7','P.BBY4',              00000500
    ###                           'P.BBF1','P.BBL5','P.BBTA',                       00000600
    ###                           'P.BBTA','P.BXDSTER')                             00000700
    ### in this case, need to get [BBY1,BEE7, ... , BXDSTER]
    ### to do this, firstly need to check, whether found [DIST] and dist_flag changed to True
    ### and also, at line 00000300, only '('  found, but not found the other ')', to search PGM in PARM definition after, it need to find ')', so bracket_flag_dist = False when line 00000400
    ### and from line 00000500 , dist_flag=True and bracket_flag_dist = False, it is possible to define PGM in PARM definition, so check by SCREEN-PARM
    ### PARM definition is also continue until ')' found, so if ')' found,  bracket_flag_parm = False and DIST definition is end and dist_flag = False
    
    for file in screen_files:
        file_name,member_name = get_filenames(file)
        
        with open(file) as f:
            dist_flag = False
            bracket_flag_dist = False
            bracket_flag_parm = False
            for line in f:
                if line[0] == "*":
                    continue
                
                if " DIST " in line:
                    
                    if "(" in line:
                        bracket_flag_dist = True
                        
                    if ")" in line:
                        bracket_flag_dist = False
                        
                    pgm_name = take_data_from_string(line,"SCREEN-DIST")
                    dist_flag = True
                    
                    if pgm_name == 1:
                        continue
                    
                    if judge_screen(pgm_name) == -1:
                        screen_definition_list.add(("",file_name,member_name,"画面→PGM呼出",pgm_name,"パターン2 FMID"))
                        
                    else:
                        screen_definition_list.add(("",file_name,member_name,"画面→画面呼出",pgm_name,"パターン2 FMID"))
                    
                    dist_flag = False
                    
                    
                ### TODO　CALLパターン
                elif " CALL=" in line:
                    
                    if "(" in line:
                        bracket_flag_parm = True
                        
                    if ")" in line:
                        bracket_flag_parm = False
                    
                    pgm_name = take_data_from_string(line,"SCREEN-CALL")
                    dist_flag = True
                    
                    if pgm_name == [] or bracket_flag_parm == False:
                        dist_flag = False
                        
                    for pgm in pgm_name:
                        
                        if judge_screen(pgm) == -1:
                            screen_definition_list.add(("",file_name,member_name,"画面→PGM呼出",pgm,"パターン1 FID"))
                            
                        else:
                            screen_definition_list.add(("",file_name,member_name,"画面→画面呼出",pgm,"パターン1 FID"))
                            
                
                elif dist_flag == True and bracket_flag_dist == True:
                    if ")" in line:
                        bracket_flag_dist = False
                
                elif dist_flag == True and bracket_flag_dist == False:
                    
                    if "(" in line:
                        bracket_flag_parm = True
                        
                    if ")" in line:
                        bracket_flag_parm = False
                    
                    pgm_name = take_data_from_string(line,"SCREEN-PARM")
                    
                    if pgm_name == [] or bracket_flag_parm == False:
                        dist_flag = False
                        
                    for pgm in pgm_name:
                        
                        if judge_screen(pgm) == -1:
                            screen_definition_list.add(("",file_name,member_name,"画面→PGM呼出",pgm,"パターン2 FMID"))
                            
                        else:
                            screen_definition_list.add(("",file_name,member_name,"画面→画面呼出",pgm,"パターン2 FMID"))
                            
                
                else:
                    dist_flag = False
                    bracket_flag_dist = False
                    bracket_flag_parm = False

    return screen_definition_list

def make_data_definition_list(damschema_files,mcp_files,ped_files,dbschema_files,dbsubschema_files,jcl_files,proc_files):
    
    data_definition_list = set()
    
    for filepath in ped_files:
        
        filename,_ = get_filenames(filepath)
        
        ped = ""
        dataset = ""
        database = ""
        with open(filepath, errors="ignore") as tf:
            
            data= []
            for i in tf:
                if i[0] !='*':
                    data.append(i[0:72])
            
            # data1 = ','.join(data)
            data1 = re.split(';|\\.\s', ' '.join(data))
            PED_NAME      = re.compile(r'^.*PED(\s)*NAME(\s|(IS))*(?P<ped_name>.*)\s*.*')        
            DATASET_NAME  = re.compile(r'^[;\s]*DATASET(\s)*NAME(\s|(IS))*(?P<dataset_name>.*)')       
            DATABASE_NAME  = re.compile(r'^.*DATABASE(\s)*NAME(\s|(IS))*(?P<database_name>\w*)')    
             
            for i,line in enumerate(data1):
                if(PED_NAME.match(line)):
                    ped = re.sub(r'(\.)$','', (PED_NAME.match(line).group('ped_name'))\
                                .replace(';','').replace(' ','').replace('.',''))
                    data_definition_list.add((filename,ped+"_PED","PED-PED(ファイル名)",filename,""))

                elif(DATASET_NAME.match(line)):
                    dataset_info = DATASET_NAME.match(line).group('dataset_name')
                    if re.search('\sFOR\s',line):
                        dataset = dataset_info.split('FOR')[0].replace(' ','')

                    else:
                        dataset = dataset_info.replace(' ','')
                        dataset_info = 'x'
     
                    if ped != "":
                        data_definition_list.add((filename,ped+"_PED","PED-DAM",dataset,""))
                        # data_definition_list.add((filename,ped+"_PED","PED-PED(ファイル名)",filename,""))

                elif(DATABASE_NAME.match(line)):
                    database = re.sub(r'(\.)$','',DATABASE_NAME.match(line).group('database_name').replace(';','')\
                            .replace(' ',''))
                    
                    if ped != "":
                        data_definition_list.add((filename,ped+"_PED","PED-SUB",database,""))
                        # data_definition_list.add((filename,ped+"_PED","PED-PED(ファイル名)",filename,""))
       
                
                
    for filepath in dbsubschema_files:
        
        filename,_ = get_filenames(filepath)
        
        subschema = ""
        schema = ""
     
                
        with open(filepath, errors="ignore") as tf:
            data= []
            for i in tf:
                if i[0] !='*':
                    data.append(i[0:72])
                    
            SUBSCHEMA_NAME   = re.compile(r'^[;\s]*SUBSCHEMA(\s)*NAME(\s|(IS))*(?P<subschma_name>.*)$')
            SCHEMA_NAME      = re.compile(r'^[;\s]*SCHEMA(\s)*NAME(\s|(IS))*(?P<schema_name>.*)$')    
            SCHEMA_NAME2     = re.compile(r'^[;\s]*(?P<schema_name2>.*)$')       
            for i,line in enumerate(data):
                            
                if(SUBSCHEMA_NAME.match(line)):
                    subschema = (SUBSCHEMA_NAME.match(line).group('subschma_name'))\
                                .replace(';','').replace(' ','')
                                
                    data_definition_list.add((filename,subschema,"DBサブスキーマ-DBサブスキーマ(ファイル名)",filename,""))

                elif(SCHEMA_NAME.match(line)):
                    schema_line = SCHEMA_NAME.match(line).group('schema_name')

                    record_to_schema_list =list(filter(None,(schema_line)\
                                        .replace(';','').replace('.','').replace(' ','').split(',')))

                    if(schema_line.replace(' ','')[-1:]=="," or schema_line=='' or data[i+1].replace(' ','')[0]==","):
                        schema_line2 = SCHEMA_NAME2.match(data[i+1]).group('schema_name2')
                        add_list = list(filter(None,(schema_line2)\
                                            .replace(';','').replace('.','').replace(' ','').split(',')))
                        record_to_schema_list.extend(add_list)

                    k= i
                    while True:
                        schema_line3 = SCHEMA_NAME2.match(data[k+1]).group('schema_name2')

                        if(schema_line3.replace(' ','')[-1:]=="," or schema_line3=='' or data[k+2].replace(' ','')[0]==","):
                            schema_line4 = SCHEMA_NAME2.match(data[k+2]).group('schema_name2')

                            add_list = list(filter(None,(schema_line4)\
                                        .replace(';','').replace('.','').replace(' ','').split(',')))
                            record_to_schema_list.extend(add_list)
                            k+=1
                        else:
                            break                        
                    
                    if subschema == "":
                        continue
                    
                    for schema in record_to_schema_list:
                        data_definition_list.add((filename,subschema,"SUB-DB",schema,""))
                        
                        
                        
    dbschema_error_list = []
    for filepath in dbschema_files:
        
        filename,_ = get_filenames(filepath)
        

        schema = ""
        dataset = ""
        record = ""
        
        with open(filepath, errors="ignore") as tf:
            data= []
            for i in tf:
                if i[0] !='*':
                    data.append(i[0:72])

            """
            range_record:rangeとrecodeの対応関係を格納する辞書
            dataset_list:dataset,record毎に、情報をリスト化
            
            SCHEMA_NAME:DBスキーマ名
            RANGE_NAME:レンジ名
            RECORD_NAME:レコード名
            DATASET_NAME:データセット名
            VOLUME_NAME:ボリューム名
            RANGE_TO_DATASET:レンジ名とデータセットの関連性
            """
        
            SCHEMA_NAME   = re.compile(r'^(\s)*SCHEMA(\s)*NAME(\s|(IS))*(?P<schma_name>\w*)')
            RANGE_NAME    = re.compile(r'^(\s)*RANGE(\s)*NAME(\s|(IS))*(?P<range_name>\w*)')
            RECORD_NAME   = re.compile(r'^[;\s]*RECORD(\s)*NAME(\s|(IS))*(?P<record_name>.*)$')
            DATASET_NAME  = re.compile(r'^(\s)*DATASET(\s)*NAME(\s|(IS))*(?P<dataset_name>\w*)')
            VOLUME_NAME   = re.compile(r'^(\s)*VOLUME(\s|(IS))*(?P<volume_name>[\w]*)')
            RANGE_TO_DATASET = re.compile(r'^[;\s]*LOCATE(\s|(IS))*(?P<range_to_dataset>.*)$')          
            RANGE_TO_DATASET2 = re.compile(r'^[;\s]*(?P<range_to_dataset2>.*)$')       
            range_record_list = []             
            for i,line in enumerate(data):
                if(SCHEMA_NAME.match(line)):
                    schema = (SCHEMA_NAME.match(line).group('schma_name'))

                    data_definition_list.add((filename,schema,"DBスキーマ-DBスキーマ(ファイル名)",filename,""))
                    
                elif(RANGE_NAME.match(line)):
                    range1=(RANGE_NAME.match(line).group('range_name'))
                    for j in range(5):
                        try:
                            if(RECORD_NAME.match(data[i+j])):
                                record_line =(RECORD_NAME.match(data[i+j]).group('record_name'))
                                record_list = list(filter(None,(record_line)\
                                                .replace(';','').replace('.','').replace(' ','').split(',')))
                                for record in record_list:
                                    range_record ={}
                                    range_record["range"] = range1
                                    range_record["record"] = record
                                    range_record_list.append(range_record)
                                break
                        except:
                            dbschema_error_list.append(filename)


                elif(DATASET_NAME.match(line)):
                    dataset = (DATASET_NAME.match(line).group('dataset_name'))
                                              
                elif(VOLUME_NAME.match(line)):
                    volume = (VOLUME_NAME.match(line).group('volume_name'))
    
                elif(RANGE_TO_DATASET.match(line)):
                    locate_line =  re.sub(r'\(.*\)','',RANGE_TO_DATASET.match(line).group('range_to_dataset'))
                    record_to_dataset_list =list(filter(None,(locate_line)\
                                            .replace('.','').replace(' ','').split(',')))


                    #RANGE_TO_DATASETが二行以上に渡る際の処理
                    if(locate_line.replace(' ','')[-1:]==","):
                        locate_line2 = RANGE_TO_DATASET2.match(data[i+1]).group('range_to_dataset2')
                        add_list = list(filter(None,(locate_line2)\
                                            .replace('.','').replace(' ','').split(',')))
                        record_to_dataset_list.extend(add_list)

                        m = i
                        while True:
                            if(RANGE_TO_DATASET2.match(data[m+1]).group('range_to_dataset2').replace(' ','')[-1:]==","):
                                add_list = list(filter(None,(RANGE_TO_DATASET2.match(data[m+2]).group('range_to_dataset2'))\
                                            .replace('.','').replace(' ','').split(',')))
                                record_to_dataset_list.extend(add_list) 
                                m+=1
                            else:
                                break       
                                             
                    #データセットの情報をdataset_listに格納  
                    
                    if schema == "":
                        continue
                    
                    data_definition_list.add((filename,schema,"DB-DSN",dataset,""))
            
                    for range_info in record_to_dataset_list:              
                        for k in range_record_list:
                            if( range_info == k["range"]):                                
                                data_definition_list.add((filename,schema,"DB-RECORD",k["record"],""))
                                
                                
           
    for filepath in damschema_files:                          
        damschema = ""
        dataset = ""
        filename,_ = get_filenames(filepath)
        with open(filepath, errors="ignore") as tf:
            data= []
            for i in tf:
                if i[0] !='*':
                    data.append(i[0:72])
                
            DAMSCHEMA_NAME  = re.compile(r'^[;\s]*SCHEMA(\s)*NAME(\s|(IS))*(?P<damschema_name>.*)$')    
            DATASET_NAME    = re.compile(r'^[;\s]*DATASET(\s)*NAME(\s|(IS))*(?P<dataset_name>.*)')   
            
            for i,line in enumerate(data):
                
                if(DAMSCHEMA_NAME.match(line)):
                    damschema = (DAMSCHEMA_NAME.match(line).group('damschema_name'))\
                                .replace(';','').replace(' ','').replace('FORDS','')

                    data_definition_list.add((filename,damschema,"DAMスキーマ-DAMスキーマ(ファイル名)",filename,""))
                    

                elif(DATASET_NAME.match(line)):
                    dataset = DATASET_NAME.match(line).group('dataset_name').replace(';','')\
                            .replace('WITH','').replace('RESIDENT','').replace(' ','')
                            
                    if damschema != "":
                        data_definition_list.add((filename,damschema,"DAM-DSN",dataset,""))
                        
    
    for filepath in mcp_files:                          
        dam = ""
        dataset = ""         
        subschema = ""
        appl = ""
        subschema_to_appl = ""
        
        filename,_ = get_filenames(filepath)
        
        with open(filepath, errors="ignore") as tf:
                    data= []
                    for i in tf:
                        if i[0] !='*':
                            data.append(i[0:72])

                    APPL_NAME     = re.compile(r'^[;\s]*APPL(\s)*NAME=(\s)*(?P<appl_name>[\w\-]*)[,;\s]')
                    SUBSCHEMA_TO_APPL_NAME     = re.compile(r'^[;\s]*APPL(\s)*NAME=(\s)*(?P<appl_name>[\w\-]*)[,;\s].*DB=(\s)*(?P<subschema_name>[\w\-]*)[,\s]')
                    SUBSCHEMA_NAME   = re.compile(r'^[;\s]*DB(\s)*NAME=(\s)*(?P<subschema_name>[\w\-]*)[,;\s]')
                    DAMSCHEMA_NAME   = re.compile(r'^[;\s]*ADS(\s)*SCHEMA=(\s)*(?P<damschma_name>[\w\-]*)[,\s]') 
                    DATASET_NAME     = re.compile(r'^[;\s]*ODS(\s)*DSNAME=(\s)*(?P<dataset_name>[\w\-\.]*)[,;\s]')  

                    for i,line in enumerate(data):
                        
                        if(SUBSCHEMA_NAME.match(line)):
                            subschema = re.sub(r'(\.)$','',(SUBSCHEMA_NAME.match(line).group('subschema_name'))\
                                        .replace(';','').replace(' ',''))
                            
                            data_definition_list.add((filename,filename,"MCP-SUB",subschema,""))

                        elif(DAMSCHEMA_NAME.match(line)):
                            dam = re.sub(r'(\.)$','',DAMSCHEMA_NAME.match(line).group('damschma_name').replace(';','')\
                                    .replace(' ',''))
                            data_definition_list.add((filename,filename,"MCP-DAM",dam,""))

                        elif(DATASET_NAME.match(line)):
                            dataset = re.sub(r'(\.)$','',DATASET_NAME.match(line).group('dataset_name').replace(';','')\
                                    .replace(' ',''))
                            data_definition_list.add((filename,filename,"MCP-DSN",dataset,""))


                        elif(APPL_NAME.match(line)):
                            appl = re.sub(r'(\.)$','',APPL_NAME.match(line).group('appl_name').replace(';','')\
                                    .replace(' ',''))
                            # if(SUBSCHEMA_TO_APPL_NAME.match(line)):
                            #     subschema_to_appl = re.sub(r'(\.)$','',SUBSCHEMA_TO_APPL_NAME.match(line).group('subschema_name').replace(';','')\
                            #                         .replace(' ',''))
                            #     self.dataset_dic_MCP(filename,appl,subschema_to_appl,"×","×","×")
                            # else:
                            #     self.dataset_dic_MCP(filename,appl,"×","×","×","×")

    endline = " "*69
    
    for filepath in jcl_files:        
        filename,_ = get_filenames(filepath)                  

        pedname = ""
        ped1name = ""
        ped2name = ""
        ped3name = ""
        aimped = ""
        
        ped_list = []
        ped1_list = []
        ped2_list = []
        ped3_list = []
        
        if filename in jcl_to_internal_proc_dic:
            internal_proc_name = filename + "%" + jcl_to_internal_proc_dic[filename]
            
            if internal_proc_name in proc_variable_dic:
                for dic,nsource in proc_variable_dic[internal_proc_name]:
                    if "PED" in dic:
                        s = dic["PED"]
                        ped_list.append(s)
                    if "PED1" in dic:
                        s = dic["PED1"]
                        ped1_list.append(s)
                    if "PED2" in dic:
                        s = dic["PED2"]
                        ped2_list.append(s)
                    if "PED3" in dic:
                        s = dic["PED3"]
                        ped3_list.append(s)
                    
            # if (internal_proc_name,"PED") in proc_variable_dic:
            #     for s,nsource in proc_variable_dic[(internal_proc_name,"PED")]: 
            #         ped_list.append(s)

                    
            # if (internal_proc_name,"PED1") in proc_variable_dic:
            #     for s,nsource in proc_variable_dic[(internal_proc_name,"PED1")]: 
            #         ped1_list.append(s)

                    
            # if (internal_proc_name,"PED2") in proc_variable_dic:
            #     for s,nsource in proc_variable_dic[(internal_proc_name,"PED2")]: 
            #         ped2_list.append(s)
                    
            # if (internal_proc_name,"PED3") in proc_variable_dic:
            #     for s,nsource in proc_variable_dic[(internal_proc_name,"PED3")]: 
            #         ped3_list.append(s)

        end_flag = False
        language_type = "JCL"
        with open(filepath, errors="ignore") as tf:
            # data= []
            # for i in tf:
            #     if (i[0:3] !='//*'):
            #         if i[3:72] == endline:
            #             break
            #         data.append(i[0:72])
            data= []
            for line in tf:
                if comment_line_check(string=line, language_type=language_type) == -1:
                    continue
                if end_flag:
                    if end_line_check(string=line,language_type=language_type) == 2:
                        end_flag = False
                        
                if end_line_check(string=line,language_type=language_type) == -1:
                    end_flag = True
                
                if end_flag:
                    continue
                
                data.append(line[0:72])

            PED_NAME         = re.compile(r'.*[\s,]PED=(?P<ped_name>[\w_\-\.]*[,\s])')
            PED1_NAME        = re.compile(r'.*[\s,]PED1=(?P<ped1_name>[\w_\-\.]*[,\s])')  
            PED2_NAME        = re.compile(r'.*[\s,]PED2=(?P<ped2_name>[\w_\-\.]*[,\s])')    
            PED3_NAME        = re.compile(r'.*[\s,]PED3=(?P<ped3_name>[\w_\-\.]*[,\s])') 
            AIMPED_NAME      = re.compile(r'^//AIMPED(\s)*DD.*SUBSYS(\s)*=(\s)*(?P<aimped_name>.*)$')    
            for i,line in enumerate(data):
                
                if(PED_NAME.match(line)):
                    pedname = (PED_NAME.match(line).group('ped_name'))\
                                .replace(';','').replace(' ','').replace(',','')

                if(PED1_NAME.match(line)):
                    ped1name = (PED1_NAME.match(line).group('ped1_name'))\
                                .replace(';','').replace(' ','').replace(',','')

                if(PED2_NAME.match(line)):
                    ped2name = (PED2_NAME.match(line).group('ped2_name'))\
                                .replace(';','').replace(' ','').replace(',','')

                if(PED3_NAME.match(line)):
                    ped3name = (PED3_NAME.match(line).group('ped3_name'))\
                                .replace(';','').replace(' ','').replace(',','')


                if(AIMPED_NAME.match(line)):
                    aim_list = []
                    aimped = (AIMPED_NAME.match(line).group('aimped_name'))\
                                .split(',')[1].replace(' ','').replace(')','')
                    find = False
                    if(aimped=="&PED"):
                        if pedname!='':
                            aimped = pedname
                            find = True
                        else:
                            for s in ped_list:
                                aim_list.append(s)
                            
                                
                    elif aimped=="&PED1":
                        if ped1name!='':
                            aimped = ped1name
                            find = True
                        else:
                            for s in ped1_list:
                                aim_list.append(s)
                    elif aimped=="&PED2":
                        if ped2name!='':
                            aimped = ped2name
                            find = True    
                        else:
                            for s in ped2_list:
                                aim_list.append(s)
                                
                    elif aimped=="&PED3":
                        if ped3name!='':
                            aimped = ped3name
                            find = True
                        else:
                            for s in ped3_list:
                                aim_list.append(s)
                                
                    elif aimped != "":
                        find = True
                        
                    if find == True:
                        data_definition_list.add((filename,filename,"JCL-PED",aimped+"_PED",""))  
                    else:
                        if len(aim_list) == 0:
                            # data_definition_list.add((filename,filename,"JCL-PED",aimped+"_PED","JCL変数不明")) 
                            need_search_and_check_list.add((filename,filename,"JCL-PED",aimped+"_PED","JCL変数不明")) 
                            
                    for aimped in aim_list:
                        data_definition_list.add((filename,filename,"JCL-PED",aimped+"_PED","内部PROC")) 
                            
                        
                        
    for filepath in proc_files:                          
        filename,_ = get_filenames(filepath)
        if filename not in has_relation_proc_set:
            continue
        pedname = ""
        ped1name = ""
        ped2name = ""
        ped3name = ""
        aimped = ""
        
        ped_list = []
        ped1_list = []
        ped2_list = []
        ped3_list = []
        
        if filename in proc_variable_dic:
            for dic,nsource in proc_variable_dic[filename]:
                if "PED" in dic:
                    s = dic["PED"]
                    ped_list.append([s,nsource])
                if "PED1" in dic:
                    s = dic["PED1"]
                    ped1_list.append([s,nsource])
                if "PED2" in dic:
                    s = dic["PED2"]
                    ped2_list.append([s,nsource])
                if "PED3" in dic:
                    s = dic["PED3"]
                    ped3_list.append([s,nsource])
                    
        if ped_list == [] and (filename,"PED") in proc_parm_dic:
            for s in proc_parm_dic[(filename,"PED")]: 
                ped_list.append([s,filename])
                
        if ped1_list == [] and (filename,"PED1") in proc_parm_dic:
            for s in proc_parm_dic[(filename,"PED1")]: 
                ped1_list.append([s,filename])
        
        if ped2_list == [] and (filename,"PED2") in proc_parm_dic:
            for s in proc_parm_dic[(filename,"PED2")]: 
                ped2_list.append([s,filename])
                
        if ped3_list == [] and (filename,"PED3") in proc_parm_dic:
            for s in proc_parm_dic[(filename,"PED3")]: 
                ped3_list.append([s,filename])
                    
                
        end_flag = False
        language_type = "PROC"
        with open(filepath, errors="ignore") as tf:
            # data= []
            # for i in tf:
            #     if (i[0:3] !='//*'):
            #         if i[3:72] == endline:
            #             break
            #         data.append(i[0:72])
            data= []
            for line in tf:
                if comment_line_check(string=line, language_type=language_type) == -1:
                    continue
                if end_flag:
                    if end_line_check(string=line,language_type=language_type) == 2:
                        end_flag = False
                        
                if end_line_check(string=line,language_type=language_type) == -1:
                    end_flag = True
                
                if end_flag:
                    continue
                
                data.append(line[0:72])

            PED_NAME         = re.compile(r'.*[\s,]PED=(?P<ped_name>[\w_\-\.]*[,\s])')
            PED1_NAME        = re.compile(r'.*[\s,]PED1=(?P<ped1_name>[\w_\-\.]*[,\s])')  
            PED2_NAME        = re.compile(r'.*[\s,]PED2=(?P<ped2_name>[\w_\-\.]*[,\s])')    
            PED3_NAME        = re.compile(r'.*[\s,]PED3=(?P<ped3_name>[\w_\-\.]*[,\s])') 
            AIMPED_NAME      = re.compile(r'^//AIMPED(\s)*DD.*SUBSYS(\s)*=(\s)*(?P<aimped_name>.*)$')    
            for i,line in enumerate(data):
                
                if(PED_NAME.match(line)):
                    pedname = (PED_NAME.match(line).group('ped_name'))\
                                .replace(';','').replace(' ','').replace(',','')

                if(PED1_NAME.match(line)):
                    ped1name = (PED1_NAME.match(line).group('ped1_name'))\
                                .replace(';','').replace(' ','').replace(',','')

                if(PED2_NAME.match(line)):
                    ped2name = (PED2_NAME.match(line).group('ped2_name'))\
                                .replace(';','').replace(' ','').replace(',','')

                if(PED3_NAME.match(line)):
                    ped3name = (PED3_NAME.match(line).group('ped3_name'))\
                                .replace(';','').replace(' ','').replace(',','')


                if(AIMPED_NAME.match(line)):
                    aim_list = []
                    aimped = (AIMPED_NAME.match(line).group('aimped_name'))\
                                .split(',')[1].replace(' ','').replace(')','')
                    find = False
                    if(aimped=="&PED"):
                        if pedname!='':
                            aimped = pedname
                            find = True
                        else:
                            for s in ped_list:
                                aim_list.append(s)
                            
                                
                    elif aimped=="&PED1":
                        if ped1name!='':
                            aimped = ped1name
                            find = True
                        else:
                            for s in ped1_list:
                                aim_list.append(s)
                    elif aimped=="&PED2":
                        if ped2name!='':
                            aimped = ped2name
                            find = True    
                        else:
                            for s in ped2_list:
                                aim_list.append(s)
                                
                    elif aimped=="&PED3":
                        if ped3name!='':
                            aimped = ped3name
                            find = True
                        else:
                            for s in ped3_list:
                                aim_list.append(s)
                                
                    elif aimped != "":
                        find = True
                        
                    if find == True:
                        data_definition_list.add((filename,filename,"JCL-PED",aimped+"_PED",""))  
                    else:
                        if len(aim_list) == 0:
                            # data_definition_list.add((filename,filename,"JCL-PED",aimped+"_PED","PROC引数不明")) 
                            need_search_and_check_list.add((filename,filename,"JCL-PED",aimped+"_PED","PROC引数不明")) 
                        for aimped,sourcename in aim_list:
                            data_definition_list.add((sourcename,sourcename,"JCL-PED-変数",aimped+"_PED","PROC引数: " + filename)) 
                            
                        

    print("DAM_ERRORLIST: " + str(dbschema_error_list))
    
    return data_definition_list


def make_acsapi_acsext_list(cobol_files,ped_files,mqn_files):
    
    acsapi_acsext_list = set()
    acsapi_switch_list = set()

    mqn_to_ap_dic = {}

    ### make MQN to AP dictionary
    ### ex)   AP   NAME               IS  UPWEB                ;                     00041600
    ###       I-O    ERROR      IS  REJECT.                                     00042000
    ###     MQN NAME   IS  CYQ14   FOR  MQWEBIN.                                  00042100
    
    ### if source code is like ex,
    ### in this case, AP=UPWEB and MQN=CYQ14 and make dictionary CYQ14:[UPWEB]
    for filepath in ped_files:

        ap = ""
        mqn = ""
        AP_NAME      = re.compile(r'^.*AP(\s)*NAME(\s|(IS))*(?P<ap_name>.*)\s*.*')        
        MQN_NAME  = re.compile(r'^.*MQN(\s)*NAME(\s|(IS))*(?P<mqn_name>\w*)')    
            
        with open(filepath, errors="ignore") as tf:
            data= []
            for i in tf:
                if i[0] !='*':
                    data.append(i[0:72])
            
            data1 = re.split(';|\\.\s', ' '.join(data))
             
            for line in data1:
                if(AP_NAME.match(line)):
                    slist = re.split("[; .,\'\"]",line[line.find(" IS "):])
                    for s in slist[1:]:
                        if s == " " or s == "" or s == "\n" or s == "IS":
                            continue
                        
                        ap = s
                        break

                elif(MQN_NAME.match(line)):
                    slist = re.split("[; .,\'\"]",line[line.find(" IS "):])
      
                    for s in slist[1:]:
                        if s == " " or s == "" or s == "\n" or s == "IS":
                            continue
                        
                        mqn = s
                        break
                    
                    if ap == "":
                        continue
                    
                    if mqn not in mqn_to_ap_dic:
                        mqn_to_ap_dic[mqn] = set()
                        
                    mqn_to_ap_dic[mqn].add(ap)
   
    smqn_to_mqn_dic = {}

    ### make SMQN to MQN dictionary
    ### ex)     MQN NAME IS CYQ14          BELONGS TO CY00PC01                        00000400
    ###         DD NAME IS MQWEBOUT OUTPUT                                            00001400
    ###          ;    OPTION-CODE IS   W C D F                                          00001500
    ###          .                                                                     00001600
    ###          SMQN NAME IS CYSMQ14                                                  00001700
    
    ### if source code is like ex,
    ### in this case, SMQN=CYSMQ14 and MQN=CYQ14 and make dictionary CYSMQ14:[CYQ14]
    for filepath in mqn_files:
        
        smqn = ""
        mqn = ""

        SMQN_NAME      = re.compile(r'^.*SMQN(\s)*NAME(\s|(IS))*(?P<smqn_name>.*)\s*.*')        
        MQN_NAME  = re.compile(r'^.*MQN(\s)*NAME(\s|(IS))*(?P<mqn_name>\w*)') 
        with open(filepath, errors="ignore") as tf:
            data= []
            for i in tf:
                if i[0] !='*':
                    data.append(i[0:72])
            
            data1 = re.split(';|\\.\s', ' '.join(data))
            
            for line in data1:
                if len(line) > 0:
                
                    if line[0] == "*":
                        continue
                   
                    ### if, firstly check MQN_NAME by regular expression, SMQN_NAME pattern also match and can't get SMQN=xxxx
                    ### so, firstly check SMQN_NAME
                    if(SMQN_NAME.match(line)):
                        slist = re.split("[; .,\'\"]",line[line.find(" IS "):])
                        for s in slist[1:]:
                            if s == " " or s == "" or s == "\n" or s == "IS":
                                continue
                            
                            smqn = s
                            break
                        
                        if mqn == "":
                            continue
                        
                        if smqn not in smqn_to_mqn_dic:
                            smqn_to_mqn_dic[smqn] = set()
                            
                        smqn_to_mqn_dic[smqn].add(mqn)
                        
                    elif(MQN_NAME.match(line)):
                        slist = re.split("[; .,\'\"]",line[line.find(" IS "):])
                   
                        for s in slist[1:]:
                            if s == " " or s == "" or s == "\n" or s == "IS":
                                continue
                            
                            mqn = s
                            break
                        
                
    ### in ACSAPI-ACSEXT, 
    ### if source code is like ex) 053000     CALL  'ACSAPI'  USING  ACSEXT  ASYNC-DCOM  OUT-MSG.   
    ### CALL 'ACSAPI' or CALL 'XPAPI' and [USING ACSEXT], then most of the case, get the value after ACSEXT, in this case ASYNC-DCOM
    ### and ASYNC-DCOM is variable, so check after     
    cobol_call_grep_list = grep_and_make_list_cobol(files=cobol_files,keywords=[" ACSEXT "],type="ACSAPI-ACSEXT",returnpath=True)
    
    ### in CALL-VARIABLE-ACSAPI-ACSEXT,
    ### if source code is like ex) 052800     MOVE  'CYSMQ14 '           TO  SNAME     OF ASYNC-DCOM.      
    ### in this case, get CYSMQ14 and this is SMQN
    ### so search, 1 SMQN to MQN dictionary -> 2 MQN to AP dictionary and make relation of source code -> AP
    for file, member in cobol_call_grep_list:
        find = False
        file_name,name = get_filenames(file)
        sub = get_cobol_group_info(file)
 
        with open(file) as f:
            for line in f:
                if member not in line:
                    continue
                get_val = take_data_from_string(line,"CALL-VARIABLE-ACSAPI-ACSEXT",member)
                if get_val == -1:
                    continue
                find = True
                if get_val not in smqn_to_mqn_dic:
                    need_search_and_check_list.add((file_name,name,"ACSAPI_ACSEXT-変数不明-SMQN",get_val,"変数調査対象: "+member+"→"+get_val+sub))
                    continue
                
                for mqn in smqn_to_mqn_dic[get_val]:
                    if mqn not in mqn_to_ap_dic:
                        need_search_and_check_list.add((file_name,name,"ACSAPI_ACSEXT-変数不明-MQN","変数調査対象: "+mqn,member+"→"+get_val+"→"+mqn+sub))
                        continue
                    for ap in mqn_to_ap_dic[mqn]:
                        acsapi_acsext_list.add((file_name,name,"ACSAPI_ACSEXT",ap,member+"→"+get_val+"→"+mqn+"→"+ap+sub))
                        
        if find == False:
            need_search_and_check_list.add((file_name,name,"ACSAPI_ACSEXT-変数不明",member,"変数調査対象"+sub))



    for filepath in cobol_files:
        variable_list = set()
        variable_variable_list = set()
        file_name,name = get_filenames(filepath)
        sub = get_cobol_group_info(filepath)
        with open(filepath, errors="ignore") as tf:
            data= []
            for i in tf:
                if comment_line_check(i,"COBOL") == -1:
                    continue
                data.append(i[6:72])
                
        data1 = re.split(';|\\.\s|\*', ' '.join(data))

        switch_cand = set(["SWITCH"])
        for line in data1:
            if "SWITCH" in line:
                get_val = take_data_from_string(line,"DEFINE-SWITCH")
                
                if get_val != -1:
                    switch_cand.add(get_val)

        for line in data1:
            for cand in switch_cand:
                if cand not in line:
                    continue 

                member = take_data_from_string(line,"ACSAPI-SWITCH",switch_cand)
                    
                if member != -1:
                    
                    variable_list.add(member)
                        
        with open(filepath, errors="ignore") as tf:     
            for member in variable_list:
                find = False
                lastline = ""
                for i in tf:
                    if comment_line_check(i,"COBOL") == -1:
                        continue
                    
                    line = i[6:72]
                    
                    get_val,val_flag = take_data_from_string(line,"CALL-VARIABLE-ACSAPI-SWITCH",member+sub)
                    if get_val == -1:
                        get_val,val_flag = take_data_from_string(lastline+" "+line,"CALL-VARIABLE-ACSAPI-SWITCH",member+sub)
                        
                        if get_val == -1:
                            lastline = line
                            continue

                    find = True
                    if val_flag == 1:
                        acsapi_switch_list.add((file_name,name,"ACSAPI_SWITCH",get_val,sub))
                    else:
                        variable_variable_list.add(get_val)
                        
                    lastline = line
                        
                if find == False:
                    need_search_and_check_list.add((file_name,name,"ACSAPI_SWITCH-変数不明",member,"個別調査対象"+sub))
                    
            
            for member in variable_variable_list:
                
                find = False
                for i in tf:
                    if comment_line_check(i,"COBOL") == -1:
                        continue
                    
                    line = i[6:72]

                    if member not in line:
                        continue
                    get_val = take_data_from_string(line,"CALL-VARIABLE",member)
                    if get_val == -1:
                        continue
                    find = True
                    acsapi_switch_list.add((file_name,name,"ACSAPI_SWITCH",get_val,"変数-変数: "+member+sub))

                        
                if find == False:
                    need_search_and_check_list.add((file_name,name,"ACSAPI_SWITCH-変数-変数不明",member,"個別調査対象"+sub))
 
      

    return acsapi_acsext_list,acsapi_switch_list

