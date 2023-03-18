import logging
from PyQt5.QtWidgets import QApplication

from runtimeConstants import LOGFILE_PATH, DEBUG_BUILD, LOG_FORMAT, TIME_FORMAT, VERSION
from login import LoginWindow
from postgre import Database
from gui import MainWindow


if DEBUG_BUILD:
    logging.basicConfig(level=logging.DEBUG,
                        format=LOG_FORMAT, datefmt=TIME_FORMAT)
else:
    logging.basicConfig(filename=LOGFILE_PATH, filemode='w', encoding='utf-8', level=logging.INFO,
                        format=LOG_FORMAT, datefmt=TIME_FORMAT)

logging.info("Logging has started")
logging.info("Errors Tracing Application {}, Moscow Aviation Institue, 2023".format(VERSION))


def new_session():
    try:
        app = QApplication([])

        w = app.primaryScreen().size().width()
        h = app.primaryScreen().size().height()

        logging.info("Screen size is {}x{}".format(w, h))

        database = Database()
        loginWindow = LoginWindow(w, h, database)
        mainWindow = MainWindow(w, h)

        # CRITICAL if closed skips to next window
        loginWindow.show()
        app.exec()

        if database.conn == None:
            raise Exception('Connection failed or incorrect credentials')

        mainWindow.show()
        app.exec()

        del database
        del loginWindow
        del mainWindow
        app.closeAllWindows()

    except Exception as e:
        app.closeAllWindows()
        logging.error(type(e).__name__ + ": " + str(e))

if __name__ == "__main__":
    new_session()
    exit(0)
