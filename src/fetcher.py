from typing import List, Dict
import feedparser
import requests
from newspaper import Article
from bs4 import BeautifulSoup
from .config import settings
from .utils import retry, log

HEADERS = {"User-Agent": settings.user_agent}

class Fetcher:
    def __init__(self):
        pass

    @retry(times=3, delay=1)
    def fetch_rss(self, rss_url: str) -> List[Dict]:
        feed = feedparser.parse(rss_url)
        items = []
        for e in feed.entries:
            items.append({
                "title": e.get("title"),
                "link": e.get("link"),
                "published": e.get("published", None),
                "summary": e.get("summary", ""),
                "source": rss_url
            })
        return items

    @retry(times=3, delay=1)
    def fetch_article(self, url: str) -> Dict:
        try:
            art = Article(url)
            art.download()
            art.parse()
            text = art.text
            title = art.title or ""
        except Exception as e:
            log.warning(f"newspaper failed for {url}: {e}, fallback to requests+bs4")
            r = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(r.text, "lxml")
            main = soup.find(["article", "main"]) or soup
            text = "\n".join(p.get_text(strip=True) for p in main.find_all("p"))
            title = soup.title.string if soup.title else ""
        return {"title": title, "link": url, "text": text, "source": url}

    def fetch_from_sources(self, sources: List[Dict]) -> List[Dict]:
        results = []
        for s in sources:
            t = s.get("type", "rss")
            url = s["url"]
            try:
                if t == "rss":
                    entries = self.fetch_rss(url)
                    results.extend(entries)
                else:
                    art = self.fetch_article(url)
                    results.append(art)
            except Exception as e:
                log.error(f"failed to fetch {url}: {e}")
        return results
