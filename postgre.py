import psycopg2
import logging
import enum

from runtimeConstants import DATABASE_HOST, DATABASE_NAME, resultFail, resultOk


class QueryType(enum.Enum):
    select  =   'SELECT * FROM public.\"ErrorsTable\" WHERE (...);'
    selectAll = 'SELECT * FROM public.\"ErrorsTable\";'
    update  =   'UPDATE public.\"ErrorsTable\" SET author_name = \'{}\', program_name = \'{}\', \"isActive\" = {}, \"isFixed\" = {}, \"isImportant\" = {}, \"isDelayed\" = {}, \"isUnstable\" = {}, found_date = \'{}\', fixed_date = \'{}\' WHERE id = {};'
    insert  =   'INSERT INTO public.\"ErrorsTable\" (author_name, program_name, \"isActive\", \"isFixed\", \"isImportant\", \"isDelayed\", \"isUnstable\", found_date, fixed_date) VALUES (\'{}\', \'{}\', True, False, {}, {}, {}, \'{}\', \'NULL\');'
    delete  =   'DELETE FROM public.\"ErrorsTable\" WHERE id = {};'
    none    =   None

class Database:
    conn = None
    cursor = None

    def connect(self, username_, password_):
        try:
            self.username = username_

            logging.info('Trying to connect...')
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

    def processQuery(self, queryType, queryString):
        try:
            logging.info('Processing query')
            self.cursor.execute(queryString)

            if queryType == QueryType.select or queryType == QueryType.selectAll:
                return self.cursor.fetchall()
            else:
                self.conn.commit()
        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))
            return None

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()

        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))