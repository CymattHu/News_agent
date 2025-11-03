from typing import List
import openai
from .config import settings
from .utils import log

openai.api_key = settings.openai_api_key

class Summarizer:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model

    def summarize(self, title: str, text: str, max_tokens: int = 512) -> str:
        if not text:
            return ""
        prompt = (
            f"请用{settings.default_language}对下面新闻做简洁摘要，3-6句话，保留关键事实与时间、主体。\n"
            f"标题：{title}\n正文：\n{text[:6000]}"
        )
        try:
            r = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.2,
            )
            summary = r["choices"][0]["message"]["content"].strip()
            return summary
        except Exception as e:
            log.error(f"OpenAI summarize error: {e}")
            return text[:400].strip()

    def batch_summarize(self, items: List[dict]) -> List[dict]:
        out = []
        for it in items:
            text = it.get("text") or it.get("summary") or ""
            summary = self.summarize(it.get("title", ""), text)
            it["summary_generated"] = summary
            out.append(it)
        return out
