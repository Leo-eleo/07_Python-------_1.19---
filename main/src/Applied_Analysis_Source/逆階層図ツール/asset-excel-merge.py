# ========================================================================
# TOOL-NAME : 資産関連性調査結果 マージツール
# 使用方法   :
# ========================================================================

import pandas as pd
import os,sys
from typing import Callable
from pandas import DataFrame
from pathlib import Path
from datetime import datetime


def get_file_path(target:str):
    """
    logファイルのパスを返す
    """
    return os.path.join(os.path.dirname(__file__),target + '.txt')

def init_file():
    """
    ファイルを初期化する。
    """
    if os.path.exists(get_file_path('log')):
        os.remove(get_file_path('log'))
    
    if os.path.exists(get_file_path('output')):
        os.remove(get_file_path('output'))
    

def msg_print(msg:str,write_file:bool):
    """
    Logを出力する。
    """
    log_msg:str=f'{datetime.now().strftime("%H:%M:%S")} : {msg}'
    print(log_msg)
    if write_file:
        with open(get_file_path('log'),'a',encoding='UTF-8') as writer:
            writer.write(log_msg + '\n')
    

def read_setting(): 
    """
    入力値を取得してPandas.DataFrame型で返す
    """
    setting_path:str=os.path.join(os.path.dirname(__file__),'Setting','入力値設定.xlsx')
    return pd.read_excel(setting_path,'TOOL設定')
    
def read_excel(excel_path:str,sheet_name:str,out_path:str):
    """
    Excelを読み込み、調整して返す
    """
    #Excel読み込み
    excel_name=Path(excel_path).stem
    df:DataFrame=pd.read_excel(excel_path,sheet_name=sheet_name)
    df.fillna('',inplace=True)
    df.to_csv(out_path + excel_name + '.txt', sep="	")
    
    msg_print(out_path + excel_name + '.txt',False)
    msg_print(f'Excel={excel_name} Sheet={sheet_name} 読み込み完了。件数={str(len(df))}件',True)
    #return df
    
    
def main():
    #開始ログ
    init_file()
    msg_print('--------------------------------------------------------------', True)
    msg_print(f'処理開始 {datetime.now().strftime("%H:%M:%S")}', True)
    msg_print('--------------------------------------------------------------', True)
    
    
    #設定情報を読み込み
    setting_df:DataFrame=read_setting()
    #出力Excel
    out_path:str=os.path.join(os.path.dirname(__file__),'txt',f'逆階層図マージ版_{datetime.now().year}{datetime.now().month}{datetime.now().day}_')
    msg_print(out_path, False)
    #Excelを読み込む
    [read_excel(excel_path,sheet_name,out_path) for excel_path,sheet_name in zip(setting_df['Excelのパス'],setting_df['シート名'])]
    
    msg_print('--------------------------------------------------------------', True)
    msg_print(f'処理完了 {datetime.now().strftime("%H:%M:%S")}', True)
    msg_print('--------------------------------------------------------------', True)


if __name__=='__main__':
    main()
    