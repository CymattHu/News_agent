from typing import List
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from .tools.BaseModel import Article
import json
from .config import settings
import re


def extract_json_block(text: str):
    # 尝试提取 ```…``` 中的内容
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.S | re.I)
    if match:
        return match.group(1).strip()

    # 如果没有代码块，则原样返回
    return text.strip()

class ArticleSelector:
    def __init__(self, model: str = "gemini-2.5-pro"):
        """
        :param model_name: LLM 模型名称
        :param api_key: OpenAI API key
        """
        self.model = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=settings.google_api_key,
            temperature=0.2,
            max_output_tokens=4096,
        )
        
    def select_top_articles(self, articles: List[Article], top_k: int = 5) -> List[Article]:
        """
        从文章列表中挑选出最重要的 top_k 条，按重要性排序。
        """
        if top_k > 7:
            top_k = 7  # 限制最多选择 7 条
        prompt = "你是新闻助手，请从下面新闻中挑选出最重要的{}条，按重要性从高到低排序。只返回每条新闻的索引，不要删除或修改字段。\n\n".format(top_k)
        for i, a in enumerate(articles):
            prompt += f"{i}: 标题：{a['title']}\n"

        prompt += "\n请返回 JSON 数组，例如：[0,3,2,1,4]"

        try:
            response = self.model.invoke([HumanMessage(content=prompt)])
            content = response.content.strip()
            # 去除可能的代码块标记
            cleaned_content = extract_json_block(content)
            # 提取 JSON 部分
            top_indices= json.loads(cleaned_content)
        except Exception:
            # 如果解析失败，直接返回前 top_k 条
            print("Warning: 解析文章选择结果失败，返回前 {} 条。".format(top_k))
            top_indices = list(range(min(top_k, len(articles))))

        # 返回 Article 对象
        return [articles[i] for i in top_indices[:top_k]]
    
if __name__ == "__main__":
    selector = ArticleSelector()
    test_articles = [
        Article(
            title="新闻标题1",
            summary="这是第一条新闻的摘要，内容涉及科技和创新。",
            link="https://example.com/news1"
        ),
        Article(
            title="新闻标题2",
            summary="这是第二条新闻的摘要，内容涉及财经和市场动态。",
            link="https://example.com/news2"
        ),
        Article(
            title="新闻标题3",
            summary="这是第三条新闻的摘要，内容涉及国际关系和外交政策。",
            link="https://example.com/news3"
        ),
    ]

    top_articles = selector.select_top_articles(test_articles, top_k=2)
    for i, article in enumerate(top_articles):
        print(f"Top Article {i+1}:\n Title: {article.title}\n Summary: {article.summary}\n Link: {article.link}\n")
