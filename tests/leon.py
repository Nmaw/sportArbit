#!/usr/bin/python3
# Вся обработка в памяти
__author__ = 'anton'

import logging
import re
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
TABLE = 'leonbets'
URL_RU = 'https://ru.leonbets.net/sportsbook'
URL = 'https://www.leonbets.com/?lang=en'
SQL_INSERT = 'INSERT INTO ' + TABLE + ' (EVENT_URL, EVENT_TIME, EVENT_NAME, EVENT_NAME_BETS, EVENT_BET) ' \
             'VALUES (%s, %s, %s, %s, %s);'
SQL_INSERT_MON = 'INSERT INTO monitor (TIME_RUN, TIME_BEGIN_LOAD, TIME_END_LOAD, COUNT_UPDATE, COUNT_INSERT, ' \
                 'COUNT_DELETE, DESCRIPTION, URL) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
SQL_UPDATE = 'UPDATE ' + TABLE + ' SET EVENT_URL=%s, EVENT_TIME=%s, EVENT_NAME=%s, EVENT_NAME_BETS=%s, EVENT_BET=%s ' \
             'WHERE EVENT_TIME=%s AND EVENT_NAME=%s AND EVENT_NAME_BETS=%s ;'
SQL_SELECT = 'SELECT EVENT_URL, EVENT_TIME, EVENT_NAME, EVENT_NAME_BETS, EVENT_BET FROM ' + TABLE + ' '
WHERE1 = 'WHERE EVENT_URL=%s AND EVENT_TIME=%s AND EVENT_NAME=%s AND EVENT_NAME_BETS=%s AND EVENT_BET=%s'  # Select
WHERE2 = 'WHERE EVENT_TIME=%s AND EVENT_NAME=%s AND EVENT_NAME_BETS=%s AND EVENT_BET=%s'  # Check duplicate
SQL_DELETE = 'DELETE FROM ' + TABLE + ' WHERE id = (SELECT MIN(id) FROM ' + TABLE + ' ' + WHERE2 + ')'  # "id = (" or "id in ("
PROXY = 'localhost:9050'
PROXY_TYPE = 'socks4'
URL_IP = 'http://ifconfig.me/ip'
TIME_RUN = datetime.datetime.today()
UPDATE_COL = 0
INSERT_COL = 0
DELETE_COL = 0
DESCRIPTION = ''

g = grab.Grab()
g.setup(debug_post=False, reuse_cookies=True, connect_timeout=15000, proxy=PROXY, proxy_type=PROXY_TYPE)
g.go(URL_IP)
ip_tor = g.doc.unicode_body()
print(ip_tor.__str__())
g.setup(debug_post=False, reuse_cookies=True, connect_timeout=150000, proxy=PROXY, proxy_type=PROXY_TYPE,
        cookies={'JSESSIONID': '9959080DAC4413B1288A2F4A5CA3F26B',
                 'YPF8827340282Jdskjhfiw_928937459182JAX666': ip_tor.__str__(),
                 'ipfrom': ip_tor.__str__(),
                 'tc_cookie': '69b8855cb50a2fb7e27ca0f06fa9ed29'}
        )

#print(g.dump_config())


def main():
    time_begin_load = datetime.datetime.today()
    g.go(URL)  # Working
    #match = re.findall(r'\w{5}://\w{2}.\w{8}.\w{3}/b\w+/\d+/\d+', g.response.unicode_body())  # Working for RU
    match = re.findall(r'\w{5}://\w{3}.\w{8}.\w{3}/b\w+/\d+/\d+', g.response.unicode_body())  # Working for US
    if match:
        for elem in match:
            g.go(elem)
            parse(g.response.unicode_body())
    d = 'Done!'
    time_end_load = datetime.datetime.today()
    db(SQL_INSERT_MON,
       (TIME_RUN, time_begin_load, time_end_load, UPDATE_COL, INSERT_COL, DELETE_COL, DESCRIPTION, URL), typ='2')
    return print(d)


def parse(body):
    for elem in re.split(r'(\bprintShortDate\()', body):
        if elem[:13].isdecimal():
            for elem_bets in re.findall(r'title=.+>\s*<\w+>\d+\.\d{2}', elem):
                url = re.findall(r'\w{5}://\w{3}.\w{8}.\w{3}/\w{8}/\d+/\d+/\d+', elem)
                time = datetime.datetime.fromtimestamp(int(elem[:10]))
                name = re.findall(r'nou2.>.*</a>\s</strong>',
                                  grab.tools.text.normalize_space(elem, replace=' '))[0][7:-15]
                name_bets = elem_bets[7:elem_bets.find('><') - 1]
                bets = elem_bets[elem_bets.rfind('>') + 1:]
                #print(url, time, name, name_bets, bets)  # Working
                db(SQL_INSERT, (url, time, name, name_bets, bets), typ='1')


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
        #print(SQL_INSERT_MON, args)
        cur.execute(SQL_INSERT_MON, args)
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    main()

#Insert:  10399 Update:  5685 Done! 2015/03/11