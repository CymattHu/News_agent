from langchain.tools import tool
from ..reporter import Reporter

@tool("generate_report_pdf", return_direct=True)
def generate_report_pdf(articles: list, filename: str = "news_report.pdf") -> str:
    """
    根据新闻文章列表生成 PDF 报告。

    Args:
        articles (list): 新闻条目列表，每个元素为包含 'title'、'summary'、'source' 等键的字典。
        filename (str, optional): 生成的 PDF 文件名，默认为 "news_report.pdf"。

    Returns:
        str: 生成的 PDF 文件路径。
    """
    reporter = Reporter(filename)
    grouped = {}
    for a in articles:
        src = a.get('source', '其他')
        grouped.setdefault(src, []).append(a)
    reporter.generate("今日新闻报告", grouped)
    return filename
