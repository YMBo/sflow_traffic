# !/usr/local/bin/python
# -*- coding: UTF-8 -*-
'''定时器,每天指定时间执行'''
import datetime
import threading
from log import logger


# 格式TIME = '02:00:00'
class Timer:
    def __init__(self, fun, TIME):
        time = TIME.split(':')
        self.__hour = int(time[0])
        self.__minute = int(time[1])
        self.__second = int(time[2])
        self.fun = fun

    def intervalBody(self):
        self.fun()
        self.setSecond()
        self.setTimer()

    def setTimer(self):
        intervalTime = self.__intervalTime
        self.timer = threading.Timer(intervalTime, self.intervalBody)
        self.timer.start()

    def setSecond(self):
        current = datetime.datetime.now()
        # 当前时间
        currentTime = current.time()
        tomorrow = current + datetime.timedelta(1)
        tomorrowdate = tomorrow.date()
        year = tomorrowdate.year
        month = tomorrowdate.month
        day = tomorrowdate.day
        # 如果当前时间小时比指定小时小，那么先执行一次
        if currentTime.hour < self.__hour:
            # 当天
            newdate = datetime.datetime(year, month, day - 1, self.__hour,
                                        self.__minute, self.__second)
        else:
            # 第二天
            newdate = datetime.datetime(year, month, day, self.__hour,
                                        self.__minute, self.__second)
        second = (newdate - current).total_seconds()
        logger.info("当前时间：%s", current)
        logger.info("下次间隔（秒）：%s", second)
        self.__intervalTime = second

    def start(self):
        self.setSecond()
        self.setTimer()

    def cancel(self):
        self.timer.cancel()


# def a():
#     print('传')

# t = Timer(a, '00:00:00')
# t.start()