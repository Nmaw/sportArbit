# TODO Write new information about pairs and price
# TODO Read information for analytics price


import sqlite3
import time
import sys


class SQLite:

    def __init__(self):
        pass

    def __del__(self):
        pass

    @staticmethod
    def connect(logger):
        dbfile = '{}/{}'.format('data', 'main.db')
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
        logger.info('Connected {} to database {} with cursor {}'.format(conn, dbfile, cursor))
        return conn, cursor, dbfile

    @staticmethod
    def close(conn):
        conn.close()

    @staticmethod
    def create_db(logger):
        conn, cursor, dbfile = SQLite.connect(logger)
        logger.info('Database {} was created with connect {} and cursor {}'.format(dbfile, conn, cursor))

        try:
            cursor.execute('CREATE TABLE IF NOT EXISTS stats (pair text, period real, volume real, PRIMARY KEY(pair '
                           'ASC));')
        except sqlite3.DatabaseError as err:
            logger.error('Error: {} create tables in database: {} '.format(err, dbfile))
            sys.exit()
        else:
            conn.commit()
        logger.info('Create all tables for database {}'.format(dbfile))
        conn.close()

    @staticmethod
    def read(cursor, table, logger):
        # print('Read data from DB:', cursor, table)
        if table == 'symbols':
            request = 'SELECT pair FROM symbols_details ORDER BY pair;'
            try:
                cursor.execute(request)
            except sqlite3.DatabaseError as err:
                logger.error('Error: {} reading from table {}'.format(err, table))
            logger.info('Read table {} with cursor {}'.format(table, cursor))
            result = cursor.fetchall()
            # time.sleep(1)
            return result
        elif table == 'tickers':
            pass
        else:
            logger.info('We have not information for table: {} and no select data.', table)

    @staticmethod
    def insert(conn, cursor, table, data, logger):
        """
        :param logger: logger for logs
        :param table: where write
        :param conn: Connection
        :param cursor: Cursor
        :param data: Structure with data from exchange
        :return:
        """
        if table == 'symbols_details':
            try:
                cursor.executemany('insert into symbols_details values ('
                                   ':pair, '
                                   ':price_precision, '
                                   ':initial_margin, '
                                   ':minimum_margin, '
                                   ':maximum_order_size, '
                                   ':minimum_order_size, '
                                   ':expiration);', data)
            except sqlite3.DatabaseError as err:
                logger.error('Error: {} insert table to {}'.format(err, table))
            else:
                conn.commit()
            logger.info('Insert table {} for connection {}'.format(table, conn))
        elif table == 'tickers':
            try:
                cursor.executemany('insert into tickers values ('
                                   ':pair, '
                                   ':mid, '
                                   ':bid, '
                                   ':ask, '
                                   ':last_price, '
                                   ':low, '
                                   ':high, '
                                   ':volume, '
                                   ':timestamp);', data)
            except sqlite3.DatabaseError as err:
                logger.error('Error: {} insert table to {}'.format(err, table))
            else:
                conn.commit()
            logger.info('Insert table {} for connection {}'.format(table, conn))
        elif table == 'stats':
            try:
                cursor.executemany('insert into stats values ('
                                   ':period, '
                                   ':volume);', data)
            except sqlite3.DatabaseError as err:
                logger.error('Error: {} insert table to {}'.format(err, table))
            else:
                conn.commit()
            logger.info('Insert table {} for connection {}'.format(table, conn))
        else:
            logger.info('We have not information for table: {} and no write data.', table)
