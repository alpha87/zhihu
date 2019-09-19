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
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    """
    首页
    :return:
    """
    return render_template("index.html")


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


if __name__ == '__main__':
    app.run(debug=True)
