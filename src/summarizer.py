from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from .config import settings
from .utils import log


class Summarizer:
    def __init__(self, model: str = "gemini-2.0-flash"):
        # 初始化 LangChain 的 Gemini 接口
        self.model = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=settings.google_api_key,
            temperature=0.2,
            max_output_tokens=512,
        )

    def summarize(self, title: str, summary: str, link: str = "", max_tokens: int = 512) -> str:
        if not summary:
            return ""

        prompt = (
            f"请用{settings.default_language}根据原文链接对下面新闻做简洁摘要，3-6句话，保留关键事实与时间(如有）、主体。\n"
            f"标题：{title}\n摘要：\n{summary[:6000]}\n原文链接：{link}\n"
        )

        try:
            response = self.model.invoke([HumanMessage(content=prompt)])
            summary = (response.content or "").strip()
            return summary
        except Exception as e:
            log.error(f"LangChain Gemini summarize error: {e}")
            return summary[:400].strip()

    def batch_summarize(self, items: List[dict]) -> List[dict]:
        out = []
        for it in items:
            summary = it.get("summary") or ""
            link = it.get("link", "")
            summarized = self.summarize(it.get("title", ""), summary, link)
            it["summary_generated"] = summarized
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
