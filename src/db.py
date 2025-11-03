from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from .config import settings

Base = declarative_base()
engine = create_engine(settings.db_url, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(1024))
    link = Column(String(2048))
    published = Column(String(128), nullable=True)
    source = Column(String(256), nullable=True)
    text = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

def init_db():
    Base.metadata.create_all(bind=engine)

def save_items(items: list):
    db = SessionLocal()
    for it in items:
        n = News(
            title=it.get("title"),
            link=it.get("link"),
            published=it.get("published"),
            source=it.get("source"),
            text=it.get("text"),
            summary=it.get("summary_generated") or it.get("summary")
        )
        db.add(n)
    db.commit()
    db.close()
