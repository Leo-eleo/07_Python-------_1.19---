#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

df_base = pd.read_excel("C:\\Users\\kohei.mori\\Downloads\\KAOSS一覧.xlsx")
api_dic = {}
for api,code in zip(df_base["API"],df_base["機能コード"]):
    if code == "ー":
        code = ""
    api_dic[(api,code)] = [0,0,0,0,0]
    
for key,val in api_dic.items():
    print(key,val)
    
    
    
# excel_path = "C:\\Users\\kohei.mori\\JFE\\起点資産関連性調査\\起点資産ツール用.xlsx"

# df_sheet_all = pd.read_excel(excel_path, sheet_name=None)
# df_sheet_list = df_sheet_all.keys()


# members_dic = {}
# members_dic2 = {}
# key_dic = {}

# no_need_members_dic = {}
# no_need_key_dic = {}

# members_dic_jcl = {}
# key_dic_jcl = {}
# jcl_dic = {}

# asset_index_dic = {}
# all_module_set = set()
# all_asset_set = set()

# ### get the list of members
# sheet_members = df_sheet_all["settings"]["メンバ一覧"]
# for sheet in sheet_members:
#     if sheet not in df_sheet_list:
#         continue
    
#     df = df_sheet_all[sheet]

#     for asset,module, library, unit, classification, valid, gr1_a,gr1_b,gr1_c,gr2,gr3,gr4,gr5,gr6,gr7 in zip(df["KEY2"],df["モジュールID"],df["ライブラリ"],df["ソース管理号機"],df["資産分類(ACN)"], df["JSI資産有効判定"], df["Gr1(形鋼)"],df["Gr1(基盤)"],df["Gr1(その他)"],df["Gr2"],df["Gr3"],df["Gr4"],df["Gr5"],df["Gr6"],df["Gr7"]):
            
#             asset = take_extensions(asset)
#             all_asset_set.add(asset)
#             all_module_set.add(module)
#             gr = [""]*9
#             for i,g in enumerate([gr1_a,gr1_b,gr1_c,gr2,gr3,gr4,gr5,gr6,gr7]):
#                 if g == "○":
#                     gr[i] = "○"
#             key_dic[asset] = gr
                
 
all_sheet = []
df_all = pd.read_excel("C:\\Users\\kohei.mori\\JFE\関連性調査\\KAOSS_一覧_更新版.xlsx",sheet_name=None)
df_sheet_list = df_all.keys()
sheet_names = []

for sheet_name in df_sheet_list:
    df = df_all[sheet_name]
    df.fillna("",inplace=True)
    sheet_names.append(sheet_name)
    
    l_new = []
    for i in range(len(df)):
        data = df.iloc[i].to_list()
        
        l_new.append(data)
    for i in range(len(l_new)):
        name = l_new[i][2]
        gr = l_new[i][7:]
        par = (l_new[i][0],l_new[i][1])
        gr1 = gr[0]

        gr2 = gr[1]
                
        adds = [gr1,gr2] + gr[:6]
        l_new[i] += adds
        
        if par in api_dic:
            if gr1 == "○":
                api_dic[par][0] += 1
            if gr2 == "○":
                api_dic[par][1] += 1
            for j in range(5,8):
                if gr[j] == "○":
                    api_dic[par][j-3] += 1
        
        
    all_sheet.append(l_new)    
    
    
summary = []
for key,val in api_dic.items():
    l = [key[0],key[1]] + val
    summary.append(l)
    
summary.sort()

title = "C:\\Users\\kohei.mori\\JFE\\関連性調査"
output_header = ["API","機能コード","Gr1","Gr2-4","Gr2","Gr3","Gr4"]
write_excel_multi_sheet("KAOSS_一覧_summary.xlsx",summary,"summary",title,output_header)
exit()
def write_excel_multi_sheet3(filename,df_list,sheet_name_list,path,output_header=output_header):
    writer = pd.ExcelWriter(path+"/"+filename,engine='xlsxwriter')
    
    df_list_all = []
    sheet_name_list_all = []
    for list,sheet_name in zip(df_list,sheet_name_list):
        M = len(list)
        for i in range(M//1000000+1):
            df_list_all.append(list[i*1000000:min(M,(i+1)*1000000)])
            if i == 0:
                sheet_name_list_all.append(sheet_name)
            else:
                sheet_name_list_all.append(sheet_name +"_" + str(i+1))
     
    for list,sheet_name in zip(df_list_all,sheet_name_list_all):
        df = pd.DataFrame(list,columns=output_header)
        df.to_excel(writer, sheet_name=sheet_name,index=False)
        
    writer.save()
    writer.close()
    
title = "C:\\Users\\kohei.mori\\JFE\\関連性調査"
output_header = ["API","機能コード","資産ID","COBOL_ID","該当命令","変数ケース_変数","変数ケース_変数定義","Gr1","Gr2-4","Gr1(形鋼)","Gr1(基盤))","Gr1(その他)","Gr2","Gr3","Gr4"]
write_excel_multi_sheet3("KAOSS_一覧_new.xlsx",all_sheet,sheet_names,title,output_header)

exit()

               
# conn = connect_accdb("C:\\Users\\kohei.mori\\JFE\関連性調査\\言語解析DB_V1.29.00.accdb")
# sql = "SELECT * FROM ①JCL_CMD情報"

# df = pd.read_sql(sql,conn)
# l_new = []
# for i in range(len(df)):
#     data = df.iloc[i]
#     parm = data["PARM"]
#     if "UPBOMSG" not in parm and "UPBOCLR" not in parm:
#         continue
#     if "EXEC" not in parm:
#         continue
    
#     jcl = data["資産ID"]
#     jcl = take_extensions(jcl)
#     module = jcl.split("%")[-1]
#     code = "UPBOMSG" if "UPBOMSG" in parm else "UPBOCLR"
#     l_new.append([code,"",jcl,module,parm])


    
# df = pd.read_excel("C:\\Users\\kohei.mori\\JFE\関連性調査\\KAOSS_一覧_変数3.xlsx")
# upd_dic = {}
# for i in range(len(df)):
#     data = df.iloc[i]
#     # if data["該当命令"] != "○":
#     #     continue
#     # if "CALL" in data["マッチ"]:
#     #     continue
#     datal = data.tolist()
#     upd_dic[(datal[0],datal[2],datal[3])] = [datal[1],datal[4]]    

# df = pd.read_excel("C:\\Users\\kohei.mori\\JFE\関連性調査\\KAOSS_一覧2.xlsx")
# print(len(df))
# l_new = []
# for i in range(len(df)):
#     data = df.iloc[i]
#     datal = data.tolist()
#     datal.append("")
#     a,b,c = datal[0],datal[2],datal[5]
#     if (a,b,c) in upd_dic:
#         datal[1],datal[6] = upd_dic[(a,b,c)]
        
#     l_new.append(datal)
title = "C:\\Users\\kohei.mori\\JFE\\関連性調査"
output_header = ["API","機能コード","資産ID","COBOL_ID","該当命令"]
write_excel_multi_sheet("KAOSS_一覧_JCL.xlsx",l_new,"KAOSS_一覧",title,output_header)
exit()
    

base = "C:\\Users\\kohei.mori\\JFE\\資産一覧\\COBOL"
val_set = set()
for api,source,val in zip(df["API"],df["資産ID"],df["変数"]):
    print(api,source,val)
    val_set.add((api,source,val))
lis = []
import re

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

# for api,source,val in val_set:
    
#     path = base + "\\" + source + ".txt"
#     # print(path)
#     with open(path) as tf:
#         data= []
#         for i in tf:
#             if comment_line_check(i,"COBOL") == -1:
#                 continue
#             data.append(i[6:72])
                
#     data1 = re.split(';|\\.\s|\*', ' '.join(data))
    
#     for line in data1:
#         if val in line:
#             lis.append([api,source,val,line])

for api,source,val in val_set:
    # print(api,source,val)
    path = base + "\\" + source + ".txt"
    # print(path)
    find = 0
    data= []
    with open(path) as tf:
       
        for i in tf:
            if comment_line_check(i,"COBOL") == -1:
                continue
            data.append(i[6:72])
    data1 = re.split(';|\\.\s|\*', ' '.join(data)) 
    for i in data:
        for code in api_dic[api]:
            if code in i:
                y = "○" if val in i else ""
                lis.append([api,code,source,val,y,i])
                find = 1
    if find == 0:
        lis.append([api,"",source,val,"",i])
            
title = "C:\\Users\\kohei.mori\\JFE\\関連性調査"

output_header = ["API","機能コード","資産ID","変数","該当命令","マッチ"]
write_excel_multi_sheet("KAOSS_一覧_変数3.xlsx",lis,"KAOSS_一覧",title,output_header)
