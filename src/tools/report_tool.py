from langchain.tools import tool
from ..reporter import Reporter

@tool("generate_report_pdf", return_direct=True)
def generate_report_pdf(articles: list, filename: str = "news_report.pdf") -> str:
    reporter = Reporter(filename)
    grouped = {}
    for a in articles:
        src = a.get('source', '其他')
        grouped.setdefault(src, []).append(a)
    reporter.generate("今日新闻报告", grouped)
    return filename
