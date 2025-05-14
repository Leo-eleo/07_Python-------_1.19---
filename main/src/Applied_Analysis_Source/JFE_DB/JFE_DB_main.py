#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
sys.path.append(os.path.dirname(__file__))
import time

from JFE_DB_analysis1 import analysis1
from JFE_DB_analysis2 import analysis2

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


def main(db_path,title):
    analysis1(db_path,title)
    excel_file = os.path.join(title,"JFE-DB利用箇所特定1.xlsx")
    analysis2(db_path,title,excel_file)
    
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])