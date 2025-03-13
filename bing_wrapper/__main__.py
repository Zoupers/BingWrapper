from argparse import ArgumentParser
from bing_wrapper import BingWallpaperFetcher

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--update-latest",
        action="store_true",
        default=False,
        help="更新latest.jpg文件",
    )
    parser.add_argument(
        "--retry-count",
        type=int,
        default=3,
        help="重试次数",
    )
    args = parser.parse_args()
    fetcher = BingWallpaperFetcher()
    if not fetcher.fetch(
        update_latest=args.update_latest, retry_count=args.retry_count
    ):
        exit(1)
