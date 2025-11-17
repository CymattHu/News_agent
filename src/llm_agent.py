from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver  
from .tools.fetch_tools import fetch_news
from .tools.summarize_tool import summarize_articles
from .tools.report_tool import generate_report_pdf
from .tools.news_report_tool import news_report
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
        # fetch_news,
        # summarize_articles,
        # generate_report_pdf,
        news_report,
    ]
    
    NEWS_AGENT_PROMPT = """
            你是一个专业的新闻助手，能够高效地帮助用户收集、总结和生成新闻报告。

            你有一个可用工具：
            1. news_report(query,top_k,report_file_name)：根据用户提供的查询关键词，自动完成以下步骤：
            a) 抓取相关新闻；
            b) 对新闻进行摘要和分类；
            c) 根据摘要生成 PDF 报告，文件名为 "report.pdf"。

            使用指南：
            - 在处理任务时，始终使用 news_report 工具，不要直接回答问题。
            - 如果用户输入缺少关键信息（如查询关键词或 top_k,report_file_name），请先向用户询问完整信息。
            - top_k 表示选择的重要新闻数量,不超过7条。
            - report_file_name 表示生成的 PDF 报告文件名，例如 "news_report.pdf"。
            - 工具会自动完成抓取、摘要、分类和 PDF 生成，无需用户手动干预。
            - 报告生成后再向用户反馈结果。
            - 执行完成后，向用户返回生成的 PDF 文件路径或报告信息。

            交互示例：
            1. 用户提供新闻主题或查询。
            2. 你调用 news_report(query,top_k,report_file_name) 自动完成新闻抓取、摘要和 PDF 生成。
            3. 将 PDF 文件路径或相关摘要信息展示给用户。

            始终保持专业、高效，确保用户能够快速获取完整的新闻报告。
            """



    agent = create_agent(
    model= model,
    tools=tools,
    system_prompt=NEWS_AGENT_PROMPT,
    checkpointer=InMemorySaver()
)
    return agent

if __name__ == "__main__":
    init_db()
    log.info("启动 LLM Agent... 请以自然语言指令和 agent 交互，例如：\n\n  抓取机器人新闻并生成 PDF。\n")
    agent = build_news_agent()
    
    # print(fetch_news.args_schema())
    
    while True:
        try:
            prompt = input("用户: ")
            if prompt.strip().lower() in {"exit", "quit"}:
                break

            res = agent.invoke({"messages": [{"role": "user", "content": prompt}]},{"configurable": {"thread_id": "1"}})

            # 获取 AI 回复内容（取最后一条 AIMessage 对象的 content 属性）
            ai_reply = None

            for m in reversed(res.get("messages", [])):
                if hasattr(m, "content") and m.content:
                    # content 可能是 list
                    content = m.content
                    
                    # 如果 content 是 list，就逐个从字典提取 text
                    if isinstance(content, list):
                        texts = []
                        for part in content:
                            if isinstance(part, dict) and "text" in part:
                                texts.append(part["text"])
                            elif hasattr(part, "text"):
                                texts.append(part.text)
                            elif isinstance(part, str):
                                texts.append(part)
                        ai_reply = "\n".join(texts)
                    else:
                        # 如果 content 就是字符串
                        ai_reply = content
                        print("DEBUG: AI message content:", ai_reply)
                    break

            print("Agent:", ai_reply)

        except KeyboardInterrupt:
            break


