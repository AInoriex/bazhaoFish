# FileName  startHere_v0.3.py
# Date      22.08.25
# Author    AInoriex

import os
import queue
from mainCycle import autoProcess
import operateDB as cmdDB

def main():
    start_url = input("[Info] 请输入起始url：")
    total = eval(input("[Info] 请输入需要爬图的图片总数："))
    deepth = eval(input("[Info] 请输入需要遍历的层数深度（默认∞）："))
    num_addQueue = eval(input("[Info] 请输入每次加入队列二次搜索的图片个数n(range from [1,20])："))
    if num_addQueue not in range(1,21):
        print("[ERR] n 不符合输入要求（从1到20，包括20），程序退出")
        return
    cmdDB.initDB()
    links = queue.Queue(100000000)
    links.put(start_url)
    # def autoProcess()
    # args      queue,total,deepth,num_addQueue
    # return    status(0:ok 1:full)
    autoProcess(queue=links,totalNeed=total,eachAddQueue=num_addQueue,deepth=deepth)
    os.system("pause")

if __name__ == '__main__':
    main()


