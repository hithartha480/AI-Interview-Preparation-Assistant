from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from datetime import datetime
def add_page_number(canvas, doc):
    page_num = canvas.getPageNumber()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(
        570,
        20,
        f"Page {page_num}"
    )
def clean_text(text):
    if not text:
        return ""
    return (
        text.replace("####", "")
            .replace("###", "")
            .replace("##", "")
            .replace("#", "")
            .replace("**", "")
            .replace("•", "&bull;")
            .replace("\t", "    ")
            .replace("\n", "<br/><br/>")
    )
def generate_pdf(
    filename,
    similarity_score,
    ats_score,
    matched_skills,
    missing_skills,
    resume_suggestions,
    interview_questions,
    mock_question,
    answer_feedback,
    rewritten_resume,
    cover_letter
):
    doc = SimpleDocTemplate(
    filename,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40
    )
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    title_style.alignment = TA_CENTER
    title_style.textColor = colors.HexColor("#1565C0")
    title_style.spaceAfter = 20
    heading_style = styles["Heading2"]
    heading_style.textColor = colors.HexColor("#0D47A1")
    normal_style = styles["BodyText"]
    normal_style.leading = 18
    normal_style.spaceAfter = 8
    story = []
    story.append(
        Table(
            [["AI Interview Preparation Assistant"]],
            colWidths=[450]
        )
    )
    story[-1].setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#1565C0")),
        ("TEXTCOLOR", (0,0), (-1,-1), colors.white),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 22),
        ("BOTTOMPADDING", (0,0), (-1,-1), 16),
        ("TOPPADDING", (0,0), (-1,-1), 16),
    ]))
    story.append(Spacer(1, 0.3 * inch))
    title_table = Table(
        [["Professional Resume Analysis Report"]],
        colWidths=[450]
    )
    title_table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#0D47A1")),
        ("TEXTCOLOR",(0,0),(-1,-1),colors.white),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),16),
        ("BOTTOMPADDING",(0,0),(-1,-1),12),
        ("TOPPADDING",(0,0),(-1,-1),12),
    ]))
    story.append(title_table)
    story.append(Spacer(1, 0.25 * inch))
    story.append(
        Paragraph(
            f"<b>Generated:</b> {datetime.now().strftime('%d %B %Y')}",
            normal_style
        )
    )
    story.append(Paragraph("<b>SUMMARY</b>", styles["Heading2"]))
    
    if ats_score >= 85:
        rating = "Excellent"
    elif ats_score >= 70:
        rating = "Very Good"
    elif ats_score >= 55:
        rating = "Good"
    else:
        rating = "Needs Improvement"
    if ats_score >= 90:
        grade = "A+"
    elif ats_score >= 80:
        grade = "A"
    elif ats_score >= 70:
        grade = "B"
    elif ats_score >= 60:
        grade = "C"
    elif ats_score >= 50:
        grade = "D"
    else:
        grade = "F"
    summary = [
        ["Metric", "Result"],
        ["Resume Match", f"{similarity_score:.2f}%"],
        ["ATS Score", f"{ats_score:.2f}/100"],
        ["Overall Rating", rating],
        ["Resume Grade", grade]
    ]
    summary_table = Table(summary, colWidths=[3.5*inch, 2.5*inch])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1565C0")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),1,colors.grey),
        ("BACKGROUND",(0,1),(-1,-1),colors.HexColor("#F5F5F5")),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTNAME",(0,1),(-1,-1),"Helvetica"),
        ("BOTTOMPADDING",(0,0),(-1,0),10),
        ("TOPPADDING",(0,1),(-1,-1),8),
        ("ALIGN",(0,0),(-1,-1),"CENTER")
    ]))
    story.append(summary_table)
    story.append(Spacer(1,0.3*inch))
    story.append(Paragraph("<b>Skills Analysis</b>", heading_style))
    story.append(Spacer(1, 0.2 * inch))
    matched = "<br/>".join(
        [f"✅ {skill}" for skill in matched_skills]
    ) if matched_skills else "None"
    missing = "<br/>".join(
        [f"❌ {skill}" for skill in missing_skills]
    ) if missing_skills else "No Missing Skills"
    table_data = [
        [
            Paragraph("<b>Matched Skills</b>", styles["Heading3"]),
            Paragraph("<b>Missing Skills</b>", styles["Heading3"])
        ],
        [
            Paragraph(matched, normal_style),
            Paragraph(missing, normal_style)
        ]
    ]
    table = Table(table_data, colWidths=[3.2 * inch, 3.2 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#2E7D32")),
        ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#C62828")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("BOX", (0, 0), (-1, -1), 1.5, colors.black),
        ("BACKGROUND", (0, 1), (0, 1), colors.HexColor("#E8F5E9")),
        ("BACKGROUND", (1, 1), (1, 1), colors.HexColor("#FFEBEE")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("TOPPADDING", (0, 1), (-1, 1), 12),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("<b>Resume Suggestions</b>", heading_style))
    clean_resume = clean_text(resume_suggestions)
    story.append(Paragraph(clean_resume, normal_style))
    story.append(Spacer(1,0.2*inch))
    story.append(Paragraph("<b>Interview Questions</b>", heading_style))
    clean_questions = clean_text(interview_questions)
    story.append(Paragraph(clean_questions, normal_style))
    story.append(Spacer(1, 0.25 * inch))
    story.append(
        Paragraph(
            "<b>Generated by AI Interview Preparation Assistant</b>",
            styles["Heading3"]
        )
    )
    story.append(
            Paragraph(
            "This report is AI-generated for educational and interview preparation purposes.",
            styles["Italic"]
        )
    )
    story.append(Paragraph("<b>AI Mock Interview</b>", heading_style))
    clean_mock = clean_text(mock_question)
    story.append(Spacer(1,0.2*inch))
    story.append(Paragraph("<b>AI Feedback</b>", heading_style))
    clean_feedback = clean_text(answer_feedback)
    story.append(Paragraph(clean_feedback, normal_style))
    story.append(Spacer(1,0.2*inch))
    story.append(Paragraph("<b>AI Rewritten Resume</b>", heading_style))
    clean_resume_ai = clean_text(rewritten_resume)
    story.append(Paragraph(clean_resume_ai, normal_style))
    story.append(Spacer(1,0.2*inch))
    story.append(Paragraph("<b>AI Cover Letter</b>", heading_style))
    clean_cover = clean_text(cover_letter)
    story.append(Paragraph(clean_cover, normal_style))
    story.append(Spacer(1,0.2*inch))
    doc.build(
    story,
    onFirstPage=add_page_number,
    onLaterPages=add_page_number
)
    