from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QCheckBox, QDateEdit, QRadioButton
import logging
import datetime

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
            logging.info('Initializing main window UI')
            # username
            self.username_label = QLabel('Username:', self)
            self.username_label.move(20, 20)
            self.username_value = QLineEdit(self)
            self.username_value.setGeometry(120, 20, 200, 25)
            self.username_value.setText(self.username)
            self.__flipReadOnly(self.username_value, True)

            # input labels
            # line edit ProgramName
            self.programName_label = QLabel('Program:', self)
            self.programName_label.move(20, 60)
            self.programName_value = QLineEdit(self)
            self.programName_value.setGeometry(120, 60, 200, 25)

            # Radiobuttons is active or is fixed
            self.isActive_value = QRadioButton('is active', self)
            self.isActive_value.move(120, 100)
            self.isActive_value.setChecked(True)
            self.isFixed_value = QRadioButton('is fixed', self)
            self.isFixed_value.move(120, 130)
            self.isActive_value.toggled.connect(self.__flipActiveState)

            # Checkbox is important
            self.isImportant_value = QCheckBox('is important', self)
            self.isImportant_value.move(120, 160)

            # Checkbox is delayed
            self.isDelayed_value = QCheckBox('is delayed', self)
            self.isDelayed_value.move(120, 190)

            # Checkbox is unstable
            self.isUnstable_value = QCheckBox('is unstable', self)
            self.isUnstable_value.move(120, 220)

            # datetime found date
            self.foundDate_label = QLabel('Found date:', self)
            self.foundDate_label.move(20, 263)
            self.foundDate_value = QDateEdit(self)
            self.foundDate_value.move(120, 260)
            self.foundDate_value.setDate(datetime.datetime.today())

            # datetime fixed date
            self.fixedDate_label = QLabel('Fixed date:', self)
            self.fixedDate_label.move(20, 306)
            self.fixedDate_value = QDateEdit(self)
            self.fixedDate_value.move(120, 300)
            self.fixedDate_value.setDate(datetime.datetime.today())
            self.__flipReadOnly(self.fixedDate_value, self.isActive_value.isChecked())

            # buttons
            # select button
            selectAll_button = QPushButton('Request all', self)
            selectAll_button.setGeometry(40, 720, 120, 50)
            selectAll_button.clicked.connect(lambda: self.__processQuery(QueryType.selectAll))
            # insert button
            insert_button = QPushButton('Add', self)
            insert_button.setGeometry(300, 720, 120, 50)
            insert_button.clicked.connect(lambda: self.__processQuery(QueryType.insert))
            # select button
            # TODO hidden button
            select_button = QPushButton('Request', self)
            select_button.setGeometry(450, 720, 120, 50)
            select_button.clicked.connect(lambda: self.__processQuery(QueryType.select))
            select_button.hide()
            # update button
            update_button = QPushButton('Update', self)
            update_button.setGeometry(600, 720, 120, 50)
            update_button.clicked.connect(lambda: self.__processQuery(QueryType.update))
            # delete button
            delete_button = QPushButton('Delete', self)
            delete_button.setGeometry(750, 720, 120, 50)
            delete_button.clicked.connect(lambda: self.__processQuery(QueryType.delete))
            # print button
            print_button = QPushButton('Print', self)
            print_button.setGeometry(1050, 720, 120, 50)
            print_button.clicked.connect(self.__printTable)

        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __flipReadOnly(self, obj, state):
        try:
            obj.setReadOnly(state)
            if state is True:
                obj.setStyleSheet("background-color: rgb(180,180,180)")
            else:
                obj.setStyleSheet("")
        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __flipActiveState(self, enabled):
        try:
            self.__flipReadOnly(self.foundDate_value, not enabled)
            self.__flipReadOnly(self.fixedDate_value, enabled)
            self.isImportant_value.setCheckable(enabled)
            self.isDelayed_value.setCheckable(enabled)
            self.isUnstable_value.setCheckable(enabled)
            if enabled is False:
                self.isImportant_value.setStyleSheet("background-color: rgb(180,180,180)")
                self.isDelayed_value.setStyleSheet("background-color: rgb(180,180,180)")
                self.isUnstable_value.setStyleSheet("background-color: rgb(180,180,180)")
            else:
                self.isImportant_value.setStyleSheet("")
                self.isDelayed_value.setStyleSheet("")
                self.isUnstable_value.setStyleSheet("")
        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __processQuery(self, queryType=QueryType.none):
        try:
            if queryType == QueryType.none:
                raise RuntimeError('Query type is not defined!')

            if queryType == QueryType.insert and len(self.programName_value.text()) == 0:
                logging.warning('No program name for INSERT QueryType')
                # show an error
                return None

            query = queryType.value.format(self.username_value.text(), self.programName_value.text(),
                str(self.isImportant_value.isChecked()), str(self.isActive_value.isChecked()),
                str(self.isDelayed_value.isChecked()), str(self.isUnstable_value.isChecked()),
                str(self.isFixed_value.isChecked()), self.foundDate_value.date().toPyDate(),
                self.fixedDate_value.date().toPyDate())

            logging.info(f'Executing query: {query}')
            return self.database.processQuery(query)
        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __printTable(self):
        try:
            reportWriter = ExcelReporter()
            # data = self.__processQuery(queryType='SELECT')
            logging.critical('test data!')
            data = [('test_program_name', 'test_author_name', 'true', 'true', 'false', 'false', 'false', '01.01.2001', '02.02.2002')]
            reportWriter.write(data)

        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __del__(self):
        try:
            logging.info("\'{}\' window destroyed".format(self.title))

        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))