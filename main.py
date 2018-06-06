#!/usr/bin/env python3

from threading import Thread
from modules.database import *
from modules.logger import *
from modules.config import *
from modules.proxy import *


def main():
    config = 'main.cfg'
    id_conf, logfile = Config().config_load(config)
    logger = Logger().load_logger(logfile)

    logger.info('*********************************************************************************')
    logger.info('SportArbit starting | LogsFile: {} | ConfigFile: {} '.format(logfile, config))

    proxy = get_proxy()
    database = SQLite()


if __name__ == '__main__':
    main()
