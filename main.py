#!/usr/bin/env python3

# from configparser import ConfigParser, NoSectionError
# import logging
# import sys
# from bs4 import BeautifulSoup
from threading import Thread
from modules.database import *
from modules.logger import *
from modules.config import *
from modules.proxy import *


def get_html(url, headers, proxy, timeout=5):
    # sleep(1)
    r = requests.get(url, headers=headers, proxies=proxy, timeout=timeout)
    return r.text


def main():
    headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    config = 'main.cfg'
    id_conf, logsfile = Config().config_load(config)
    logger = Logger().load_logger(logsfile)

    logger.info('*********************************************************************************')
    logger.info('SportOBot starting | LogsFile: {} | ConfigFile: {} '.format(logsfile, config))

    proxy = get_proxy()
    database = SQLite()

    logger.debug('Main sections from config file: {}'.format(Config().get_config(id_conf, 'all')))

    active_bets = Config().get_config(id_conf, 'bets')
    logger.debug('Active bets: {}.'.format(active_bets))
    logger.debug('Active proxy: {}.'. format(proxy))
    logger.debug('Active DB: {}'.format(database))


    # TODO Run get data from bets on subprocess or thread
    for bet in active_bets:
        #url = '{}/urls.json?0.56692639492'.format(bet['url'])
        #r = get_html(url, headers, proxy, 5)
        print(bet)

    # sys.exit()


if __name__ == '__main__':
    main()
