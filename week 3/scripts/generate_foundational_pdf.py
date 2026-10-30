"""
generate_foundational_pdf.py
Generates the publication-grade corporate executive PDF report for:
Phase 1: Foundational Framework & Business Problem Analysis Report
AnalystLab Africa Experience Lab - Week 3 Hospital Operations, Cost & Patient Flow Intelligence
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

base_dir = r"c:\Users\HyperX\Desktop\analystLab\week 3"
pdf_path = os.path.join(base_dir, "reports", "Phase1_Foundational_Report.pdf")
fig_dir = os.path.join(base_dir, "reports", "figures")
os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "AnalystLab Africa | Week 3: Hospital Operations, Cost & Patient Flow Intelligence")
            self.drawRightString(558, 755, "Phase 1: Foundational Report")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 748, 558, 748)
        
        # Footer (all pages)
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 34, page_str)
        self.drawString(54, 34, "Official Deliverable — AnalystLab Africa Internship Programme (Batch F) | Confidential")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 44, 558, 44)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=3
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=8
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor('#334155'),
        leftIndent=10,
        spaceAfter=2
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
        alignment=1
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#1E293B')
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#0F172A')
    )

    table_cell_center = ParagraphStyle(
        'TableCellCenter',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#1E293B'),
        alignment=1
    )

    caption_style = ParagraphStyle(
        'CaptionStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#475569'),
        alignment=1,
        spaceBefore=4,
        spaceAfter=6
    )

    alert_box_style = ParagraphStyle(
        'AlertBoxStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor('#7F1D1D')
    )

    info_box_style = ParagraphStyle(
        'InfoBoxStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor('#1E3A8A')
    )

    story = []

    # Title Banner
    story.append(Paragraph("Healthcare Operations, Cost & Patient Flow Intelligence", title_style))
    story.append(Paragraph("Phase 1: Foundational Framework, Problem Analysis & Project Governance", subtitle_style))
    
    meta_text = (
        "<b>Programme:</b> AnalystLab Africa Experience Lab &nbsp;|&nbsp; "
        "<b>Week:</b> Week 3 (Batch F) &nbsp;|&nbsp; "
        "<b>Deliverable:</b> General Phase 1 Milestone &nbsp;|&nbsp; "
        "<b>Status:</b> Approved Governance"
    )
    story.append(Paragraph(meta_text, body_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceBefore=3, spaceAfter=6))

    # KPI Governance Metric Cards Table
    kpi_data = [
        [
            Paragraph("<font size=12><b>6</b></font><br/><font color='#64748B'>Data Assets</font>", table_cell_center),
            Paragraph("<font size=12><b>5</b></font><br/><font color='#64748B'>Learning Tracks</font>", table_cell_center),
            Paragraph("<font size=12><b>4</b></font><br/><font color='#16A34A'><b>Executive Roles</b></font>", table_cell_center),
            Paragraph("<font size=12><b>5</b></font><br/><font color='#2563EB'><b>Quality Gates</b></font>", table_cell_center),
            Paragraph("<font size=12><b>$0.00</b></font><br/><font color='#D97706'>Reconciliation Delta</font>", table_cell_center),
        ]
    ]
    kpi_table = Table(kpi_data, colWidths=[100, 100, 105, 100, 99])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 6))

    # 1. Executive Summary
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        "Modern healthcare provider organisations face severe operational friction driven by misaligned bed capacity, "
        "unpredictable patient inflow volumes, and significant financial exposure resulting from the gap between total medical charges "
        "and payer reimbursements. As part of the <b>AnalystLab Africa Experience Lab Internship (Week 3)</b>, this foundational report "
        "establishes the governance, problem definition, analytical architecture, and quality assurance framework required to develop "
        "evidence-based intelligence from multi-table healthcare datasets.",
        body_style
    ))
    story.append(Paragraph(
        "The project integrates six foundational data assets (<code>encounters.csv</code>, <code>patients.csv</code>, "
        "<code>procedures.csv</code>, <code>payers.csv</code>, <code>organizations.csv</code>, and <code>data_dictionary.csv</code>) "
        "alongside SQL reference benchmarks. In adherence to official programme guidelines, this report establishes non-clinical "
        "operational boundaries, profiles technical constraints, establishes five measurable success criteria, and delivers five "
        "corporate architectural diagrams to guide downstream implementation across Data Analytics, Data Science, Machine Learning, "
        "Generative AI, or Project Management tracks.",
        body_style
    ))

    # 2. Business Problem & Operational Context (Task 1)
    story.append(Paragraph("2. Business Problem & Operational Context (Assignment Task 1)", h1_style))
    story.append(Paragraph(
        "Healthcare delivery networks operate in high-friction environments where clinical workflow delays propagate across entire hospital systems. "
        "The primary operational challenges addressed in this investigation include:",
        body_style
    ))
    story.append(Paragraph("• <b>Bed & Capacity Bottlenecks:</b> Inability to forecast prolonged encounters (>24 hours) leads to emergency department boarding, delayed surgical admissions, and intensive care bed shortages.", bullet_style))
    story.append(Paragraph("• <b>Revenue Cycle & Payer Coverage Exposure:</b> Uncompensated care and zero-coverage encounters place heavy financial burdens on health systems. Billing managers need transparency on out-of-pocket liabilities.", bullet_style))
    story.append(Paragraph("• <b>Procedural Resource Utilization:</b> High-volume and high-cost clinical procedures require synchronized operating theater scheduling, specialist staffing, and specialized inventory controls.", bullet_style))
    story.append(Paragraph("• <b>Return Visits & Readmission Patterns:</b> Repeated emergency encounters without scheduled outpatient follow-ups reveal care-continuity breakdowns that drive up avoidable operational expenditure.", bullet_style))

    # Figure 2: Patient Flow & Bottlenecks
    fig2_path = os.path.join(fig_dir, "fig2_patient_flow_bottlenecks.png")
    if os.path.exists(fig2_path):
        story.append(Spacer(1, 4))
        story.append(Image(fig2_path, width=504, height=220))
        story.append(Paragraph("<b>Figure 1:</b> Hospital Patient Flow, Length of Stay (LoS) & Operational Bottlenecks Architecture.", caption_style))

    story.append(PageBreak())

    # 3. Decision Support Matrix & Stakeholder Personas
    story.append(Paragraph("3. Multi-Stakeholder Decision Support Matrix", h1_style))
    story.append(Paragraph(
        "To ensure that analytical deliverables translate directly into managerial actions, this project maps intelligence outputs to four core leadership personas:",
        body_style
    ))

    # Stakeholder Table
    stakeholder_table_data = [
        [
            Paragraph("Stakeholder Persona", table_header),
            Paragraph("Operational Focus", table_header),
            Paragraph("Monitored Metrics (KPIs)", table_header),
            Paragraph("Supported Operational Decisions", table_header)
        ],
        [
            Paragraph("<b>Chief Operating Officer (COO)</b>", table_cell_bold),
            Paragraph("Facility Throughput & Bed Management", table_cell),
            Paragraph("• ALoS (Days/Hours)<br/>• % Encounters > 24h<br/>• ED Boarding Hours", table_cell),
            Paragraph("Reallocate inpatient bed pools, adjust nurse-to-patient staffing for peak arrival days, and enforce discharge cutoffs before 11:00 AM.", table_cell)
        ],
        [
            Paragraph("<b>Chief Financial Officer (CFO)</b>", table_cell_bold),
            Paragraph("Revenue Cycle & Bad Debt Risk", table_cell),
            Paragraph("• Total Claim Cost vs Coverage<br/>• % Zero Payer Coverage<br/>• Avg Cost by Payer", table_cell),
            Paragraph("Renegotiate commercial payer reimbursement schedules, establish bad-debt reserves, and deploy pre-service financial counseling.", table_cell)
        ],
        [
            Paragraph("<b>Director of Clinical Services</b>", table_cell_bold),
            Paragraph("Surgical Suites & Procedure Volume", table_cell),
            Paragraph("• Procedure Frequency<br/>• Average Base Cost<br/>• OR Utilization Rate", table_cell),
            Paragraph("Prioritize preventive maintenance for high-frequency equipment, schedule elective procedures during low-ED inflow periods, and standardize surgical trays.", table_cell)
        ],
        [
            Paragraph("<b>Health Informatics Officer</b>", table_cell_bold),
            Paragraph("Data Integrity & Continuity of Care", table_cell),
            Paragraph("• % Missing Timestamps<br/>• 30-Day Return Visit Rate<br/>• Uncoded Encounter Ratio", table_cell),
            Paragraph("Implement EHR validation rules preventing open encounter closure without discharge timestamps, and audit coding uniformity across facilities.", table_cell)
        ]
    ]

    s_table = Table(stakeholder_table_data, colWidths=[110, 110, 130, 154])
    s_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    story.append(s_table)

    # Figure 4: Stakeholder Matrix Diagram
    fig4_path = os.path.join(fig_dir, "fig4_stakeholder_decision_matrix.png")
    if os.path.exists(fig4_path):
        story.append(Spacer(1, 4))
        story.append(Image(fig4_path, width=504, height=220))
        story.append(Paragraph("<b>Figure 2:</b> Executive Decision Support Matrix & Monitored Operational Interventions.", caption_style))

    # 4. Data Ecosystem & Relational Architecture (Task 2)
    story.append(Paragraph("4. Healthcare Data Ecosystem & Relational Architecture (Assignment Task 2)", h1_style))
    story.append(Paragraph(
        "The project ecosystem models real-world healthcare administrative and billing workflows using Synthea-derived data structures. "
        "The relational schema connects encounters, patient demographics, clinical procedures, payer contracts, and healthcare provider organizations:",
        body_style
    ))

    # Figure 1: Data Ecosystem
    fig1_path = os.path.join(fig_dir, "fig1_healthcare_data_ecosystem.png")
    if os.path.exists(fig1_path):
        story.append(Image(fig1_path, width=504, height=225))
        story.append(Paragraph("<b>Figure 3:</b> Relational Entity Architecture, Key Constraints & Attribute Mapping.", caption_style))

    story.append(PageBreak())

    # Dataset Asset Inventory Table
    story.append(Paragraph("Data Asset Inventory & Structural Specifications", h2_style))
    asset_table_data = [
        [
            Paragraph("Data Asset File", table_header),
            Paragraph("Primary Relational Purpose", table_header),
            Paragraph("Key Identifier(s)", table_header),
            Paragraph("Data Quality & Governance Check", table_header)
        ],
        [
            Paragraph("<b>encounters.csv</b>", table_cell_bold),
            Paragraph("Central Fact: Volume, duration, claim cost, payer coverage.", table_cell),
            Paragraph("PK: <code>Id</code><br/>FK: <code>PATIENT, PAYER, ORG</code>", table_cell),
            Paragraph("Verify Stop >= Start; flag missing stop timestamps; validate zero-coverage claims.", table_cell)
        ],
        [
            Paragraph("<b>patients.csv</b>", table_cell_bold),
            Paragraph("Dimension: Patient demographics, birthdate, expenses, coverage.", table_cell),
            Paragraph("PK: <code>Id</code>", table_cell),
            Paragraph("Mask PII; audit birthdate logic; check longitudinal demographic distribution.", table_cell)
        ],
        [
            Paragraph("<b>procedures.csv</b>", table_cell_bold),
            Paragraph("Fact Table: Procedure codes, dates, base costs, encounters.", table_cell),
            Paragraph("FK: <code>ENCOUNTER, PATIENT</code>", table_cell),
            Paragraph("Maintain N:1 cardinality with encounters; prevent cost double-counting.", table_cell)
        ],
        [
            Paragraph("<b>payers.csv</b>", table_cell_bold),
            Paragraph("Dimension: Payer names, covered amounts, revenue metrics.", table_cell),
            Paragraph("PK: <code>Id</code>", table_cell),
            Paragraph("Compare payer-level covered amounts against encounter-level totals.", table_cell)
        ],
        [
            Paragraph("<b>organizations.csv</b>", table_cell_bold),
            Paragraph("Dimension: Provider facilities, coordinates, bed utilization.", table_cell),
            Paragraph("PK: <code>Id</code>", table_cell),
            Paragraph("Audit facility identifiers; map geographical coverage and facility revenue.", table_cell)
        ],
        [
            Paragraph("<b>data_dictionary.csv</b>", table_cell_bold),
            Paragraph("Metadata: Official attribute definitions, types, relationships.", table_cell),
            Paragraph("N/A (Schema Reference)", table_cell),
            Paragraph("Authoritative schema ground truth; verify against physical CSV columns.", table_cell)
        ]
    ]

    a_table = Table(asset_table_data, colWidths=[90, 150, 110, 154])
    a_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    story.append(a_table)
    story.append(Spacer(1, 6))

    # 5. Financial Dynamics & Payer Exposure
    story.append(Paragraph("5. Healthcare Financial Dynamics & Payer Coverage Exposure", h1_style))
    story.append(Paragraph(
        "A critical responsibility in healthcare financial intelligence is decomposing medical encounter claims into their underlying cost components "
        "and evaluating the distribution of insurance reimbursements versus out-of-pocket patient liabilities:",
        body_style
    ))

    # Figure 3: Financial Dynamics
    fig3_path = os.path.join(fig_dir, "fig3_financial_cost_coverage_flow.png")
    if os.path.exists(fig3_path):
        story.append(Image(fig3_path, width=504, height=225))
        story.append(Paragraph("<b>Figure 4:</b> Encounter Financial Dynamics, Claim Cost Decomposition & Payer Adjudication Flow.", caption_style))

    story.append(PageBreak())

    # 6. Quality Gates & Measurable Success Criteria (Task 3 & 4)
    story.append(Paragraph("6. Quality Gates & Measurable Success Criteria (Tasks 3 & 4)", h1_style))
    story.append(Paragraph(
        "To satisfy the rigorous technical and governance standards established by AnalystLab Africa, this project defines five verifiable quality gates:",
        body_style
    ))

    # Figure 5: Quality Gates
    fig5_path = os.path.join(fig_dir, "fig5_quality_gates_governance.png")
    if os.path.exists(fig5_path):
        story.append(Image(fig5_path, width=504, height=215))
        story.append(Paragraph("<b>Figure 5:</b> Technical Quality Gates & Governance Verification Pipeline.", caption_style))

    story.append(Spacer(1, 4))

    # Quality Gates Detail Table
    gate_table_data = [
        [
            Paragraph("Quality Gate", table_header),
            Paragraph("Verification Metric", table_header),
            Paragraph("Acceptance Standard", table_header),
            Paragraph("Governance & Testing Methodology", table_header)
        ],
        [
            Paragraph("<b>Gate 1: Financial Reconciliation</b>", table_cell_bold),
            Paragraph("Reconciliation Delta", table_cell),
            Paragraph("<b>Delta = $0.00</b>", table_cell_bold),
            Paragraph("Independent script verifies: <code>TOTAL_CLAIM_COST == PAYER_COVERAGE + PATIENT_LIABILITY</code>.", table_cell)
        ],
        [
            Paragraph("<b>Gate 2: Temporal Logic Check</b>", table_cell_bold),
            Paragraph("Negative Duration Rate", table_cell),
            Paragraph("<b>0.00%</b> Negative Durations", table_cell_bold),
            Paragraph("Calculated duration <code>(STOP - START) >= 0</code>; missing end times systematically flagged as open.", table_cell)
        ],
        [
            Paragraph("<b>Gate 3: Relational Grain</b>", table_cell_bold),
            Paragraph("Encounter Grain Preservation", table_cell),
            Paragraph("<b>Zero Cartesian Row Duplication</b>", table_cell_bold),
            Paragraph("Joining <code>procedures</code> to <code>encounters</code> must not duplicate encounter claim totals in summary KPIs.", table_cell)
        ],
        [
            Paragraph("<b>Gate 4: Pipeline Reproducibility</b>", table_cell_bold),
            Paragraph("Script Execution Success", table_cell),
            Paragraph("<b>100% Automated Re-run</b>", table_cell_bold),
            Paragraph("Complete pipeline can be executed end-to-end via a single command with zero manual spreadsheet steps.", table_cell)
        ],
        [
            Paragraph("<b>Gate 5: Privacy & Clinical Safety</b>", table_cell_bold),
            Paragraph("PII Leaks & Clinical Claims", table_cell),
            Paragraph("<b>Zero PII / Zero Treatment Claims</b>", table_cell_bold),
            Paragraph("Direct identifiers removed from dashboards; all insights strictly confined to operational decision support.", table_cell)
        ]
    ]

    g_table = Table(gate_table_data, colWidths=[110, 95, 115, 184])
    g_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    story.append(g_table)
    story.append(Spacer(1, 6))

    # Safety Alerts Box
    alert_data = [
        [
            Paragraph(
                "<b>CRITICAL DATABASE SAFETY MANDATE (AnalystLab Africa Document Control Task 4):</b><br/>"
                "The provided database setup script <code>create_hospital_db.sql</code> begins by executing <code>DROP DATABASE IF EXISTS hospital_db; CREATE DATABASE hospital_db;</code>. "
                "Interns are strictly instructed to inspect scripts prior to execution and use only an isolated practice environment. "
                "Never execute this script against production instances or existing servers containing important databases.",
                alert_box_style
            )
        ]
    ]
    alert_table = Table(alert_data, colWidths=[504])
    alert_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF2F2')),
        ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor('#DC2626')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(alert_table)

    story.append(Spacer(1, 6))

    # 7. Assignment Learning Tracks & Next Steps Roadmap
    story.append(Paragraph("7. Learning Tracks & Downstream Project Roadmap", h1_style))
    story.append(Paragraph(
        "Following completion of Phase 1 Foundational Governance, interns branch into their designated specialization track:",
        body_style
    ))

    tracks = [
        "<b>Track A (Data Analytics):</b> Build interactive Power BI Healthcare Operations & Financial Intelligence Dashboard answering 8 core operational questions with DAX measures and KPI definition sheets.",
        "<b>Track B (Data Science):</b> Execute rigorous Exploratory Data Analysis (EDA) and parametric/non-parametric hypothesis testing on encounter costs, length of stay, and procedure frequency.",
        "<b>Track C (Machine Learning Engineering):</b> Train, validate, and package predictive models for encounter duration thresholds (>24h), claim cost regression, or 30-day operational return visits.",
        "<b>Track D (Generative AI):</b> Develop a grounded Healthcare Operations Knowledge Assistant using LLMs and structured RAG retrieval over verified dataset definitions with safety guardrails.",
        "<b>Track E (Project Management):</b> Deliver an execution-ready Project Management Plan featuring WBS, critical-path Gantt schedules, resource budgets, risk registers, and change simulation."
    ]
    for trk in tracks:
        story.append(Paragraph(f"• {trk}", bullet_style))

    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceBefore=4, spaceAfter=8))
    story.append(Paragraph(
        "<b>Report Authorization:</b> Submitted by Junior Healthcare Analytics Intern | Reviewed & Governed by Senior Healthcare Analytics Mentor | AnalystLab Africa Internship Programme Week 3.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated PDF Report: {pdf_path}")

if __name__ == "__main__":
    build_pdf()

