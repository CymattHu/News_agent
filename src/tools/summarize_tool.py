from langchain.tools import tool
from ..summarizer import Summarizer

summarizer = Summarizer()

@tool("summarize_articles", return_direct=False)
def summarize_articles(articles: list) -> list:
    """
    对文章列表进行摘要并返回带有 `summary_generated` 字段的列表
    """
    return summarizer.batch_summarize(articles)
