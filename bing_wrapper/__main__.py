from argparse import ArgumentParser
from bing_wrapper import BingWallpaperFetcher

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--update-latest", action="store_true", default=False, help="更新latest.jpg文件"
    )
    args = parser.parse_args()
    fetcher = BingWallpaperFetcher()
    fetcher.fetch(update_latest=args.update_latest)
