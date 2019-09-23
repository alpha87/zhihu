#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 - Time: 2019/9/23 7:58 上午
 - Author: Jianxun
 - File: update.py
 - Website: https://lijianxun.top
 - Email: jianxun2004@gmail.com
 - 关注微信小程序: 宅宅生活收藏夹
 - Description:
   - 
"""
import requests
from concurrent.futures import ThreadPoolExecutor
from src.db import ZhihuData
from src.spider import ZhihuSpider


class Update(object):

    def __init__(self):
        self.db = ZhihuData()

    @staticmethod
    def tell_me(msg):
        """
        通知
        :param msg: 通告的信息
        :return: 无
        """
        url = "https://sc.ftqq.com/SCU36473T2e02a4ff1d2f525370cbca327553d0cc5bfcb7899e2a7.send?text={}"
        requests.get(url.format(msg))

    def do_task(self):
        """
        执行更新任务
        """

        # 通知
        self.tell_me("开始更新数据。")

        # 获取话题 ID 列表
        qid_list = self.db.merge_container()

        # 先更新后添加的新问题
        qid_list.reverse()

        # 知乎正常爬虫
        crawler_list = [ZhihuSpider(qid, self.db).run for qid in qid_list]

        with ThreadPoolExecutor() as executor:
            future = [executor.submit(task) for task in crawler_list]
            for f in future:
                f.result()

        self.tell_me("数据更新完成。")


if __name__ == '__main__':
    update = Update()
    update.do_task()