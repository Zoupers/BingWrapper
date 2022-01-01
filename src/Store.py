"""
@filename: Store
@author: Zoupers
@createTime: 2022/1/1 10:40
@lastUpdate: 2022/1/1 10:40
@info: 存储器
"""
import os
import sys
import requests


class Store:
    def __init__(self, root):
        if root:
            self.project_root = root
        else:
            self.project_root = os.path.abspath('..')
        self.images_root = os.path.join(self.project_root, "images")
        if not os.path.exists(self.images_root):
            os.mkdir(self.images_root)

    def saveBinary(self, filename, binary):
        try:
            with open(os.path.join(self.images_root, filename), 'wb') as f:
                f.write(binary)
        except Exception as e:
            print(e)
            return False
        return True

    def saveFromURL(self, url):
        res = requests.get(url)


if __name__ == '__main__':
    store = Store()
