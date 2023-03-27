from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QCheckBox, QDateEdit, QRadioButton, QMessageBox, QTableWidget, QTableWidgetItem
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
            self.last_query_result = None

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
            selectAll_button = QPushButton('Sync data', self)
            selectAll_button.setGeometry(40, 720, 120, 50)
            selectAll_button.clicked.connect(lambda: self.__processQuery(QueryType.selectAll))
            # insert button
            insert_button = QPushButton('Add', self)
            insert_button.setGeometry(300, 720, 120, 50)
            insert_button.clicked.connect(lambda: self.__processQuery(QueryType.insert))
            # update button
            update_button = QPushButton('Update', self)
            update_button.setGeometry(600, 720, 120, 50)
            update_button.clicked.connect(lambda: self.__processQuery(QueryType.update))
            # delete button
            delete_button = QPushButton('Delete', self)
            delete_button.setGeometry(750, 720, 120, 50)
            delete_button.clicked.connect(lambda: self.__processQuery(QueryType.delete))
            delete_button.hide()
            # print button
            print_button = QPushButton('Print', self)
            print_button.setGeometry(1050, 720, 120, 50)
            print_button.clicked.connect(self.__createReport)

            # BFT - big f table
            logging.debug('init table')
            self.data_table = QTableWidget(self)
            self.data_table.setGeometry(350, 20, 800, 650)
            self.data_table.setColumnCount(10)
            self.data_table.setHorizontalHeaderLabels(['ID', 'Author', 'Program', 'Active', 'Fixed', 'Important', 'Delayed', 'Unstable', 'Found date', 'Fixed date'])
            self.data_table.setColumnWidth(0, 50)
            self.data_table.setColumnWidth(1, 120)
            self.data_table.setColumnWidth(2, 120)
            self.data_table.setColumnWidth(3, 50)
            self.data_table.setColumnWidth(4, 50)
            self.data_table.setColumnWidth(5, 70)
            self.data_table.setColumnWidth(6, 50)
            self.data_table.setColumnWidth(7, 70)
            self.data_table.cellClicked.connect(self.__loadRowToGui)

            logging.critical('test data')
            self.data_table.setRowCount(1)
            self.data_table.setItem(0, 0, QTableWidgetItem('1'))
            self.data_table.setItem(0, 1, QTableWidgetItem('author'))
            self.data_table.setItem(0, 2, QTableWidgetItem('program'))
            self.data_table.setItem(0, 3, QTableWidgetItem('true'))
            self.data_table.setItem(0, 4, QTableWidgetItem('false'))
            self.data_table.setItem(0, 5, QTableWidgetItem('false'))
            self.data_table.setItem(0, 6, QTableWidgetItem('false'))
            self.data_table.setItem(0, 7, QTableWidgetItem('true'))
            self.data_table.setItem(0, 8, QTableWidgetItem('08.02.01'))
            self.data_table.setItem(0, 9, QTableWidgetItem('09.03.02'))
            logging.critical('test data end')
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

    def __updateTable(self):
        try:
            assert self.last_query_result is not None
            self.data_table.setRowCount(len(self.last_query_result))
            for i in range(len(self.last_query_result)):
                item = self.last_query_result[i]
                for j in range(10):
                    self.data_table.setItem(i, j, QTableWidgetItem(str(item[j])))
        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __str2bool(self, str):
        return bool(str.lower() is 'true')

    def __loadRowToGui(self, row):
        try:
            self.programName_value.setText(self.data_table.item(row, 2).text())
            self.isActive_value.setChecked(self.__str2bool(self.data_table.item(row, 3).text()))
            self.isFixed_value.setChecked(self.__str2bool(self.data_table.item(row, 4).text()))
            self.isImportant_value.setChecked(self.__str2bool(self.data_table.item(row, 5).text()))
            self.isDelayed_value.setChecked(self.__str2bool(self.data_table.item(row, 6).text()))
            self.isUnstable_value.setChecked(self.__str2bool(self.data_table.item(row, 7).text()))
            self.foundDate_value.setDate(self.data_table.item(row, 8).text())
            self.fixedDate_value.setDate(self.data_table.item(row, 9).text())
        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __displayMsgBox(self, title, text, icon=QMessageBox.Warning, buttons=QMessageBox.Ok):
        try:
            msgBox = QMessageBox()
            msgBox.setIcon(icon)
            msgBox.setWindowTitle(title)
            msgBox.setText(text)
            msgBox.setStandardButtons(buttons)
            msgBox.exec()
        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __processQuery(self, queryType=QueryType.none):
        try:
            self.last_query_result = None
            query = None

            if queryType == QueryType.none:
                raise RuntimeError('Query type is not defined!')

            elif queryType == QueryType.selectAll:
                query = queryType.value

            elif queryType == QueryType.insert:
                if len(self.programName_value.text()) == 0:
                    logging.warning('No program name for INSERT QueryType')
                    self.__displayMsgBox("Warning: missing fields", "Program name must be inserted")
                    return

                if self.isFixed_value.isChecked():
                    logging.warning('Cannot insert a fixed error')
                    self.__displayMsgBox("Error: forbidden action", "Cannot insert a fixed error", QMessageBox.Critical)
                    return

                query = queryType.value.format(self.username_value.text(), self.programName_value.text(),
                    str(self.isImportant_value.isChecked()), str(self.isDelayed_value.isChecked()),
                    str(self.isUnstable_value.isChecked()), str(self.foundDate_value.date().toPyDate()))

            elif queryType == QueryType.select:
                logging.critical(f'Skipping query of type: {queryType}')
                return

            elif queryType == QueryType.update:
                if self.data_table.currentRow() is None:
                    self.__displayMsgBox('Error: no entry selected', 'Select an entry to update from table',QMessageBox.Critical)
                    raise IndexError('Row from table was not selected')
                query = queryType.value.format(self.username_value.text(), self.programName_value.text(),
                    str(self.isActive_value.isChecked()), str(self.isFixed_value.isChecked()),
                    str(self.isImportant_value.isChecked()), str(self.isDelayed_value.isChecked()),
                    str(self.isUnstable_value.isChecked()), str(self.foundDate_value.date().toPyDate()),
                    str(self.fixedDate_value.date().toPyDate()), str(self.data_table.currentRow()[0]))

            elif queryType == QueryType.delete:
                logging.critical(f'Skipping query of type: {queryType}')
                return

            logging.info(f'Executing query: {query}')
            self.last_query_result = self.database.processQuery(queryType, query)
            logging.debug(f'Query returned: {self.last_query_result}')
        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))
        finally:
            if queryType == QueryType.selectAll:
                self.__updateTable()
            pass

    def __createReport(self):
        try:
            reportWriter = ExcelReporter()
            assert self.last_query_result is not None
            reportWriter.write(self.last_query_result)
        except AssertionError as e:
            logging.error(type(e).__name__ + ": " + str(e))
            self.__displayMsgBox("Error: no data", "The data is empty! Try to Sync data first!", QMessageBox.Critical)
        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))

    def __del__(self):
        try:
            logging.info("\'{}\' window destroyed".format(self.title))

        except Exception as e:
            logging.error(type(e).__name__ + ": " + str(e))