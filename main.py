#!/usr/bin/env python3

from threading import Thread
from modules.database import *
from modules.logger import *
from modules.config import *
from modules.proxy import *


def main():
    config = 'main.cfg'
    id_conf, logfile = Config().load_config(config)
    logger = Logger().load_logger(logfile)

    logger.info('*********************************************************************************')
    logger.info('SportArbit starting | LogsFile: {} | ConfigFile: {} '.format(logfile, config))
    logger.info('Config sections: {}.'.format(Config.get_config(id_conf, 'all')))
    logger.info('Config sections: {}.'.format(Config.get_config(id_conf, 'default')))
    # proxy = get_proxy()
    database = SQLite().create_db(logger)


if __name__ == '__main__':
    main()
