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

from .headers import HEADERS_LIST


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

    def merge_container(self) -> list:
        """
        合并 beauty_container 和 show_question 数据库
        :return: show_question 的问题列表
        """
        items = self.beauty_container.find()
        for item in items:
            data = self.show_question.find({
                "question_id": item["question_id"]
            })
            if data.count() == 0:
                self.show_question.insert_one({
                    "title": item["title"],
                    "question_id": item["question_id"],
                    # 问题是否关闭
                    "close": False,
                    # 回答总数
                    "count": -1
                })
        print("beauty_container == show_question [ 合并完成 ]")

    def insert_beauty_container(self, url: str):
        """
        新问题 id 插入到 beauty_container
        :param url: 问题对应链接
        :return:
        """
        if not (url.startswith("https://www.zhihu.com/question")
                or url.startswith("http://www.zhihu.com/question")):
            return False
        else:
            question_id = str(url.split("/")[4])
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
                items = self.beauty_container.find({"question_id": question_id})
                if items.count() == 0:
                    self.beauty_container.insert_one(question_dict)
                    return True
            return False

    def get_part_title(self, skip: int):
        """
        获取部分标题
        :param skip: 指针位置
        :return:
        """
        result = list()
        items = self.show_question.find().sort("_id", -1).limit(10).skip(skip)
        for item in items:
            del item["_id"]
            result.append(item)
        return result