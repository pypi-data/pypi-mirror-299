#from email import *

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger import Logger

"""
from src.postgre.dbPgsql import *
from src.mssql.dbMssql import *
from src.pipeline import *
from src.timer import *
from src.logger import *
from src.global_config import *
"""



def new_logger(logger_connection, log_level, logger_name, table_name, details_table_name):
    return Logger(logger_connection, log_level, logger_name, table_name, details_table_name)

def test():
    print("YES")

if __name__ == "__main__":
    print("Hello")


