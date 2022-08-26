import queue
from waterRPA.code import bzy_main
import operateDB as cmdDB
import operateExcel as cmdExcel
import time

def autoProcess(queue:queue,totalNeed:int,eachAddQueue:int,deepth=99999):
    round = 0
    cur_get = 0
    cur_dpth = 1
    rest_curLayer,total_nextLayer = 1,0
    flag_add = True     # 层级逻辑，是否往队列继续插入元素遍历判断
    while(cur_get < totalNeed and cur_dpth <= deepth):
        round += 1
        print("[Notice] 当前轮数：%d"%round)
        if queue.empty():
            print("[Warn] 队列为空，退出循环")
            break
        if round > 1:
            last_url = cur_url
        cur_url = queue.get()
        if round > 1 and last_url == cur_url:
            print("[Warn] No.%d 当前url与上一匹配url一致，跳过此轮"%round)
            continue
        elif cur_url == "":
            print("[ERR] No.%d 队列没有数据可获取，退出循环"%round)

        # edit new url into cmd.xls
        print("[Notice] 即将把新url写入cmd.txt")
        time.sleep(2)
        ret = cmdExcel.editUrl(cur_url)
        if ret == 0:
            print("[Info] 成功修改文件")
        elif ret == -1:
            # print("[Warn] No.%d 修改文件失败，跳过此轮循环"%round)
            print("[Warn] No.%d 修改文件失败，退出循环"%round)
            break
        else:
            print("[ERR] No.%d occurred Unknown Error"%round)
            break
        time.sleep(1)

        # run the waterRPA on Bazhao Fish
        print("[Info] No.%d cmd.txt就绪，开始执行八爪鱼脚本"%round)
        time.sleep(2)
        ret = bzy_main()
        if ret == 0:
            print("[Info] No.%d 八爪鱼脚本运行完成"%round)
        elif ret == -1:
            print("[Warn] No.%d Bazhao Fish run FAILED"%round)
        else:
            print("[ERR] No.%d Bazhao Fish process occurred Unknown Error"%round)
        
        # sql things
        print("[Notice] 准备从数据库获取采集的数据个数")
        time.sleep(2)
        temp_list = cmdDB.mySelect(cur_url,20)
        temp_len = len(temp_list)
        cur_get += temp_len
        print("[Info] 当前已获取的数据总量为%d,目标总数为%d"%(cur_get,totalNeed))
        print("[Info] 当前进度：%.2f%%"%(cur_get/totalNeed*100))

        print("[Notice] 准备从数据库获取子链接")
        time.sleep(2)
        temp_list = cmdDB.mySelect(cur_url,eachAddQueue)
        temp_len = len(temp_list)
        if temp_len == 0:
            print("[Warn] No.%d could NOT GET ANY URLs from sql"%round)
        else:
            print("[Info] No.%d 共获取到 %d 个子链接"%(round,temp_len))
            for each in temp_list:
                if queue.full():
                    print("[Warn] No.%d 队列已满,加入子链接%d失败"%(round,each))
                    break
                if flag_add:
                    print("[Info] 当前层数：%d 成功往队列加入子链接：%s"%(cur_dpth,each))
                    queue.put(each)
                    total_nextLayer += 1

        #处理层数逻辑
        rest_curLayer -= 1
        if rest_curLayer == 0 : #队列该层没有元素
            rest_curLayer = total_nextLayer
            cur_dpth += 1
        if cur_dpth > deepth and flag_add == True:
            flag_add = False

        print("[Notice] 第%d轮执行完毕"%round)

    del queue
    print("[Info] 循环完成,汇总数据如下")
    print("[Info] 总轮数：%d    目标获取图片数：%d  实际获取图片数目：%d    完成率：%.2f%%"%(round,totalNeed,cur_get,cur_get/totalNeed*100))
    return 0