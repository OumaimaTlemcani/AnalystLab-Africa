"""
generate_report_figures.py
Generates 5 publication-grade corporate diagrams and visual assets for:
Phase 1: Foundational Framework & Business Problem Analysis Report
AnalystLab Africa - Week 3 Hospital Operations, Cost & Patient Flow Intelligence
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ArrowStyle, ConnectionStyle
import numpy as np

# Output directory
FIGURES_DIR = r"c:\Users\HyperX\Desktop\analystLab\week 3\reports\figures"
os.makedirs(FIGURES_DIR, exist_ok=True)

# Corporate styling defaults
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 0.8

# Color Palette
NAVY_PRIMARY = '#1E3A8A'
BLUE_ACCENT = '#2563EB'
BLUE_LIGHT = '#EFF6FF'
TEAL_PRIMARY = '#0D9488'
TEAL_LIGHT = '#F0FDFA'
AMBER_WARNING = '#D97706'
AMBER_LIGHT = '#FFFBEB'
ROSE_DANGER = '#E11D48'
ROSE_LIGHT = '#FFF1F2'
SLATE_DARK = '#0F172A'
SLATE_MID = '#475569'
SLATE_LIGHT = '#F8FAFC'
BORDER_COLOR = '#94A3B8'


def create_fig1_data_ecosystem():
    """
    Figure 1: Healthcare Data Ecosystem & Relational Architecture
    Maps the 5 core relational entities, primary/foreign keys, cardinality, and data dictionary.
    """
    fig, ax = plt.subplots(figsize=(13.5, 7.8), dpi=300)
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title & Subtitle Header Box
    title_box = FancyBboxPatch((3, 88), 94, 9.5, boxstyle="round,pad=0.6,rounding_size=1.2",
                               facecolor='#1E3A8A', edgecolor='#0F172A', linewidth=1.5)
    ax.add_patch(title_box)
    ax.text(50, 93.8, "Healthcare Relational Data Ecosystem & Entity Architecture",
            fontsize=15, fontweight='bold', color='white', ha='center', va='center')
    ax.text(50, 90.0, "AnalystLab Africa Week 3 | Relational Schema, Key Constraints & Attribute Mapping (Synthea Specification)",
            fontsize=9.5, color='#BFDBFE', ha='center', va='center')

    # Helper function to draw table entity cards
    def draw_entity_card(x, y, w, h, title, subtitle, color_hdr, color_bg, border_color, fields):
        # Background card
        card = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.0",
                              facecolor=color_bg, edgecolor=border_color, linewidth=1.2)
        ax.add_patch(card)
        # Header banner
        hdr = FancyBboxPatch((x, y + h - 4.2), w, 4.2, boxstyle="round,pad=0.2,rounding_size=0.8",
                             facecolor=color_hdr, edgecolor=color_hdr)
        ax.add_patch(hdr)
        ax.text(x + w/2, y + h - 1.8, title, fontsize=10.5, fontweight='bold', color='white', ha='center', va='center')
        ax.text(x + w/2, y + h - 3.4, subtitle, fontsize=7.5, color='#F1F5F9', ha='center', va='center')
        
        # Field list
        cur_y = y + h - 6.0
        for fld, role, fld_color in fields:
            prefix = "[PK] " if role == "PK" else ("[FK] " if role == "FK" else " -  ")
            weight = 'bold' if role in ['PK', 'FK'] else 'normal'
            ax.text(x + 1.2, cur_y, prefix + fld, fontsize=7.6, fontweight=weight, color=fld_color, va='center')
            cur_y -= 2.05

    # 1. encounters.csv (Central Fact Table)
    encounter_fields = [
        ("Id", "PK", "#1E3A8A"),
        ("START", "ATTR", "#0F172A"),
        ("STOP", "ATTR", "#0F172A"),
        ("PATIENT", "FK", "#2563EB"),
        ("ORGANIZATION", "FK", "#0D9488"),
        ("PAYER", "FK", "#D97706"),
        ("ENCOUNTERCLASS", "ATTR", "#0F172A"),
        ("CODE / DESCRIPTION", "ATTR", "#475569"),
        ("BASE_ENCOUNTER_COST", "ATTR", "#166534"),
        ("TOTAL_CLAIM_COST", "ATTR", "#166534"),
        ("PAYER_COVERAGE", "ATTR", "#166534"),
        ("REASONCODE / DESC", "ATTR", "#475569"),
    ]
    draw_entity_card(36, 26, 28, 55, "encounters.csv", "Central Core Transaction Fact Table",
                     "#1E3A8A", "#FFFFFF", "#1E3A8A", encounter_fields)

    # 2. patients.csv (Demographics Dimension)
    patient_fields = [
        ("Id", "PK", "#2563EB"),
        ("BIRTHDATE", "ATTR", "#0F172A"),
        ("DEATHDATE", "ATTR", "#0F172A"),
        ("GENDER / RACE / ETHNICITY", "ATTR", "#475569"),
        ("MARITAL / CITY / STATE", "ATTR", "#475569"),
        ("HEALTHCARE_EXPENSES", "ATTR", "#166534"),
        ("HEALTHCARE_COVERAGE", "ATTR", "#166534"),
    ]
    draw_entity_card(4, 52, 26, 32, "patients.csv", "Patient Demographics Dimension",
                     "#2563EB", "#FFFFFF", "#3B82F6", patient_fields)

    # 3. procedures.csv (Procedural Events Fact Table)
    procedure_fields = [
        ("DATE", "ATTR", "#0F172A"),
        ("PATIENT", "FK", "#2563EB"),
        ("ENCOUNTER", "FK", "#1E3A8A"),
        ("CODE", "ATTR", "#475569"),
        ("DESCRIPTION", "ATTR", "#0F172A"),
        ("BASE_COST", "ATTR", "#166534"),
        ("REASONCODE / DESC", "ATTR", "#475569"),
    ]
    draw_entity_card(4, 12, 26, 32, "procedures.csv", "Clinical Procedures & Interventions",
                     "#7C3AED", "#FFFFFF", "#8B5CF6", procedure_fields)

    # 4. payers.csv (Financial Coverage Dimension)
    payer_fields = [
        ("Id", "PK", "#D97706"),
        ("NAME", "ATTR", "#0F172A"),
        ("AMOUNT_COVERED", "ATTR", "#166534"),
        ("AMOUNT_UNCOVERED", "ATTR", "#B91C1C"),
        ("REVENUE", "ATTR", "#166534"),
        ("COVERED_ENCOUNTERS", "ATTR", "#0F172A"),
        ("UNCOVERED_ENCOUNTERS", "ATTR", "#B91C1C"),
    ]
    draw_entity_card(70, 52, 26, 32, "payers.csv", "Payer Organizations & Coverage",
                     "#D97706", "#FFFFFF", "#F59E0B", payer_fields)

    # 5. organizations.csv (Healthcare Facilities Dimension)
    org_fields = [
        ("Id", "PK", "#0D9488"),
        ("NAME", "ATTR", "#0F172A"),
        ("ADDRESS / CITY / STATE", "ATTR", "#475569"),
        ("LAT / LON", "ATTR", "#475569"),
        ("REVENUE", "ATTR", "#166534"),
        ("UTILIZATION", "ATTR", "#0F172A"),
    ]
    draw_entity_card(70, 12, 26, 32, "organizations.csv", "Provider Facilities & Locations",
                     "#0D9488", "#FFFFFF", "#14B8A6", org_fields)

    # Relationship Arrows & Badges
    # Patient -> Encounter (1 : N)
    ax.annotate("", xy=(36, 62), xytext=(30, 68),
                arrowprops=dict(arrowstyle="->", lw=2, color="#2563EB",
                                connectionstyle="arc3,rad=-0.1"))
    ax.text(32, 67, "1 : N\nPATIENT", fontsize=8, fontweight='bold', color="#2563EB", ha='center',
            bbox=dict(boxstyle="round,pad=0.2", facecolor='#DBEAFE', edgecolor='#93C5FD', lw=0.8))

    # Procedures -> Encounter (N : 1)
    ax.annotate("", xy=(36, 38), xytext=(30, 30),
                arrowprops=dict(arrowstyle="->", lw=2, color="#7C3AED",
                                connectionstyle="arc3,rad=0.1"))
    ax.text(32, 32, "N : 1\nENCOUNTER", fontsize=8, fontweight='bold', color="#7C3AED", ha='center',
            bbox=dict(boxstyle="round,pad=0.2", facecolor='#EDE9FE', edgecolor='#C4B5FD', lw=0.8))

    # Payers -> Encounter (1 : N)
    ax.annotate("", xy=(64, 62), xytext=(70, 68),
                arrowprops=dict(arrowstyle="->", lw=2, color="#D97706",
                                connectionstyle="arc3,rad=0.1"))
    ax.text(67.5, 67, "1 : N\nPAYER", fontsize=8, fontweight='bold', color="#D97706", ha='center',
            bbox=dict(boxstyle="round,pad=0.2", facecolor='#FEF3C7', edgecolor='#FCD34D', lw=0.8))

    # Organizations -> Encounter (1 : N)
    ax.annotate("", xy=(64, 38), xytext=(70, 30),
                arrowprops=dict(arrowstyle="->", lw=2, color="#0D9488",
                                connectionstyle="arc3,rad=-0.1"))
    ax.text(67.5, 32, "1 : N\nORGANIZATION", fontsize=8, fontweight='bold', color="#0D9488", ha='center',
            bbox=dict(boxstyle="round,pad=0.2", facecolor='#CCFBF1', edgecolor='#5EEAD4', lw=0.8))

    # Bottom Governance & Data Dictionary Banner
    dict_box = FancyBboxPatch((3, 2), 94, 7.5, boxstyle="round,pad=0.4,rounding_size=0.8",
                              facecolor='#1E293B', edgecolor='#0F172A', linewidth=1)
    ax.add_patch(dict_box)
    ax.text(5, 6.8, "DATA GOVERNANCE & SCHEMA VALIDATION GATES (Task 2 & 4)",
            fontsize=8.5, fontweight='bold', color='#38BDF8')
    ax.text(5, 3.8, "• Schema Key Validation: Verify 100% of foreign keys resolve without orphaned records in procedures or encounters.\n"
                    "• Zero-Inflation Guarantee: Aggregations joining procedures to encounters must preserve encounter grain without multiplying claim costs.\n"
                    "• Privacy Guardrail: Synthetic patient identifiers (PII) masked; zero clinical diagnosis claims derived from administrative codes.",
            fontsize=7.2, color='#E2E8F0', va='center')

    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, "fig1_healthcare_data_ecosystem.png")
    fig.savefig(fig_path, bbox_inches='tight', dpi=300)
    plt.close(fig)
    print(f"Generated: {fig_path}")


def create_fig2_patient_flow():
    """
    Figure 2: Hospital Patient Flow, Encounter Duration & Capacity Bottlenecks
    Visualizes patient arrival streams, triage, duration boundaries (>24h), and operational bottlenecks.
    """
    fig, ax = plt.subplots(figsize=(13.5, 7.8), dpi=300)
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title & Subtitle Header Box
    title_box = FancyBboxPatch((3, 88), 94, 9.5, boxstyle="round,pad=0.6,rounding_size=1.2",
                               facecolor='#0F172A', edgecolor='#020617', linewidth=1.5)
    ax.add_patch(title_box)
    ax.text(50, 93.8, "Hospital Patient Flow, Encounter Duration & Operational Bottlenecks",
            fontsize=15, fontweight='bold', color='white', ha='center', va='center')
    ax.text(50, 90.0, "Operational Dynamics Across Inflow Streams, Length of Stay (LoS), Bed Turnover, and Discharge Adjudication",
            fontsize=9.5, color='#94A3B8', ha='center', va='center')

    # Step 1: Patient Inflow Streams (Left Column)
    inflow_box = FancyBboxPatch((3, 14), 22, 69, boxstyle="round,pad=0.5,rounding_size=1.0",
                                facecolor='#EFF6FF', edgecolor='#3B82F6', linewidth=1.2)
    ax.add_patch(inflow_box)
    ax.text(14, 79.5, "1. INFLOW STREAMS", fontsize=11, fontweight='bold', color='#1E3A8A', ha='center')
    ax.text(14, 77.0, "Encounter Class Ingestion", fontsize=8, color='#3B82F6', ha='center')

    streams = [
        ("Ambulatory / Outpatient", "Scheduled routine specialist visits,\nsame-day diagnostics", "#1E3A8A"),
        ("Wellness / Preventive", "Annual wellness exams, pediatric\ncheckups, immunizations", "#0D9488"),
        ("Urgent Care", "Unscheduled episodic care for\nacute non-emergent needs", "#D97706"),
        ("Emergency (ED Inflow)", "High-acuity urgent walk-ins\nand ambulance transfers", "#DC2626")
    ]
    cur_y = 66
    for name, desc, col in streams:
        box = FancyBboxPatch((4.5, cur_y - 8), 19, 10.5, boxstyle="round,pad=0.3,rounding_size=0.6",
                             facecolor='white', edgecolor=col, linewidth=1.2)
        ax.add_patch(box)
        ax.text(5.5, cur_y + 0.5, name, fontsize=8.5, fontweight='bold', color=col)
        ax.text(5.5, cur_y - 4.5, desc, fontsize=7.2, color='#475569')
        cur_y -= 13.5

    # Step 2: Triage & Bed Allocation Center (Middle Column)
    triage_box = FancyBboxPatch((29, 14), 38, 69, boxstyle="round,pad=0.5,rounding_size=1.0",
                                facecolor='#FFFFFF', edgecolor='#64748B', linewidth=1.2)
    ax.add_patch(triage_box)
    ax.text(48, 79.5, "2. CLINICAL TRIAGE & BED CAPACITY GATE", fontsize=11, fontweight='bold', color='#0F172A', ha='center')
    ax.text(48, 77.0, "Duration Classification & Resource Partitioning", fontsize=8, color='#64748B', ha='center')

    # Stream A: Outpatient / Short Stay (< 24 Hours)
    short_stay = FancyBboxPatch((31, 52), 34, 21, boxstyle="round,pad=0.4,rounding_size=0.8",
                                facecolor='#F0FDF4', edgecolor='#16A34A', linewidth=1.2)
    ax.add_patch(short_stay)
    ax.text(48, 69.5, "Rapid Encounter / Outpatient Track", fontsize=9.5, fontweight='bold', color='#166534', ha='center')
    ax.text(48, 66.5, "[ Duration < 24 Hours ]", fontsize=8.5, fontweight='bold', color='#15803D', ha='center')
    ax.text(32.5, 61.5, "• Characteristic: Wellness, ambulatory, short ED encounters.\n"
                        "• Resource Impact: Low bed occupancy; high turnover velocity.\n"
                        "• Key Metric: Time-to-Consultation & Discharge Cycle Time.",
            fontsize=7.3, color='#14532D')

    # Stream B: Inpatient / Prolonged Stay (> 24 Hours)
    long_stay = FancyBboxPatch((31, 18), 34, 28, boxstyle="round,pad=0.4,rounding_size=0.8",
                               facecolor='#FEF2F2', edgecolor='#DC2626', linewidth=1.2)
    ax.add_patch(long_stay)
    ax.text(48, 42.5, "Inpatient Admission Track (Critical Resource)", fontsize=9.5, fontweight='bold', color='#991B1B', ha='center')
    ax.text(48, 39.5, "[ Duration > 24 Hours -- Bed Consuming ]", fontsize=8.5, fontweight='bold', color='#DC2626', ha='center')
    ax.text(32.5, 30.5, "• Characteristic: Multi-day hospitalizations, surgeries, ICU.\n"
                        "• Capacity Bottlenecks: ED Boarding delays, ward shortages.\n"
                        "• Operational Exposure: Occupies staffed physical bed capacity.\n"
                        "• Task 2 Focus: Identify proportion of encounters >24h.",
            fontsize=7.3, color='#7F1D1D')

    # Connecting arrows from inflow to triage
    ax.annotate("", xy=(31, 62), xytext=(25, 62),
                arrowprops=dict(arrowstyle="->", lw=2, color="#2563EB"))
    ax.annotate("", xy=(31, 32), xytext=(25, 32),
                arrowprops=dict(arrowstyle="->", lw=2, color="#DC2626"))

    # Step 3: Discharge & Operational Outcomes (Right Column)
    outcomes_box = FancyBboxPatch((71, 14), 26, 69, boxstyle="round,pad=0.5,rounding_size=1.0",
                                  facecolor='#F8FAFC', edgecolor='#0D9488', linewidth=1.2)
    ax.add_patch(outcomes_box)
    ax.text(84, 79.5, "3. DISCHARGE & IMPACT", fontsize=11, fontweight='bold', color='#0F766E', ha='center')
    ax.text(84, 77.0, "Operational Metrics & Turnover", fontsize=8, color='#0D9488', ha='center')

    # Discharge Cards
    disch_cards = [
        ("Same-Day Release", "Encounter closed without bed allocation;\nzero inpatient overnight overhead.", "#0D9488", 61),
        ("Inpatient Discharge", "Requires bed sanitization, nursing\nhandover, and pharmacy clearance.", "#0284C7", 43),
        ("Return Visit Risk", "Unplanned readmission or recurrent\nencounter tracking within 30 days.", "#D97706", 25)
    ]
    for d_title, d_desc, d_col, pos_y in disch_cards:
        box = FancyBboxPatch((72.5, pos_y - 6), 23, 13, boxstyle="round,pad=0.3,rounding_size=0.6",
                             facecolor='white', edgecolor=d_col, linewidth=1.2)
        ax.add_patch(box)
        ax.text(73.5, pos_y + 4.5, d_title, fontsize=8.5, fontweight='bold', color=d_col)
        ax.text(73.5, pos_y - 1.5, d_desc, fontsize=7.2, color='#475569')

    # Connect Middle to Right
    ax.annotate("", xy=(72.5, 62), xytext=(65, 62),
                arrowprops=dict(arrowstyle="->", lw=2, color="#16A34A"))
    ax.annotate("", xy=(72.5, 35), xytext=(65, 35),
                arrowprops=dict(arrowstyle="->", lw=2, color="#DC2626"))

    # Bottom Callout: Key Operational Takeaway
    bot_box = FancyBboxPatch((3, 2), 94, 8, boxstyle="round,pad=0.4,rounding_size=0.8",
                             facecolor='#1E3A8A', edgecolor='#0F172A', linewidth=1)
    ax.add_patch(bot_box)
    ax.text(5, 7.2, "OPERATIONAL BOTTLENECK INSIGHT FOR HOSPITAL EXECUTIVES",
            fontsize=8.5, fontweight='bold', color='#93C5FD')
    ax.text(5, 4.0, "Tracking encounter duration thresholds (>24h vs <=24h) allows Chief Operating Officers to separate routine outpatient traffic\n"
                    "from acute bed-consuming inpatient volume, resolving emergency department boarding and improving bed turnover efficiency.",
            fontsize=7.3, color='#F8FAFC', va='center')

    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, "fig2_patient_flow_bottlenecks.png")
    fig.savefig(fig_path, bbox_inches='tight', dpi=300)
    plt.close(fig)
    print(f"Generated: {fig_path}")


def create_fig3_financial_dynamics():
    """
    Figure 3: Financial Dynamics & Payer Reimbursement Exposure Flow
    Illustrates claim cost decomposition, payer reimbursement, zero-payer coverage gap, and hospital debt risk.
    """
    fig, ax = plt.subplots(figsize=(13.5, 7.8), dpi=300)
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title Banner
    title_box = FancyBboxPatch((3, 88), 94, 9.5, boxstyle="round,pad=0.6,rounding_size=1.2",
                               facecolor='#1E3A8A', edgecolor='#0F172A', linewidth=1.5)
    ax.add_patch(title_box)
    ax.text(50, 93.8, "Healthcare Financial Dynamics & Payer Coverage Exposure",
            fontsize=15, fontweight='bold', color='white', ha='center', va='center')
    ax.text(50, 90.0, "Decomposition of Encounter Claim Costs, Payer Adjudication, and Hospital Uncompensated Care Risk",
            fontsize=9.5, color='#BFDBFE', ha='center', va='center')

    # Left Section: Gross Claim Generation
    left_box = FancyBboxPatch((3, 14), 28, 69, boxstyle="round,pad=0.5,rounding_size=1.0",
                              facecolor='#FFFFFF', edgecolor='#2563EB', linewidth=1.2)
    ax.add_patch(left_box)
    ax.text(17, 79.5, "1. GROSS CLAIM GENERATION", fontsize=10.5, fontweight='bold', color='#1E3A8A', ha='center')
    ax.text(17, 77.0, "Encounter Billing Mechanics", fontsize=8, color='#2563EB', ha='center')

    # Decomposition Components
    comp1 = FancyBboxPatch((4.5, 60), 25, 14, boxstyle="round,pad=0.3,rounding_size=0.6",
                           facecolor='#EFF6FF', edgecolor='#3B82F6', linewidth=1)
    ax.add_patch(comp1)
    ax.text(5.5, 70.5, "Base Encounter Cost", fontsize=8.5, fontweight='bold', color='#1E3A8A')
    ax.text(5.5, 65.0, "• Class-based facility fee\n• Nursing overhead & bed rate\n• Baseline room & board", fontsize=7.2, color='#334155')

    comp2 = FancyBboxPatch((4.5, 41), 25, 16, boxstyle="round,pad=0.3,rounding_size=0.6",
                           facecolor='#F5F3FF', edgecolor='#8B5CF6', linewidth=1)
    ax.add_patch(comp2)
    ax.text(5.5, 53.5, "Procedure Base Costs", fontsize=8.5, fontweight='bold', color='#6D28D9')
    ax.text(5.5, 47.0, "• Surgical suite fees\n• High-cost specialized tests\n• Linked via ENCOUNTER foreign key", fontsize=7.2, color='#334155')

    comp3 = FancyBboxPatch((4.5, 18), 25, 20, boxstyle="round,pad=0.3,rounding_size=0.6",
                           facecolor='#FEF3C7', edgecolor='#D97706', linewidth=1)
    ax.add_patch(comp3)
    ax.text(5.5, 34.5, "TOTAL_CLAIM_COST", fontsize=9, fontweight='bold', color='#B45309')
    ax.text(5.5, 26.5, "TOTAL = Base Cost + Procedures\n\nOfficial Assignment Metric:\nCore financial measure across classes\nand payer contracts.", fontsize=7.2, color='#78350F')

    # Middle Section: Payer Adjudication Engine
    mid_box = FancyBboxPatch((35, 14), 30, 69, boxstyle="round,pad=0.5,rounding_size=1.0",
                             facecolor='#F8FAFC', edgecolor='#64748B', linewidth=1.2)
    ax.add_patch(mid_box)
    ax.text(50, 79.5, "2. PAYER ADJUDICATION", fontsize=10.5, fontweight='bold', color='#0F172A', ha='center')
    ax.text(50, 77.0, "Coverage Split & Rules", fontsize=8, color='#64748B', ha='center')

    # Tier A: Covered Portion
    tier_a = FancyBboxPatch((36.5, 48), 27, 26, boxstyle="round,pad=0.3,rounding_size=0.6",
                            facecolor='#F0FDF4', edgecolor='#16A34A', linewidth=1.2)
    ax.add_patch(tier_a)
    ax.text(50, 70.0, "Payer Covered Reimbursement", fontsize=8.5, fontweight='bold', color='#166534', ha='center')
    ax.text(50, 66.5, "[ PAYER_COVERAGE > $0 ]", fontsize=8, fontweight='bold', color='#15803D', ha='center')
    ax.text(38, 57.5, "• Commercial Insurance / Medicaid / Medicare\n"
                      "• Contracted reimbursement schedule\n"
                      "• Direct cash settlement to hospital",
            fontsize=7.2, color='#14532D')

    # Tier B: Zero Payer Coverage
    tier_b = FancyBboxPatch((36.5, 18), 27, 26, boxstyle="round,pad=0.3,rounding_size=0.6",
                            facecolor='#FFF1F2', edgecolor='#E11D48', linewidth=1.2)
    ax.add_patch(tier_b)
    ax.text(50, 40.0, "Zero Payer Coverage Exposure", fontsize=8.5, fontweight='bold', color='#9F1239', ha='center')
    ax.text(50, 36.5, "[ PAYER_COVERAGE == $0 ]", fontsize=8, fontweight='bold', color='#E11D48', ha='center')
    ax.text(38, 27.5, "• Uninsured patients / Self-pay\n"
                      "• Denied / Non-covered claims\n"
                      "• Core Track A Question #5 Focus",
            fontsize=7.2, color='#881337')

    # Arrow Left to Middle
    ax.annotate("", xy=(35, 48), xytext=(29.5, 48),
                arrowprops=dict(arrowstyle="->", lw=2, color="#0F172A"))

    # Right Section: Financial Exposure & Decision Support
    right_box = FancyBboxPatch((69, 14), 28, 69, boxstyle="round,pad=0.5,rounding_size=1.0",
                               facecolor='#FFFFFF', edgecolor='#0D9488', linewidth=1.2)
    ax.add_patch(right_box)
    ax.text(83, 79.5, "3. FINANCIAL EXPOSURE", fontsize=10.5, fontweight='bold', color='#0F766E', ha='center')
    ax.text(83, 77.0, "CFO & Revenue Cycle Impact", fontsize=8, color='#0D9488', ha='center')

    # Outcome 1: Secured Revenue
    out1 = FancyBboxPatch((70.5, 52), 25, 22, boxstyle="round,pad=0.3,rounding_size=0.6",
                          facecolor='#F0FDFA', edgecolor='#0D9488', linewidth=1)
    ax.add_patch(out1)
    ax.text(71.5, 70.0, "Secured Hospital Revenue", fontsize=8.5, fontweight='bold', color='#0F766E')
    ax.text(71.5, 62.0, "• Predictable operational cash flow\n• Low collection default risk\n• Foundation for operating budgets", fontsize=7.2, color='#134E4A')

    # Outcome 2: Uncompensated Care & Bad Debt
    out2 = FancyBboxPatch((70.5, 18), 25, 30, boxstyle="round,pad=0.3,rounding_size=0.6",
                          facecolor='#FEF2F2', edgecolor='#DC2626', linewidth=1)
    ax.add_patch(out2)
    ax.text(71.5, 44.0, "Uncompensated Care & Risk", fontsize=8.5, fontweight='bold', color='#991B1B')
    ax.text(71.5, 33.5, "• Patient Out-of-Pocket Liability:\n  Liability = Claim Cost - Coverage\n• Bad Debt & Charity Write-Offs\n• Financial Distress on Solvency\n• Requirement: Pre-service financial\n  counseling & payer renegotiation", fontsize=7.1, color='#7F1D1D')

    # Arrows Middle to Right
    ax.annotate("", xy=(69, 62), xytext=(63.5, 62),
                arrowprops=dict(arrowstyle="->", lw=2, color="#16A34A"))
    ax.annotate("", xy=(69, 32), xytext=(63.5, 32),
                arrowprops=dict(arrowstyle="->", lw=2, color="#DC2626"))

    # Bottom Banner
    bot_box = FancyBboxPatch((3, 2), 94, 8, boxstyle="round,pad=0.4,rounding_size=0.8",
                             facecolor='#0F172A', edgecolor='#020617', linewidth=1)
    ax.add_patch(bot_box)
    ax.text(5, 7.2, "CRITICAL FINANCIAL RECONCILIATION RULE (Success Criterion #1)",
            fontsize=8.5, fontweight='bold', color='#F59E0B')
    ax.text(5, 4.0, "Total Claim Cost must reconcile exactly with (Payer Coverage + Patient Liability) with $0.00 delta.\n"
                    "Zero-coverage encounters identify the immediate target population for hospital charity care policy and risk provisioning.",
            fontsize=7.3, color='#F8FAFC', va='center')

    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, "fig3_financial_cost_coverage_flow.png")
    fig.savefig(fig_path, bbox_inches='tight', dpi=300)
    plt.close(fig)
    print(f"Generated: {fig_path}")


def create_fig4_stakeholder_matrix():
    """
    Figure 4: Multi-Stakeholder Decision Support Matrix
    4-quadrant layout matching the 4 key roles: COO, CFO, Clinical Directors, Health Informatics.
    """
    fig, ax = plt.subplots(figsize=(13.5, 7.8), dpi=300)
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Header
    title_box = FancyBboxPatch((3, 88), 94, 9.5, boxstyle="round,pad=0.6,rounding_size=1.2",
                               facecolor='#1E3A8A', edgecolor='#0F172A', linewidth=1.5)
    ax.add_patch(title_box)
    ax.text(50, 93.8, "Multi-Stakeholder Operational Decision Support Matrix",
            fontsize=15, fontweight='bold', color='white', ha='center', va='center')
    ax.text(50, 90.0, "Translating Healthcare Data Intelligence into Targeted Executive Interventions",
            fontsize=9.5, color='#BFDBFE', ha='center', va='center')

    # 4 Quadrants
    quadrants = [
        # Q1: COO (Top-Left)
        {
            "rect": (3, 49, 45.5, 36),
            "hdr_col": "#1E3A8A", "bg_col": "#EFF6FF", "border_col": "#3B82F6",
            "role": "CHIEF OPERATING OFFICER (COO)",
            "subtitle": "Patient Throughput, Bed Capacity & Staffing",
            "kpis": "• Average Length of Stay (ALoS)\n• % Encounters > 24 Hours\n• Emergency Boarding Hours",
            "decisions": "• Shift nurse staffing toward high-volume intake days.\n• Streamline inpatient discharge before 11:00 AM.\n• Reallocate staffed beds from low-acuity to acute care."
        },
        # Q2: CFO (Top-Right)
        {
            "rect": (51.5, 49, 45.5, 36),
            "hdr_col": "#D97706", "bg_col": "#FFFBEB", "border_col": "#F59E0B",
            "role": "CHIEF FINANCIAL OFFICER (CFO)",
            "subtitle": "Revenue Cycle, Payer Mix & Uncompensated Care",
            "kpis": "• Total Claim Cost vs Reimbursement\n• % Zero Payer Coverage Encounters\n• Average Claim Cost by Payer",
            "decisions": "• Renegotiate sub-optimal commercial payer contracts.\n• Establish bad-debt reserves for high-cost self-pay classes.\n• Deploy pre-procedure insurance verification & counseling."
        },
        # Q3: Clinical Services Director (Bottom-Left)
        {
            "rect": (3, 9, 45.5, 37),
            "hdr_col": "#0D9488", "bg_col": "#F0FDFA", "border_col": "#14B8A6",
            "role": "DIRECTOR OF CLINICAL SERVICES",
            "subtitle": "Operating Theaters, Specialized Suites & Utilization",
            "kpis": "• Procedure Frequency Distribution\n• Procedure Average Base Cost\n• Operating Room Block Utilization Rate",
            "decisions": "• Prioritize maintenance contracts for high-frequency gear.\n• Schedule elective procedures on low-emergency inflow days.\n• Standardize surgical trays to reduce procedural cost variance."
        },
        # Q4: Health Informatics & Quality (Bottom-Right)
        {
            "rect": (51.5, 9, 45.5, 37),
            "hdr_col": "#7C3AED", "bg_col": "#F5F3FF", "border_col": "#8B5CF6",
            "role": "HEALTH INFORMATICS & QUALITY OFFICER",
            "subtitle": "EHR Integrity, Care Continuity & Return Visits",
            "kpis": "• % Missing Start/Stop Encounter Timestamps\n• 30-Day Operational Return Visit Rate\n• Uncoded Encounter Ratio",
            "decisions": "• Implement EHR mandatory field validation at discharge.\n• Track recurrent emergency visit cohorts for care plans.\n• Audit clinical coding consistency across facilities."
        }
    ]

    for q in quadrants:
        x, y, w, h = q["rect"]
        card = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=0.8",
                              facecolor=q["bg_col"], edgecolor=q["border_col"], linewidth=1.2)
        ax.add_patch(card)
        hdr = FancyBboxPatch((x, y + h - 5), w, 5, boxstyle="round,pad=0.2,rounding_size=0.6",
                             facecolor=q["hdr_col"], edgecolor=q["hdr_col"])
        ax.add_patch(hdr)
        ax.text(x + w/2, y + h - 2.2, q["role"], fontsize=9.5, fontweight='bold', color='white', ha='center')
        ax.text(x + w/2, y + h - 4.0, q["subtitle"], fontsize=7.5, color='#F1F5F9', ha='center')

        # Content
        ax.text(x + 2, y + h - 7.5, "CORE MONITORED METRICS (KPIs):", fontsize=7.8, fontweight='bold', color=q["hdr_col"])
        ax.text(x + 2, y + h - 13.5, q["kpis"], fontsize=7.4, color='#334155')

        ax.text(x + 2, y + h - 17.0, "SUPPORTED OPERATIONAL DECISIONS:", fontsize=7.8, fontweight='bold', color=q["hdr_col"])
        ax.text(x + 2, y + h - 26.5, q["decisions"], fontsize=7.4, color='#334155')

    # Bottom Footer
    ax.text(50, 4, "Ethical Guardrail: All decisions strictly address operational logistics, facility capacity, and financial risk — never individual medical therapy.",
            fontsize=7.8, style='italic', color='#64748B', ha='center')

    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, "fig4_stakeholder_decision_matrix.png")
    fig.savefig(fig_path, bbox_inches='tight', dpi=300)
    plt.close(fig)
    print(f"Generated: {fig_path}")


def create_fig5_quality_gates():
    """
    Figure 5: Phase 1 Quality Gate & Verification Pipeline
    Visualizes the 5 measurable success criteria as verifiable engineering quality gates.
    """
    fig, ax = plt.subplots(figsize=(13.5, 7.8), dpi=300)
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title Banner
    title_box = FancyBboxPatch((3, 88), 94, 9.5, boxstyle="round,pad=0.6,rounding_size=1.2",
                               facecolor='#0F172A', edgecolor='#020617', linewidth=1.5)
    ax.add_patch(title_box)
    ax.text(50, 93.8, "Technical Quality Gates & Measurable Success Criteria Pipeline",
            fontsize=15, fontweight='bold', color='white', ha='center', va='center')
    ax.text(50, 90.0, "Assignment Task 3 & Task 4 Operational Verification Standards",
            fontsize=9.5, color='#94A3B8', ha='center', va='center')

    gates = [
        ("GATE 1", "Financial Reconciliation", "Delta = $0.00",
         "100% of calculated Total Claim Costs,\nPayer Coverage, and Patient Liability\nmust match an independent calculation\nscript to the exact cent.",
         "#1E3A8A", "#EFF6FF", 4),
        ("GATE 2", "Temporal Logic Check", "0% Negative Durations",
         "Stop timestamp must be >= Start timestamp.\nEncounters missing Stop time must be\nsystematically flagged as open/censored\nwithout distorting duration averages.",
         "#0D9488", "#F0FDFA", 23),
        ("GATE 3", "Relational Grain Integrity", "1:N Grain Preservation",
         "When joining procedures to encounters,\nanalytical aggregation layers must\npreserve encounter grain without Cartesian\nrow multiplication or cost inflation.",
         "#7C3AED", "#F5F3FF", 42),
        ("GATE 4", "Scripted Reproducibility", "100% Automated Re-run",
         "All data preparation, cleaning scripts,\nand reporting calculations must execute\nend-to-end via a single automated run\nwithout manual adjustments.",
         "#D97706", "#FFFBEB", 61),
        ("GATE 5", "Privacy & Ethical Safety", "Zero PII & Clinical Claims",
         "Zero synthetic patient identifiers (names,\naddresses, SSNs) exposed in outputs.\nZero clinical treatment claims derived\nfrom administrative billing codes.",
         "#DC2626", "#FEF2F2", 80)
    ]

    for g_num, g_title, g_badge, g_desc, col_hdr, col_bg, pos_x in gates:
        card = FancyBboxPatch((pos_x, 18), 16.5, 66, boxstyle="round,pad=0.4,rounding_size=0.8",
                              facecolor=col_bg, edgecolor=col_hdr, linewidth=1.2)
        ax.add_patch(card)

        # Header Badge
        hdr = FancyBboxPatch((pos_x, 77), 16.5, 7, boxstyle="round,pad=0.2,rounding_size=0.6",
                             facecolor=col_hdr, edgecolor=col_hdr)
        ax.add_patch(hdr)
        ax.text(pos_x + 8.25, 81.8, g_num, fontsize=9.5, fontweight='bold', color='white', ha='center')
        ax.text(pos_x + 8.25, 79.0, g_title, fontsize=7.2, fontweight='bold', color='#F1F5F9', ha='center')

        # Metric Target Pill
        pill = FancyBboxPatch((pos_x + 1, 68), 14.5, 6, boxstyle="round,pad=0.2,rounding_size=0.5",
                              facecolor='white', edgecolor=col_hdr, linewidth=1)
        ax.add_patch(pill)
        ax.text(pos_x + 8.25, 71.0, g_badge, fontsize=8, fontweight='bold', color=col_hdr, ha='center')

        # Description
        ax.text(pos_x + 1.2, 52, g_desc, fontsize=7.2, color='#1E293B', va='center')

        # Status Checkmark icon badge
        badge_bot = FancyBboxPatch((pos_x + 2.5, 21), 11.5, 5, boxstyle="round,pad=0.2,rounding_size=0.4",
                                   facecolor=col_hdr, edgecolor=col_hdr)
        ax.add_patch(badge_bot)
        ax.text(pos_x + 8.25, 23.5, "VERIFIED GATE", fontsize=7.5, fontweight='bold', color='white', ha='center')

        # Arrow between gates
        if pos_x < 80:
            ax.annotate("", xy=(pos_x + 18.5, 50), xytext=(pos_x + 16.5, 50),
                        arrowprops=dict(arrowstyle="->", lw=2, color="#64748B"))

    # Bottom Safety Warning
    warn_box = FancyBboxPatch((3, 2), 94, 11, boxstyle="round,pad=0.4,rounding_size=0.8",
                              facecolor='#FEF2F2', edgecolor='#DC2626', linewidth=1.2)
    ax.add_patch(warn_box)
    ax.text(5, 10.0, "CRITICAL SAFETY MANDATE (AnalystLab Africa Document Control Task 4):",
            fontsize=8.5, fontweight='bold', color='#991B1B')
    ax.text(5, 5.5, "• Practice Database Isolation: The SQL script `create_hospital_db.sql` drops and recreates `hospital_db`. Never execute it against production.\n"
                    "• Evidence Boundary: Results reflect administrative and financial encounter trends. Correlation does not imply clinical quality.",
            fontsize=7.3, color='#7F1D1D')

    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, "fig5_quality_gates_governance.png")
    fig.savefig(fig_path, bbox_inches='tight', dpi=300)
    plt.close(fig)
    print(f"Generated: {fig_path}")


if __name__ == "__main__":
    print("Generating corporate report figures...")
    create_fig1_data_ecosystem()
    create_fig2_patient_flow()
    create_fig3_financial_dynamics()
    create_fig4_stakeholder_matrix()
    create_fig5_quality_gates()
    print("All 5 report figures generated successfully.")

