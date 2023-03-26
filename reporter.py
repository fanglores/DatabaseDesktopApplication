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
        try:
            logging.info('Writing data to excel sheet')
            i = 2
            for item in data:
                self.__insert_value(f"A{i}", value=str(item[1]))
                self.__insert_value(f"B{i}", value=str(item[2]))
                self.__insert_value(f"C{i}", value=str(item[3]))
                self.__insert_value(f"D{i}", value=str(item[4]))
                self.__insert_value(f"E{i}", value=str(item[5]))
                self.__insert_value(f"F{i}", value=str(item[6]))
                self.__insert_value(f"G{i}", value=str(item[7]))
                self.__insert_value(f"H{i}", value=str(item[8]))
                self.__insert_value(f"I{i}", value=str(item[9]))
                i += 1
        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __insert_value(self, cell_name, value):
        try:
            sheet = self.report_book[self.default_sheetname]
            cell = sheet[cell_name]
            cell.value = value
        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __save_book(self):
        try:
            logging.info('Saving the excel file')
            self.report_book.save("{}.xlsx".format(self.default_filename))
        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __write_header(self):
        try:
            self.__insert_value("A1", value='Имя автора')
            self.__insert_value("B1", value='Название программы')
            self.__insert_value("C1", value="Активна")
            self.__insert_value("D1", value="Устранена")
            self.__insert_value("E1", value="Важна")
            self.__insert_value("F1", value="Отложена")
            self.__insert_value("G1", value="Нестабильна")
            self.__insert_value("H1", value="Дата обнаружения")
            self.__insert_value("I1", value="Дата устранения")
        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))