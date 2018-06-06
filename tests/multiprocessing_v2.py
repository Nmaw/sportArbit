from threading import Thread
import time

urls = {'ticket11': {'pause': 1, 'url': 'url_1'},
        'ticket12': {'pause': 3, 'url': 'url_2'},
        'ticket13': {'pause': 5, 'url': 'utl_3'}}

urls2 = {'ticket21': {'pause': 2, 'url': 'url_1'},
         'ticket22': {'pause': 4, 'url': 'url_2'},
         'ticket23': {'pause': 6, 'url': 'utl_3'}}


def get_data(key, pause, url):
    for i in range(5):
        time.sleep(pause)
        print('Request: {}, url: {} with sleep: {}. Time: {}'.format(key, url, pause, time.time()))


if __name__ == '__main__':
    for item in urls:
        t = Thread(name=item, target=get_data, args=(item, urls[item]['pause'], urls[item]['url'],))
        t.daemon = True
        t.start()
        # print('Item: {}, pause: {}, url: {}'.format(item, urls[item]['pause'], urls[item]['url']))
    for item2 in urls2:
        t2 = Thread(name=item2, target=get_data, args=(item2, urls2[item2]['pause'], urls2[item2]['url'],))
        t2.daemon = True
        t2.start()

    print('Start. Time {}'.format(time.time()))
    t.join()
    t2.join()
    print('End. Time {}'.format(time.time()))
