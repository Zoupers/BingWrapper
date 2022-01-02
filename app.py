import datetime
import os

from flask import Flask
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from src.WallpaperWrapper import WallpaperWrapper

project_root = os.path.abspath(".")
start_time = datetime.datetime.now()
app = Flask(__name__)


def fetch_wallpaper(ww):
    print("Fetching", datetime.date.today().strftime(format="%Y%m%d"))
    ww.fetch()
    print("Finished")


def schedule():
    scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
    ww = WallpaperWrapper(root=project_root)
    ww.fetch()
    trigger = IntervalTrigger(days=1)
    scheduler.add_job(lambda: fetch_wallpaper(ww), trigger)
    scheduler.start()


@app.route('/')
def index():
    now = datetime.datetime.now()
    running_time = now - start_time
    running_time_str = "{}天".format(running_time.days)
    return 'Hello, I\'m a happy wrapper dreaming of hang out with my lady, ' \
           'Miss Bing! 我已经运行' + running_time_str + '啦*V*'


if __name__ == '__main__':
    print("starting scheduler")
    schedule()
    print("start flask")
    app.run()
