#!/usr/bin/python3
# Вся обработка в памяти
__author__ = 'anton'

import logging
import grab
import psycopg2
import datetime

logger = logging.getLogger('grab')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

DB = 'bets'
USER = 'bets_user'
PASS = 'madnet'
HOST = 'localhost'
TABLE = 'one_x_bet'
URL = 'https://1-x-bet.com/en/line/'
SQL_INSERT = 'INSERT INTO ' + TABLE + ' (EVENT_URL, EVENT_TIME, EVENT_NAME, EVENT_NAME_BETS, EVENT_BET) ' \
             'VALUES (%s, %s, %s, %s, %s);'
SQL_INSERT_MON = 'INSERT INTO monitor (TIME_RUN, TIME_BEGIN_LOAD, TIME_END_LOAD, COUNT_UPDATE, COUNT_INSERT, ' \
                 'COUNT_DELETE, DESCRIPTION, URL) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
SQL_UPDATE = 'UPDATE ' + TABLE + ' SET EVENT_URL=%s, EVENT_TIME=%s, EVENT_NAME=%s, EVENT_NAME_BETS=%s, EVENT_BET=%s ' \
             'WHERE EVENT_TIME=%s AND EVENT_NAME=%s AND EVENT_NAME_BETS=%s ;'
SQL_SELECT = 'SELECT EVENT_URL, EVENT_TIME, EVENT_NAME, EVENT_NAME_BETS, EVENT_BET FROM ' + TABLE + ' '
WHERE1 = 'WHERE EVENT_URL=%s AND EVENT_TIME=%s AND EVENT_NAME=%s AND EVENT_NAME_BETS=%s AND EVENT_BET=%s'  # Select
WHERE2 = 'WHERE EVENT_TIME=%s AND EVENT_NAME=%s AND EVENT_NAME_BETS=%s AND EVENT_BET=%s'  # Check duplicate
SQL_DELETE = 'DELETE FROM ' + TABLE + ' WHERE id = (SELECT MIN(id) FROM ' + TABLE + ' ' + WHERE2 + ')'
PROXY = 'localhost:9050'
PROXY_TYPE = 'socks4'
URL_IP = 'http://ifconfig.me/ip'
TIME_RUN = datetime.datetime.today()
UPDATE_COL = 0
INSERT_COL = 0
DELETE_COL = 0
DESCRIPTION = ''

g = grab.Grab()
g.setup(debug_post=False, reuse_cookies=True, connect_timeout=1500, proxy=PROXY, proxy_type=PROXY_TYPE)
g.go(URL_IP)
ip_tor = g.doc.unicode_body()
print(ip_tor.__str__())

g_liga = grab.Grab()
g.setup(reuse_cookies=True, connect_timeout=1500, proxy=PROXY, proxy_type=PROXY_TYPE)
g_liga.setup(reuse_cookies=True, connect_timeout=1500, proxy=PROXY, proxy_type=PROXY_TYPE)


def main():
    time_begin_load = datetime.datetime.today()
    g.go(URL)  # Working
    for id_liga in g.doc.select('//a/@id').text_list():
        if id_liga[:4] == 'liga':
            g_liga.go(URL[:-5] + g.doc.select('//a[@id="' + id_liga + '"]/@href').text())
            for pid_game in g_liga.doc.select('//*[@id="' + 'liga_' + id_liga[9:] + '"]/li/a/@pid').text_list():
                date_xpath = '//*[@pid="' + pid_game + '"]/span/span[1]/span/text()'  # 14.03.2015
                time_xpath = '//*[@pid="' + pid_game + '"]/span/span[1]/text()[2]'
                url = URL[:-5] + g_liga.doc.select('//*[@pid="' + pid_game + '"]/@href').text()
                tm_old = g_liga.doc.select(date_xpath).text() + ' ' + g_liga.doc.select(time_xpath).text()[1:-1] + ':00'
                time = datetime.datetime.strptime(tm_old, '%d.%m.%Y %H:%M:%S').__str__()
                name = g_liga.doc.select('//*[@pid="' + pid_game + '"]/span/span[3]/text()').text()
                for number_bet in g_liga.doc.select('//*[@u="' + pid_game + '"]/@id').text_list():
                    xpath_nb = '//*[@id="' + number_bet + '" and @u="' + pid_game + '"]/@n'
                    for name_bets in g_liga.doc.select(xpath_nb).text_list():
                        xpath_b = '//*[@id="' + number_bet + '" and @u="' + pid_game + '" and @n="' + \
                                  name_bets + '"]/text()'
                        for bets in g_liga.doc.select(xpath_b).text_list():
                            #print(url, time, name, name_bets, bets)  # name and data bets
                            db(SQL_INSERT, ([url, ], time, name, name_bets, bets), typ='1')

    d = 'Done! '
    time_end_load = datetime.datetime.today()
    db(SQL_INSERT_MON,
       (TIME_RUN, time_begin_load, time_end_load, UPDATE_COL, INSERT_COL, DELETE_COL, DESCRIPTION, URL), typ='2')
    #print('Insert: ', INSERT_COL, '\n', 'Update: ', UPDATE_COL)
    return print(d)


def db(sql, args, typ):
    global INSERT_COL
    global UPDATE_COL
    global DELETE_COL

    conn = psycopg2.connect(database=DB, user=USER, password=PASS, host=HOST)
    cur = conn.cursor()
    if sql[:6].__eq__('INSERT') and typ.__eq__('1'):
        cur_select = db(SQL_SELECT + WHERE2, (args[1], args[2], args[3], args[4]), typ='1')
        if cur_select.rowcount < 1:
            #print('<-INSERT new row.')
            cur.execute(sql, args)  # INSERT
            INSERT_COL += 1
        elif cur_select.rowcount > 1:
            print('Please wait. Delete duplicate!')
            cur.execute(SQL_DELETE, (args[1], args[2], args[3], args[4]))
            DELETE_COL += 1
            conn.commit()
        else:
            #print('<-UPDATE exist row.')
            cur.execute(SQL_UPDATE, args + (args[1], args[2], args[3]))
            UPDATE_COL += 1
    elif sql[:6].__eq__('SELECT') and typ.__eq__('1'):
        #print('Checking duplicate')
        cur.execute(sql, args)
        return cur
    elif sql[:6].__eq__('INSERT') and typ.__eq__('2'):
        cur.execute(SQL_INSERT_MON, args)
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    main()

# Insert:  1074 Update:  10997 Done! 2015/03/11