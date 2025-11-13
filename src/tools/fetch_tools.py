import os
import yaml
from pathlib import Path
from typing import List
from pydantic import BaseModel
from langchain.tools import tool
from .BaseModel import Article,FetchNewsArgs  
from ..fetcher import Fetcher

# 从环境变量读取路径（默认路径为 ../asset/news_sources.yaml）
SOURCES_FILE = os.getenv(
    "NEWS_SOURCES_FILE",
    str(Path(__file__).parent / "../asset/news_sources.yaml")
)
# 读取 YAML 文件
with open(SOURCES_FILE, "r", encoding="utf-8") as f:
    NEWS_SOURCES = yaml.safe_load(f)

fetcher = Fetcher()


# 工具函数
def parse_query_to_sources(query: str) -> List[dict]:
    """
    根据用户自然语言 query 匹配新闻源
    优先 name 匹配，如果 name 匹配成功，则不考虑 tag 匹配
    """
    query_lower = query.lower()
    matched_sources = []

    for source in NEWS_SOURCES:
        name_match = source["name"].lower() in query_lower
        if name_match:
            matched_sources.append(source)
            continue  # 如果 name 匹配成功，就不检查 tag 了

        tag_match = any(tag.lower() in query_lower for tag in source.get("tags", []))
        if tag_match:
            matched_sources.append(source)

    return matched_sources

# 工具函数定义
@tool("fetch_news", return_direct=False, args_schema=FetchNewsArgs)
def fetch_news(query) -> List[Article]:
    """
    抓取新闻内容。
    query: keywords or news source names in natural language.
    返回 list[dict]
    """
    matched_sources = parse_query_to_sources(query)

    if not matched_sources:
        return []  # 没匹配到新闻源

    results = fetcher.fetch_from_sources(matched_sources)
    articles = []
    for r in results:
        articles.append(
            Article(
                title=r.get("title", ""),
                summary=r.get("summary", ""),
                link = r.get("link", "")
            )
        )
    return articles

if __name__ == "__main__":
    # 测试抓取工具,测试前请注释 line45 @tool("fetch_news", return_direct=False, args_schema=FetchNewsArgs)
    test_query = "请抓取机器人新闻"
    articles = fetch_news(test_query)
    for art in articles:
        print(art.title,"\n\n", art.summary,"\n",art.link,"\n\n")
    print(f"共抓取到 {len(articles)} 篇文章。")