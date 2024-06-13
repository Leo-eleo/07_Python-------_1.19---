#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


def main(db_path,excel_path):
    print("start to setup data dsn info to db")
    received_asset_df = pd.read_excel(excel_path,sheet_name="DATA_DSN別データ分類情報")
    received_asset_df.fillna("",inplace=True)
    keys = received_asset_df.columns.tolist()
    assert len(keys) <= 5, "DATA_DSN別データ分類情報の列は5個までの必要があります。"
    
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    table_name = "DATA_DSN別データ分類情報"
    sql,_ = make_delete_sql(table_name,[],[])
    cursor.execute(sql)

    for i in range(len(received_asset_df)):
        
        data = received_asset_df.iloc[i]
        values = [data[key] for key in keys]
        sql,values = make_insert_sql(table_name,values,keys)
        cursor.execute(sql,values)
        
    print("finish to setup data dsn info to db")
    
    
if __name__ == "__main__":     
    main(sys.argv[1],sys.argv[2])