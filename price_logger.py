from threading import Thread

import ftx_data
import bitmex_data


if __name__ == '__main__':
    threads = list()
    threads.append(Thread(target=bitmex_data.log_data))
    threads.append(Thread(target=ftx_data.log_data))
    for thread in threads:
        thread.start()
        thread.join()