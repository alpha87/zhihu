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
from flask import Flask, render_template, request, jsonify
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


# ------------------------
# 万能好评模板 调用接口

@app.route("/thanks")
def thanks():
    return jsonify(
        {
            "data": [
                {
                    "name": "Ash.",
                    "money": 10
                },
                {
                    "name": "柒月的風",
                    "money": 10
                },
                {
                    "name": "？！",
                    "money": 5
                },
                {
                    "name": "英俊侠",
                    "money": 3
                },
                {
                    "name": "log",
                    "money": 3
                },
                {
                    "name": "乔克叔叔",
                    "money": 1
                },
                {
                    "name": "丘比特",
                    "money": 1
                }
            ]
        }
    )

@app.route("/comment/list")
def comment_list():
    return jsonify(
        [
            "发货很快，跟在超市买的一样，大牌子，品质不用质疑，正好做活动，比在超市买的便宜很多，开始不敢买那么多，先买了4包，吃了之后果断又买几包，独立包装，干净卫生，核桃大枣更大，吃着过瘾，东西也很新鲜，口感好，老人和孩子都很喜欢吃，强烈推荐",
            "质量非常好，颜色好看，款式时尚漂亮，宝贝自己也很喜欢。这个袜子穿上舒服弹性又大，大小也合适，小孩也比较喜欢，颜色好看，摸上去手感好，面料很柔软，袜子做工精致，透气性好，非常不错，很棒的小袜子，非常的可爱，很满意哦~",
            "面对商家各种形式、各种节点或脑洞大开、或狂轰滥炸、或坑蒙拐骗等等等等等等等的促销大法，我自认为我的脑细胞已经跟不上了。还好有强大的设备在手，还好有伟大的互联网同胞为伍。我倡议大家以后一定要把买货截图附在评论区图片内，这样就可以为广大的卖家们和买家们节省很多很多的脑细胞，相信借助大家的努力我们的购物环境会越来越好！越来越好，啦啦啦啦～～越来越好，啦啦啦啦～～马爸爸，我这次评论的字数够了么？"
        ]
    )


if __name__ == '__main__':
    app.run(debug=True)