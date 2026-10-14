"""
ShopSmart Retail Analytics — Week 1 ML01
Enhanced PDF Report Generator (v2)
Includes: Cover page, Data Architecture/Schema diagram, all metrics tables,
embedded figures, feature importance tables, business questions, and roadmap.
"""

import os
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, KeepTogether, PageBreak, HRFlowable, BalancedColumns
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = r"c:\Users\HyperX\Desktop\analystLab\Week1_MachineLearning"
PDF_OUT  = os.path.join(BASE_DIR, "reports", "ML_Report_v2.pdf")
FIG_DIR  = os.path.join(BASE_DIR, "reports", "figures")

TODAY = datetime.date.today().strftime("%B %d, %Y")

# ── Colour palette ────────────────────────────────────────────────────────────
NAVY    = colors.HexColor("#0F2D5C")
BLUE    = colors.HexColor("#1A56DB")
LBLUE   = colors.HexColor("#3B82F6")
ACCENT  = colors.HexColor("#F59E0B")
TEAL    = colors.HexColor("#0EA5E9")
RED     = colors.HexColor("#DC2626")
GREEN   = colors.HexColor("#16A34A")
GREY95  = colors.HexColor("#F3F4F6")
GREY80  = colors.HexColor("#CBD5E1")
GREY60  = colors.HexColor("#6B7280")
DARK    = colors.HexColor("#111827")
WHITE   = colors.white


# ── Custom canvas with header/footer ─────────────────────────────────────────
class BrandedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        n = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_chrome(n)
            super().showPage()
        super().save()

    def _draw_chrome(self, total):
        pn = self._pageNumber
        w, h = A4

        if pn == 1:
            # Full-bleed cover bar
            self.setFillColor(NAVY)
            self.rect(0, h - 3.5*cm, w, 3.5*cm, fill=1, stroke=0)
            self.setFillColor(ACCENT)
            self.rect(0, h - 3.7*cm, w, 0.2*cm, fill=1, stroke=0)
            return

        # Header bar
        self.setFillColor(NAVY)
        self.rect(0, h - 1.2*cm, w, 1.2*cm, fill=1, stroke=0)
        self.setFillColor(ACCENT)
        self.rect(0, h - 1.35*cm, w, 0.15*cm, fill=1, stroke=0)

        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(WHITE)
        self.drawString(1.8*cm, h - 0.82*cm,
            "ShopSmart Retail Analytics & AI | Mission ML01 — Week 1 Report")
        self.setFont("Helvetica", 7)
        self.drawRightString(w - 1.8*cm, h - 0.82*cm, f"AnalystLab Africa | Batch F")

        # Footer
        self.setFillColor(GREY80)
        self.rect(0, 0, w, 1.0*cm, fill=1, stroke=0)
        self.setFillColor(DARK)
        self.setFont("Helvetica", 7)
        self.drawString(1.8*cm, 0.35*cm,
            "Confidential — AnalystLab Africa Experience Lab Internship Programme")
        self.drawRightString(w - 1.8*cm, 0.35*cm, f"Page {pn} of {total}")


# ── Style factory ─────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()

    def S(name, parent="Normal", **kw):
        return ParagraphStyle(name, parent=base[parent], **kw)

    return {
        "cover_title": S("cover_title",
            fontName="Helvetica-Bold", fontSize=28, leading=34,
            textColor=WHITE, alignment=TA_CENTER),

        "cover_sub": S("cover_sub",
            fontName="Helvetica", fontSize=13, leading=17,
            textColor=colors.HexColor("#93C5FD"), alignment=TA_CENTER),

        "cover_meta": S("cover_meta",
            fontName="Helvetica", fontSize=9.5, leading=13,
            textColor=colors.HexColor("#BFDBFE"), alignment=TA_CENTER),

        "h1": S("h1",
            fontName="Helvetica-Bold", fontSize=15, leading=19,
            textColor=NAVY, spaceBefore=16, spaceAfter=6, keepWithNext=1),

        "h2": S("h2",
            fontName="Helvetica-Bold", fontSize=11, leading=14,
            textColor=BLUE, spaceBefore=10, spaceAfter=4, keepWithNext=1),

        "h3": S("h3",
            fontName="Helvetica-Bold", fontSize=9.5, leading=12,
            textColor=DARK, spaceBefore=6, spaceAfter=3, keepWithNext=1),

        "body": S("body",
            fontName="Helvetica", fontSize=9, leading=13,
            textColor=DARK, spaceAfter=6, alignment=TA_JUSTIFY),

        "bullet": S("bullet",
            fontName="Helvetica", fontSize=9, leading=13,
            textColor=DARK, leftIndent=14, spaceAfter=4),

        "caption": S("caption",
            fontName="Helvetica-Oblique", fontSize=8, leading=11,
            textColor=GREY60, alignment=TA_CENTER, spaceAfter=6),

        "callout": S("callout",
            fontName="Helvetica-Oblique", fontSize=9, leading=13,
            textColor=DARK, leftIndent=10, rightIndent=10),

        "th": S("th",
            fontName="Helvetica-Bold", fontSize=8.5, leading=11,
            textColor=WHITE, alignment=TA_CENTER),

        "td": S("td",
            fontName="Helvetica", fontSize=8.5, leading=11,
            textColor=DARK),

        "td_c": S("td_c",
            fontName="Helvetica", fontSize=8.5, leading=11,
            textColor=DARK, alignment=TA_CENTER),

        "td_b": S("td_b",
            fontName="Helvetica-Bold", fontSize=8.5, leading=11,
            textColor=NAVY),

        "td_g": S("td_g",
            fontName="Helvetica-Bold", fontSize=8.5, leading=11,
            textColor=GREEN, alignment=TA_CENTER),

        "schema_key": S("schema_key",
            fontName="Helvetica-Bold", fontSize=7.5, leading=9,
            textColor=NAVY, alignment=TA_CENTER),

        "schema_val": S("schema_val",
            fontName="Helvetica", fontSize=7.5, leading=9,
            textColor=DARK, alignment=TA_LEFT),

        "code": S("code",
            fontName="Courier", fontSize=8, leading=11,
            textColor=colors.HexColor("#1E40AF"), spaceAfter=4),

        "right": S("right",
            fontName="Helvetica", fontSize=9, leading=13,
            textColor=DARK, alignment=TA_RIGHT),
    }


def tbl_style(header_color=NAVY, row_bg=GREY95, stripe=True):
    s = [
        ("BACKGROUND", (0, 0), (-1, 0), header_color),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8.5),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("BOX", (0, 0), (-1, -1), 0.5, GREY80),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#E5E7EB")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [WHITE, row_bg] if stripe else [WHITE]),
    ]
    return TableStyle(s)


def img(name, w, h):
    path = os.path.join(FIG_DIR, name)
    if os.path.exists(path):
        return Image(path, width=w*cm, height=h*cm)
    return Paragraph(f"[Figure: {name} not found]",
                     ParagraphStyle("err", fontSize=8, textColor=RED))


# ═══════════════════════════════════════════════════════════════════════════════
def build():
    doc = SimpleDocTemplate(
        PDF_OUT, pagesize=A4,
        leftMargin=1.8*cm, rightMargin=1.8*cm,
        topMargin=1.6*cm, bottomMargin=1.6*cm,
        title="ShopSmart ML01 Report",
        author="AnalystLab Africa Intern",
        subject="Week 1 Machine Learning Foundations"
    )
    S = make_styles()
    story = []
    W = A4[0] - 3.6*cm   # usable width ~16.0 cm

    # ── COVER PAGE ────────────────────────────────────────────────────────────
    story.append(Spacer(1, 3.0*cm))  # push below navy bar
    story.append(Paragraph("ShopSmart Retail Analytics", S["cover_title"]))
    story.append(Paragraph("&amp; AI Implementation", S["cover_title"]))
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph(
        "Mission ML01 — Building Your First Machine Learning Models",
        S["cover_sub"]))
    story.append(Spacer(1, 0.8*cm))

    # Cover meta box
    meta = [
        ["Programme", "AnalystLab Africa Experience Lab Internship"],
        ["Batch",     "Batch F  ·  Week 1"],
        ["Client",    "ShopSmart Retail Ltd., Nigeria"],
        ["Dataset",   "50,000 Transactions  ·  9 Relational CSV Sources"],
        ["Models",    "Linear Regression  ·  Logistic Regression"],
        ["Date",      TODAY],
    ]
    meta_tbl = Table(
        [[Paragraph(r, S["th"]), Paragraph(v, S["cover_meta"])]
         for r, v in meta],
        colWidths=[3.8*cm, 10.2*cm]
    )
    meta_tbl.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (0,-1), colors.HexColor("#1E3A6E")),
        ("BACKGROUND",  (1,0), (1,-1), colors.HexColor("#172554")),
        ("BOX",         (0,0), (-1,-1), 0.5, ACCENT),
        ("INNERGRID",   (0,0), (-1,-1), 0.3, colors.HexColor("#1E40AF")),
        ("TOPPADDING",  (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("ALIGN",       (0,0), (0,-1), "RIGHT"),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(meta_tbl)
    story.append(Spacer(1, 1.2*cm))

    # KPI strip on cover
    kpis = [
        ("88.74%", "Regression R²"),
        ("NGN 29,575", "Test MAE"),
        ("45.70%", "Return Recall"),
        ("50,000", "Orders Analysed"),
    ]
    kpi_tbl = Table(
        [[Paragraph(f"<b>{v}</b>", ParagraphStyle("kv", fontName="Helvetica-Bold",
            fontSize=18, textColor=ACCENT, alignment=TA_CENTER)),
          Paragraph(l, ParagraphStyle("kl", fontName="Helvetica", fontSize=8,
            textColor=colors.HexColor("#93C5FD"), alignment=TA_CENTER))]
         for v, l in kpis],
        colWidths=[W/4]*4,
        rowHeights=[1.1*cm, 0.5*cm]
    )
    # Reshape to 2 rows x 4 cols
    kpi_data = [
        [Paragraph(f"<b>{v}</b>", ParagraphStyle("kv2",
            fontName="Helvetica-Bold", fontSize=17, textColor=ACCENT,
            alignment=TA_CENTER)) for v, _ in kpis],
        [Paragraph(l, ParagraphStyle("kl2",
            fontName="Helvetica", fontSize=8,
            textColor=colors.HexColor("#93C5FD"), alignment=TA_CENTER))
         for _, l in kpis],
    ]
    kpi_tbl = Table(kpi_data, colWidths=[W/4]*4)
    kpi_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#0F2D5C")),
        ("BOX", (0,0), (-1,-1), 0.5, ACCENT),
        ("INNERGRID", (0,0), (-1,-1), 0.3, colors.HexColor("#1E3A6E")),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ]))
    story.append(kpi_tbl)
    story.append(PageBreak())

    # ── 1. EXECUTIVE SUMMARY ─────────────────────────────────────────────────
    story.append(Paragraph("1. Executive Summary", S["h1"]))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY, spaceAfter=8))
    story.append(Paragraph(
        "ShopSmart Retail Ltd. commissioned AnalystLab Africa to build foundational Machine Learning "
        "prototypes on 50,000 omnichannel transactions across Nigeria. Two predictive engines were "
        "designed and deployed as part of <b>Mission ML01</b>:", S["body"]))
    story.append(Paragraph(
        "• <b>Regression Task:</b> Forecast <code>Order_Total</code> (NGN) to optimise inventory "
        "procurement and working capital reserves. The Linear Regression pipeline achieved "
        "<b>R² = 0.8874</b> on held-out test data — explaining <b>88.7%</b> of order-value "
        "variance and reducing prediction error by <b>69.8%</b> vs. a naïve baseline.", S["bullet"]))
    story.append(Paragraph(
        "• <b>Classification Task:</b> Detect return-prone orders (<code>Return_Flag</code>) to "
        "pre-stage return logistics and reduce reverse-supply-chain friction. A balanced Logistic "
        "Regression model intercepted <b>45.7% of all returns</b> (recall) while the dataset's "
        "synthetic uniform return distribution limited ROC-AUC to 0.491.", S["bullet"]))

    # ── 2. DATA ARCHITECTURE ─────────────────────────────────────────────────
    story.append(Paragraph("2. Data Architecture &amp; Schema", S["h1"]))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY, spaceAfter=8))
    story.append(Paragraph(
        "Nine relational CSV files were ingested, cleaned, and merged into a single "
        "<b>50,000-row Master Dataset</b>. The entity-relationship diagram below shows the join "
        "strategy used. All joins were Many-to-One (dimension → fact) to preserve transaction "
        "granularity.", S["body"]))

    # Schema table — dataset descriptions
    schema_headers = [
        Paragraph(h, S["th"]) for h in
        ["Dataset", "Rows", "Columns (Key)", "Role", "Join Key"]
    ]
    schema_rows = [
        ["Orders.csv",      "50,000", "Order_ID · Customer_ID · Store_ID · Order_Date · Order_Total · Order_Status · Shipping_Cost · Payment_Method", "Fact table — transaction backbone", "Order_ID (PK)"],
        ["Order_Items.csv", "50,000", "Order_ID · Product_ID · Quantity · Unit_Price · Discount · Line_Total",                                         "Line-item detail per order",         "Order_ID (FK)"],
        ["Customers.csv",   "5,000",  "Customer_ID · Age · Gender · Segment · Registration_Date",                                                      "Customer demographics dimension",    "Customer_ID (FK)"],
        ["Products.csv",    "500",    "Product_ID · Category · Cost_Price · Catalog_Price",                                                            "Product metadata dimension",         "Product_ID (FK)"],
        ["Stores.csv",      "30",     "Store_ID · Store_Name · Region",                                                                                "Store location dimension",           "Store_ID (FK)"],
        ["Returns.csv",     "~2,440", "Return_ID · Order_ID · Return_Date · Return_Reason · Refund_Amount",                                            "Return event log → Return_Flag",     "Order_ID (FK)"],
        ["Inventory.csv",   "500",    "Product_ID · Stock_Level · Reorder_Level",                                                                      "Inventory depth (not joined to fact)", "Product_ID"],
        ["Employees.csv",   "100",    "Employee_ID · Store_ID · Role",                                                                                 "Staff reference (not joined to fact)", "Store_ID"],
        ["Suppliers.csv",   "50",     "Supplier_ID · Product_ID · Lead_Time",                                                                          "Supply chain reference",             "Product_ID"],
    ]
    schema_data = [schema_headers]
    for row in schema_rows:
        bg = colors.HexColor("#EFF6FF") if schema_rows.index(row) < 6 else GREY95
        schema_data.append([
            Paragraph(f"<b>{row[0]}</b>", S["td_b"]),
            Paragraph(row[1], S["td_c"]),
            Paragraph(row[2], S["td"]),
            Paragraph(row[3], S["td"]),
            Paragraph(row[4], S["td_c"]),
        ])
    schema_tbl = Table(schema_data,
        colWidths=[3.2*cm, 1.4*cm, 5.2*cm, 3.8*cm, 2.4*cm])
    schema_tbl.setStyle(tbl_style())
    story.append(schema_tbl)
    story.append(Spacer(1, 0.3*cm))

    # Master Dataset schema box
    story.append(Paragraph("2.1  Master Dataset — Feature Schema (50,000 rows × 34 columns)", S["h2"]))
    story.append(Paragraph(
        "After cleaning and joining, the master dataset has the following column schema. "
        "Features used for model training are grouped below by type. Target columns and "
        "identifiers are excluded from the feature matrix.", S["body"]))

    feat_headers = [
        Paragraph(h, S["th"]) for h in
        ["Column Name", "Type", "Source Table", "Role", "Sample Values"]
    ]
    feat_rows = [
        # Numerical features
        ("Quantity",             "int",   "Order_Items", "Feature (Reg + Clf)", "1, 2, 3, 4, 5"),
        ("Unit_Price",           "float", "Order_Items", "Feature (Reg + Clf)", "3,500 – 150,000 NGN"),
        ("Discount",             "float", "Order_Items", "Feature (Reg + Clf)", "0 – 50 NGN"),
        ("Shipping_Cost",        "float", "Orders",      "Feature (Reg + Clf)", "500 – 5,000 NGN"),
        ("Customer_Age",         "int",   "Customers",   "Feature (Reg + Clf)", "18 – 70 years"),
        ("Product_Cost_Price",   "float", "Products",    "Feature (Reg + Clf)", "2,000 – 90,000 NGN"),
        ("Product_Catalog_Price","float", "Products",    "Feature (Reg + Clf)", "3,500 – 150,000 NGN"),
        ("Order_Month",          "int",   "Orders",      "Feature (Reg + Clf)", "1 – 12"),
        ("Order_Day",            "int",   "Orders",      "Feature (Reg + Clf)", "1 – 31"),
        ("Order_DayOfWeek",      "int",   "Orders",      "Feature (Reg + Clf)", "0 (Mon) – 6 (Sun)"),
        ("Order_Quarter",        "int",   "Orders",      "Feature (Reg + Clf)", "1 – 4"),
        ("Is_Weekend",           "int",   "Orders",      "Feature (Reg + Clf)", "0 = Weekday, 1 = Weekend"),
        # Categorical features
        ("Customer_Gender",      "str",   "Customers",   "Feature (Reg + Clf)", "Male, Female"),
        ("Customer_Segment",     "str",   "Customers",   "Feature (Reg + Clf)", "Bronze, Silver, Gold"),
        ("Product_Category",     "str",   "Products",    "Feature (Reg + Clf)", "Electronics, Fashion, …"),
        ("Payment_Method",       "str",   "Orders",      "Feature (Reg + Clf)", "Card, Cash, Transfer"),
        ("Sales_Channel",        "str",   "Orders",      "Feature (Reg + Clf)", "Online, In-Store"),
        ("Store_Region",         "str",   "Stores",      "Feature (Reg + Clf)", "North, South, East, West"),
        ("Order_Status",         "str",   "Orders",      "Feature (Reg + Clf)", "Completed, Pending, …"),
        # Targets
        ("Order_Total",          "float", "Orders",      "TARGET (Regression)",      "Mean: NGN 154,253"),
        ("Return_Flag",          "int",   "Returns",     "TARGET (Classification)",  "0 = No Return (95.1%), 1 = Return (4.9%)"),
        # Excluded
        ("Order_ID",             "str",   "Orders",      "EXCLUDED — identifier", "ORD-00001 …"),
        ("Customer_ID",          "str",   "Customers",   "EXCLUDED — identifier", "CUST-0001 …"),
        ("Return_Date",          "date",  "Returns",     "EXCLUDED — post-event leakage", "—"),
        ("Refund_Amount",        "float", "Returns",     "EXCLUDED — post-event leakage", "—"),
    ]

    feat_data = [feat_headers]
    TARGET_ROWS = {19, 20}
    EXCL_ROWS   = {21, 22, 23, 24}
    for i, r in enumerate(feat_rows):
        if i in TARGET_ROWS:
            bg_row = colors.HexColor("#FEF3C7")
            style_ = S["td_b"]
        elif i in EXCL_ROWS:
            bg_row = colors.HexColor("#FEE2E2")
            style_ = S["td"]
        elif i < 12:
            bg_row = colors.HexColor("#EFF6FF")
            style_ = S["td"]
        else:
            bg_row = colors.HexColor("#F0FDF4")
            style_ = S["td"]
        feat_data.append([Paragraph(f"<b>{r[0]}</b>", style_)] +
                          [Paragraph(v, S["td"]) for v in r[1:]])

    feat_tbl = Table(feat_data,
        colWidths=[3.8*cm, 1.1*cm, 3.2*cm, 4.2*cm, 3.7*cm])
    feat_tbl.setStyle(tbl_style(stripe=False))
    # Row colouring
    for i, r in enumerate(feat_rows, start=1):
        row_i = i
        if i - 1 in TARGET_ROWS:
            feat_tbl.setStyle(TableStyle([("BACKGROUND", (0, row_i), (-1, row_i),
                colors.HexColor("#FEF3C7"))]))
        elif i - 1 in EXCL_ROWS:
            feat_tbl.setStyle(TableStyle([("BACKGROUND", (0, row_i), (-1, row_i),
                colors.HexColor("#FEE2E2"))]))
        elif i - 1 < 12:
            feat_tbl.setStyle(TableStyle([("BACKGROUND", (0, row_i), (-1, row_i),
                colors.HexColor("#EFF6FF"))]))
        else:
            feat_tbl.setStyle(TableStyle([("BACKGROUND", (0, row_i), (-1, row_i),
                colors.HexColor("#F0FDF4"))]))
    story.append(feat_tbl)

    # Legend
    legend_data = [[
        Paragraph("🔵 Blue = Numerical Features", ParagraphStyle("lg",
            fontName="Helvetica", fontSize=7.5, textColor=BLUE)),
        Paragraph("🟢 Green = Categorical Features", ParagraphStyle("lg",
            fontName="Helvetica", fontSize=7.5, textColor=GREEN)),
        Paragraph("🟡 Yellow = Model Targets", ParagraphStyle("lg",
            fontName="Helvetica", fontSize=7.5, textColor=colors.HexColor("#92400E"))),
        Paragraph("🔴 Red = Excluded (leakage/IDs)", ParagraphStyle("lg",
            fontName="Helvetica", fontSize=7.5, textColor=RED)),
    ]]
    legend_tbl = Table(legend_data, colWidths=[W/4]*4)
    legend_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), GREY95),
        ("BOX", (0,0), (-1,-1), 0.4, GREY80),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ]))
    story.append(Spacer(1, 0.2*cm))
    story.append(legend_tbl)
    story.append(Spacer(1, 0.3*cm))

    # Pipeline schema
    story.append(Paragraph("2.2  Preprocessing Pipeline Architecture", S["h2"]))
    pipe_data = [
        [Paragraph("Step", S["th"]), Paragraph("Component", S["th"]),
         Paragraph("Applied To", S["th"]), Paragraph("Detail", S["th"])],
        ["1 — Imputation",    "SimpleImputer (median / most_frequent)", "All features",
         "Fitted on train set only. Median for numerical; mode for categorical."],
        ["2 — Scaling",       "StandardScaler (z-score)",                "12 Numerical Features",
         "Centres mean=0, std=1. Prevents dominance of high-magnitude NGN prices."],
        ["3 — Encoding",      "OneHotEncoder (handle_unknown=ignore)",   "7 Categorical Features",
         "Expands to dummy columns. Unknown categories at inference → zero vector."],
        ["4 — Estimator",     "LinearRegression / LogisticRegression",   "Full feature matrix",
         "Wrapped in sklearn Pipeline. Reg: fit_intercept=True. Clf: class_weight='balanced'."],
        ["5 — Persistence",   "joblib.dump(pipeline, path)",             "Full Pipeline object",
         "Saved as .pkl. Inference calls pipeline.predict() — identical transforms applied."],
    ]
    pipe_rows = [[Paragraph(str(r[j]), S["td"] if j > 0 else S["td_b"])
                  for j in range(4)] for r in pipe_data[1:]]
    pipe_tbl = Table([pipe_data[0]] + pipe_rows,
        colWidths=[2.8*cm, 4.5*cm, 3.8*cm, 4.9*cm])
    pipe_tbl.setStyle(tbl_style(header_color=TEAL))
    story.append(pipe_tbl)
    story.append(PageBreak())

    # ── 3. REGRESSION MODEL ───────────────────────────────────────────────────
    story.append(Paragraph("3. Regression Model — Predicting Order_Total", S["h1"]))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY, spaceAfter=8))
    story.append(Paragraph(
        "A <b>Linear Regression</b> pipeline was trained on 40,000 transaction records. "
        "Performance was benchmarked against a <i>DummyRegressor</i> that always predicts "
        "the historical mean (NGN 154,253). The model generalises cleanly with "
        "<b>train R² = 0.8833 vs test R² = 0.8874</b> — indicating no overfitting.", S["body"]))

    reg_data = [
        [Paragraph(h, S["th"]) for h in
         ["Metric", "Dummy Baseline", "Train Set", "Test Set", "Improvement"]],
        ["Mean Abs Error (MAE)", "NGN 97,868", "NGN 30,009", "NGN 29,575", "↓ 69.8%"],
        ["Root Mean Sq Err (RMSE)", "NGN 119,494", "NGN 40,648", "NGN 40,088", "↓ 66.5%"],
        ["R² Coefficient", "−0.0002", "0.8833", "0.8874", "from −0.0002 → 0.8874"],
    ]
    reg_rows = [
        [Paragraph(str(r[j]),
            S["td_b"] if j == 0 else (S["td_g"] if j == 4 else S["td_c"]))
         for j in range(5)]
        for r in reg_data[1:]
    ]
    reg_tbl = Table([reg_data[0]] + reg_rows,
        colWidths=[4.0*cm, 3.0*cm, 2.8*cm, 2.8*cm, 3.4*cm])
    reg_tbl.setStyle(tbl_style())
    story.append(reg_tbl)
    story.append(Spacer(1, 0.4*cm))

    # Figures
    story.append(Paragraph("3.1  Diagnostic Plots", S["h2"]))
    story.append(Table([[
        img("actual_vs_predicted_regression.png", 8.5, 7.0),
        img("residual_plot_regression.png", 8.5, 7.0),
    ]], colWidths=[8.5*cm, 8.5*cm]))
    story.append(Table([[
        Paragraph("<b>Figure 1</b> — Actual vs. Predicted Order_Total (NGN). "
                  "Five diagonal rays emerge from the multiplicative Qty×Price structure.", S["caption"]),
        Paragraph("<b>Figure 2</b> — Residuals vs. Predicted. Residuals cluster along "
                  "five parallel bands confirming the same structural pattern.", S["caption"]),
    ]], colWidths=[8.5*cm, 8.5*cm]))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "<b>Technical Insight:</b> The five-ray pattern occurs because "
        "<code>Order_Total ≈ Quantity × Unit_Price + Shipping_Cost</code> is inherently "
        "<b>multiplicative</b>, while linear regression is additive "
        "(<code>β₁·Qty + β₂·Price</code>). With Quantity ∈ {1,2,3,4,5}, the model fits "
        "an average multiplier, systematically under-predicting Qty=4/5 orders and "
        "over-predicting Qty=1 orders. Adding explicit <code>Quantity × Unit_Price</code> "
        "interaction terms or switching to a tree-based model will resolve this.", S["body"]))

    # Feature importance regression
    story.append(Paragraph("3.2  Top Feature Importance — Regression (Standardized Coefficients)", S["h2"]))
    ri_data = [
        [Paragraph(h, S["th"]) for h in
         ["Rank", "Feature", "Std. Coefficient (NGN)", "Business Interpretation"]],
        ["1", "Unit_Price",          "+85,880", "Primary ticket driver — 1 std rise adds NGN 85,880"],
        ["2", "Quantity",            "+71,292", "Basket volume multiplier — 1 std more units"],
        ["3", "Shipping_Cost",       "+1,334",  "Logistics pass-through cost"],
        ["4", "Order_Month",         "+515",    "Late-year seasonal uplift"],
        ["5", "Customer_Segment_Gold","+468",   "Gold loyalty tier premium spend"],
        ["6", "Order_Quarter",       "−435",    "Q2/Q3 slight dip vs Q1/Q4"],
        ["7", "Product_Category_Groceries","+369","Grocery bundles slightly elevate totals"],
        ["8", "Store_Region_South",  "+358",    "Southern stores marginally higher orders"],
        ["9", "Order_Status_Pending","−338",    "Pending orders tend to be smaller"],
        ["10","Order_Day",           "+328",    "Late-month payroll payday effect"],
    ]
    ri_rows = [[Paragraph(str(r[j]),
        S["td_b"] if j == 1 else (S["td_g"] if j == 2 else S["td_c"]))
        for j in range(4)] for r in ri_data[1:]]
    ri_tbl = Table([ri_data[0]] + ri_rows,
        colWidths=[1.0*cm, 4.5*cm, 3.5*cm, 7.0*cm])
    ri_tbl.setStyle(tbl_style(header_color=LBLUE))
    story.append(ri_tbl)
    story.append(PageBreak())

    # ── 4. CLASSIFICATION MODEL ───────────────────────────────────────────────
    story.append(Paragraph("4. Classification Model — Predicting Return_Flag", S["h1"]))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY, spaceAfter=8))
    story.append(Paragraph(
        "Returns constitute only <b>4.88%</b> of 50,000 orders (2,442 unique returning "
        "Order_IDs out of 2,500 return events). Without class balancing, the model simply "
        "predicts zero returns with 95.12% accuracy — a useless retail tool. "
        "Setting <code>class_weight='balanced'</code> forces the model to learn "
        "minority-class patterns at the cost of overall accuracy but gains "
        "<b>45.7% recall</b> — intercepting 223 of 488 actual returns in the test set.", S["body"]))

    clf_data = [
        [Paragraph(h, S["th"]) for h in
         ["Metric", "Majority Baseline", "Default Logistic Reg", "Balanced Logistic Reg", "Implication"]],
        ["Accuracy",  "95.12%", "95.12%", "51.60%",   "Misleading on imbalanced data"],
        ["Precision", "0.00%",  "0.00%",  "4.65%",    "Low: high FP rate vs rare positives"],
        ["Recall",    "0.00%",  "0.00%",  "45.70%",   "Catches 223 / 488 returns ✓"],
        ["F1-Score",  "0.0000", "0.0000", "0.0844",   "Harmonic Precision-Recall balance"],
        ["ROC-AUC",   "0.5000", "0.4906", "0.4912",   "Limited by uniform synthetic labels"],
    ]
    clf_rows = [
        [Paragraph(str(r[j]),
            S["td_b"] if j == 0 else (S["td_g"] if j == 3 else S["td_c"]))
         for j in range(5)]
        for r in clf_data[1:]
    ]
    clf_tbl = Table([clf_data[0]] + clf_rows,
        colWidths=[2.6*cm, 2.8*cm, 3.0*cm, 3.2*cm, 4.4*cm])
    clf_tbl.setStyle(tbl_style())
    story.append(clf_tbl)
    story.append(Spacer(1, 0.4*cm))

    # Confusion matrix
    story.append(Paragraph("4.1  Confusion Matrix Detail (Balanced Classifier — Test Set)", S["h2"]))
    cm_detail = [
        [Paragraph(h, S["th"]) for h in
         ["", "Predicted: No Return (0)", "Predicted: Return (1)"]],
        [Paragraph("<b>Actual: No Return (0)</b>", S["td_b"]),
         Paragraph("4,937  ✓  True Negatives", ParagraphStyle("tn",
            fontName="Helvetica-Bold", fontSize=9, textColor=GREEN, alignment=TA_CENTER)),
         Paragraph("4,575  ✗  False Positives\n(Return slip printed unnecessarily)",
            ParagraphStyle("fp", fontName="Helvetica", fontSize=8.5, textColor=RED, alignment=TA_CENTER))],
        [Paragraph("<b>Actual: Return (1)</b>", S["td_b"]),
         Paragraph("265  ✗  False Negatives\n(Missed returns — no pre-staging)",
            ParagraphStyle("fn", fontName="Helvetica", fontSize=8.5, textColor=RED, alignment=TA_CENTER)),
         Paragraph("223  ✓  True Positives\n(Returns correctly flagged)",
            ParagraphStyle("tp", fontName="Helvetica-Bold", fontSize=9, textColor=GREEN, alignment=TA_CENTER))],
    ]
    cm_tbl = Table(cm_detail, colWidths=[3.8*cm, 6.1*cm, 6.1*cm])
    cm_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY),
        ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#1E3A6E")),
        ("BACKGROUND", (1,1), (1,1), colors.HexColor("#D1FAE5")),
        ("BACKGROUND", (2,2), (2,2), colors.HexColor("#D1FAE5")),
        ("BACKGROUND", (1,2), (1,2), colors.HexColor("#FEE2E2")),
        ("BACKGROUND", (2,1), (2,1), colors.HexColor("#FEE2E2")),
        ("BOX", (0,0), (-1,-1), 0.8, NAVY),
        ("INNERGRID", (0,0), (-1,-1), 0.5, GREY80),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(cm_tbl)
    story.append(Spacer(1, 0.4*cm))

    # ROC figure
    story.append(Table([[
        img("confusion_matrix.png", 8.5, 6.0),
        img("roc_pr_curve.png", 8.5, 6.0),
    ]], colWidths=[8.5*cm, 8.5*cm]))
    story.append(Table([[
        Paragraph("<b>Figure 3</b> — Confusion matrices: Default (left) vs. Balanced (right).", S["caption"]),
        Paragraph("<b>Figure 4</b> — ROC and Precision-Recall curves for balanced classifier.", S["caption"]),
    ]], colWidths=[8.5*cm, 8.5*cm]))
    story.append(Spacer(1, 0.3*cm))

    # Feature importance classification
    story.append(Paragraph("4.2  Top Return Risk Factors — Classification (Log-Odds Coefficients)", S["h2"]))
    fi_data = [
        [Paragraph(h, S["th"]) for h in
         ["Rank", "Feature", "Log-Odds Coef", "Odds Ratio", "Interpretation"]],
        ["1",  "Order_Month",                    "+0.1045", "1.1102", "Late-year orders 11% more likely to be returned"],
        ["2",  "Product_Catalog_Price",           "+0.0949", "1.0995", "Premium-priced items marginally more returned"],
        ["3",  "Store_Region_East",               "+0.0847", "1.0884", "East region 8.8% higher return risk"],
        ["4",  "Product_Category_Home",           "+0.0812", "1.0846", "Home goods slightly higher return rate"],
        ["5",  "Order_Quarter",                   "−0.0803", "0.9228", "Q4 orders slightly lower return risk"],
        ["6",  "Store_Region_North",              "−0.0714", "0.9311", "North region 6.9% lower return risk"],
        ["7",  "Product_Category_Electronics",    "−0.0478", "0.9533", "Electronics marginally lower return rate"],
        ["8",  "Quantity",                        "+0.0392", "1.0400", "Larger baskets slightly more return-prone"],
        ["9",  "Customer_Segment_Bronze",         "+0.0386", "1.0394", "Bronze tier marginally higher return propensity"],
        ["10", "Product_Cost_Price",              "−0.0956", "0.9088", "Higher cost items returned less often"],
    ]
    fi_rows = [[Paragraph(str(r[j]),
        S["td_b"] if j == 1 else (
            S["td_g"] if j in [2,3] else S["td_c"]))
        for j in range(5)] for r in fi_data[1:]]
    fi_tbl = Table([fi_data[0]] + fi_rows,
        colWidths=[1.0*cm, 4.0*cm, 2.4*cm, 2.4*cm, 6.2*cm])
    fi_tbl.setStyle(tbl_style(header_color=TEAL))
    story.append(fi_tbl)
    story.append(PageBreak())

    # ── 5. INFERENCE SCHEMA ───────────────────────────────────────────────────
    story.append(Paragraph("5. Inference Engine — Prediction Schema", S["h1"]))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY, spaceAfter=8))
    story.append(Paragraph(
        "The standalone <code>scripts/predict.py</code> script loads both trained "
        "pipelines and accepts transaction features to produce real-time predictions. "
        "The table below shows the complete input→output schema.", S["body"]))

    inf_data = [
        [Paragraph(h, S["th"]) for h in
         ["Input Field", "Type", "Valid Range / Values", "Default", "CLI Flag"]],
        ["Quantity",           "int",   "1 – 50",                     "1",          "--quantity"],
        ["Unit_Price",         "float", "> 0 NGN",                    "25,000",     "--unit_price"],
        ["Discount",           "float", "≥ 0 NGN",                    "0",          "--discount"],
        ["Shipping_Cost",      "float", "≥ 0 NGN",                    "2,500",      "--shipping_cost"],
        ["Customer_Age",       "int",   "10 – 120",                   "35",         "--age"],
        ["Customer_Gender",    "str",   "Male, Female",               "Male",       "--gender"],
        ["Customer_Segment",   "str",   "Bronze, Silver, Gold",       "Silver",     "--segment"],
        ["Product_Category",   "str",   "Electronics, Fashion, Groceries, Home, Beauty", "Electronics", "--category"],
        ["Product_Cost_Price", "float", "> 0 NGN",                    "unit_price × 0.65", "(auto)"],
        ["Product_Catalog_Price","float","> 0 NGN",                   "unit_price", "(auto)"],
        ["Payment_Method",     "str",   "Card, Cash, Transfer",       "Card",       "--payment"],
        ["Sales_Channel",      "str",   "Online, In-Store",           "Online",     "--channel"],
        ["Store_Region",       "str",   "North, South, East, West",   "South",      "--region"],
        ["Order_Status",       "str",   "Completed, Pending, Cancelled","Completed", "(auto)"],
        ["Order_Month",        "int",   "1 – 12",                     "current",    "--order_month"],
        ["Order_Day",          "int",   "1 – 31",                     "current",    "(auto)"],
        ["Order_DayOfWeek",    "int",   "0 (Mon) – 6 (Sun)",          "current",    "(auto)"],
        ["Order_Quarter",      "int",   "1 – 4",                      "derived",    "(auto)"],
        ["Is_Weekend",         "int",   "0 or 1",                     "derived",    "(auto)"],
    ]
    inf_rows = [[Paragraph(str(r[j]),
        S["td_b"] if j == 0 else S["td_c"])
        for j in range(5)] for r in inf_data[1:]]
    inf_tbl = Table([inf_data[0]] + inf_rows,
        colWidths=[3.8*cm, 1.2*cm, 3.8*cm, 2.8*cm, 4.4*cm])
    inf_tbl.setStyle(tbl_style(header_color=colors.HexColor("#7C3AED")))
    story.append(inf_tbl)
    story.append(Spacer(1, 0.3*cm))

    # Output schema
    story.append(Paragraph("5.1  Output Schema", S["h2"]))
    out_data = [
        [Paragraph(h, S["th"]) for h in ["Output", "Type", "Description"]],
        ["Predicted Order Value", "float (NGN)", "Continuous revenue forecast from Linear Regression pipeline"],
        ["Return Probability",    "float (%)",   "P(Return=1) from Logistic Regression predict_proba()"],
        ["Return Flag",           "int (0/1)",   "Binary classification: 1 = HIGH RISK, 0 = NORMAL"],
        ["Operational Guidance",  "string",      "Human-readable action message for store operations staff"],
    ]
    out_rows = [[Paragraph(str(r[j]),
        S["td_b"] if j == 0 else S["td_c"])
        for j in range(3)] for r in out_data[1:]]
    out_tbl = Table([out_data[0]] + out_rows,
        colWidths=[4.0*cm, 2.8*cm, 9.2*cm])
    out_tbl.setStyle(tbl_style(header_color=colors.HexColor("#7C3AED")))
    story.append(out_tbl)
    story.append(Spacer(1, 0.3*cm))

    # Sample output
    story.append(Paragraph("5.2  Sample Live Prediction Output", S["h2"]))
    sample = (
        "=================================================================\n"
        "           SHOPSMART AI INFERENCE ENGINE (ML01)\n"
        "=================================================================\n"
        "TRANSACTION DETAILS:\n"
        "  * Quantity & Price : 2 unit(s) @ NGN 85,000.00\n"
        "  * Discount & Ship  : NGN 20.00 disc | NGN 3,500.00 shipping\n"
        "  * Product Category : Electronics\n"
        "  * Customer Profile : 42 yrs, Male (Gold Tier)\n"
        "  * Channel & Region : Online (Card) in South Region\n"
        "-----------------------------------------------------------------\n"
        "MODEL PREDICTIONS:\n"
        "  >> PREDICTED ORDER VALUE : NGN     209,814.52\n"
        "  >> RETURN PROBABILITY    :         45.41%\n"
        "  >> PREDICTED RETURN FLAG :              0 (MODERATE / NORMAL RISK)\n"
        "-----------------------------------------------------------------\n"
        "OPERATIONAL GUIDANCE:\n"
        "  [OK] Standard transaction. Expected to be retained by customer.\n"
        "================================================================="
    )
    for line in sample.split("\n"):
        story.append(Paragraph(line, S["code"]))
    story.append(PageBreak())

    # ── 6. BUSINESS QUESTIONS ─────────────────────────────────────────────────
    story.append(Paragraph("6. Empirical Business Questions — Part 7 (30 Marks)", S["h1"]))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY, spaceAfter=8))

    bqs = [
        ("Q1", "Which variables best predict customer spending?",
         "Unit_Price (Std. Coef: +85,880 NGN) and Quantity (+71,292 NGN) dominate order value, "
         "together accounting for the overwhelming majority of predictive signal. Customer loyalty "
         "tier (Gold: +NGN 468) and shipping cost add marginal secondary influence. "
         "Demographics such as gender and age have negligible direct linear effect on total spend."),
        ("Q2", "Which variables influence product returns?",
         "Order_Month (Odds Ratio: 1.1102) — late-year orders are 11% more likely to be returned, "
         "consistent with post-holiday return seasonality. Product_Catalog_Price (OR: 1.0995) — "
         "premium items are marginally more return-prone. Store_Region_East (OR: 1.0884) shows "
         "elevated risk; however all effects are small, reflecting the uniform synthetic return distribution."),
        ("Q3", "Which products are easiest to predict by value?",
         "Beauty products achieve the lowest prediction error (MAPE: 70.8%). "
         "Groceries (72.7%) and Fashion (76.2%) follow. "
         "Home goods are hardest to predict (MAPE: 83.0%) due to widest unit-price variance across subcategories."),
        ("Q4", "Which customer groups generate the highest order values?",
         "Spend across loyalty tiers is remarkably uniform — Silver: NGN 154,579 avg (NGN 2.59B total), "
         "Gold: NGN 154,093 avg (NGN 2.61B total), Bronze: NGN 154,084 avg (NGN 2.51B total). "
         "This suggests ShopSmart's loyalty programme does not yet drive differential basket sizes."),
        ("Q5", "Which stores generate the highest revenue?",
         "Top 5 by revenue: STR015 ShopSmart Lagos-North (NGN 317.7M), "
         "STR021 Lagos-West (NGN 316.8M), STR017 Abuja-South (NGN 315.3M), "
         "STR010 Abuja-North (NGN 314.8M), STR018 Ibadan-East (NGN 314.2M). "
         "The South Region leads nationally at ~NGN 2.47B (32% of total)."),
        ("Q6", "How could the business use these models?",
         "1. <b>POS Cash-Flow Forecasting:</b> Integrate predict.py into checkout to forecast "
         "daily revenue and adjust credit reserves in real time. "
         "2. <b>Proactive Returns Staging:</b> Flag high-probability return orders at fulfillment to "
         "pre-print return labels and schedule regional collection vehicles. "
         "3. <b>Loyalty Targeting:</b> Identify high-spend, low-return cohorts for premium retention campaigns."),
        ("Q7", "What are the model limitations?",
         "1. <b>Linear Additive Assumption:</b> Linear Regression cannot natively model "
         "Quantity × Unit_Price multiplicative interactions — causing the five-ray residual pattern. "
         "2. <b>Synthetic Returns:</b> Return_Flag is uniformly distributed (~4.9%) without "
         "product/customer pattern, capping ROC-AUC near 0.50. "
         "3. <b>No Temporal Validation:</b> Train/test split is random rather than chronological — "
         "a production system should evaluate on held-out future months."),
        ("Q8", "What additional data would improve predictions?",
         "1. Customer historical return rate over the prior 90 days (strongest likely predictor). "
         "2. Product sizing/fit reviews and defect QA batch logs. "
         "3. Carrier delivery delay data (days late vs SLA). "
         "4. Social sentiment and review scores per product SKU."),
    ]

    for qid, qtitle, qbody in bqs:
        q_box_data = [[
            Paragraph(qid, ParagraphStyle("qid",
                fontName="Helvetica-Bold", fontSize=10,
                textColor=WHITE, alignment=TA_CENTER)),
            Paragraph(f"<b>{qtitle}</b>", S["h3"]),
        ]]
        q_box = Table(q_box_data, colWidths=[1.2*cm, W - 1.2*cm])
        q_box.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (0,0), NAVY),
            ("BACKGROUND", (1,0), (1,0), colors.HexColor("#EFF6FF")),
            ("BOX", (0,0), (-1,-1), 0.5, NAVY),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
            ("LEFTPADDING", (0,0), (-1,-1), 6),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ]))
        story.append(q_box)
        story.append(Paragraph(qbody, S["body"]))
        story.append(Spacer(1, 0.15*cm))
    story.append(PageBreak())

    # ── 7. RECOMMENDATIONS ────────────────────────────────────────────────────
    story.append(Paragraph("7. Strategic Recommendations &amp; Roadmap", S["h1"]))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY, spaceAfter=8))

    recs = [
        ("🚀 Deploy Revenue Estimator to POS",
         "Integrate the Linear Regression pipeline (R²=0.8874) into ShopSmart's POS/ERP systems "
         "via predict.py to generate real-time checkout revenue forecasts and working-capital buffers."),
        ("📦 Expand Lagos &amp; Southern Hub Operations",
         "The South region generates 32% of total revenue (NGN 2.47B) led by Lagos stores. "
         "New store openings and premium shelf space should prioritise Southern hub expansion."),
        ("🔄 Implement Return Pre-Staging Workflow",
         "Flag predicted high-risk orders (Return_Flag=1) at the packing station to pre-print "
         "return labels, schedule reverse logistics vehicles, and reduce return-processing SLA by ~40%."),
        ("📊 Upgrade to Non-Linear Models (Week 2 Roadmap)",
         "Transition from linear baselines to Random Forest and XGBoost to capture "
         "Quantity×Price multiplicative interactions, resolve the five-ray residual pattern, "
         "and improve return classification AUC beyond 0.50 when real return patterns are available."),
    ]
    rec_data = [
        [Paragraph(r[0], S["h2"]), Paragraph(r[1], S["body"])]
        for r in recs
    ]
    rec_tbl = Table(rec_data, colWidths=[4.5*cm, W - 4.5*cm])
    rec_tbl.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0,0), (-1,-1),
         [colors.HexColor("#EFF6FF"), colors.HexColor("#F0FDF4"),
          colors.HexColor("#FEF3C7"), GREY95]),
        ("BOX", (0,0), (-1,-1), 0.5, GREY80),
        ("INNERGRID", (0,0), (-1,-1), 0.3, GREY80),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LINEAFTER", (0,0), (0,-1), 1.5, NAVY),
    ]))
    story.append(rec_tbl)
    story.append(Spacer(1, 0.5*cm))

    # Deliverables verification
    story.append(Paragraph("8. Deliverables Verification", S["h1"]))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY, spaceAfter=8))

    del_data = [
        [Paragraph(h, S["th"]) for h in ["#", "Deliverable", "File Path", "Status"]],
        ["1",  "Main Notebook",           "ML01_Foundations.ipynb",                   "✅ Complete"],
        ["2",  "Master Dataset",          "data/master_dataset.csv",                  "✅ 50,000 rows × 34 cols"],
        ["3",  "Train / Test Splits",     "data/train.csv + test.csv",                "✅ 40,000 / 10,000"],
        ["4",  "Regression Pipeline",     "models/linear_regression_pipeline.pkl",    "✅ R²=0.8874"],
        ["5",  "Classification Pipeline", "models/logistic_regression_pipeline.pkl",  "✅ Recall=45.7%"],
        ["6",  "Actual vs Predicted",     "reports/figures/actual_vs_predicted…png",  "✅ Saved"],
        ["7",  "Residual Plot",           "reports/figures/residual_plot…png",        "✅ Saved"],
        ["8",  "Confusion Matrix",        "reports/figures/confusion_matrix.png",     "✅ Saved"],
        ["9",  "ROC / PR Curves",         "reports/figures/roc_pr_curve.png",         "✅ Saved"],
        ["10", "Inference Script",        "scripts/predict.py",                       "✅ Demo tested"],
        ["11", "Business Report (PDF)",   "reports/ML_Report_v2.pdf",                 "✅ This document"],
        ["12", "README",                  "README.md",                                "✅ Complete"],
        ["13", "requirements.txt",        "requirements.txt",                         "✅ 10 packages"],
        ["14", ".gitignore",              ".gitignore",                               "✅ Complete"],
    ]
    del_rows = [[Paragraph(str(r[j]),
        S["td_c"] if j in [0,3] else (S["td_b"] if j == 1 else S["td"]))
        for j in range(4)] for r in del_data[1:]]
    del_tbl = Table([del_data[0]] + del_rows,
        colWidths=[0.8*cm, 4.4*cm, 7.0*cm, 3.8*cm])
    del_tbl.setStyle(tbl_style(header_color=GREEN))
    story.append(del_tbl)

    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=GREY80, spaceAfter=8))
    story.append(Paragraph(
        "<b>Prepared by:</b> Machine Learning Intern — AnalystLab Africa Experience Lab | "
        f"Batch F | Week 1 | {TODAY}",
        S["caption"]))

    doc.build(story, canvasmaker=BrandedCanvas)
    size = os.path.getsize(PDF_OUT)
    print(f"✅ PDF generated: {PDF_OUT} ({size:,} bytes)")


if __name__ == "__main__":
    build()
