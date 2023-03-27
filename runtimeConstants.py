DEBUG_BUILD         =   False

# application constants
APPLICATION_NAME    =   "Errors Tracing Application"
VERSION             =   "v1.1" + ("_dev" if DEBUG_BUILD else "")
TITLE_POSTFIX       =   " - {} {}".format(APPLICATION_NAME, VERSION)

# logging constants
LOG_FORMAT          =   '%(asctime)s.%(msecs)03d\t%(levelname)s\t%(module)s.py::%(funcName)s\t%(message)s'
TIME_FORMAT         =   '%H:%M:%S'
LOGFILE_PATH        =   'application.log'

# database credentials constants
DATABASE_NAME       =   'ErrorsTracingDatabase'
DATABASE_HOST       =   'localhost'

# result codes
resultOk            =   0
resultFail          =   -1

# credentials
AUTHORS             =   "Tsaturyan Konstantin, Kulik Maxim, Smolkina Anastasia"
GITHUB              =   "https://www.github.com/fanglores"