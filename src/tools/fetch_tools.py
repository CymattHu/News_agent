from langchain.tools import tool
from ..fetcher import Fetcher

fetcher = Fetcher()

@tool("fetch_news", return_direct=False)
def fetch_news(sources: list) -> list:
    """
    抓取新闻内容。
    sources: list of dicts or url strings. 支持 [{'type': 'rss', 'url': '...'}, 'https://...']
    返回 list[dict]
    """
    normalized = []
    for s in sources:
        if isinstance(s, str):
            normalized.append({"type": "rss", "url": s})
        else:
            normalized.append(s)
    results = fetcher.fetch_from_sources(normalized)
    return results
