import enum
from sqlite3 import DatabaseError
import psycopg2
import logging
import enum

from runtimeConstants import DATABASE_HOST, DATABASE_NAME, DEBUG_BUILD, resultFail, resultOk


class QueryType(enum.Enum):
    select  =   'SELECT'
    update  =   'UPDATE'
    insert  =   'INSERT'
    delete  =   'DELETE'
    none    =   None

class Database:
    conn = None
    cursor = None

    def connect(self, username_, password_):
        try:
            self.username = username_

            if(DEBUG_BUILD):
                if (username_ == 'user' and password_ == 'user') or (username_ == 'admin' and password_ == 'admin'):
                    self.conn = 0
                    return resultOk
                else:
                    raise DatabaseError('Incorrect credentials')

            self.conn = psycopg2.connect(
                host=DATABASE_HOST,
                database=DATABASE_NAME,
                user=username_,
                password=password_
            )

            self.cursor = self.conn.cursor()
            logging.info('Database connection established')
            return resultOk

        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))
            return resultFail

    def processQuery(self, queryString):
        raise NotImplemented()
        # process query and return result as array

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()

        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))