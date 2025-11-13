from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
import trafilatura
from concurrent.futures import ThreadPoolExecutor
from .config import settings
from .utils import retry, log
import logging

log = logging.getLogger(__name__)

HEADERS = {"User-Agent": settings.user_agent}


class Fetcher:
    def __init__(self):
        pass

    @retry(times=3, delay=1)
    def fetch_article(self, url: str, config: Optional[Dict] = None) -> List[Dict]:
        """
        抓取一个网页中的多个文章块（适用于新闻首页或列表页）。
        每个结果包含 title, content(简短摘要), link, source。

        config 可选项：
            - headers: dict，自定义请求头
            - timeout: int，请求超时时间
            - encoding: str，指定网页编码
            - selectors: dict，自定义CSS选择器
        """
        config = config or {}
        headers = config.get("headers", HEADERS)
        timeout = config.get("timeout", 10)
        encoding = config.get("encoding")
        selectors = config.get("selectors", {
            "item": "article, .post, .news-item, li, .entry",
            "title": "h2, h3, a.title, .entry-title a",
            "summary": "p, .summary, .desc",
            "link_attr": "href"
        })

        try:
            r = requests.get(url, headers=headers, timeout=timeout)
            r.raise_for_status()
            if encoding:
                r.encoding = encoding

            soup = BeautifulSoup(r.text, "lxml")

            results = []
            for item in soup.select(selectors["item"]):
                title_tag = item.select_one(selectors["title"])
                summary_tag = item.select_one(selectors["summary"])

                title = title_tag.get_text(strip=True) if title_tag else ""
                summary = summary_tag.get_text(strip=True) if summary_tag else ""
                link = (
                    title_tag.get(selectors["link_attr"])
                    if title_tag and title_tag.has_attr(selectors["link_attr"])
                    else ""
                )

                # 若 link 是相对路径，则拼接成完整 URL
                if link and link.startswith("/"):
                    from urllib.parse import urljoin
                    link = urljoin(url, link)

                if title:
                    results.append({
                        "title": title,
                        "content": summary,
                        "link": link or url,
                        "source": url
                    })

            # 如果没提取出结果，则使用 trafilatura 尝试提取全文
            if not results:
                extracted = trafilatura.extract(r.text)
                if extracted:
                    results = [{
                        "title": soup.title.string if soup.title else "",
                        "content": extracted[:500],
                        "link": url,
                        "source": url
                    }]

            return results

        except Exception as e:
            log.error(f"Failed to fetch {url}: {e}")
            return []

    def fetch_from_sources(self, sources: List[Dict], min_length: int = 200) -> List[Dict]:
        """
        sources = [
            {"url": "https://www.example.com", "config": {...}},
            {"url": "https://www.another.com", "config": {...}}
        ]
        """
        results = []

        def fetch_one(s):
            try:
                articles = self.fetch_article(s["url"], s.get("config"))
                return articles
            except Exception as e:
                log.error(f"Failed to fetch {s.get('url')}: {e}")
                return []

        with ThreadPoolExecutor(max_workers=5) as executor:
            for res in executor.map(fetch_one, sources):
                results.extend(res)
                
        return results


if __name__ == "__main__":
    fetcher = Fetcher()

    # ✅ 测试单个网页抓取
    test_url = "https://it.ithome.com/"
    config = {
    "encoding": "utf-8",
    "selectors": {
        # 每条新闻块的外层（标题所在）
        "item": "div.c",
        # 标题选择器（通常是 a 或 h2 a）
        "title": "a, h2 a, h3 a",
        # 摘要选择器 —— 紧邻 .c 的 .m
        "summary": "div.m, .m p",
        # 链接属性
        "link_attr": "href"
    }
}

    articles = fetcher.fetch_article(test_url, config)

    print(f"抓取 {test_url} 共 {len(articles)} 条：")
    for i, art in enumerate(articles[:5]):
        print(f"\n[{i+1}] {art['title']}")
        print(f"摘要: {art['content'][:150]}...")
        print(f"链接: {art['link']}")

    # ✅ 测试多源抓取
    sources = [
        {"url": "https://it.ithome.com/", "config": config}
    ]
    all_articles = fetcher.fetch_from_sources(sources)
    print("\n\n多源抓取结果预览：")
    for i, art in enumerate(all_articles[:5]):
        print(f"\n[{i+1}] {art['title']}")
        print(f"摘要: {art['content'][:150]}...")
        print(f"链接: {art['link']}")
    print(f"\n总共抓取到 {len(all_articles)} 条文章。")
