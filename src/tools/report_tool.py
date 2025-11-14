from langchain.tools import tool
from ..reporter import Reporter

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union
from .BaseModel import SourceItem, Article, GenerateReportArgs

@tool("generate_report_pdf", return_direct=True, args_schema=GenerateReportArgs)
def generate_report_pdf(args: GenerateReportArgs) -> str:
    """ 
    根据新闻文章列表生成 PDF 报告。 
    Args: articles (list): 新闻条目列表，每个元素为包含 'title'、'summary'、'link' 等键的字典。 
    filename (str, optional): 生成的 PDF 文件名，默认为 "news_report.pdf"。 
    Returns: str: 生成的 PDF 文件路径。 
    """
    reporter = Reporter(args.filename)
    grouped = {}
    for a in args.articles:
        src = a.categories[0] if a.categories else  "其他"
        grouped.setdefault(src, []).append(a.model_dump())
    reporter.generate("今日新闻报告", grouped)
    return args.filename

if __name__ == "__main__":
    #如果需要测试，请注释line11的@tool装饰器
    test_articles = [
        Article(
            title="新型机器人问世",
            summary="这是一款能够自主学习的机器人，具有广泛的应用前景。",
            summary_generated="这是一款能够自主学习的机器人，具有广泛的应用前景。",
            link="https://example.com/robot",
            categories=["科技"],
        ),
        Article(
            title="健康饮食新指南",
            summary="专家发布了最新的健康饮食指南，强调均衡营养的重要性。",
            summary_generated="专家发布了最新的健康饮食指南，强调均衡营养的重要性。",
            link="https://example.com/health",
            categories=["健康"],
        )
    ]
    args = GenerateReportArgs(articles=test_articles, filename="test_report.pdf")
    pdf_path = generate_report_pdf(args)
    print(f"Generated PDF report at: {pdf_path}")