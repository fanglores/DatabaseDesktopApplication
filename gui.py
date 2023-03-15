from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton
import logging

from runtimeConstants import TITLE_POSTFIX, resultOk, resultFail

class MainWindow(QWidget):
    title = "Workspace"
    sizeX = 800
    sizeY = 600

    def __init__(self, screenWidth, screenHeight):
        try:
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
            #raise NotImplementedError()
            pass

        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __del__(self):
        try:
            logging.info("\'{}\' window destroyed".format(self.title))

        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))