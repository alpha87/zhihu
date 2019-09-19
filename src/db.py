#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 - Time: 2019/9/19 1:35 下午
 - Author: Jianxun
 - File: db.py
 - Website: https://lijianxun.top
 - Email: jianxun2004@gmail.com
 - 关注微信小程序: 宅宅生活收藏夹
 - Description:
   - 数据库操作。
"""
import re
import time
from requests import get
from random import choice
from pymongo import MongoClient

from headers import HEADERS_LIST


class ZhihuData(object):

    def __init__(self):

        client = MongoClient('mongodb://localhost:27017/')
        db = client["Zhihu"]

        # 存放最新的 id
        self.beauty_container = db["BeautyContainer"]
        # 首页展示的 id
        self.show_question = db["ShowQuestion"]
        # 答案
        self.answer_items = db["AnswerItems"]

    def insert_beauty_container(self, url: str):
        """
        新问题 id 插入到 beauty_container
        :param question_id: 问题对应链接
        :return:
        """
        if not (url.startswith("https://www.zhihu.com/question")
                or url.startswith("http://www.zhihu.com/question")):
            return False
        else:
            question_id = url.split("/")[4]
            url = "https://www.zhihu.com/question/{}".format(question_id)
            headers = choice(HEADERS_LIST)
            html = get(url, headers=headers)
            if html.status_code == 200:
                title = re.findall(
                    r'title data-react-helmet="true">(.*?) - 知乎</title>',
                    html.text)[0]
                question_dict = {
                    "title": title,
                    "question_id": question_id,
                    # 问题是否关闭
                    "close": False,
                    # 回答总数
                    "count": -1
                }
                self.beauty_container.insert_one(question_dict)
                return True
            return False


if __name__ == '__main__':
    db = ZhihuData()
    with open("result.txt", "r") as f:
        a = f.read()
    qid_list = list(eval(a))
    for qid in qid_list:
        time.sleep(1)
        db.insert_beauty_container("https://www.zhihu.com/question/{}".format(qid))
        # print(qid)