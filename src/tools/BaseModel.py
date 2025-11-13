from pydantic import BaseModel
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