import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# --- COTTINGTON BRANDING ---
st.set_page_config(page_title="Cottington Capital", page_icon="🏛️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #d4af37; }
    h1, h2, h3, h4, p, label { font-family: 'Times New Roman', serif; color: #d4af37 !important; }
    .stSelectbox > div > div { background-color: #1c1f26; color: #ffffff; }
    .stButton>button { color: #000000; background-color: #d4af37; border-radius: 5px; font-weight: bold; }
    .stTextInput > div > div > input { color: #ffffff; background-color: #1c1f26; }
    .stNumberInput > div > div > input { color: #ffffff; background-color: #1c1f26; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-family: 'Arial', sans-serif; }
    div[data-testid="stTable"] { color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- PDF GENERATOR (2-Page Professional Report) ---
def create_pdf(client_name, inputs, val_nom, val_real, inflation_loss, val_shield, schedule_df):
    class PDF(FPDF):
        def header(self):
            # Header is only for Page 1 mainly, but we keep branding small on Page 2
            if self.page_no() == 1:
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
    
    # --- PAGE 1: EXECUTIVE SUMMARY ---
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
    pdf.cell(0, 6, '  1. CLIENT PARAMETERS', 0, 1, 'L', fill=True)
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

    # Audit
    pdf.set_fill_color(212, 175, 55)
    pdf.set_font('Times', 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, '  2. INFLATION IMPACT AUDIT', 0, 1, 'L', fill=True)
    pdf.ln(4)
    
    pdf.set_font('Arial', 'B', 9)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(95, 7, "METRIC", 1, 0, 'C', fill=True)
    pdf.cell(95, 7, "PROJECTED VALUE", 1, 1, 'C', fill=True)
    
    pdf.set_font('Arial', '', 9)
    pdf.cell(95, 8, "Nominal Value (Face Value)", 1, 0, 'L')
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(95, 8, f"R {val_nom:,.0f}", 1, 1, 'R')
    
    pdf.set_font('Arial', '', 9)
    pdf.cell(95, 8, "Real Buying Power (Today's Terms)", 1, 0, 'L')
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(200, 0, 0)
    pdf.cell(95, 8, f"R {val_real:,.0f}", 1, 1, 'R')
    pdf.set_text_color(0, 0, 0)

    pdf.ln(4)
    pdf.set_fill_color(255, 235, 235)
    pdf.set_draw_color(200, 0, 0)
    pdf.rect(10, pdf.get_y(), 190, 12, 'DF')
    pdf.set_xy(12, pdf.get_y() + 3)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(150, 0, 0)
    pdf.cell(0, 6, f"WARNING: Inflation is projected to erode R {inflation_loss:,.0f} of your purchasing power.", 0, 1, 'C')
    pdf.ln(6)

    # Strategy
    pdf.set_fill_color(14, 17, 23)
    pdf.set_text_color(212, 175, 55)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 6, '  3. COTTINGTON RECOVERY STRATEGY', 0, 1, 'L', fill=True)
    pdf.ln(4)
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', '', 9)
    pdf.multi_cell(0, 4, "To neutralize inflation, an 'Annual Escalation' strategy is recommended. By increasing contributions annually to match inflation, the projected Nominal Value increases to:")
    pdf.ln(1)
    pdf.set_font('Times', 'B', 16)
    pdf.set_text_color(14, 17, 23)
    pdf.cell(0, 8, f"R {val_shield:,.0f}", 0, 1, 'C')
    
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, "(See Page 2 for Full Contribution Schedule)", 0, 1, 'C')

    # Disclaimer (Bottom of Page 1)
    pdf.set_y(-30)
    pdf.set_font('Arial', 'B', 6)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 4, "DISCLAIMER OF LIABILITY", 0, 1, 'L')
    pdf.set_font('Arial', '', 5)
    pdf.multi_cell(0, 3, "This document contains proprietary financial projections generated by Cottington Capital. 'Real Value' is calculated using the Fisher Equation to adjust for inflation. These figures are mathematical estimates based on the parameters provided and assume a constant rate of return. They do not account for tax implications or market volatility unless explicitly stated.")

    # --- PAGE 2: FULL SCHEDULE ---
    pdf.add_page()
    
    # Page 2 Header
    pdf.set_font('Times', 'B', 14)
    pdf.set_text_color(14, 17, 23)
    pdf.cell(0, 10, 'APPENDIX: REQUIRED CONTRIBUTION SCHEDULE', 0, 1, 'L')
    pdf.ln(5)
    
    # Table Header
    pdf.set_font('Arial', 'B', 9)
    pdf.set_fill_color(212, 175, 55)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(30, 8, "Year", 1, 0, 'C', fill=True)
    pdf.cell(50, 8, "Required Monthly Premium", 1, 1, 'C', fill=True)
    
    # Table Content (Full Loop)
    pdf.set_font('Arial', '', 9)
    pdf.set_fill_color(245, 245, 245)
    
    # Loop through EVERY year in the schedule
    for index, row in schedule_df.iterrows():
        # Clean up the output
        year_val = int(row['Year'])
        premium_val = f"R {row['Shielded Premium']:,.2f}"
        
        # Simple alternation for readability
        fill = True if index % 2 == 0 else False
        pdf.cell(30, 7, f"Year {year_val}", 1, 0, 'C', fill=fill)
        pdf.cell(50, 7, premium_val, 1, 1, 'C', fill=fill)

    return pdf.output(dest='S').encode('latin-1')

# --- ACTUARIAL LOGIC ---
def calculate_scenarios(principal, contribution, rate, inflation, years, freq_option, timing_option):
    freq_map = {"Monthly": 12, "Quarterly": 4, "Semi-Annually": 2, "Yearly": 1}
    m = freq_map[freq_option]
    total_periods = int(years * m)

    r_nom_per = (rate / 100) / m
    real_rate_annual = ((1 + rate/100) / (1 + inflation/100)) - 1
    r_real_per = real_rate_annual / m

    data = []
    bal_nom = principal
    bal_real_power = principal 
    bal_shield = principal
    curr_shield_contrib = contribution
    
    for period in range(1, total_periods + 1):
        if period > 1 and (period - 1) % m == 0:
            curr_shield_contrib *= (1 + inflation / 100)
        
        if timing_option == "Start of Period (Advance)":
            bal_nom += contribution
            bal_real_power += contribution 
            bal_nom += (bal_nom * r_nom_per)
            bal_real_power += (bal_real_power * r_real_per)
            bal_shield += curr_shield_contrib
            bal_shield += (bal_shield * r_nom_per)
        else:
            bal_nom += (bal_nom * r_nom_per)
            bal_real_power += (bal_real_power * r_real_per)
            bal_nom += contribution
            bal_real_power += contribution
            bal_shield += (bal_shield * r_nom_per)
            bal_shield += curr_shield_contrib
        
        if period % m == 0:
            data.append({
                "Year": period // m, 
                "Nominal Value (Bank Balance)": round(bal_nom, 2),
                "Real Buying Power": round(bal_real_power, 2),
                "Shielded Value (Smart Plan)": round(bal_shield, 2),
                "Shielded Premium": round(curr_shield_contrib, 2)
            })
            
    return pd.DataFrame(data), bal_nom, bal_real_power, bal_shield

# --- UI LOGIC ---
st.title("🏛️ COTTINGTON CAPITAL")
st.markdown("#### Strategic Wealth Advisory")
st.write("---")

# Use Number Input for Precision
col1, col2 = st.columns(2)
with col1:
    initial_investment = st.number_input("Starting Capital (R)", value=0.0, step=1000.0)
    contribution_amount = st.number_input("Monthly Contribution (R)", value=1000.0, step=100.0)
with col2:
    # PRECISION CHANGE: number_input instead of slider
    interest_rate = st.number_input("Market Return (%)", value=10.0, step=0.1, format="%.2f")
    inflation_rate = st.number_input("Inflation / CPI (%)", value=6.0, step=0.1, format="%.2f")

col3, col4 = st.columns(2)
with col3:
    time_horizon = st.number_input("Duration (Years)", value=10, step=1)
    frequency = st.selectbox("Frequency", ("Monthly", "Quarterly", "Semi-Annually", "Yearly"))
with col4:
    timing = st.selectbox("Timing", ("Start of Period (Advance)", "End of Period (Arrears)"))

st.write("---")

# BUTTON ACTION
if st.button("Initialize Reality Check"):
    df, val_nom, val_real, val_shield = calculate_scenarios(
        initial_investment, contribution_amount, interest_rate, 
        inflation_rate, time_horizon, frequency, timing
    )
    st.session_state['results'] = {
        'df': df,
        'val_nom': val_nom,
        'val_real': val_real,
        'val_shield': val_shield,
        'loss': val_nom - val_real
    }

# CHECK SESSION STATE
if 'results' in st.session_state:
    res = st.session_state['results']
    
    st.subheader("The Reality of Inflation")
    m1, m2, m3 = st.columns(3)
    with m1: st.metric("Nominal Value (Face Value)", f"R {res['val_nom']:,.0f}")
    with m2: st.metric("Real Buying Power", f"R {res['val_real']:,.0f}", delta_color="off")
    with m3: st.metric("Loss Due to Inflation", f"- R {res['loss']:,.0f}", delta_color="inverse")

    st.line_chart(res['df'], x="Year", y=["Nominal Value (Bank Balance)", "Real Buying Power"], color=["#d4af37", "#ff4b4b"])

    st.write("---")
    st.subheader("🛡️ The Cottington Solution")
    st.info(f"""
    **STRATEGIC ADVICE:** To stop this loss of buying power, you must increase your contribution by **{inflation_rate}% annually**.
    **Outcome if you switch to the Smart Plan:** R {res['val_shield']:,.0f}
    """)
    
    with st.expander("View Full Payment Schedule"):
        st.dataframe(res['df'][["Year", "Shielded Premium"]].set_index("Year"))

    # PDF SECTION
    st.write("---")
    st.subheader("📄 Client Report Generator")
    
    client_name = st.text_input("Enter Client Name for Report", "Valued Client")
    
    input_data = {
        "Initial Investment": f"R {initial_investment:,.2f}",
        "Contribution": f"R {contribution_amount:,.2f} ({frequency})",
        "Annual Return (Rate)": f"{interest_rate}%",
        "Inflation (CPI)": f"{inflation_rate}%",
        "Duration": f"{time_horizon} Years"
    }
    
    pdf_bytes = create_pdf(client_name, input_data, res['val_nom'], res['val_real'], res['loss'], res['val_shield'], res['df'])
    
    st.download_button(
        label="📥 Download Cottington Report",
        data=pdf_bytes,
        file_name=f"Cottington_Report_{client_name.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )
