import streamlit as st
import pandas as pd
import numpy as np
from fpdf import FPDF
from datetime import datetime

# --- COTTINGTON BRANDING ---
st.set_page_config(page_title="Cottington Capital", page_icon="🏛️", layout="wide") # Switched to Wide Mode for Dashboard feel

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #d4af37; }
    h1, h2, h3, h4, p, label { font-family: 'Times New Roman', serif; color: #d4af37 !important; }
    .stSelectbox > div > div { background-color: #1c1f26; color: #ffffff; }
    .stTextInput > div > div > input { color: #ffffff; background-color: #1c1f26; }
    .stNumberInput > div > div > input { color: #ffffff; background-color: #1c1f26; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-family: 'Arial', sans-serif; }
    
    /* BUTTON STYLING */
    .stButton > button {
        color: #000000 !important;
        background-color: #d4af37 !important;
        border-radius: 5px;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #bfa345 !important;
        color: #000000 !important;
        border: 1px solid #ffffff;
    }

    /* TABS */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #1c1f26;
        border-radius: 4px 4px 0px 0px;
        color: #ffffff !important;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #d4af37 !important;
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- PDF GENERATOR ---
def create_pdf(report_type, client_name, inputs, metrics, schedule_df, advice_text):
    class PDF(FPDF):
        def header(self):
            self.set_draw_color(212, 175, 55)
            self.set_line_width(1)
            self.rect(5, 5, 200, 287)
            self.set_line_width(0.3)
            self.rect(7, 7, 196, 283)
            self.set_fill_color(14, 17, 23)
            self.rect(7, 7, 196, 33, 'F')
            self.set_y(13)
            self.set_font('Times', 'B', 24)
            self.set_text_color(212, 175, 55)
            self.cell(0, 10, 'COTTINGTON CAPITAL', 0, 1, 'C')
            self.set_font('Times', 'I', 10)
            self.set_text_color(255, 255, 255)
            self.cell(0, 5, 'Wealth Architecture & Strategic Advisory', 0, 1, 'C')
            self.ln(15)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 7)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'CONFIDENTIAL - Page {self.page_no()}', 0, 0, 'C')

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=25)
    pdf.add_page()
    
    # Metadata
    pdf.set_y(45)
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(100, 8, f"PREPARED FOR: {client_name.upper()}", 0, 0, 'L')
    pdf.cell(0, 8, f"DATE: {datetime.now().strftime('%d %B %Y').upper()}", 0, 1, 'R')
    pdf.ln(2)

    # Parameters
    pdf.set_fill_color(212, 175, 55)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 6, f'  1. {report_type.upper()} PARAMETERS', 0, 1, 'L', fill=True)
    pdf.ln(3)

    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(50, 50, 50)
    for key, value in inputs.items():
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(70, 6, f"{key}", 0, 0)
        pdf.set_font('Arial', '', 9)
        pdf.cell(0, 6, f"{value}", 0, 1)
        pdf.set_draw_color(220, 220, 220)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # Analysis
    pdf.set_fill_color(212, 175, 55)
    pdf.set_font('Times', 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, '  2. FINANCIAL ANALYSIS (NET OF FEES)', 0, 1, 'L', fill=True)
    pdf.ln(4)
    
    pdf.set_font('Arial', 'B', 9)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(95, 7, "METRIC", 1, 0, 'C', fill=True)
    pdf.cell(95, 7, "VALUE", 1, 1, 'C', fill=True)
    
    pdf.set_font('Arial', '', 9)
    for label, value in metrics.items():
        pdf.cell(95, 8, label, 1, 0, 'L')
        pdf.set_font('Arial', 'B', 9)
        if "Real" in label or "Net" in label: pdf.set_text_color(150, 0, 0)
        else: pdf.set_text_color(0, 0, 0)
        pdf.cell(95, 8, value, 1, 1, 'R')
        pdf.set_font('Arial', '', 9)
        pdf.set_text_color(0, 0, 0)

    pdf.ln(6)

    # Verdict
    pdf.set_fill_color(14, 17, 23)
    pdf.set_text_color(212, 175, 55)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 6, '  3. COTTINGTON ADVISORY VERDICT', 0, 1, 'L', fill=True)
    pdf.ln(4)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', '', 9)
    pdf.multi_cell(0, 4, advice_text)
    pdf.ln(4)
    
    # Disclaimer
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 6)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 4, "IMPORTANT LEGAL DISCLAIMER & INDEMNITY", 0, 1, 'L')
    pdf.set_font('Arial', '', 5)
    disclaimer_text = (
        "1. STRATEGIC TOOL ONLY: This report is a quantitative decision-support tool. Cottington Capital is not a registered FSP. "
        "2. PROJECTION METHODOLOGY: Figures are projections. 'Net Value' accounts for estimated fees and taxes as provided. "
        "3. LIMITATION OF LIABILITY: You assume full responsibility for financial decisions. Consult a qualified actuary."
    )
    pdf.multi_cell(0, 3, disclaimer_text)

    return pdf.output(dest='S').encode('latin-1')

# --- LOGIC: WEALTH PROJECTOR (WITH FEES) ---
def calculate_projection(principal, contribution, rate, inflation, years, freq_option, timing_option, annual_fee, tax_rate):
    freq_map = {"Monthly": 12, "Quarterly": 4, "Semi-Annually": 2, "Yearly": 1}
    m = freq_map[freq_option]
    total_periods = int(years * m)

    # Rates
    r_nom_per = (rate / 100) / m
    real_rate_annual = ((1 + rate/100) / (1 + inflation/100)) - 1
    r_real_per = real_rate_annual / m
    
    # Fee Deduction (Approximate monthly drag)
    fee_per = (annual_fee / 100) / m
    
    # Net Rate (Growth - Fee)
    r_net_per = r_nom_per - fee_per

    data = []
    bal_nom = principal
    bal_net = principal # Net of Fees
    curr_shield_contrib = contribution
    
    for period in range(1, total_periods + 1):
        # Inflation Escalation
        if period > 1 and (period - 1) % m == 0:
            curr_shield_contrib *= (1 + inflation / 100)
        
        # Advance Timing
        if timing_option == "Start of Period (Advance)":
            bal_nom += contribution
            bal_net += contribution
            
            # Growth
            bal_nom += (bal_nom * r_nom_per)
            bal_net += (bal_net * r_net_per) # Grow at net rate
            
        else: # Arrears
            bal_nom += (bal_nom * r_nom_per)
            bal_net += (bal_net * r_net_per)
            
            bal_nom += contribution
            bal_net += contribution
        
        if period % m == 0:
            # Apply Tax only at reporting intervals for visualization? 
            # No, tax is usually on exit. We calculate "Post-Tax Value" as a derived metric.
            
            # Simple CGT Estimate on Gains: (Current Balance - Total Contribs) * Tax Rate
            # This is a simplification for the "Truth" visual
            total_invested = principal + (contribution * period) # Base invested
            gain = max(0, bal_net - total_invested)
            tax_drag = gain * (tax_rate / 100)
            final_pocket = bal_net - tax_drag
            
            # Real Value of that Final Pocket
            real_pocket = final_pocket / ((1 + inflation/100)**(period/m))

            data.append({
                "Year": period // m, 
                "Gross Value (Bank Promise)": round(bal_nom, 2),
                "Net Value (After Fees & Tax)": round(final_pocket, 2),
                "Real Value (Buying Power)": round(real_pocket, 2)
            })
            
    return pd.DataFrame(data), bal_nom, bal_net - tax_drag, real_pocket

# --- MAIN UI ---
st.title("🏛️ COTTINGTON CAPITAL")

# SIDEBAR FOR THE "SILENT KILLERS"
with st.sidebar:
    st.header("💀 The Silent Killers")
    st.markdown("Most projections ignore costs. Add them here to see the truth.")
    p_fee = st.number_input("Annual Fee (%)", value=1.5, step=0.1, help="Asset Management + Platform Fees (Avg 1.5%)")
    p_tax = st.number_input("Exit Tax Rate (%)", value=18.0, step=0.5, help="Effective Capital Gains Tax")
    st.markdown("---")
    st.caption("Cottington Capital © 2026")

tab1, tab2 = st.tabs(["Wealth Projector", "Goal Seeker"])

# --- TAB 1: PROJECTOR ---
with tab1:
    st.markdown("#### The Truth Projector")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        p_initial = st.number_input("Start Capital (R)", 0.0, step=1000.0)
        p_contrib = st.number_input("Monthly Contrib (R)", 1000.0, step=100.0)
    with c2:
        p_rate = st.number_input("Return (%)", 10.0, step=0.5)
        p_inf = st.number_input("Inflation (%)", 6.0, step=0.5)
    with c3:
        p_years = st.number_input("Years", 10, step=1)
        p_time = st.selectbox("Timing", ("Advance", "Arrears"))

    if st.button("Reveal the Truth"):
        df, val_gross, val_net, val_real = calculate_projection(
            p_initial, p_contrib, p_rate, p_inf, p_years, "Monthly", 
            "Start of Period (Advance)" if p_time == "Advance" else "End of Period (Arrears)", 
            p_fee, p_tax
        )
        st.session_state['res'] = {'df': df, 'gross': val_gross, 'net': val_net, 'real': val_real}

    if 'res' in st.session_state:
        r = st.session_state['res']
        
        # The Iconic "Truth" Display
        k1, k2, k3 = st.columns(3)
        with k1: st.metric("Bank's Promise (Gross)", f"R {r['gross']:,.0f}")
        with k2: st.metric("Your Reality (Net of Fee/Tax)", f"R {r['net']:,.0f}", delta_color="off")
        with k3: 
            loss = r['gross'] - r['net']
            st.metric("Lost to Fees/Tax", f"- R {loss:,.0f}", delta_color="inverse")

        st.line_chart(r['df'], x="Year", y=["Gross Value (Bank Promise)", "Net Value (After Fees & Tax)", "Real Value (Buying Power)"], color=["#d4af37", "#808080", "#ff4b4b"])
        
        st.info(f"💡 **ACTUARIAL INSIGHT:** Fees and Taxes consumed **{((loss/r['gross'])*100):.1f}%** of your potential wealth. Minimizing fees is as important as maximizing returns.")

        # PDF Report
        st.write("---")
        c_name = st.text_input("Client Name", "Valued Client")
        if st.button("Download Truth Report"):
            inputs = {"Investment": f"R {p_contrib}", "Return": f"{p_rate}%", "Fees": f"{p_fee}%", "Tax": f"{p_tax}%"}
            metrics = {"GROSS VALUE": f"R {r['gross']:,.2f}", "NET VALUE": f"R {r['net']:,.2f}", "LOST TO FEES": f"- R {loss:,.2f}"}
            advice = f"Warning: Fees and Taxes are projected to erode R {loss:,.0f} of your wealth. This report highlights the discrepancy between Gross Returns ({p_rate}%) and Net Real Returns."
            pdf_bytes = create_pdf("Truth Audit", c_name, inputs, metrics, r['df'], advice)
            st.download_button("📥 Download PDF", pdf_bytes, "Cottington_Truth_Report.pdf", "application/pdf")

# --- TAB 2: GOAL SEEKER (Simplified for Logic) ---
with tab2:
    st.info("The Goal Seeker module is currently being upgraded to include Tax Drag. Use Tab 1 for the full 'Silent Killer' analysis.")
