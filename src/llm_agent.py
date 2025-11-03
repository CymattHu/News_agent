from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from .tools.fetch_tool import fetch_news
from .tools.summarize_tool import summarize_articles
from .tools.report_tool import generate_report_pdf
from .db import init_db
from .utils import log
import os
from .config import settings

def build_news_agent(api_key: str | None = None):
    api_key = api_key or settings.openai_api_key or os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2, openai_api_key=api_key)
    # Wrap tools into LangChain Tool objects (Tool.from_function may differ across versions)
    tools = [
        Tool.from_function(fetch_news, name="fetch_news"),
        Tool.from_function(summarize_articles, name="summarize_articles"),
        Tool.from_function(generate_report_pdf, name="generate_report_pdf"),
    ]
    agent = initialize_agent(
        tools,
        llm,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
    )
    return agent

if __name__ == '__main__':
    init_db()
    log.info("启动 LLM Agent... 请以自然语言指令和 agent 交互，例如：\n\n  抓取 BBC 和 CNN 的科技新闻并生成 PDF。\n")
    agent = build_news_agent()
    while True:
        try:
            prompt = input("用户: ")
            if prompt.strip().lower() in {"exit", "quit"}:
                break
            res = agent.run(prompt)
            print("Agent:", res)
        except KeyboardInterrupt:
            break
