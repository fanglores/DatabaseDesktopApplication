from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton
import logging

from runtimeConstants import TITLE_POSTFIX, resultOk

class LoginWindow(QWidget):
    title = 'Login'
    sizeX = 600
    sizeY = 300

    # window setup
    def __init__(self, screenWidth, screenHeight, db):
        try:
            self.db = db
            super().__init__()
            self.setWindowTitle(self.title + TITLE_POSTFIX)
            self.move((screenWidth - self.sizeX)//2, (screenHeight - self.sizeY)//2)
            self.setFixedSize(self.sizeX, self.sizeY)
            logging.debug("\'{}\' window setGeometry({}, {}, {}, {})".format(self.title, self.geometry().x(), self.geometry().y(), self.sizeX, self.sizeY))
            self.__initUI()
            logging.info("\'{}\' window created".format(self.title))
        
        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    # UI layout and setup
    def __initUI(self):
        try:
            # Create labels of input fields
            username_label = QLabel('Username:', self)
            username_label.move(100, 50)
            password_label = QLabel('Password:', self)
            password_label.move(100, 100)

            # Create label for incorrect password
            self.login_label = QLabel('Password is incorrect!', self)
            self.login_label.setHidden(True)
            self.login_label.setStyleSheet("color: rgb(255,0,0)")
            self.login_label.move(220, self.sizeY//2)

            # Create input field
            self.username_input = QLineEdit(self)
            self.username_input.setGeometry(200, 50, 300, 25)
            self.password_input = QLineEdit(self)
            self.password_input.setGeometry(200, 100, 300, 25)
            self.password_input.setEchoMode(QLineEdit.Password)

            # Create login button
            login_button = QPushButton('Login', self)
            login_button.setGeometry(self.sizeX//4, self.sizeY*10//16, self.sizeX//2, 75)
            login_button.clicked.connect(self.__login)
        
        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __login(self):
        try:
            # Get data from fields
            username = self.username_input.text()
            password = self.password_input.text()

            # Attempt login
            if(resultOk == self.db.connect(username, password)):
                self.login_label.setHidden(True)
                logging.debug("Login successful!")
                self.close()
            else:
                self.login_label.setHidden(False)
                logging.debug("Login failed!")

        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __del__(self):
        try:
            logging.info("\'{}\' window destroyed".format(self.title))
        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))
