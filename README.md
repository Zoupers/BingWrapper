# Bing Wallpaper Wrapper

专门每天爬必应壁纸的，没错，就这

## 使用

1. 直接通过app.py运行`python ./app.py`, 默认运行在127.0.0.1:8000，并且每天爬取一次壁纸
2. 通过`python -m bing_wrapper`运行，每次会爬取当天的壁纸，并保存到`./images`目录下

## 开发

本项目使用`uv`管理依赖，安装好uv后，通过`uv sync`安装依赖，暂时还没有测试.