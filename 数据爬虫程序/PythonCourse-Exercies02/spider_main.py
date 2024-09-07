# -*- coding: utf-8 -*-
import random
import time

from html_downloader import HtmlDownloader
from html_outputer import HtmlOutputer
from url_manager import UrlManager
from html_parser import HtmlParser
from utils import save_set_to_csv

class SpiderMain():
    """爬虫程序主模块"""

    def __init__(self):
        """构造函数，初始化属性"""
        self.urls = UrlManager()
        self.downloader = HtmlDownloader()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.outputer = HtmlOutputer()

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

    def crawl_each_page(self):
        '''
        如果想要让程序重新爬取列表页面的话，可以删除resale_house_urls.csv文件
        当resale_house_urls.csv文件存在时，程序会从该文件中读取二手房详情页面的链接
        '''
        # 2、解析二手房具体页面
        id = 1
        stop = 1
        # 2.1 从文件中读取二手房详情页面的链接
        self.urls.add_new_urls_from_csv("resale_house_urls.csv")
        print("2.1 从文件中读取二手房详情页面的链接，目前有" + str(len(self.urls.new_urls)) + "个链接")

        # 为了操作方便，我们在课堂上授课的时候，取其中的 10 条来进行抓取
        while self.urls.has_new_url() and id < 11:# while self.urls.has_new_url():
            # 2.1 获取url
            try:
                detail_url = self.urls.get_new_url()
                print("2.1 二手房页面地址：" + detail_url)
            except Exception as e:
                print("2.1 拼接地址出现异常:" + detail_url + repr(e))

            # 2.2 下载页面
            try:
                detail_html = self.downloader.download(detail_url)
            except Exception as e:
                print("2.2 下载页面出现异常:" + repr(e))
                self.urls.add_new_url(detail_url)
                # time.sleep(60 * 30)
            else:
                # 2.3 解析页面
                try:
                    ershoufang_data = self.parser.get_resale_houses_data(detail_html, id)
                except Exception as e:
                    print("2.3 解析页面出现异常:" + repr(e))
                else:
                    # 2.4 输出数据
                    try:
                        self.outputer.collect_data(ershoufang_data)
                    except Exception as e:
                        print("2.4 输出数据出现异常:" + repr(e))
                    else:
                        print(id)
                        id = id + 1
                        stop = stop + 1
                        # 暂停0~3秒的整数秒，时间区间：[0,3]
                        time.sleep(random.randint(0, 3))
                        if stop == 2500:
                            stop = 1;
                            time.sleep(60 * 20)


if __name__ == "__main__":
    # 设定爬虫入口URL
    root_url = "https://nj.lianjia.com/ershoufang/"
    # 初始化爬虫对象
    obj_spider = SpiderMain()
    # 启动爬虫
    # obj_spider.crawl(root_url)
    obj_spider.crawl_each_page()