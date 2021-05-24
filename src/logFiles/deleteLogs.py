#!/usr/bin/python
""" Service wich is executed by a crontab
ones a day to delete the log files"""

open("log_file.log", "w").close()
