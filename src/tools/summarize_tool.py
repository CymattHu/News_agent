from langchain.tools import tool
from ..summarizer import Summarizer
from pydantic import BaseModel
from typing import List, Dict, Union
from .BaseModel import SourceItem, Article, SummarizeArticlesArgs

summarizer = Summarizer()

@tool("summarize_articles", return_direct=False, args_schema=SummarizeArticlesArgs)
def summarize_articles(articles: List[Article]) -> List[Article]:
    """ 
    对文章列表进行摘要并返回带有 summary_generated 字段的列表 
    """
    # 将 BaseModel 转 dict（兼容 Pydantic V2）
    articles_data = [a.model_dump() for a in articles.articles]
    # 批量摘要
    summarized = summarizer.batch_summarize(articles_data)
    # 重新构造 Article 对象
    return [Article(**a) for a in summarized]


if __name__ == "__main__":
    #如果需要测试，请注释line11的@tool装饰器
    test_articles = [
        Article(
            title="PickNik expands support for Franka Research 3 robot on MoveIt Pro示例新闻标题",
            summary="PickNik Robotics said this collaboration will help to address one of the central bottlenecks in AI and robotics development.",
            link="https://www.therobotreport.com/picknik-expands-support-for-franka-research-3-robot-on-moveit-pro/ "
        )
    ]
    
    summarized_articles = summarize_articles(SummarizeArticlesArgs(articles=test_articles))
    for i, article in enumerate(summarized_articles):
        print(f"Article {i+1} Generated Summary:\n", article.summary_generated)