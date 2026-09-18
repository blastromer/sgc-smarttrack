# -*- coding: utf-8 -*-
"""Generate development proposal PDF: Developer -> Jobel Oberio (PHP 50,000 incl. hosting & domain)."""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUT = Path(__file__).resolve().parent / "SGC-SmartTrack-Proposal-and-Costing.pdf"

NAVY = colors.HexColor("#1B3A4B")
TEAL = colors.HexColor("#2A6F6F")
LIGHT = colors.HexColor("#F4F7F7")
LINE = colors.HexColor("#C5D0D0")
MUTED = colors.HexColor("#4A5A5A")


def make_styles():
    base = getSampleStyleSheet()
    return {
        "cover_title": ParagraphStyle(
            "cover_title", parent=base["Title"], fontName="Helvetica-Bold",
            fontSize=22, leading=26, textColor=NAVY, alignment=TA_CENTER, spaceAfter=8,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub", parent=base["Normal"], fontName="Helvetica",
            fontSize=11, leading=15, textColor=TEAL, alignment=TA_CENTER, spaceAfter=6,
        ),
        "meta": ParagraphStyle(
            "meta", parent=base["Normal"], fontName="Helvetica",
            fontSize=9, leading=12, textColor=MUTED, alignment=TA_CENTER,
        ),
        "h1": ParagraphStyle(
            "h1", parent=base["Heading1"], fontName="Helvetica-Bold",
            fontSize=13, leading=16, textColor=NAVY, spaceBefore=14, spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2", parent=base["Heading2"], fontName="Helvetica-Bold",
            fontSize=11, leading=14, textColor=TEAL, spaceBefore=10, spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "body", parent=base["Normal"], fontName="Helvetica",
            fontSize=9.5, leading=13, textColor=colors.HexColor("#222222"),
            alignment=TA_JUSTIFY, spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "bullet", parent=base["Normal"], fontName="Helvetica",
            fontSize=9.5, leading=12.5, textColor=colors.HexColor("#222222"),
            leftIndent=8, spaceAfter=2,
        ),
        "cell": ParagraphStyle(
            "cell", parent=base["Normal"], fontName="Helvetica",
            fontSize=8.5, leading=11, textColor=colors.HexColor("#222222"),
        ),
        "cell_b": ParagraphStyle(
            "cell_b", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=8.5, leading=11, textColor=NAVY,
        ),
        "callout": ParagraphStyle(
            "callout", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=10, leading=13, textColor=NAVY, alignment=TA_CENTER,
        ),
        "small": ParagraphStyle(
            "small", parent=base["Normal"], fontName="Helvetica-Oblique",
            fontSize=8, leading=10, textColor=MUTED, alignment=TA_CENTER, spaceBefore=8,
        ),
    }


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(2 * cm, A4[1] - 1.4 * cm, A4[0] - 2 * cm, A4[1] - 1.4 * cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(2 * cm, A4[1] - 1.1 * cm, "Development Proposal - SGC SmartTrack")
    canvas.drawRightString(A4[0] - 2 * cm, A4[1] - 1.1 * cm, "To: Jovel J. Oberio")
    canvas.line(2 * cm, 1.3 * cm, A4[0] - 2 * cm, 1.3 * cm)
    canvas.drawCentredString(
        A4[0] / 2, 0.8 * cm,
        f"Page {doc.page}  |  Package: PHP 50,000 (dev + hosting + domain)  |  Quotation",
    )
    canvas.restoreState()


def table(data, col_widths):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.4, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
            ]
        )
    )
    return t


def build():
    styles = make_styles()
    story = []

    # Cover
    story.append(Spacer(1, 1.8 * cm))
    story.append(Paragraph("SOFTWARE DEVELOPMENT PROPOSAL", styles["meta"]))
    story.append(Spacer(1, 0.35 * cm))
    story.append(Paragraph("SGC SmartTrack", styles["cover_title"]))
    story.append(
        Paragraph(
            "Web platform for School Governance Council (SGC)<br/>"
            "compliance submission, division monitoring &amp; alerts",
            styles["cover_sub"],
        )
    )
    story.append(Spacer(1, 0.25 * cm))
    story.append(
        HRFlowable(width="80%", thickness=1.2, color=TEAL, spaceBefore=4, spaceAfter=12, hAlign="CENTER")
    )
    story.append(
        Paragraph(
            "<b>Fixed package: PHP 50,000</b><br/>"
            "Includes development, domain, and Year-1 hosting",
            styles["callout"],
        )
    )
    story.append(Spacer(1, 1.0 * cm))

    meta_rows = [
        [
            Paragraph("<b>Prepared for (Client)</b>", styles["cell_b"]),
            Paragraph(
                "Jovel J. Oberio<br/>Education Program Supervisor<br/>"
                "Department of Education - Negros Island Region",
                styles["cell"],
            ),
        ],
        [
            Paragraph("<b>Prepared by (Developer)</b>", styles["cell_b"]),
            Paragraph(
                "Romer Necesario<br/>Independent Software Developer",
                styles["cell"],
            ),
        ],
        [
            Paragraph("<b>Project</b>", styles["cell_b"]),
            Paragraph("SGC SmartTrack - Division pilot (public elementary SGC FAT)", styles["cell"]),
        ],
        [
            Paragraph("<b>Document type</b>", styles["cell_b"]),
            Paragraph("Quotation / development proposal (fixed package)", styles["cell"]),
        ],
        [Paragraph("<b>Date</b>", styles["cell_b"]), Paragraph("September 2026", styles["cell"])],
        [
            Paragraph("<b>Total package</b>", styles["cell_b"]),
            Paragraph("<b>PHP 50,000</b> (all-in for scope below)", styles["cell"]),
        ],
    ]
    mt = Table(meta_rows, colWidths=[4.5 * cm, 11.2 * cm])
    mt.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.8, TEAL),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, LINE),
                ("BACKGROUND", (0, 0), (0, -1), LIGHT),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(mt)
    story.append(Spacer(1, 1.2 * cm))
    story.append(
        Paragraph(
            "This proposal is submitted to Sir Jobel (Jovel J. Oberio) for the design and development "
            "of SGC SmartTrack, including domain registration and first-year hosting.",
            styles["meta"],
        )
    )
    story.append(PageBreak())

    # 1 Purpose
    story.append(Paragraph("1. Purpose of This Proposal", styles["h1"]))
    story.append(
        Paragraph(
            "This is a <b>development quotation from the developer to Sir Jobel Oberio</b>. "
            "It covers building a lean web system so schools can submit SGC Functionality Assessment "
            "forms and Means of Verification (MOVs), and so the Division can monitor compliance, "
            "validate submissions, and notify schools of missed deadlines-aligned with DepEd Order "
            "No. 26, s. 2022 and the 2026 SGC FAT process-within a fixed budget of <b>PHP 50,000</b>.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "Your concept paper (SGC SmartTrack: analytics, TA management, Responsible AI) remains "
            "the long-term product vision. This package delivers the working foundation first; "
            "advanced AI/TA features can be scoped later as a separate agreement.",
            styles["body"],
        )
    )

    # 2 Understanding
    story.append(Paragraph("2. Understanding of the Need", styles["h1"]))
    story.append(
        Paragraph(
            "Today, schools use Google Forms + Drive + spreadsheets. That creates heavy admin work, "
            "weak live monitoring, reactive technical assistance, and privacy risk from public Drive links. "
            "SGC SmartTrack will replace that friction for a Division pilot with:",
            styles["body"],
        )
    )
    for b in [
        "School-side guided submission of the 12 Functionality Indicators and MOV uploads",
        "Automatic Functional / Not-yet scoring (official 10-of-12 rule)",
        "Division validation desk and diagnostic dashboard",
        "Email alerts when forms are incomplete or past the submission date",
        "Secure, role-based file storage (not \"anyone with the link\")",
    ]:
        story.append(Paragraph(f"- {b}", styles["bullet"]))

    # 3 Scope
    story.append(Paragraph("3. Scope of Work (Included in PHP 50,000)", styles["h1"]))
    story.append(Paragraph("3.1 Development", styles["h2"]))
    for b in [
        "Web application (desktop + mobile-friendly / PWA-ready)",
        "User roles: School Head/Encoder, Division Focal/Validator, Viewer (SDS/ASDS/PSDS)",
        "SGC assessment cycle wizard (school profile, FI1-FI12, Validity Form)",
        "MOV upload per indicator; draft / submit / returned / validated statuses",
        "Scoring engine: Primary Sub-Indicators + Minimum MOVs; Functional if >= 10/12",
        "Division queue: validate, mark invalid with reason, request revision",
        "Dashboard: submission funnel, overdue schools, Functional vs Not-yet counts",
        "Email notifications: cycle open, T-7 / T-3 / T-1, overdue, returned MOV",
        "Basic admin: school list import, user accounts, assessment deadline settings",
        "Handover: credentials, short user guide, 1 orientation session (online or on-site if agreed)",
    ]:
        story.append(Paragraph(f"- {b}", styles["bullet"]))

    story.append(Paragraph("3.2 Domain &amp; hosting (included)", styles["h2"]))
    for b in [
        "One domain name registration for 1 year (e.g. .com or similar available name)",
        "Web hosting + database for 12 months from go-live (or from domain activation, whichever is agreed)",
        "SSL (HTTPS) and routine backups as provided by the chosen host plan",
        "Deployment of the application to production and DNS setup",
    ]:
        story.append(Paragraph(f"- {b}", styles["bullet"]))

    story.append(Paragraph("3.3 Not included in this package (optional later)", styles["h2"]))
    for b in [
        "Paid SMS blasts at scale (email is included)",
        "Full Responsible AI engine / SGIP auto-generation (roadmap; separate quote)",
        "Full Technical Assistance scheduling module beyond a simple notes/status field",
        "Region-wide multi-SDO tenancy and National CO consolidation",
        "Ongoing Year-2 hosting renewal (quoted separately near end of Year 1, typically PHP 15,000-25,000)",
        "On-site travel outside agreed orientation; hardware; DepEd official procurement paperwork",
    ]:
        story.append(Paragraph(f"- {b}", styles["bullet"]))

    # 4 Package price
    story.append(Paragraph("4. Package Price Breakdown", styles["h1"]))
    story.append(
        Paragraph(
            "Fixed all-in package for Sir Jobel. Development fee and infrastructure are combined so "
            "there is one clear number-not to exceed <b>PHP 50,000</b>.",
            styles["body"],
        )
    )

    cost_rows = [
        [
            Paragraph("<b>Item</b>", styles["cell_b"]),
            Paragraph("<b>Amount (PHP)</b>", styles["cell_b"]),
            Paragraph("<b>Description</b>", styles["cell_b"]),
        ],
        [
            Paragraph("Domain (1 year)", styles["cell"]),
            Paragraph("1,500", styles["cell"]),
            Paragraph("Registration + DNS pointed to host", styles["cell"]),
        ],
        [
            Paragraph("Hosting &amp; database (12 months)", styles["cell"]),
            Paragraph("12,000", styles["cell"]),
            Paragraph("Production server suitable for Division pilot", styles["cell"]),
        ],
        [
            Paragraph("File storage for MOVs (Year 1)", styles["cell"]),
            Paragraph("4,000", styles["cell"]),
            Paragraph("Secure storage allowance for uploaded PDFs", styles["cell"]),
        ],
        [
            Paragraph("Email notification service (Year 1)", styles["cell"]),
            Paragraph("2,500", styles["cell"]),
            Paragraph("Transactional email for deadline/compliance alerts", styles["cell"]),
        ],
        [
            Paragraph("Software development &amp; setup", styles["cell"]),
            Paragraph("27,000", styles["cell"]),
            Paragraph("Design, build, deploy, UAT support, orientation, docs", styles["cell"]),
        ],
        [
            Paragraph("Contingency / misc tools", styles["cell"]),
            Paragraph("3,000", styles["cell"]),
            Paragraph("SSL extras, small SaaS, buffer", styles["cell"]),
        ],
        [
            Paragraph("<b>TOTAL PACKAGE</b>", styles["cell_b"]),
            Paragraph("<b>50,000</b>", styles["cell_b"]),
            Paragraph("<b>Fixed - development + domain + hosting</b>", styles["cell_b"]),
        ],
    ]
    story.append(table(cost_rows, [5.8 * cm, 3.2 * cm, 7.2 * cm]))
    story.append(Spacer(1, 0.25 * cm))
    story.append(
        Paragraph(
            "<b>Payment suggestion:</b> 50% upon acceptance (PHP 25,000) to start and secure domain/hosting; "
            "50% (PHP 25,000) upon UAT acceptance / go-live. Adjustable if you prefer another schedule.",
            styles["body"],
        )
    )

    # 5 Timeline
    story.append(Paragraph("5. Timeline", styles["h1"]))
    timeline = [
        [Paragraph("<b>Week</b>", styles["cell_b"]), Paragraph("<b>Deliverable</b>", styles["cell_b"])],
        [
            Paragraph("1", styles["cell"]),
            Paragraph("Requirements lock, school list format, roles, wireframes; domain reservation", styles["cell"]),
        ],
        [
            Paragraph("2-5", styles["cell"]),
            Paragraph("Build: submission wizard, MOV upload, scoring, validation, dashboard, emails", styles["cell"]),
        ],
        [
            Paragraph("6", styles["cell"]),
            Paragraph("Hosting deploy, SSL, DNS; UAT with you + sample schools; fixes", styles["cell"]),
        ],
        [
            Paragraph("7-8", styles["cell"]),
            Paragraph("Orientation, handover, soft launch; 2 weeks hypercare bug fixes included", styles["cell"]),
        ],
    ]
    story.append(table(timeline, [2.5 * cm, 13.7 * cm]))
    story.append(
        Paragraph(
            "Target: about <b>6-8 weeks</b> from down payment and receipt of school list / DepEd email contacts.",
            styles["body"],
        )
    )

    # 6 Client provides
    story.append(Paragraph("6. What You Will Provide", styles["h1"]))
    for b in [
        "School master list (School ID, name, district) for the pilot Division",
        "Official DepEd emails for School Heads / encoders (for login and alerts)",
        "Assessment deadline dates and any Division-specific reminders",
        "Focal person for feedback during UAT (you or designated SGOD staff)",
        "Preferred domain name ideas (availability will be checked)",
    ]:
        story.append(Paragraph(f"- {b}", styles["bullet"]))

    # 7 Vision roadmap
    story.append(Paragraph("7. Your Full Vision (Roadmap After This Package)", styles["h1"]))
    story.append(
        Paragraph(
            "This PHP 50,000 package implements the core of SGC SmartTrack so the Division can run "
            "the SGC FAT digitally. Features from your concept paper that are <b>explicitly next-phase</b>:",
            styles["body"],
        )
    )
    road = [
        [
            Paragraph("<b>Feature</b>", styles["cell_b"]),
            Paragraph("<b>Status in this quote</b>", styles["cell_b"]),
        ],
        [
            Paragraph("Compliance submit + validate + dashboard + email alerts", styles["cell"]),
            Paragraph("Included", styles["cell"]),
        ],
        [
            Paragraph("Domain + Year-1 hosting", styles["cell"]),
            Paragraph("Included", styles["cell"]),
        ],
        [
            Paragraph("Full TA management (schedule, interventions, outcomes)", styles["cell"]),
            Paragraph("Roadmap - separate quote", styles["cell"]),
        ],
        [
            Paragraph("Responsible AI recommendations / SGIP drafts", styles["cell"]),
            Paragraph("Roadmap - separate quote", styles["cell"]),
        ],
        [
            Paragraph("Region multi-SDO / predictive risk heat maps", styles["cell"]),
            Paragraph("Roadmap - separate quote", styles["cell"]),
        ],
    ]
    story.append(table(road, [9.5 * cm, 6.7 * cm]))

    # 8 Terms
    story.append(Paragraph("8. Terms (Simple)", styles["h1"]))
    for b in [
        "Fixed price PHP 50,000 for the scope in Section 3; change requests outside scope will be estimated separately.",
        "Source code of the delivered app will be turned over to you upon final payment.",
        "Domain registrar and hosting accounts can be registered under your name/email, or transferred to you at handover.",
        "Warranty: critical bug fixes for 30 days after go-live at no extra cost (excludes new features).",
        "Personal data handled for DepEd use only; aligned with RA 10173 principles (role-based access, no public MOV links).",
        "This quotation is valid for 30 days from the date above.",
    ]:
        story.append(Paragraph(f"- {b}", styles["bullet"]))

    # 9 Acceptance
    story.append(Paragraph("9. Acceptance", styles["h1"]))
    story.append(
        Paragraph(
            "If this package is acceptable, please reply with confirmation and preferred domain name. "
            "Upon your go-ahead and down payment, development and domain/hosting setup will begin.",
            styles["body"],
        )
    )

    sign = [
        [
            Paragraph(
                "<b>Prepared by (Developer)</b><br/><br/><br/>_________________________<br/>"
                "Romer Necesario / Signature / Date",
                styles["cell"],
            ),
            Paragraph(
                "<b>Accepted by (Client)</b><br/><br/><br/>_________________________<br/>"
                "Jovel J. Oberio / Signature / Date",
                styles["cell"],
            ),
        ]
    ]
    st = Table(sign, colWidths=[8.1 * cm, 8.1 * cm])
    st.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.6, TEAL),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
            ]
        )
    )
    story.append(Spacer(1, 0.4 * cm))
    story.append(st)

    story.append(
        Paragraph(
            "Quotation for development services including domain and Year-1 hosting. "
            "Not a DepEd formal procurement document unless separately converted.",
            styles["small"],
        )
    )

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=1.8 * cm,
        title="SGC SmartTrack - Development Proposal to Jovel J. Oberio",
        author="Romer Necesario",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
