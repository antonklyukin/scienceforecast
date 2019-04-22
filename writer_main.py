import os

from dbwriter import write_to_db as dbwrite
from dbwriter import delete_double as remove

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    #remove.main()    
    dbwrite.main()
