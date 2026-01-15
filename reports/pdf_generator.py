from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


def generate_pdf_report_bytes(summary: dict):
    buffer = BytesIO()
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("AI-Powered Resume Screener Report", styles["Title"]))
    story.append(Paragraph(f"Final Match Score: {summary['final_score']}%", styles["Normal"]))
    story.append(Paragraph(f"Matched Skills: {', '.join(summary['matched_skills'])}", styles["Normal"]))
    story.append(Paragraph(f"Missing Skills: {', '.join(summary['missing_skills'])}", styles["Normal"]))

    story.append(Paragraph("Recommendations:", styles["Heading2"]))
    for rec in summary["recommendations"]:
        story.append(Paragraph(rec, styles["Normal"]))

    doc = SimpleDocTemplate(buffer)
    doc.build(story)

    buffer.seek(0)
    return buffer.getvalue()   
