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
    content: str
    summary: Optional[str] = None
    source: Optional[str] = "其他"
    
# ----------------------
# fetch_tools.py
# ----------------------
    
class FetchNewsArgs(BaseModel):
    query: str