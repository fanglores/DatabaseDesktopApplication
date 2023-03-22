import logging

import openpyxl as excel
import datetime


class ExcelReporter:
    DEFAULT_SHEETNAME = 'Отчет'

    def __init__(self, filename = None, sheetname = None):
        try:
            if sheetname is not None:
                self.DEFAULT_SHEETNAME = sheetname

            datetime_postfix = datetime.datetime.strftime("__%d-%m-%Y_%H-%M-%S")
            if filename is not None:
                self.DEFAULT_FILENAME = filename + datetime_postfix
            else:
                self.DEFAULT_FILENAME = 'report' + datetime_postfix

        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def write(self, data):
        try:
            self.__create_book()
            self.__write_header()
            self.__write_data(data)
            self.__save_book()
        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __create_book(self):
        try:
            self.report_book = excel.Workbook(self.DEFAULT_FILENAME)
            self.report_book.create_sheet(self.DEFAULT_SHEET_NAME, index=0)
        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __write_data(self):
        pass
        # insert each data

    def __insert_value(self, cell_name, value):
        try:
            sheet = self.report_book[self.DEFAULT_SHEET_NAME]
            cell = sheet[cell_name]
            cell.value = value
        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    # TODO: add optinon for definind a save path?
    def __save_book(self):
        self.report_book.save("{}.xlsx".format(self.DEFAULT_FILENAME))

    def __write_header(self):
        logging.critical('not implemented')
        raise NotImplemented
        self.insert_value("A2", value='Имя автора')
        self.insert_value("C2", value="Статус")
        self.insert_value("D2", value="Важность")
        self.insert_value("F1", value="Динамика")
        self.insert_value("J2", value="Время проверки")