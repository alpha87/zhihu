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
from flask import Flask, render_template, request
from src.db import ZhihuData

app = Flask(__name__)
db = ZhihuData()

@app.route('/')
def index():
    """
    首页
    :return:
    """
    _skip = request.args.get("skip", None)
    skip = int(_skip) if _skip else 0
    result = db.get_part_title(skip=skip)
    return render_template("index.html", result=result)


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
    return render_template("detail.html")


if __name__ == '__main__':
    app.run(debug=True)
