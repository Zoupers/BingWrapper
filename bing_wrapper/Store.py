"""
@filename: Store
@author: Zoupers
@createTime: 2022/1/1 10:40
@lastUpdate: 2022/1/1 10:40
@info: 存储器
"""

import os


class Store:
    def __init__(self, root: str = "", images_root: str = "images"):
        if root:
            self.project_root = root
        else:
            self.project_root = os.path.abspath(os.path.join(__file__, ".."))
        self.images_root = os.path.join(self.project_root, images_root)
        if not os.path.exists(self.images_root):
            os.mkdir(self.images_root)

    def saveBinary(self, filename: str, binary: bytes):
        try:
            with open(os.path.join(self.images_root, filename), "wb") as f:
                f.write(binary)
        except Exception as e:
            print(e)
            return False
        return True


if __name__ == "__main__":
    store = Store()
