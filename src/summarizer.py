from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from .config import settings
from .utils import log
import re
import json

class Summarizer:
    def __init__(self, model: str = "gemini-2.0-flash"):
        # 初始化 LangChain 的 Gemini 接口
        self.model = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=settings.google_api_key,
            temperature=0.2,
            max_output_tokens=512,
        )

    def summarize(self, title: str, summary: str, link: str = "", max_tokens: int = 512):
        if not summary:
            return "", "其他"

        categories = [
            "科技", "财经", "商业", "国际", "时政", "社会",
            "健康", "医疗", "娱乐", "体育", "汽车", "出行",
            "科普", "生活方式", "其他"
        ]

        prompt = f"""
                    请用{settings.default_language}根据链接丰富摘要并判断类别。

                    要求：
                    1. 只输出 JSON：
                    {{
                    "summary": "...",        # 3-6句话摘要，保留主体、关键信息和时间
                    "categories": ["..."]    # 从指定列表选择最合适的类别
                    }}
                    2. 类别列表（只能选择其中的）：{categories}
                    3. 原文标题、摘要和链接如下，请直接生成 JSON：
                    标题：{title}
                    原始摘要：{summary[:3000]}
                    链接：{link}
                    """



        try:
            response = self.model.invoke([HumanMessage(content=prompt)])
            content = response.content.strip()
            # 去除可能的代码块标记
            cleaned_content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip(), flags=re.IGNORECASE)
            # 提取 JSON 部分
            data = json.loads(cleaned_content)

            summary_final = data.get("summary", "").strip()
            categories_final = data.get("categories", [])

            allowed = set(categories)
            if not all(cat in allowed for cat in categories_final):
                categories_final = ["其他"]
            return summary_final, categories_final

        except Exception as e:
            log.error(f"Summarize error: {e}")
            return summary[:400].strip(), ["其他"]


    def batch_summarize(self, items: List[dict]) -> List[dict]:
        out = []
        for it in items:
            summary = it.get("summary") or ""
            link = it.get("link", "")
            summarized, categories = self.summarize(it.get("title", ""), summary, link)
            it["summary_generated"] = summarized
            it["categories"] = categories
            out.append(it)
        return out

if __name__ == "__main__":
    summarizer = Summarizer()
    test_title = "PickNik expands support for Franka Research 3 robot on MoveIt Pro示例新闻标题"
    test_summary = "PickNik Robotics said this collaboration will help to address one of the central bottlenecks in AI and robotics development."
    test_link = "https://www.therobotreport.com/picknik-expands-support-for-franka-research-3-robot-on-moveit-pro/ "

    summarized = summarizer.summarize(test_title, test_summary, test_link)
    print("Original Summary:\n", test_summary)
    print("\nGenerated Summary:\n", summarized)
    
    #test batch summarize
    items = [
        {"title": test_title, "summary": test_summary, "link": test_link},
    ]
    summarized_items = summarizer.batch_summarize(items)
    for i, item in enumerate(summarized_items):
        print(f"\nItem {i+1} Generated Summary:\n", item["summary_generated"])  
