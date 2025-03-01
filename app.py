import os
import logging
import datetime

from fastapi import FastAPI, Response
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from bing_wrapper import BingWallpaperFetcher

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
project_root = os.path.abspath(os.path.dirname(__file__))
start_time = datetime.datetime.now()


def fetch_wallpaper(fetcher: BingWallpaperFetcher):
    logging.info("Fetching " + datetime.date.today().strftime(format="%Y%m%d"))
    image_name = fetcher.fetch()
    if not image_name:
        logging.error("Failed to fetch wallpaper")
    logging.info("Finished fetching wallpaper: %s" % image_name)


def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
    fetcher = BingWallpaperFetcher(project_root)
    fetch_wallpaper(fetcher)
    trigger = IntervalTrigger(days=1)
    scheduler.add_job(lambda: fetch_wallpaper(fetcher), trigger)
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def index():
    now = datetime.datetime.now()
    running_time = now - start_time
    running_time_str = "{}天".format(running_time.days)
    return Response(
        "Hello, I'm a happy wrapper dreaming of hang out with my lady, "
        "Miss Bing! 我已经运行" + running_time_str + "啦*V*",
        media_type="text/plain; charset=utf-8",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
