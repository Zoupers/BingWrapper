"""
@filename: WallpaperWrapper
@author: Zoupers
@createTime: 2022/1/1 10:36
@lastUpdate: 2025/9/28 17:56

方法一，通过以下接口
    cn.bing.com
    GET /hp/api/model HTTP/1.1
    Host: cn.bing.com
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0
    Accept: */*
    Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
    Accept-Encoding: gzip, deflate, br
    Referer: https://cn.bing.com/?mkt=zh-CN
    Content-type: application/json
    Connection: keep-alive
    Sec-Fetch-Dest: empty
    Sec-Fetch-Mode: no-cors
    Sec-Fetch-Site: same-origin
    DNT: 1
    Sec-GPC: 1
    TE: trailers
    Pragma: no-cache
    Cache-Control: no-cache
方法二
    https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc=1612409408851&pid=hp&FORM=BEHPTB&uhd=1&uhdwidth=3840&uhdheight=2160
"""

import os
import requests
import json
import datetime
import logging
from bing_wrapper.store import Store


logging.basicConfig(level=logging.INFO)


class BingWallpaperFetcher:
    def __init__(self, store_root: str = "."):
        self.root = "https://global.bing.com"
        self.region = "zh-CN"
        self.language = "zh"
        # 全球壁纸和中国壁纸不一样，另外在中国似乎访问不了全球壁纸
        # self.region = "en-US"
        # self.language = "en"
        self.url = (
            "https://global.bing.com/HPImageArchive.aspx"
            "?format=js&idx=0&n=1&nc=1612409408851&pid=hp"
            f"&FORM=BEHPTB&uhd=1&uhdwidth=3840&uhdheight=2160&setmkt={self.region}&setlang={self.language}"
        )
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; "
            "x64; rv:95.0) Gecko/20100101 Firefox/95.0",
            "Referer": "https://cn.bing.com/?mkt=zh-CN",
            "Host": "cn.bing.com",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        }
        self.store = Store(store_root)
        self.logger = logging.getLogger(self.__class__.__name__)

    def fetch(
        self,
        update_latest: bool = False,
        retry_count: int = 3,
        update_rss: bool = False,
        rss_max_items: int = 7,
        rss_raw_base_url: str = "",
    ):
        for idx in range(retry_count):
            try:
                res = requests.get(url=self.url, headers=self.headers)
                res_json = json.loads(res.text)
                break
            except requests.exceptions.RequestException as e:
                self.logger.error(f"第{idx + 1}次获取壁纸失败", exc_info=e)
                if idx == retry_count - 1:
                    return False
                continue
        image_info = res_json["images"][0]
        url = self.root + image_info["url"]
        pic_res = requests.get(url, headers=self.headers)
        image_name = image_info["copyright"].split("(")[0]
        today = datetime.datetime.now()
        save_name = (
            today.strftime("%Y%m%d")
            + "-"
            + image_name.strip()
            + "."
            + url.split("&")[1].split(".")[-1]
        )
        self.store.save_image(save_name, pic_res.content)
        if update_latest:
            self.store.save_image("latest.jpg", pic_res.content)
        if update_rss:
            from bing_wrapper.rss.models import Item

            rss = self.store.load_rss()
            image_link_url = os.path.join(
                rss_raw_base_url, self.store.get_reletive_image_path(save_name)
            )
            item = Item(
                title=today.strftime("%Y-%m-%d") + f" {image_info['title']}",
                description=image_info["copyright"],
                content=f'<img src="{image_link_url}" alt="{image_info["copyright"]}" />\n{image_info["copyright"]}',
                pubDate=today.strftime("%a, %d %b %Y %H:%M:%S %Z").strip(),
            )
            if len(rss.channel.items) >= rss_max_items:
                rss.channel.items = rss.channel.items[: rss_max_items - 1]
            rss.channel.items.insert(0, item)
            self.store.save_rss(rss)

        return save_name


if __name__ == "__main__":
    fetcher = BingWallpaperFetcher()
    if not fetcher.fetch():
        exit(1)
