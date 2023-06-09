DEBUG_BUILD         =   True

# application constants
APPLICATION_NAME    =   "Errors Tracing Application"
VERSION             =   "v1.2" + ("_dev" if DEBUG_BUILD else "")
TITLE_POSTFIX       =   " - {} {}".format(APPLICATION_NAME, VERSION)

# logging constants
LOG_FORMAT          =   '%(asctime)s.%(msecs)03d\t%(levelname)s\t%(module)s.py::%(funcName)s\t%(message)s'
TIME_FORMAT         =   '%H:%M:%S'
LOGFILE_PATH        =   'application.log'

# database credentials constants
DATABASE_NAME       =   'ErrorsTracingDatabase'
DATABASE_HOST       =   '192.168.158.74'

# result codes
resultOk            =   0
resultFail          =   -1

# credentials
AUTHORS             =   "Tsaturyan Konstantin, Kulik Maxim, Smolkina Anastasia"
GITHUB              =   "https://www.github.com/fanglores"