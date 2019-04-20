import os

from dbwriter import write_to_db as dbwrite

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    dbwrite.main()