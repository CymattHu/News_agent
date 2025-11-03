from .fetcher import Fetcher
from .cleaner import clean_text
from .summarizer import Summarizer
from .db import save_items
from .reporter import Reporter
from collections import defaultdict
from .utils import log

class Agent:
    def __init__(self, sources: list, reporter_out: str = "report.pdf"):
        self.sources = sources
        self.fetcher = Fetcher()
        self.summarizer = Summarizer()
        self.reporter = Reporter(reporter_out)

    def run(self):
        log.info("开始抓取新闻源...")
        raw = self.fetcher.fetch_from_sources(self.sources)
        items = []
        for r in raw:
            text = r.get('text') or r.get('summary') or ''
            text = clean_text(text)
            items.append({
                'title': r.get('title') or '',
                'link': r.get('link'),
                'published': r.get('published'),
                'source': r.get('source'),
                'text': text
            })
        log.info(f"共抓取 {len(items)} 条，开始摘要...")
        items = self.summarizer.batch_summarize(items)
        save_items(items)
        grouped = defaultdict(list)
        for it in items:
            grouped[it.get('source', '其他')].append(it)
        title = "热点新闻汇总"
        self.reporter.generate(title, grouped)
        log.info("报告已生成")
