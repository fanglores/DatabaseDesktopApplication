from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton
import logging

from runtimeConstants import TITLE_POSTFIX, resultOk, resultFail

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
            print_button = QPushButton('Login', self)
            print_button.setGeometry(self.sizeX // 4, self.sizeY * 10 // 16, self.sizeX // 2, 75)
            print_button.clicked.connect(self.__printTable)

        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __createQuery(self):
        raise NotImplemented()
        # ask buttons for its values
        # create string query depends on type of button?

    def __sendQuery(self):
        raise NotImplemented()
        params = self.__createQuery()
        self.database.processQuery(params)
        # send result data

    def __printTable(self):
        raise NotImplemented()
        self.__sendQuery()
        # ask DB for data? or take it from local table?
        # create xls file and insert fields

    def __del__(self):
        try:
            logging.info("\'{}\' window destroyed".format(self.title))

        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))