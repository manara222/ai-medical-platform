from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from datetime import datetime
import os


def _split_text(text: str, max_len: int = 90):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        if len(current) + len(word) + 1 <= max_len:
            current = f"{current} {word}".strip()
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def generate_pdf_report(
    output_path: str,
    image_path: str,
    disease_type: str,
    predicted_class: str,
    confidence: float
):
    clinical_notes = {
        "akiec": "Possible actinic keratosis-type lesion. Dermatology review is recommended.",
        "bcc": "Possible basal cell carcinoma pattern. Specialist dermatology follow-up is advised.",
        "bkl": "Possible benign keratosis-like lesion. Clinical confirmation is recommended.",
        "df": "Possible dermatofibroma-like finding. A dermatologist can confirm the diagnosis.",
        "mel": "Possible melanoma-related pattern. Urgent dermatology consultation is recommended.",
        "nv": "Likely nevus-type lesion. Clinical review is still advised.",
        "vasc": "Possible vascular lesion pattern. Specialist evaluation is recommended.",

        "Cataract": "Possible cataract-related pattern. Ophthalmology examination is recommended.",
        "Diabetic_Retinopathy": "Possible diabetic retinopathy finding. Retina specialist follow-up is advised.",
        "Glaucoma": "Possible glaucoma-related retinal changes. Eye pressure and optic nerve evaluation are recommended.",
        "Normal": "No strong abnormal pattern detected, but medical review is still encouraged if symptoms exist.",

        "Covid": "Possible COVID-related chest X-ray pattern. Clinical review and further testing are recommended.",
        "Viral Pneumonia": "Possible viral pneumonia pattern. Physician consultation is advised.",

        "benign": "The lesion appears more likely benign, but specialist confirmation is recommended.",
        "malignant": "The lesion appears suspicious. Immediate specialist follow-up is strongly advised.",
        "normal": "No strong abnormal breast ultrasound pattern detected, but routine follow-up is still recommended."
    }

    next_steps = {
        "akiec": "Book a dermatology appointment and consider dermoscopic evaluation.",
        "bcc": "Consult a dermatologist for further assessment and possible biopsy.",
        "bkl": "Perform clinical skin examination to confirm the lesion type.",
        "df": "Dermatology review is recommended for confirmation.",
        "mel": "Seek urgent dermatology consultation as soon as possible.",
        "nv": "Monitor clinically and confirm with a dermatologist if needed.",
        "vasc": "Consult a specialist for vascular lesion assessment.",

        "Cataract": "Schedule an ophthalmology examination.",
        "Diabetic_Retinopathy": "Retina screening and diabetic eye follow-up are recommended.",
        "Glaucoma": "Perform glaucoma-focused ophthalmology evaluation.",
        "Normal": "Continue routine monitoring if symptoms are absent.",

        "Covid": "Correlate with clinical symptoms and seek physician review.",
        "Viral Pneumonia": "Visit a physician for chest evaluation and treatment guidance.",

        "benign": "Continue specialist follow-up to confirm the benign nature.",
        "malignant": "Immediate breast specialist consultation is recommended.",
        "normal": "Continue routine screening if needed."
    }

    clinical_note = clinical_notes.get(predicted_class, "Clinical review is recommended.")
    next_step = next_steps.get(predicted_class, "Consult a medical specialist.")

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    report_id = f"AI-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ===== Header =====
    c.setFillColor(colors.HexColor("#0F172A"))
    c.rect(0, height - 80, width, 80, fill=1, stroke=0)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(40, height - 50, "AI Medical Report")

    c.setFont("Helvetica", 11)
    c.drawString(40, height - 68, "AI Multi-Disease Diagnosis Platform")

    c.setFont("Helvetica", 10)
    c.drawRightString(width - 40, height - 55, f"Report ID: {report_id}")
    c.drawRightString(width - 40, height - 70, f"Generated: {report_date}")

    # ===== Diagnosis Summary =====
    box_x = 40
    box_y = height - 250
    box_width = width - 80
    box_height = 130

    c.setFillColor(colors.whitesmoke)
    c.roundRect(box_x, box_y, box_width, box_height, 12, fill=1, stroke=0)

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(box_x + 20, box_y + 95, "Diagnosis Summary")

    c.setFont("Helvetica", 12)
    c.drawString(box_x + 20, box_y + 65, f"Disease Type: {disease_type}")
    c.drawString(box_x + 20, box_y + 40, f"Predicted Class: {predicted_class}")
    c.drawString(box_x + 20, box_y + 15, f"Confidence Score: {confidence:.2f}")

    # ===== Confidence Badge =====
    if confidence >= 0.85:
        badge_text = "High Confidence"
        badge_color = colors.HexColor("#16A34A")
    elif confidence >= 0.60:
        badge_text = "Moderate Confidence"
        badge_color = colors.HexColor("#D97706")
    else:
        badge_text = "Low Confidence"
        badge_color = colors.HexColor("#DC2626")

    c.setFillColor(badge_color)
    c.roundRect(width - 190, box_y + 78, 130, 28, 10, fill=1, stroke=0)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(width - 176, box_y + 88, badge_text)

    # ===== Clinical Insight =====
    insight_y = box_y - 125
    c.setFillColor(colors.HexColor("#DBEAFE"))
    c.roundRect(40, insight_y, width - 80, 90, 12, fill=1, stroke=0)

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(55, insight_y + 60, "Clinical Insight")

    c.setFont("Helvetica", 10)
    insight_lines = _split_text(clinical_note, max_len=85)
    line_y = insight_y + 38
    for line in insight_lines[:3]:
        c.drawString(55, line_y, line)
        line_y -= 14

    # ===== Recommended Next Step =====
    next_y = insight_y - 95
    c.setFillColor(colors.HexColor("#DCFCE7"))
    c.roundRect(40, next_y, width - 80, 75, 12, fill=1, stroke=0)

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(55, next_y + 46, "Recommended Next Step")

    c.setFont("Helvetica", 10)
    next_lines = _split_text(next_step, max_len=90)
    line_y = next_y + 24
    for line in next_lines[:2]:
        c.drawString(55, line_y, line)
        line_y -= 14

    # ===== AI Case Summary =====
    summary_y = next_y - 105
    c.setFillColor(colors.HexColor("#E0F2FE"))
    c.roundRect(40, summary_y, width - 80, 85, 12, fill=1, stroke=0)

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(55, summary_y + 58, "AI Case Summary")

    c.setFont("Helvetica", 10)
    c.drawString(55, summary_y + 38, f"Disease Type: {disease_type}")
    c.drawString(55, summary_y + 24, f"Predicted Class: {predicted_class}")
    c.drawString(55, summary_y + 10, f"Confidence: {confidence:.2f}")

    # ===== Image Section =====
    image_section_y = summary_y - 250

    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.black)
    c.drawString(40, image_section_y + 230, "Processed Medical Image")

    if os.path.exists(image_path):
        img = ImageReader(image_path)

        img_x = 40
        img_y = image_section_y
        img_w = 220
        img_h = 220

        c.setFillColor(colors.lightgrey)
        c.roundRect(img_x - 5, img_y - 5, img_w + 10, img_h + 10, 10, fill=0, stroke=1)
        c.drawImage(
            img,
            img_x,
            img_y,
            width=img_w,
            height=img_h,
            preserveAspectRatio=True,
            mask='auto'
        )

    # ===== Medical Note =====
    c.setFillColor(colors.HexColor("#FEF3C7"))
    c.roundRect(300, image_section_y + 80, 250, 110, 12, fill=1, stroke=0)

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(315, image_section_y + 160, "Important Medical Note")

    c.setFont("Helvetica", 10)
    c.drawString(315, image_section_y + 138, "This result is AI-assisted and not")
    c.drawString(315, image_section_y + 122, "a final medical diagnosis.")
    c.drawString(315, image_section_y + 106, "Please consult a qualified doctor")
    c.drawString(315, image_section_y + 90, "for professional medical advice.")

    # ===== Footer =====
    c.setStrokeColor(colors.grey)
    c.line(40, 40, width - 40, 40)

    c.setFont("Helvetica", 9)
    c.setFillColor(colors.grey)
    c.drawString(40, 25, "Generated by AI Multi-Disease Diagnosis Platform")

    c.save()