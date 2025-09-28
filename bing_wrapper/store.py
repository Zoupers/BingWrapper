"""
@filename: store
@author: Zoupers
@createTime: 2022/1/1 10:40
@lastUpdate: 2025/9/28 18:05
@info: 存储器
"""

import os
from bing_wrapper.rss.models import Rss


class Store:
    def __init__(self, root: str = "", images_root: str = "images"):
        if root:
            self.project_root = root
        else:
            self.project_root = os.path.abspath(os.path.join(__file__, ".."))
        self.images_root = os.path.join(self.project_root, images_root)
        if not os.path.exists(self.images_root):
            os.mkdir(self.images_root)

    def save_image(self, filename: str, binary: bytes):
        try:
            with open(os.path.join(self.images_root, filename), "wb") as f:
                f.write(binary)
        except Exception as e:
            print(e)
            return False
        return True

    def get_reletive_image_path(self, filename):
        return os.path.relpath(
            os.path.join(self.images_root, filename), self.project_root
        )

    def load_rss(self, filename="rss.xml"):
        with open(os.path.join(self.project_root, filename), "rb") as f:
            rss = Rss.from_xml(f.read())
        return rss

    def save_rss(self, rss: Rss, filename="rss.xml"):
        with open(os.path.join(self.project_root, filename), "wb") as f:
            f.write(rss.to_xml())


if __name__ == "__main__":
    store = Store()
