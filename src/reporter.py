import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from typing import List, Dict

# 注册中文字体
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

styles = getSampleStyleSheet()

# 基础样式
styles.add(ParagraphStyle(name='TitleCN', parent=styles['Title'], fontName='STSong-Light', fontSize=24, leading=30, spaceAfter=18))
styles.add(ParagraphStyle(name='CategoryTitle', fontName='STSong-Light', backColor=colors.HexColor("#4B7BFA"), textColor=colors.white, fontSize=16, leading=22, leftIndent=0, spaceBefore=18, spaceAfter=8, padding=6))
styles.add(ParagraphStyle(name='ItemTitleEn', fontName='Helvetica', fontSize=13, leading=18, textColor=colors.HexColor("#222222"), spaceAfter=4))
styles.add(ParagraphStyle(name='ItemTitleCn', fontName='STSong-Light', fontSize=13, leading=18, textColor=colors.HexColor("#222222"), spaceAfter=4))
styles.add(ParagraphStyle(name='BodyEn', fontName='Helvetica', fontSize=11, leading=17, spaceAfter=4))
styles.add(ParagraphStyle(name='BodyCn', fontName='STSong-Light', fontSize=11, leading=17, spaceAfter=4))
styles.add(ParagraphStyle(name='Source', fontName='Helvetica', fontSize=10, textColor=colors.HexColor("#1a0dab"), leading=14, spaceAfter=10))  # 蓝色链接

# 左侧竖条
class LeftBar(Flowable):
    def __init__(self, height, color=colors.HexColor("#4B7BFA")):
        Flowable.__init__(self)
        self.height = height
        self.color = color
    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, 3, self.height, fill=1, stroke=0)
    def wrap(self, availWidth, availHeight):
        return 3, self.height

# 判断是否包含中文
def is_chinese(text: str) -> bool:
    return bool(re.search(r'[\u4e00-\u9fff]', text))

class Reporter:
    def __init__(self, filename: str = "report.pdf"):
        self.filename = filename

    def generate(self, title: str, grouped: Dict[str, List[dict]]):
        doc = SimpleDocTemplate(
            self.filename,
            pagesize=(210*mm,297*mm),
            leftMargin=20*mm,
            rightMargin=20*mm,
            topMargin=18*mm,
            bottomMargin=18*mm
        )
        print( "Generating report to", self.filename)
        story = []

        # 大标题
        story.append(Paragraph(title, styles['TitleCN']))
        story.append(Spacer(1, 8))

        for cat, items in grouped.items():
            story.append(Paragraph(cat, styles['CategoryTitle']))

            for it in items:
                story.append(LeftBar(10))

                # 自动识别标题中英文
                if is_chinese(it.get('title','')):
                    story.append(Paragraph(f"<b>{it.get('title')}</b>", styles['ItemTitleCn']))
                else:
                    story.append(Paragraph(f"<b>{it.get('title')}</b>", styles['ItemTitleEn']))

                # 自动识别正文中英文
                summary = it.get('summary_generated') or it.get('summary','')
                if is_chinese(summary):
                    story.append(Paragraph(summary, styles['BodyCn']))
                else:
                    story.append(Paragraph(summary, styles['BodyEn']))

                # 来源，链接可点击
                link = it.get('link','')
                if link:
                    story.append(Paragraph(f'<a href="{link}">{link}</a>', styles['Source']))

                story.append(Spacer(1, 14))

        doc.build(story)

# ---------------- 示例运行 ----------------
if __name__ == "__main__":
    reporter = Reporter("test_report_clickable.pdf")
    sample_data = {
        "科技": [
            {
                "title": "New AI Breakthrough",
                "summary": "The latest AI technology achieves major breakthroughs in image recognition.",
                "link": "https://example.com/ai"
            },
            {
                "title": "新型机器人问世",
                "summary": "这是一款能够自主学习的机器人，具有广泛的应用前景。",
                "link": "https://example.com/robot"
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
