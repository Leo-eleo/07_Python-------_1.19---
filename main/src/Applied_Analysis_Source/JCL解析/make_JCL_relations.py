#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import re
import sys

import pandas as pd

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

## priority list
priority_list = ["", "NKN.PROCLIB", "NKNB.PROCLIB", "PROC_ANP.XDM.JCL", "PROC_USRA.PROCLIB", "BEST.PROCLIB", "SYS1.USERPROC", "SYS1.OSPROC", "カタプロ", "VOS.PLIB", "VOS.DSPLIB", "SYSOPN.PROCLIB","SYSJOB.PROCLIB","SYSSTC.PROCLIB","SYS1.PROCLIB","SYS2.PROCLIB","PP1.PROCLIB", "AIM1.PROCLIB", "JS.SYSJOBS", "JS.JCLIB", "JS.FXIPF.PROCLIB", "JS.TESTJCL", "D", "HULFT.FTPM.JCL", "J", "JS.AIM.SYMFOSRC", "JS.SP.JCL", "OWFT.FTPM.JCL", "P", "TSO.TEST.PROCLIB"] 


proc_variable_dic2 = {}

def no_matched_member(member_name):
    return str(member_name)+"_未受領PROC"


def check_priority_number(library_name):
    """return priority of library number

    Args:
        library_name [string]: Library name like  "NKN.PROCLIB", "NKNB.PROCLIB", "PROC_ANP.XDM.JCL", "PROC_USRA.PROCLIB", "BEST.PROCLIB", "SYS1.USERPROC", "SYS1.OSPROC", "カタプロ", "VOS.PLIB", "VOS.DSPLIB", "SYSOPN.PROCLIB","SYSJOB.PROCLIB","SYSSTC.PROCLIB","SYS1.PROCLIB","SYS2.PROCLIB","PP1.PROCLIB", "AIM1.PROCLIB", "JS.SYSJOBS", "JS.JCLIB", "JS.FXIPF.PROCLIB", "JS.TESTJCL", "D", "HULFT.FTPM.JCL", "J", "JS.AIM.SYMFOSRC", "JS.SP.JCL", "OWFT.FTPM.JCL", "P", "TSO.TEST.PROCLIB"

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
    return string




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

def take_data_from_key_val(key,value,type):
    
    key = str(key)
    value = str(value)
    
    ### in jcl step information PARM_VAR_LIST and PARM_VALUE_LIST
    ### if the two string like
    ### PARM REGION
    ### R1H2 1024K
    ### then matched index of PARM value is returned, in this case R1H2 
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
    
### Check the internal proc and make dictionary
def update_internal_proc_list(internal_proc_list):
    
    for jcl_name,member in zip(internal_proc_list["JCL名"],internal_proc_list["PROC_ID"]):
        jcl_name = take_extensions(jcl_name)
        member = str(member).replace("\\","$")
        internal_proc_dic[(jcl_name,member)] = 1
        jcl_to_internal_proc_dic[jcl_name] = member
        
jobproc_info = {}
### Check the jobproc order and make dictionary of orders
### format is list of [sisan_id, library_name]
def update_jobproc_list(jobproc_list):
    
    ### make dictionary
    for jcl_name,parm,gyo in zip(jobproc_list["資産ID"],jobproc_list["PARM"],jobproc_list["元資産行情報"]):
        jcl_name = take_extensions(jcl_name)
        
        parm = take_data_from_jcl_analysis_result(parm,"JOBPROC")
        if parm == -1 or parm == "":
            continue
        
        parm = parm.replace("\\","$")
        if jcl_name not in jobproc_dic:
            jobproc_dic[jcl_name] = []
        if jcl_name not in jobproc_info:
            jobproc_info[jcl_name] = gyo-1

        ### JOBPROC の命令は基本的に先の行に書いてある情報の優先度が高いため、順番にlistに追加する。
        ### Todo STEPが変わって、再度JOBPROCが宣言されると、優先度が変わると考えられるが、こちらは未対応。JCLの言語解析自体の改修も必要
        jobproc_dic[jcl_name].append(parm)
        jobproc_info[jcl_name] = gyo
            

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
            
        if classification == "カタプロ":
            update_catapro_dic([module,library,unit]) 
        
        if classification == "JCL":
            update_jcl_dic([module,asset],valid)
            
        if classification == "Easyパラメタ":
            update_easy_dic([module,asset])
   

def update_member_list2(df):
    
    for asset,classification in zip(df["ファイル名"],df["格納フォルダ"]):
        asset = take_extensions(asset)
        library,unit,module = asset.split("%")
        unit = "#" + unit
        valid = "○"
        
        if asset in asset_dic and asset_dic[asset] == classification:
            continue
        if asset not in asset_dic:
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
    

def update_proc_variable_dic2(jcl_name,proc_name,keys,values):
    proc_name = update_proc_library(jcl_name,proc_name)

    dic = {key:value for key,value in zip(keys,values)}
    if proc_name not in proc_variable_dic2:
        proc_variable_dic2[proc_name] = []
    proc_variable_dic2[proc_name].append((dic,jcl_name))

   
def update_proc_library(jcl_name,proc_name):
    
    proc_name = clean_proc_name(proc_name)
    
    sisan_id = jcl_name
    member_id = proc_name 
    
    unit_index = sisan_id.index("%")+1 ### sisan_id format is libraryname%unit%xxxxxx and take the index of unit
    unit = sisan_id[unit_index]
    
    ### the number 20 don't have any mean, just as the enough big number
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
    if matching_number < 20:
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


def update_step_info(df_step_info,has_relation_proc_set):

    ### jcl_proc or proc_proc candidate is PROC_NAME is not blank
    df_proc = df_step_info.dropna(subset=["PROC_NAME"])
    
    for jcl_name,proc_name,param_key,param_val in zip(df_proc["JCL_NAME"],df_proc["PROC_NAME"],df_proc["PARM_VAR_LIST"],df_proc["PARM_VALUE_LIST"]):
        jcl_name = take_extensions(jcl_name)
        
        keys,values = take_data_from_key_val(param_key,param_val,"PROC-PGM-VARIABLE")
        update_proc_variable_dic2(jcl_name,proc_name,keys,values)
    
    for jcl_name,proc_name in zip(df_proc["JCL_NAME"],df_proc["PROC_NAME"]):
        jcl_name = take_extensions(jcl_name)
            
        classification = return_asset_classification(jcl_name)
        
        ### this is the error case of jcl analysis tool 
        if proc_name in ["REGION","T","TIME","COND","PARM"]:
            continue
        
        proc_name = update_proc_library(jcl_name,proc_name)
        
        if classification == "JCL":
  
            has_relation_proc_set.add(proc_name)

    
    return has_relation_proc_set

  

            

def get_variable2(jcl_name,pgm_name):
    
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
                print("この変数定義は文法的に誤りの可能性が高いです。",pgm_name,jcl_name)
            
        else:
            last += pgm_name[i]
        i += 1
    if last:
        val_list.append(last)

    # cand_string = [["","",0]]
    ans_list = set()
    vals = []
    for v in val_list:
        if "&" in v:
            vals.append(v.replace("&",""))
            
    find = 0
    if jcl_name in proc_variable_dic2:
        for dic,source in proc_variable_dic2[jcl_name]:
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
    
    return [(pgm_name,jcl_name+" 変数調査対象")]
                
    
#################################################################################################################



