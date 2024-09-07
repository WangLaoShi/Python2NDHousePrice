# -*- coding: utf-8 -*-
import random
import time

from html_downloader import HtmlDownloader
from html_parser import HtmlParser
from url_manager import UrlManager
from utils import save_set_to_csv

class SpiderMain():
    """爬虫程序主模块"""

    def __init__(self):
        """构造函数，初始化属性"""
        self.urls = UrlManager()
        self.downloader = HtmlDownloader()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()

    def crawl(self, root_url):
        """爬虫入口函数"""
        # 前面是区域，后面是页面数（程序运行时给的固定值）
        areas = {
            "gulou": 5,
            "jianye": 2,
            "qinhuai": 1,
            "xuanwu": 6,
            "yuhuatai": 3,
            "qixia": 2,
            "baijiahu": 3,
            "chalukou1": 2,
            "jiangningqita11": 3,
            "dongshanzhen": 2,
            "jiangningdaxuecheng": 1,
            "jiulonghu": 2,
            "jiangjundadao11": 2,
            "kexueyuan": 9,
            "qilinzhen": 2,
            "tiexinqiao": 9,
            "pukou": 1,
            "liuhe": 1,
        }

        # 1、抓取所有二手房详情界面链接，并将所有连接放入URL管理模块
        for area, pg_sum in areas.items():
            for num in range(1, pg_sum + 1):
                # 1.1 拼接页面地址: https://nj.lianjia.com/ershoufang/gulou/pg2/
                pg_url = root_url + area + "/pg" + str(num) + "/"
                print("1.1 拼接页面地址：" + pg_url)
                # 1.2 启动下载器,下载页面.
                try:
                    # 暂停0~3秒的整数秒，时间区间：[0,3]
                    time.sleep(random.randint(0, 3))
                    html_content = self.downloader.download(pg_url)
                except Exception as e:
                    print("1.2 下载页面出现异常:" + repr(e))
                    time.sleep(60 * 30)
                else:
                    # 1.3 解析PG页面，获得二手房详情页面的链接,并将所有链接放入URL管理模块
                    try:
                        resale_house_urls = self.parser.get_resale_house_urls(html_content)
                    except Exception as e:
                        print("1.3 页面解析出现异常:" + repr(e))
                    else:
                        self.urls.add_new_urls(resale_house_urls)
                        print("1.3 页面解析成功，已将二手房详情页面的链接放入URL管理模块,目前有" + str(len(self.urls.new_urls)) + "个链接")
                        # 暂停0~3秒的整数秒，时间区间：[0,3]
                        time.sleep(random.randint(0, 3))

        save_set_to_csv(self.urls.new_urls, "resale_house_urls.csv")

if __name__ == "__main__":
    # 设定爬虫入口URL
    root_url = "https://nj.lianjia.com/ershoufang/"
    # 初始化爬虫对象
    obj_spider = SpiderMain()
    # 启动爬虫
    obj_spider.crawl(root_url)
