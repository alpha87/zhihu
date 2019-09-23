#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 - Time: 2019-06-25 19:24
 - Author: Jianxun
 - Site: https://lijianxun.top
 - File: spider.py
 - Software: PyCharm
 - Description:
   - 知乎未被折叠回答的爬虫。
"""
import time
import json
from random import randint, choice
from urllib.parse import quote

import requests
from lxml import etree
from .headers import HEADERS_LIST


class ZhihuSpider(object):

    def __init__(self, question_id, db):
        # 数据库初始化
        self.db = db

        # 问题
        self.question_id = question_id

        # 爬虫配置
        self.offset = 0
        self.limit = 20

        # 屏蔽以下用户
        self.filter_user_id = (
            # 小蛋卷
            "f68865d933a644763d9a2994ea04b887",
            # 良药
            "5ba6540eaf55c110b8540848797ff373",
            # ------
            # 奔跑的大基蛋
            "c06d8f3556dfaed081cffe7687b530bf"
        )

    @staticmethod
    def random_sleep():
        time.sleep(randint(2, 5))

    def spider_info(self):
        """复用请求"""

        parameters = {
            "question_id": self.question_id,
            "include": quote(
                "data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info,paid_info_content;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics"),
            "offset": self.offset,
            "limit": self.limit,
            # default: 默认顺序；updated: 时间顺序
            "sort_by": "updated",
            # "platform": "desktop"  # 使用时间顺序注释这个参数
        }

        url = "https://www.zhihu.com/api/v4/questions/{question_id}/answers?include={include}&offset={offset}&limit={limit}&sort_by={sort_by}".format(
            **parameters)

        headers = choice(HEADERS_LIST)
        return url, headers

    def get_total(self):
        """获取回答总数"""

        url, headers = self.spider_info()
        self.random_sleep()
        response = json.loads(requests.get(url, headers=headers).text)
        return response["paging"]["totals"]

    def pages(self):
        """计算爬取页数"""

        total = self.get_total()
        page = int(total / self.limit)
        if total % self.limit != 0:
            page += 1
        return page

    def crawler(self):
        """获取API接口数据"""

        url, headers = self.spider_info()
        self.random_sleep()
        print(self.offset)
        self.offset = self.offset + self.limit
        return json.loads(requests.get(url, headers=headers).text)

    def parse_response(self, response):
        """解析返回的数据"""

        # 该问题得所有回答
        all_data = response["data"]
        for data in all_data:
            question_item = data["question"]
            author_item = data["author"]
            if author_item["id"] not in self.filter_user_id:
                item = {
                    # 问题相关
                    "title": question_item["title"],
                    "question_id": question_item["id"],

                    # 作者相关
                    "user_id": author_item["id"],
                    "user_token": author_item["url_token"],
                    "name": author_item["name"],
                    "avatar_url": self.fine_definition(author_item["avatar_url"]),
                    "headline": author_item["headline"],

                    # 答案相关
                    "answer_id": data["id"],
                    "vote_count": data["voteup_count"],
                    "created_time": data["created_time"],
                    "updated_time": data["updated_time"],
                    "content": self.parse_content(data["content"])
                }

                if self.db.find_answer_id_count(data["id"]) == 0:
                    if item["content"]:
                        self.db.insert_db(item)
                else:
                    # 更新回答
                    if item["content"]:
                        self.db.update_one(
                            question_id=question_item["id"],
                            answer_id=data["id"],
                            item=item
                        )

    @staticmethod
    def fine_definition(avatar_url: str):
        """获取用户高清头像"""

        return avatar_url.replace("_is", "_xll")

    @staticmethod
    def parse_content(content):
        """
        解析答案中的 content，直接解析图片
        :param content: data["content"]
        :return: img list
        """

        if "<img " in content:
            img_list = set(etree.HTML(content).xpath("//img/@data-original"))
            if not img_list:
                img_list = [img_url
                            for img_url
                            in set(etree.HTML(content).xpath("//img/@src"))
                            if img_url.startswith("http")]
            return list(img_list)
        else:
            return []

    def run(self):
        pages = self.pages()
        print("共{}页".format(pages))
        for page in range(pages):
            resp = self.crawler()
            self.parse_response(resp)