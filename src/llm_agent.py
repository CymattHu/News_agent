from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from .tools.fetch_tools import fetch_news
from .tools.summarize_tool import summarize_articles
from .tools.report_tool import generate_report_pdf
from .db import init_db
from .utils import log
from .config import settings
import os

def build_news_agent(api_key: str | None = None):
    api_key = api_key or settings.google_api_key or os.getenv("GOOGLE_API_KEY")
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-pro",
        temperature=0.2,
        google_api_key=api_key,
        convert_system_message_to_human=True
    )

    tools = [
        fetch_news,
        summarize_articles,
        generate_report_pdf,
    ]
    
    NEWS_AGENT_PROMPT = """
        You are an expert news assistant who processes news efficiently.

        When interacting with the user, always use the tools for fetching, summarizing, or generating reports.
        """

    agent = create_agent(
    model= model,
    # tools=tools,
    system_prompt=NEWS_AGENT_PROMPT
)
    return agent

if __name__ == "__main__":
    init_db()
    log.info("启动 LLM Agent... 请以自然语言指令和 agent 交互，例如：\n\n  抓取 BBC 和 CNN 的科技新闻并生成 PDF。\n")
    agent = build_news_agent()
    
    while True:
        try:
            prompt = input("用户: ")
            if prompt.strip().lower() in {"exit", "quit"}:
                break
            # 传入字典
            print("prompt:", prompt)
            res = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
            # 根据返回类型打印
            if isinstance(res, dict) and "output_text" in res:
                print("Agent:", res["output_text"])
            else:
                print("Agent:", res)
        except KeyboardInterrupt:
            break

