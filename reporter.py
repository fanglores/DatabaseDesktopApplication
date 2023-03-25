import logging

import openpyxl as excel
import datetime


class ExcelReporter:
    default_sheetname = 'Отчет'

    def __init__(self, filename=None, sheetname=None):
        try:
            if sheetname is not None:
                self.default_sheetname = sheetname

            datetime_postfix = datetime.datetime.strftime(datetime.datetime.now(), '__%d-%m-%Y_%H-%M-%S')
            if filename is not None:
                self.default_filename = filename + datetime_postfix
            else:
                self.default_filename = 'report' + datetime_postfix

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
            logging.info('Creating execl book')
            self.report_book = excel.Workbook()
            self.report_book.create_sheet(self.default_sheetname, index=0)
        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __write_data(self, data):
        logging.info('Writing data to excel sheet')
        pass
        # insert each data

    def __insert_value(self, cell_name, value):
        try:
            sheet = self.report_book[self.default_sheetname]
            cell = sheet[cell_name]
            cell.value = value
        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    # TODO: add optinon for definind a save path?
    def __save_book(self):
        try:
            logging.info('Saving the excel file')
            self.report_book.save("{}.xlsx".format(self.default_filename))
        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __write_header(self):
        try:
            self.__insert_value("A2", value='Имя автора')
            self.__insert_value("B2", value='Название программы')
            self.__insert_value("C2", value="Важна")
            self.__insert_value("D2", value="Активна")
            self.__insert_value("E2", value="Отложена")
            self.__insert_value("F2", value="Нестабильна")
            self.__insert_value("G2", value="Устранена")
            self.__insert_value("H2", value="Дата обнаружения")
            self.__insert_value("I2", value="Дата устранения")
        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))