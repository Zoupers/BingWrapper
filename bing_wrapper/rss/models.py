"""
@filename: models
@author: Zoupers
@createTime: 2025/9/28 16:13
@lastUpdate: 2025/9/28 18:05
@info: RSS模型
"""

from typing import List, Optional, Literal
from pydantic import constr
from pydantic_xml import BaseXmlModel, attr, element, wrapped

# RSS 2.0 规范: https://cyber.harvard.edu/rss/rss.html

# -------------------------
# Item 子元素模型
# -------------------------


class Enclosure(BaseXmlModel, tag="enclosure"):
    """
    <enclosure> 是 <item> 的可选子元素，用于附加媒体对象。
    它的所有字段都是属性。
    """

    url: str = attr()  # 属性 (必选)
    length: int = attr()  # 属性 (必选)
    type: str = attr()  # 属性 (必选)


class Guid(BaseXmlModel, tag="guid"):
    """
    <guid> 是 <item> 的可选子元素，是项目的唯一标识符。
    """

    value: str = constr()  # 文本内容 (必选)
    isPermaLink: bool = attr(default=True)  # 属性 (可选, 默认为 true)


class Source(BaseXmlModel, tag="source"):
    """
    <source> 是 <item> 的可选子元素，指明项目来源的 RSS 频道。
    """

    value: str = constr()  # 文本内容 (必选)
    url: str = attr()  # 属性 (必选)


class Category(BaseXmlModel, tag="category"):
    """
    <category> 元素，可用于 <channel> 和 <item>。
    """

    value: str = constr()  # 文本内容
    domain: Optional[str] = attr()  # 属性 (可选)


# -------------------------
# Channel 子元素模型
# -------------------------


class Image(BaseXmlModel, tag="image"):
    """
    <image> 是 <channel> 的可选子元素，用于显示一个与频道关联的图像。
    """

    url: str = element()  # 子元素 (必选)
    title: str = element()  # 子元素 (必选)
    link: str = element()  # 子元素 (必选)
    width: Optional[int] = element(default=88)  # 子元素 (可选, 默认 88)
    height: Optional[int] = element(default=31)  # 子元素 (可选, 默认 31)
    description: Optional[str] = element()  # 子元素 (可选)


class TextInput(BaseXmlModel, tag="textInput"):
    """
    <textInput> 是 <channel> 的可选子元素，用于显示一个文本输入框。
    """

    title: str = element()  # 子元素 (必选)
    description: str = element()  # 子元素 (必选)
    name: str = element()  # 子元素 (必选)
    link: str = element()  # 子元素 (必选)


class Cloud(BaseXmlModel, tag="cloud"):
    """
    <cloud> 是 <channel> 的可选子元素，用于通知更新。
    它的所有字段都是属性。
    """

    domain: str = attr()  # 属性 (必选)
    port: int = attr()  # 属性 (必选)
    path: str = attr()  # 属性 (必选)
    registerProcedure: str = attr()  # 属性 (必选)
    protocol: str = attr()  # 属性 (必选)


# -------------------------
# 主要模型
# -------------------------


class Item(BaseXmlModel, tag="item"):
    """
    <item> 代表频道中的一个独立条目，如一篇新闻或博客文章。
    """

    title: Optional[str] = element(
        default=None
    )  # 子元素 (可选, 但 title 或 description 必须至少有一个)
    link: Optional[str] = element(default=None)  # 子元素 (可选)
    description: Optional[str] = element(
        default=None
    )  # 子元素 (可选, 但 title 或 description 必须至少有一个)
    author: Optional[str] = element(default=None)  # 子元素 (可选)
    categories: List[Category] = element(
        tag="category", default=[]
    )  # 子元素列表 (可选)
    comments: Optional[str] = element(default=None)  # 子元素 (可选)
    enclosure: Optional[Enclosure] = element(default=None)  # 子元素 (可选)
    guid: Optional[Guid] = element(default=None)  # 子元素 (可选)
    pubDate: Optional[str] = element(default=None)  # 子元素 (可选)
    source: Optional[Source] = element(default=None)  # 子元素 (可选)
    content: Optional[str] = element(tag="content")


class Channel(BaseXmlModel, tag="channel"):
    """
    <channel> 包含关于频道（feed）的元数据和内容。
    """

    # 必选子元素
    title: str = element()
    link: str = element()
    description: str = element()

    # 可选子元素
    language: Optional[str] = element(default=None)
    copyright: Optional[str] = element(default=None)
    managingEditor: Optional[str] = element(default=None)
    webMaster: Optional[str] = element(default=None)
    pubDate: Optional[str] = element(default=None)
    lastBuildDate: Optional[str] = element(default=None)
    categories: Optional[List[Category]] = element(tag="category", default=None)
    generator: Optional[str] = element(default=None)
    docs: Optional[str] = element(default="http://www.rssboard.org/rss-specification")
    cloud: Optional[Cloud] = element(default=None)
    ttl: Optional[int] = element(tag="ttl", default=None)  # Time To Live
    image: Optional[Image] = element(default=None)
    textInput: Optional[TextInput] = element(default=None)

    # 特殊的列表包装
    skipHours: Optional[List[int]] = wrapped(
        "skipHours", element(tag="hour", default=None)
    )
    skipDays: Optional[List[str]] = wrapped(
        "skipDays", element(tag="day", default=None)
    )

    # item 列表
    items: List[Item] = element(tag="item", default=[])


class Rss(BaseXmlModel, tag="rss"):
    """
    RSS 文档的根元素。
    """

    version: Literal["2.0"] = attr(default="2.0")  # 属性 (必选, 固定为 '2.0')
    channel: Channel = element()  # 子元素 (必选)
