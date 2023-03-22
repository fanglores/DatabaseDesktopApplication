from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton
import logging

from runtimeConstants import TITLE_POSTFIX
from postgre import QueryType
from reporter import ExcelReporter


class MainWindow(QWidget):
    title = "Workspace"
    sizeX = 1200
    sizeY = 800

    def __init__(self, screenWidth, screenHeight, database):
        try:
            self.database = database
            self.username = self.database.username
            super().__init__()
            self.setWindowTitle(self.title + TITLE_POSTFIX)
            self.move((screenWidth - self.sizeX)//2, (screenHeight - self.sizeY)//2)
            self.setFixedSize(self.sizeX, self.sizeY)
            logging.debug("\'{}\' window setGeometry({}, {}, {}, {})".format(self.title, self.geometry().x(), self.geometry().y(), self.sizeX, self.sizeY))
            self.__initUI()
            logging.info("\'{}\' window created".format(self.title))

        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __initUI(self):
        try:
            # username
            username_label = QLabel('Username:', self)
            username_label.move(20, 20)
            self.username_value = QLineEdit(self)
            self.username_value.setGeometry(120, 20, 200, 25)
            self.username_value.setText(self.username)
            self.username_value.setReadOnly(True)
            self.username_value.setStyleSheet("background-color: rgb(180,180,180)")

            # buttons
            # print button
            print_button = QPushButton('Print', self)
            print_button.setGeometry(1050, 720, 120, 50)
            print_button.clicked.connect(self.__printTable)

        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __processQuery(self, queryType=QueryType.none):
        try:
            if queryType == QueryType.none:
                raise RuntimeError('Query type is not defined!')

            # fill formatting with buttons values; create template in postgre
            query = queryType.value.format()
            return self.database.processQuery(query)

        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __printTable(self):
        try:
            reportWriter = ExcelReporter()
            # data = self.__processQuery(queryType='SELECT')
            logging.critical('test data!')
            data = ['test_program_name', 'test_author_name', 'true', 'true', 'false', 'false', 'false', '01.01.2001', '02.02.2002']
            reportWriter.write(data)

        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __del__(self):
        try:
            logging.info("\'{}\' window destroyed".format(self.title))

        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))