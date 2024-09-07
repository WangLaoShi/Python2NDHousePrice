# -*- coding: utf-8 -*-
import random

import requests

class HtmlDownloader():
    """网页加载器"""

    def __init__(self):
        """构造函数，初始化属性"""
        self.user_agent = [
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; InfoPath.2; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; 360SE) ",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0) ",
            "Mozilla/5.0 (Windows NT 5.1; zh-CN; rv:1.9.1.3) Gecko/20100101 Firefox/8.0",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; TencentTraveler 4.0; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
        ]

    def download(self, url):
        """网页下载函数"""
        if url is None:
            return None

        # 随机变换user-agent
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Host": "nj.lianjia.com",
            "User-Agent": random.choice(self.user_agent)
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"{url}页面下载：失败!")
            print(f"状态码：{response.status_code}")
            print(f"页面内容：{response.text}")
            print(f"页面头部：{response.headers}")
            print(f"页面编码：{response.encoding}")
            print(f"页面请求头：{response.request.headers}")
            print(f"页面cookies：{response.cookies}")
            return None

        print(f"{url}页面下载：成功!")
        return response.text
