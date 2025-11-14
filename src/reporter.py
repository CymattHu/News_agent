from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics
from typing import List, Dict

# 注册中文字体（ReportLab 自带，不需要 ttf 文件）
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

# 样式
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=4, fontName='STSong-Light'))
styles['Title'].fontName = 'STSong-Light'
styles['Heading2'].fontName = 'STSong-Light'
styles['Heading3'].fontName = 'STSong-Light'
styles['Normal'].fontName = 'STSong-Light'

class Reporter:
    def __init__(self, filename: str = "report.pdf"):
        self.filename = filename

    def generate(self, title: str, grouped: Dict[str, List[dict]]):
        doc = SimpleDocTemplate(self.filename, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm)
        story = []
        story.append(Paragraph(title, styles['Title']))
        story.append(Spacer(1, 12))
        for cat, items in grouped.items():
            story.append(Paragraph(f"【{cat}】", styles['Heading2']))
            for it in items:
                story.append(Paragraph(f"<b>{it.get('title')}</b>", styles['Heading3']))
                story.append(Paragraph(it.get('summary_generated') or it.get('summary', ''), styles['Normal']))
                story.append(Paragraph(f"来源: {it.get('link')}", styles['Normal']))
                story.append(Spacer(1, 8))
            story.append(Spacer(1, 12))
        doc.build(story)

if __name__ == "__main__":
    reporter = Reporter("test_report.pdf")
    sample_data = {
        "科技": [
            {
                "title": "新型机器人问世",
                "summary": "这是一款能够自主学习的机器人，具有广泛的应用前景。",
                "link": "https://example.com/robot"
            },
            {
                "title": "AI技术突破",
                "summary": "最新的AI技术在图像识别方面取得了重大突破。",
                "link": "https://example.com/ai"
            }
        ],
        "健康": [
            {
                "title": "健康饮食新指南",
                "summary": "专家发布了最新的健康饮食指南，强调均衡营养的重要性。",
                "link": "https://example.com/health"
            }
        ]
    }
    reporter.generate("今日新闻报告", sample_data)
