from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from .config import settings
from .utils import log


class Summarizer:
    def __init__(self, model: str = "gemini-1.5-flash"):
        # 初始化 LangChain 的 Gemini 接口
        self.model = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=settings.google_api_key,
            temperature=0.2,
            max_output_tokens=512,
        )

    def summarize(self, title: str, text: str, max_tokens: int = 512) -> str:
        if not text:
            return ""

        prompt = (
            f"请用{settings.default_language}对下面新闻做简洁摘要，3-6句话，保留关键事实与时间、主体。\n"
            f"标题：{title}\n正文：\n{text[:6000]}"
        )

        try:
            response = self.model.invoke([HumanMessage(content=prompt)])
            summary = (response.content or "").strip()
            return summary
        except Exception as e:
            log.error(f"LangChain Gemini summarize error: {e}")
            return text[:400].strip()

    def batch_summarize(self, items: List[dict]) -> List[dict]:
        out = []
        for it in items:
            text = it.get("text") or it.get("summary") or ""
            summary = self.summarize(it.get("title", ""), text)
            it["summary_generated"] = summary
            out.append(it)
        return out
