"""
@filename: WallpaperWrapper
@author: Zoupers
@createTime: 2022/1/1 10:36
@lastUpdate: 2022/1/1 10:36

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

import requests
import json
import datetime
import logging
from .Store import Store


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

    def fetch(self, update_latest: bool = False, retry_count: int = 3):
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
        url = self.root + res_json["images"][0]["url"]
        pic_res = requests.get(url, headers=self.headers)
        image_name = res_json["images"][0]["copyright"].split("(")[0]
        save_name = (
            datetime.date.today().strftime("%Y%m%d")
            + "-"
            + image_name.strip()
            + "."
            + url.split("&")[1].split(".")[-1]
        )
        self.store.saveBinary(save_name, pic_res.content)
        if update_latest:
            self.store.saveBinary("latest.jpg", pic_res.content)
        return save_name


if __name__ == "__main__":
    fetcher = BingWallpaperFetcher()
    if not fetcher.fetch():
        exit(1)
