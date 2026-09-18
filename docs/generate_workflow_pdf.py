# -*- coding: utf-8 -*-
"""Generate SGC SmartTrack visual workflow PDF with icons and figures."""
from pathlib import Path

from PIL import Image, ImageDraw
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    Image as RLImage,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "workflow_assets"
OUT = ROOT / "SGC-SmartTrack-Workflow.pdf"

NAVY = colors.HexColor("#1B3A4B")
TEAL = colors.HexColor("#2A6F6F")
CORAL = colors.HexColor("#C45C26")
GOLD = colors.HexColor("#C9A227")
GREEN = colors.HexColor("#2E7D4F")
BLUE = colors.HexColor("#2B6CB0")
PURPLE = colors.HexColor("#5B4B8A")
LIGHT = colors.HexColor("#F4F7F7")
LINE = colors.HexColor("#C5D0D0")
MUTED = colors.HexColor("#4A5A5A")
WHITE = colors.white


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def rounded_rect(draw, xy, radius, fill, outline=None, width=2):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def make_icon(name, bg, kind, size=256):
    """Draw a simple flat icon PNG."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad = 12
    rounded_rect(d, (pad, pad, size - pad, size - pad), 48, fill=bg + (255,), outline=None)

    ink = (255, 255, 255, 255)
    cx, cy = size // 2, size // 2

    if kind == "school":
        # building
        d.rectangle((cx - 55, cy - 20, cx + 55, cy + 60), fill=ink)
        d.polygon([(cx - 70, cy - 20), (cx, cy - 70), (cx + 70, cy - 20)], fill=ink)
        d.rectangle((cx - 18, cy + 20, cx + 18, cy + 60), fill=bg + (255,))
        for x in (-40, 40):
            d.rectangle((cx + x - 12, cy - 5, cx + x + 12, cy + 20), fill=bg + (255,))
    elif kind == "form":
        d.rounded_rectangle((cx - 50, cy - 65, cx + 50, cy + 65), 12, fill=ink)
        for i, y in enumerate(range(cy - 35, cy + 45, 22)):
            d.rectangle((cx - 32, y, cx + 32, y + 8), fill=bg + (255,))
            if i < 3:
                d.ellipse((cx - 42, y, cx - 34, y + 8), fill=bg + (255,))
    elif kind == "upload":
        d.polygon([(cx, cy - 55), (cx - 40, cy - 5), (cx - 18, cy - 5), (cx - 18, cy + 45),
                   (cx + 18, cy + 45), (cx + 18, cy - 5), (cx + 40, cy - 5)], fill=ink)
        d.rectangle((cx - 55, cy + 50, cx + 55, cy + 68), fill=ink)
    elif kind == "platform":
        # cloud + chip
        d.ellipse((cx - 70, cy - 25, cx - 10, cy + 35), fill=ink)
        d.ellipse((cx - 30, cy - 50, cx + 40, cy + 20), fill=ink)
        d.ellipse((cx + 10, cy - 20, cx + 75, cy + 40), fill=ink)
        d.rectangle((cx - 55, cy + 5, cx + 55, cy + 40), fill=ink)
        d.rounded_rectangle((cx - 35, cy - 5, cx + 35, cy + 25), 8, fill=bg + (255,))
    elif kind == "check":
        d.ellipse((cx - 60, cy - 60, cx + 60, cy + 60), fill=ink)
        d.line([(cx - 28, cy + 2), (cx - 8, cy + 25), (cx + 32, cy - 25)], fill=bg + (255,), width=14)
    elif kind == "reject":
        d.ellipse((cx - 60, cy - 60, cx + 60, cy + 60), fill=ink)
        d.line([(cx - 28, cy - 28), (cx + 28, cy + 28)], fill=bg + (255,), width=14)
        d.line([(cx + 28, cy - 28), (cx - 28, cy + 28)], fill=bg + (255,), width=14)
    elif kind == "dashboard":
        d.rounded_rectangle((cx - 60, cy - 50, cx + 60, cy + 55), 10, fill=ink)
        d.rectangle((cx - 45, cy + 5, cx - 15, cy + 40), fill=bg + (255,))
        d.rectangle((cx - 5, cy - 20, cx + 25, cy + 40), fill=bg + (255,))
        d.rectangle((cx + 30, cy - 5, cx + 48, cy + 40), fill=bg + (255,))
    elif kind == "bell":
        d.pieslice((cx - 45, cy - 50, cx + 45, cy + 40), 0, 180, fill=ink)
        d.rectangle((cx - 45, cy - 5, cx + 45, cy + 35), fill=ink)
        d.ellipse((cx - 12, cy + 40, cx + 12, cy + 62), fill=ink)
        d.ellipse((cx - 8, cy - 62, cx + 8, cy - 46), fill=ink)
    elif kind == "division":
        # people / office
        for ox in (-45, 0, 45):
            d.ellipse((cx + ox - 18, cy - 55, cx + ox + 18, cy - 20), fill=ink)
            d.pieslice((cx + ox - 32, cy - 15, cx + ox + 32, cy + 55), 0, 180, fill=ink)
    elif kind == "region":
        d.ellipse((cx - 55, cy - 55, cx + 55, cy + 55), outline=ink, width=10)
        d.ellipse((cx - 20, cy - 55, cx + 20, cy + 55), outline=ink, width=6)
        d.arc((cx - 55, cy - 25, cx + 55, cy + 25), 0, 360, fill=ink, width=6)
    elif kind == "score":
        d.ellipse((cx - 58, cy - 58, cx + 58, cy + 58), fill=ink)
        d.ellipse((cx - 42, cy - 42, cx + 42, cy + 42), fill=bg + (255,))
        d.pieslice((cx - 42, cy - 42, cx + 42, cy + 42), -90, 170, fill=ink)
    elif kind == "notify_school":
        d.rounded_rectangle((cx - 55, cy - 40, cx + 55, cy + 35), 10, fill=ink)
        d.polygon([(cx - 55, cy - 40), (cx, cy + 5), (cx + 55, cy - 40)], fill=bg + (255,))
        d.line([(cx - 55, cy - 40), (cx, cy + 5), (cx + 55, cy - 40)], fill=ink, width=4)
    elif kind == "cycle":
        d.arc((cx - 55, cy - 55, cx + 55, cy + 55), 40, 300, fill=ink, width=14)
        d.polygon([(cx + 35, cy - 55), (cx + 65, cy - 25), (cx + 20, cy - 20)], fill=ink)
    else:
        d.ellipse((cx - 40, cy - 40, cx + 40, cy + 40), fill=ink)

    ASSETS.mkdir(parents=True, exist_ok=True)
    path = ASSETS / f"{name}.png"
    img.save(path, "PNG")
    return path


def ensure_icons():
    specs = [
        ("school", "#2A6F6F", "school"),
        ("form", "#2B6CB0", "form"),
        ("upload", "#5B4B8A", "upload"),
        ("platform", "#1B3A4B", "platform"),
        ("check", "#2E7D4F", "check"),
        ("reject", "#C45C26", "reject"),
        ("dashboard", "#C9A227", "dashboard"),
        ("bell", "#C45C26", "bell"),
        ("division", "#2B6CB0", "division"),
        ("region", "#5B4B8A", "region"),
        ("score", "#2E7D4F", "score"),
        ("email", "#2A6F6F", "notify_school"),
        ("cycle", "#1B3A4B", "cycle"),
    ]
    paths = {}
    for name, color, kind in specs:
        paths[name] = make_icon(name, hex_rgb(color), kind)

    # arrow icons
    teal = (42, 111, 111, 255)
    img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle((20, 54, 78, 74), fill=teal)
    d.polygon([(78, 40), (110, 64), (78, 88)], fill=teal)
    (ASSETS / "arrow_right.png").parent.mkdir(parents=True, exist_ok=True)
    img.save(ASSETS / "arrow_right.png")
    img2 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(img2)
    d2.rectangle((54, 20, 74, 78), fill=teal)
    d2.polygon([(40, 78), (64, 110), (88, 78)], fill=teal)
    img2.save(ASSETS / "arrow_down.png")
    return paths


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title", parent=base["Title"], fontName="Helvetica-Bold",
            fontSize=20, leading=24, textColor=NAVY, alignment=TA_CENTER, spaceAfter=6,
        ),
        "subtitle": ParagraphStyle(
            "subtitle", parent=base["Normal"], fontName="Helvetica",
            fontSize=10, leading=13, textColor=TEAL, alignment=TA_CENTER, spaceAfter=12,
        ),
        "h1": ParagraphStyle(
            "h1", parent=base["Heading1"], fontName="Helvetica-Bold",
            fontSize=13, leading=16, textColor=NAVY, spaceBefore=4, spaceAfter=8, alignment=TA_CENTER,
        ),
        "h2": ParagraphStyle(
            "h2", parent=base["Heading2"], fontName="Helvetica-Bold",
            fontSize=11, leading=14, textColor=TEAL, spaceBefore=8, spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "body", parent=base["Normal"], fontName="Helvetica",
            fontSize=9, leading=12, textColor=MUTED, alignment=TA_CENTER, spaceAfter=8,
        ),
        "card_title": ParagraphStyle(
            "card_title", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=9, leading=11, textColor=NAVY, alignment=TA_CENTER, spaceBefore=4,
        ),
        "card_body": ParagraphStyle(
            "card_body", parent=base["Normal"], fontName="Helvetica",
            fontSize=7.5, leading=10, textColor=MUTED, alignment=TA_CENTER,
        ),
        "arrow": ParagraphStyle(
            "arrow", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=16, textColor=TEAL, alignment=TA_CENTER,
        ),
        "step_num": ParagraphStyle(
            "step_num", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=8, textColor=WHITE, alignment=TA_CENTER,
        ),
        "footer": ParagraphStyle(
            "footer", parent=base["Normal"], fontName="Helvetica",
            fontSize=8, textColor=MUTED, alignment=TA_CENTER,
        ),
        "legend": ParagraphStyle(
            "legend", parent=base["Normal"], fontName="Helvetica",
            fontSize=8, leading=10, textColor=MUTED, alignment=TA_LEFT,
        ),
    }


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    w, h = landscape(A4)
    canvas.line(1.5 * cm, h - 1.2 * cm, w - 1.5 * cm, h - 1.2 * cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(1.5 * cm, h - 0.9 * cm, "SGC SmartTrack - Visual Workflow")
    canvas.drawRightString(w - 1.5 * cm, h - 0.9 * cm, "Prepared by Romer Necesario for Jovel J. Oberio")
    canvas.line(1.5 * cm, 1.1 * cm, w - 1.5 * cm, 1.1 * cm)
    canvas.drawCentredString(w / 2, 0.65 * cm, f"Page {doc.page}  |  DepEd SGC Functionality Assessment Process")
    canvas.restoreState()


def icon_card(path, title, body, s, icon_cm=1.6, width=4.2 * cm):
    img = RLImage(str(path), width=icon_cm * cm, height=icon_cm * cm)
    data = [[img], [Paragraph(title, s["card_title"])], [Paragraph(body, s["card_body"])]]
    t = Table(data, colWidths=[width])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                ("BOX", (0, 0), (-1, -1), 1, TEAL),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 10),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("ROUNDEDCORNERS", [6, 6, 6, 6]),
            ]
        )
    )
    return t


def arrow_cell(s):
    return RLImage(str(ASSETS / "arrow_right.png"), width=0.55 * cm, height=0.55 * cm)


def down_arrow_flowable():
    return RLImage(str(ASSETS / "arrow_down.png"), width=0.7 * cm, height=0.7 * cm)


def build():
    icons = ensure_icons()
    s = styles()
    story = []
    page_w = landscape(A4)[0] - 3 * cm

    # ===== PAGE 1: End-to-end overview =====
    story.append(Paragraph("SGC SmartTrack Workflow Diagram", s["title"]))
    story.append(
        Paragraph(
            "End-to-end process: School submission - Platform processing - Division validation - Monitoring & alerts",
            s["subtitle"],
        )
    )

    row1 = Table(
        [[
            icon_card(icons["school"], "1. SCHOOL / SGC", "School Head & encoder prepare MOVs and encode FI1-FI12", s),
            arrow_cell(s),
            icon_card(icons["form"], "2. ASSESS & ENCODE", "Guided wizard: Yes/No indicators + Validity Form", s),
            arrow_cell(s),
            icon_card(icons["upload"], "3. UPLOAD MOVs", "PDFs per indicator; draft then official submit", s),
            arrow_cell(s),
            icon_card(icons["platform"], "4. SMARTTRACK", "Stores files, auto-scores 10/12, updates status", s),
        ]],
        colWidths=[4.4 * cm, 0.9 * cm, 4.4 * cm, 0.9 * cm, 4.4 * cm, 0.9 * cm, 4.4 * cm],
    )
    row1.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story.append(row1)
    story.append(Spacer(1, 0.45 * cm))

    # down arrow hint
    story.append(Spacer(1, 0.15 * cm))
    mid = Table([[down_arrow_flowable()], [Paragraph("Division &amp; leadership layer", s["body"])]], colWidths=[page_w])
    mid.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    story.append(mid)
    story.append(Spacer(1, 0.15 * cm))

    row2 = Table(
        [[
            icon_card(icons["division"], "5. SDO / SGOD", "Composite Team validates MOVs; return if invalid", s),
            arrow_cell(s),
            icon_card(icons["check"], "6. VALIDATE", "Valid / Invalid with reasons (Vol. 2 rules)", s),
            arrow_cell(s),
            icon_card(icons["dashboard"], "7. DASHBOARD", "Compliance funnel, overdue, Functional map", s),
            arrow_cell(s),
            icon_card(icons["bell"], "8. NOTIFY", "Email: T-7 / T-3 / T-1 / overdue / returned", s),
        ]],
        colWidths=[4.4 * cm, 0.9 * cm, 4.4 * cm, 0.9 * cm, 4.4 * cm, 0.9 * cm, 4.4 * cm],
    )
    row2.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story.append(row2)
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("Governance levels served", s["h2"]))
    levels = Table(
        [[
            icon_card(icons["school"], "SCHOOL", "Submit - revise - view score", s, icon_cm=1.2, width=5.5 * cm),
            icon_card(icons["division"], "DIVISION (SDO)", "Validate - monitor - TA notes", s, icon_cm=1.2, width=5.5 * cm),
            icon_card(icons["region"], "REGION (RO)", "Certify / monitor (roadmap)", s, icon_cm=1.2, width=5.5 * cm),
            icon_card(icons["dashboard"], "LEADERS", "SDS - ASDS - PSDS viewers", s, icon_cm=1.2, width=5.5 * cm),
        ]],
        colWidths=[5.8 * cm, 5.8 * cm, 5.8 * cm, 5.8 * cm],
    )
    levels.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(levels)

    story.append(PageBreak())

    # ===== PAGE 2: School submission detail =====
    story.append(Paragraph("Figure A - School Submission Workflow", s["title"]))
    story.append(
        Paragraph(
            "Aligned with SGC User Guide Vol. 1 (Prepare & Respond) - digitized inside SmartTrack",
            s["subtitle"],
        )
    )

    school_steps = [
        (icons["cycle"], "A1. Open cycle", "Division opens assessment period & deadline"),
        (icons["form"], "A2. Fill profile", "School ID, SGC name, establishment date"),
        (icons["score"], "A3. Answer FIs", "FI1-FI12 Yes/No; primary sub-indicators first"),
        (icons["upload"], "A4. Attach MOVs", "Minimum (+ Additional) PDFs per indicator"),
        (icons["check"], "A5. School QA", "School Head reviews before submit"),
        (icons["platform"], "A6. Submit", "Locked submission ? Division queue"),
    ]
    cells = []
    widths = []
    for i, (ic, title, body) in enumerate(school_steps):
        cells.append(icon_card(ic, title, body, s, icon_cm=1.35, width=3.5 * cm))
        widths.append(3.6 * cm)
        if i < len(school_steps) - 1:
            cells.append(arrow_cell(s))
            widths.append(0.7 * cm)
    t = Table([cells], colWidths=widths)
    t.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story.append(t)
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("Status lifecycle (school view)", s["h2"]))
    status_row = [
        ["DRAFT", "SUBMITTED", "RETURNED", "RESUBMITTED", "VALIDATED"],
    ]
    st = Table(status_row, colWidths=[5 * cm] * 5)
    st.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#6B7280")),
                ("BACKGROUND", (1, 0), (1, 0), BLUE),
                ("BACKGROUND", (2, 0), (2, 0), CORAL),
                ("BACKGROUND", (3, 0), (3, 0), PURPLE),
                ("BACKGROUND", (4, 0), (4, 0), GREEN),
                ("TEXTCOLOR", (0, 0), (-1, -1), WHITE),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ("BOX", (0, 0), (-1, -1), 1, NAVY),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, WHITE),
            ]
        )
    )
    story.append(st)
    story.append(Spacer(1, 0.35 * cm))
    story.append(
        Paragraph(
            "If Primary Sub-Indicator = NO ? Other Sub-Indicators are skipped (DepEd rule). "
            "Functional SGC = at least 10 of 12 indicators met with Minimum MOVs.",
            s["body"],
        )
    )

    # Scoring figure
    story.append(Paragraph("Figure B - Auto-scoring logic", s["h2"]))
    score_fig = Table(
        [[
            icon_card(icons["form"], "Indicators", "12 Functionality Indicators\n19 sub-indicators", s, width=6 * cm),
            arrow_cell(s),
            icon_card(icons["upload"], "Evidence", "Minimum MOVs required\nAdditional = advanced only", s, width=6 * cm),
            arrow_cell(s),
            icon_card(icons["score"], "Result", "? 10/12 = FUNCTIONAL\n< 10 = NOT YET", s, width=6 * cm),
        ]],
        colWidths=[6.2 * cm, 1 * cm, 6.2 * cm, 1 * cm, 6.2 * cm],
    )
    score_fig.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story.append(score_fig)

    story.append(PageBreak())

    # ===== PAGE 3: Division validation =====
    story.append(Paragraph("Figure C - Division Validation & Monitoring", s["title"]))
    story.append(
        Paragraph(
            "Aligned with SGC User Guide Vol. 2 (Validate & Monitor) - SDO Composite Team desk",
            s["subtitle"],
        )
    )

    div_steps = [
        (icons["platform"], "C1. Queue", "New / resubmitted schools appear in validation list"),
        (icons["form"], "C2. Open case", "View answers beside each MOV file"),
        (icons["check"], "C3. Mark Valid", "MOV meets Vol. 2 validity criteria"),
        (icons["reject"], "C4. Mark Invalid", "Wrong name, date, signatures, wrong FI, etc."),
        (icons["email"], "C5. Notify school", "Return reasons sent to School Head / encoder"),
        (icons["dashboard"], "C6. Monitor", "Division dashboard & deadline risk view"),
    ]
    cells = []
    widths = []
    for i, (ic, title, body) in enumerate(div_steps):
        cells.append(icon_card(ic, title, body, s, icon_cm=1.35, width=3.5 * cm))
        widths.append(3.6 * cm)
        if i < len(div_steps) - 1:
            cells.append(arrow_cell(s))
            widths.append(0.7 * cm)
    t = Table([cells], colWidths=widths)
    t.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story.append(t)
    story.append(Spacer(1, 0.55 * cm))

    story.append(Paragraph("Figure D - When is an MOV valid? (quick reference)", s["h2"]))
    valid_invalid = Table(
        [
            [
                Paragraph("<b>VALID</b>", s["card_title"]),
                Paragraph("<b>INVALID (common)</b>", s["card_title"]),
            ],
            [
                Paragraph(
                    "- Correctly named School Governance Council<br/>"
                    "- Structure follows DO 26, s. 2022<br/>"
                    "- Within coverage (SY 2022-2023 onward)<br/>"
                    "- Clear SGC leadership / participation<br/>"
                    "- Complete docs (signatures, quorum, attendance)<br/>"
                    "- Correct document for the indicator",
                    s["legend"],
                ),
                Paragraph(
                    "- -School Governing Council- / wrong org (PTA, SSG)<br/>"
                    "- School Head labeled as -Chairman- incorrectly<br/>"
                    "- Activity dated before required period<br/>"
                    "- Incomplete minutes / no quorum / no signatures<br/>"
                    "- Resolutions without wet signatures where required<br/>"
                    "- Wrong MOV uploaded for the FI",
                    s["legend"],
                ),
            ],
        ],
        colWidths=[12.5 * cm, 12.5 * cm],
    )
    valid_invalid.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), GREEN),
                ("BACKGROUND", (1, 0), (1, 0), CORAL),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("BACKGROUND", (0, 1), (0, 1), colors.HexColor("#E8F5EE")),
                ("BACKGROUND", (1, 1), (1, 1), colors.HexColor("#FCEDE6")),
                ("BOX", (0, 0), (-1, -1), 1, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    story.append(valid_invalid)

    story.append(PageBreak())

    # ===== PAGE 4: Notifications + swimlane summary =====
    story.append(Paragraph("Figure E - Notification & Deadline Alerts", s["title"]))
    story.append(
        Paragraph(
            "School Head and designated teacher/admin are notified by email based on submission date",
            s["subtitle"],
        )
    )

    notif = Table(
        [[
            icon_card(icons["cycle"], "Cycle opened", "Notify School Head & encoder", s, width=4.3 * cm),
            icon_card(icons["bell"], "T-7 / T-3 / T-1", "Still incomplete ? reminders", s, width=4.3 * cm),
            icon_card(icons["reject"], "Deadline missed", "Overdue alert + Division Focal digest", s, width=4.3 * cm),
            icon_card(icons["email"], "MOV returned", "Immediate notice with reasons", s, width=4.3 * cm),
            icon_card(icons["check"], "Validated", "Confirmation to School Head", s, width=4.3 * cm),
        ]],
        colWidths=[4.8 * cm] * 5,
    )
    notif.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(notif)
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("Figure F - Who does what (swimlane summary)", s["h2"]))
    swim = [
        [
            Paragraph("<b>Role</b>", s["card_title"]),
            Paragraph("<b>Actions in SmartTrack</b>", s["card_title"]),
            Paragraph("<b>Outputs</b>", s["card_title"]),
        ],
        [
            Paragraph("School Head / Encoder", s["legend"]),
            Paragraph("Encode FIs, upload MOVs, submit, revise if returned", s["legend"]),
            Paragraph("Complete submission package", s["legend"]),
        ],
        [
            Paragraph("Teacher / Admin (notifyee)", s["legend"]),
            Paragraph("Receives deadline & non-compliance emails", s["legend"]),
            Paragraph("Awareness / follow-through", s["legend"]),
        ],
        [
            Paragraph("SDO Focal / Composite Team", s["legend"]),
            Paragraph("Validate MOVs, return/accept, monitor dashboard", s["legend"]),
            Paragraph("Validated scores & TA notes", s["legend"]),
        ],
        [
            Paragraph("SDS / ASDS / PSDS", s["legend"]),
            Paragraph("View diagnostic dashboard (read-only)", s["legend"]),
            Paragraph("Oversight decisions", s["legend"]),
        ],
        [
            Paragraph("Developer (Romer Necesario)", s["legend"]),
            Paragraph("Build, host, domain, support during warranty", s["legend"]),
            Paragraph("Live platform under agreed package", s["legend"]),
        ],
    ]
    sw = Table(swim, colWidths=[5.5 * cm, 12 * cm, 7.5 * cm])
    sw.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT]),
                ("GRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(sw)
    story.append(Spacer(1, 0.45 * cm))
    story.append(
        Paragraph(
            "Package context: Development + domain + Year-1 hosting - PHP 50,000 (Romer Necesario ? Jovel J. Oberio)",
            s["footer"],
        )
    )

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=landscape(A4),
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.7 * cm,
        bottomMargin=1.5 * cm,
        title="SGC SmartTrack Visual Workflow",
        author="Romer Necesario",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"Wrote {OUT}")
    print(f"Icons in {ASSETS}")


if __name__ == "__main__":
    build()
