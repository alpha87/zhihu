![宅宅生活收藏夹](https://user-images.githubusercontent.com/25655581/61578375-829ed680-ab28-11e9-92b0-b8bde03d500a.png)

------

之前做过一个小程序项目，不过被用户投诉了。

所以开发了网页版（感觉没小程序好用啊）。

之前写过一篇日志记录小程序项目的开发心得：[宅宅生活收藏夹——项目心得](https://lijianxun.top/?p=17)

思路很简单，就是爬虫抓数据，保存到 mongo 数据库，使用 flask 展示，css 框架用的 bulma。

如何部署见：[使用FLASK，NGINX，GUNICORN，SUPERVISOR完成网站部署](https://lijianxun.top/?p=28)

------

**功能**

 - [ ] 首页异步加载展示数据
 - [ ] 详情页使用 API 异步加载数据
 - [ ] navbar 搜索框可以使用关键词搜索标题
 - [ ] 提供页面搜索框以 get 请求提交用户链接
 