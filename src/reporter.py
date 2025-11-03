from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from typing import List, Dict

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=4))

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
