from pydantic import BaseModel,Field
from typing import List, Dict, Optional, Union

# ----------------------
# 公共数据模型
# ----------------------

class SourceItem(BaseModel):
    type: str
    url: str

class Article(BaseModel):
    title: str
    summary: str
    link: Optional[str] = ""
    summary_generated: Optional[str] = ""
    categories: Optional[List[str]] = []
    

# ----------------------
# fetch_tools.py
# ----------------------      
class FetchNewsArgs(BaseModel):
    query: str
    
# ----------------------
# summarize_tool.py
# ----------------------   
class SummarizeArticlesArgs(BaseModel):
    articles: List[Article]  # 支持 dict 或 Article 对象
    
# ----------------------
# report_tool.py
# ----------------------   
class GenerateReportArgs(BaseModel):
    articles: List[Article]
    filename: Optional[str] = Field(default="news_report.pdf", description="生成的 PDF 文件名")