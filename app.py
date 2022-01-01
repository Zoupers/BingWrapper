import datetime
import os

from flask import Flask
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.WallpaperWrapper import WallpaperWrapper

project_root = os.path.abspath(".")
start_time = datetime.datetime.now()
app = Flask(__name__)

def schedule():
    scheduler = AsyncIOScheduler()
    ww = WallpaperWrapper(root=project_root)
    ww.fetch()
    trigger = IntervalTrigger(days=1)
    scheduler.add_job(lambda: ww.fetch(), trigger)
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
