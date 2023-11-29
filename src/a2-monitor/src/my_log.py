import datetime

class myLog:
    def __init__(self, context):
        self.context = context

    def logFile(self):
        log_dir = "logs/"
        str_date = str(datetime.date.today()).replace("-", "_")
        log_filename = "ping_" + str_date + ".log"
        log_file = open(log_dir + log_filename, 'a+')
        return log_file

    def readLogFile(self):
        log_dir = "logs/"
        str_date = str(datetime.date.today()).replace("-", "_")
        log_filename = "ping_" + str_date + ".log"
        log_file = open(log_dir + log_filename, 'r')
        return log_file

    def get_current_dt(self):
        str_dt = datetime.datetime.now()
        str_format = "%Y-%m-%d %H:%M:%S"
        return str_dt.strftime(str_format)

    def log_info(self, msg):
        prefix = "[INFO] "
        self.log(prefix, msg)

    def log_warn(self, msg):
        prefix = "[WARN] "
        self.log(prefix, msg)

    def log_error(self, msg):
        prefix = "[ERROR] "
        self.log(prefix, msg)

    def log(self,prefix, msg):
        log_file = self.logFile()
        current_dt = " [" + self.get_current_dt() + "] "
        log_msg = f"[{self.context}] {current_dt}  {prefix}  {msg}"
        print(log_msg)
        log_msg += "\n"
        log_file.write(log_msg)
        log_file.close()
