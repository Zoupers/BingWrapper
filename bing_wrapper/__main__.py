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
        "--update-rss", action="store_true", default=False, help="更新rss.xml文件"
    )
    parser.add_argument(
        "--rss-max-items", type=int, default=7, help="rss文件中的item最多保留数量"
    )
    parser.add_argument("--raw-base-url", type=str, default="", help="文件链接基础路径")
    parser.add_argument(
        "--retry-count",
        type=int,
        default=3,
        help="重试次数",
    )
    args = parser.parse_args()
    fetcher = BingWallpaperFetcher()
    if not fetcher.fetch(
        update_latest=args.update_latest,
        retry_count=args.retry_count,
        update_rss=args.update_rss,
        rss_max_items=args.rss_max_items,
        rss_raw_base_url=args.raw_base_url,
    ):
        exit(1)
