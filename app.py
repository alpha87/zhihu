#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 - Time: 2019/9/19 1:13 下午
 - Author: Jianxun
 - File: app.py
 - Website: https://lijianxun.top
 - Email: jianxun2004@gmail.com
 - Description:
   - 网页入口。
"""
import math
from flask import Flask, render_template, request
from src.db import ZhihuData


def after_request(response):
    response.headers['Referer'] = 'https://www.zhihu.com/'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response


app = Flask(__name__)
app.after_request(after_request)
db = ZhihuData()


@app.route('/')
def index():
    """
    首页
    :return:
    """
    page = int(request.args.get("page", 0))
    page = page + 1
    skip = (page-1)*10
    result = db.get_part_title(skip=skip)
    count = float(db.find_all_title_count())
    max_page = math.ceil(count/10)
    return render_template(
        "index.html",
        result=result,
        page=page,
        max_page=max_page
    )


@app.route("/thanks")
def thanks():
    """
    赞赏作者
    :return:
    """
    return render_template("thanks.html")


@app.route("/share")
def share():
    """
    我要提供
    :return:
    """
    return render_template("share.html")


@app.route("/detail")
def detail():
    """
    详情页
    :return:
    """
    qid = request.args.get("question_id", 1)
    page = int(request.args.get("page", 0))
    page = page + 1
    skip = (page - 1) * 10
    result = db.find(_skip=skip, qid=qid)
    count = float(db.find_qid_count(qid=qid))
    max_page = math.ceil(count / 10)
    return render_template("detail.html", result=result,
                           page=page, max_page=max_page)


if __name__ == '__main__':
    app.run(debug=True)
