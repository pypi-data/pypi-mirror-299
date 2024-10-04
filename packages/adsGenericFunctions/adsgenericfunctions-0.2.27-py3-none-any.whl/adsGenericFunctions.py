#from email import *

from src.postgre.dbPgsql import *

"""
from src.postgre.dbPgsql import *
from src.mssql.dbMssql import *
from src.pipeline import *
from src.timer import *
from src.logger import *
from src.global_config import *
"""

def pgsql(dictionnary: dict, logger: Logger):
    res = dbPgsql(dict, logger)
    return res

def test():
    print("YES")

if __name__ == "__main__":
    print("Hello")


