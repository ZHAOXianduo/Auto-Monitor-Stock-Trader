from crawl_price import thread_p
from alarm import send_out
from crawl_mass import thread_m
from crawl_abnormal import thread_ab
from Timing import price_time
import datetime
import pandas as pd

if __name__ == "__main__":
    now = datetime.datetime.now()
    ON, mark = price_time(0,now)
    Mails = []
    while ON:
        now = datetime.datetime.now()
        if now >= mark:
            message = thread_p(Mails)
            if len(message) > 0:
                print(message)
                send_out(message)
            message = []
            Mails = []
            ON, mark = price_time(30,now)
    #next_strip = datetime.datetime.now()
    #print(price_time(5,next_strip))
    #thread_m()
    #thread_ab()
    print("finish")