# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from log import MyLog

class HtmlParser():
    """网页解析模块"""

    def __init__(self):
        """构造函数，初始化属性"""
        self.log = MyLog("html_parser", "logs")

    def get_resale_houses_data(self, html_cont, id):
        """获取二手房页面详细数据"""
        if html_cont is None:
            print("页面解析(detail)：传入页面为空！")
            return

        resale_houses_data = []
        communityName = "null"
        areaName = "null"
        total = "null"
        unitPriceValue = "null"

        bsObj = BeautifulSoup(html_cont, "html.parser", from_encoding="utf-8")

        tag_com = bsObj.find("div", {"class": "communityName"}).find("a")
        if tag_com is not None:
            communityName = tag_com.get_text()
        else:
            self.log.logger.error("页面解析(detail)：找不到communityName标签！")

        tag_area = bsObj.find("div", {"class": "areaName"}).find("span", {"class": "info"}).find("a")
        if tag_area is not None:
            areaName = tag_area.get_text()
        else:
            self.log.logger.error("页面解析(detail)：找不到areaName标签！")

        tag_total = bsObj.find("span", {"class": "total"})
        if tag_total is not None:
            total = tag_total.get_text()
        else:
            self.log.logger.error("页面解析(detail)：找不到total标签！")

        tag_unit = bsObj.find("span", {"class": "unitPriceValue"})
        if tag_unit is not None:
            unitPriceValue = tag_unit.get_text()
        else:
            self.log.logger.error("页面解析(detail)：找不到total标签！")

        resale_houses_data.append(id)
        resale_houses_data.append(communityName)
        resale_houses_data.append(areaName)
        resale_houses_data.append(total)
        resale_houses_data.append(unitPriceValue)

        counta = 12
        for a_child in bsObj.find("div", {"class": "introContent"}).find("div", {"class": "base"}).find("div", {
            "class": "content"}).ul.findAll("li"):
            [s.extract() for s in a_child("span")]
            resale_houses_data.append(a_child.get_text())
            counta = counta - 1

        while counta > 0:
            resale_houses_data.append("null")
            counta = counta - 1

        countb = 8
        for b_child in bsObj.find("div", {"class": "introContent"}).find("div", {"class": "transaction"}).find("div", {
            "class": "content"}).ul.findAll("li"):
            information = b_child.span.next_sibling.next_sibling.get_text()
            resale_houses_data.append(information)
            countb = countb - 1

        while countb > 0:
            resale_houses_data.append("null")
            countb = countb - 1

        self.log.logger.info("2.3 页面解析(detail)：页面解析成功！")
        print("2.3 页面解析(detail)：页面解析成功！")
        return resale_houses_data

    def get_resale_house_urls(self, html_content):
        """获取二手房页面的链接"""
        if html_content is None:
            self.log.logger.error("页面解析(page)：pg页面为空！")
            print("页面解析(page)：pg页面为空！")
            return

        resale_house_urls = set()
        bsObj = BeautifulSoup(html_content, "html.parser", from_encoding="utf-8")

        sellListContent = bsObj.find("ul", {"class": "sellListContent"})

        if sellListContent is not None:
            for child in sellListContent.children:
                if child["class"][0] == "clear":
                    resale_house_urls.add(child.a["href"])
                    self.log.logger.info(child.a["href"])
        else:
            self.log.logger.error("页面解析(page)：找不到sellListContent标签！")

        self.log.logger.info("1.3 PG页面解析：pg页面(列表页)解析成功！")
        print("1.3 页面解析：pg页面(列表页)解析成功！得到二手房详情页面链接！", len(resale_house_urls), "个")
        return resale_house_urls
