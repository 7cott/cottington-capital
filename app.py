import streamlit as st
import pandas as pd
import numpy as np
from fpdf import FPDF
from datetime import datetime

# --- COTTINGTON BRANDING ---
st.set_page_config(page_title="Cottington Capital", page_icon="🏛️", layout="centered")

st.markdown("""
    <style>
    /* 1. Main Background */
    .stApp { background-color: #0e1117; color: #d4af37; }
    
    /* 2. Text Styling */
    h1, h2, h3, h4, p, label { font-family: 'Times New Roman', serif; color: #d4af37 !important; }
    .stSelectbox > div > div { background-color: #1c1f26; color: #ffffff; }
    .stTextInput > div > div > input { color: #ffffff; background-color: #1c1f26; }
    .stNumberInput > div > div > input { color: #ffffff; background-color: #1c1f26; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-family: 'Arial', sans-serif; }
    
    /* 3. BUTTON STYLING (FORCE BLACK TEXT) */
    .stButton > button {
        color: #000000 !important; /* Black Text Always */
        background-color: #d4af37 !important; /* Gold Background */
        border-radius: 5px;
        font-weight: bold;
        border: none;
    }
    .stButton > button:hover {
        background-color: #bfa345 !important;
        color: #000000 !important;
        border: 1px solid #ffffff;
    }
    .stButton > button:focus {
        color: #000000 !important;
        background-color: #d4af37 !important;
    }
    /* Force internal text of buttons to be black if Streamlit overrides p tags */
    .stButton > button p {
        color: #000000 !important;
    }

    /* 4. TAB STYLING (HIGH CONTRAST) */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    
    /* Inactive Tab */
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1c1f26;
        border-radius: 4px 4px 0px 0px;
        color: #ffffff !important; /* White text on Dark */
        font-weight: bold;
    }
    
    /* Active Tab (The One Selected) */
    .stTabs [aria-selected="true"] {
        background-color: #d4af37 !important; /* Gold Background */
        color: #000000 !important; /* Black Text */
    }
    /* Fix for text inside active tabs */
    .stTabs [aria-selected="true"] p {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- PDF GENERATOR (PROFESSIONAL DISCLAIMER) ---
def create_pdf(report_type, client_name, inputs, metrics, schedule_df, advice_text):
    class PDF(FPDF):
        def header(self):
            # Header
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
    
    # 1. Metadata
    pdf.set_y(45)
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(100, 8, f"PREPARED FOR: {client_name.upper()}", 0, 0, 'L')
    pdf.cell(0, 8, f"DATE: {datetime.now().strftime('%d %B %Y').upper()}", 0, 1, 'R')
    pdf.ln(2)

    # 2. Parameters
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

    # 3. Financial Analysis
    pdf.set_fill_color(212, 175, 55)
    pdf.set_font('Times', 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, '  2. FINANCIAL ANALYSIS', 0, 1, 'L', fill=True)
    pdf.ln(4)
    
    pdf.set_font('Arial', 'B', 9)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(95, 7, "METRIC", 1, 0, 'C', fill=True)
    pdf.cell(95, 7, "VALUE", 1, 1, 'C', fill=True)
    
    pdf.set_font('Arial', '', 9)
    for label, value in metrics.items():
        pdf.cell(95, 8, label, 1, 0, 'L')
        pdf.set_font('Arial', 'B', 9)
        if "Real" in label: pdf.set_text_color(150, 0, 0)
        else: pdf.set_text_color(0, 0, 0)
        pdf.cell(95, 8, value, 1, 1, 'R')
        pdf.set_font('Arial', '', 9)
        pdf.set_text_color(0, 0, 0)

    pdf.ln(6)

    # 4. Strategy
    pdf.set_fill_color(14, 17, 23)
    pdf.set_text_color(212, 175, 55)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 6, '  3. COTTINGTON ADVISORY VERDICT', 0, 1, 'L', fill=True)
    pdf.ln(4)
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', '', 9)
    pdf.multi_cell(0, 4, advice_text)
    pdf.ln(4)
    
    # 5. Schedule
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(0, 6, "Required Cash Flow Schedule (Full Term):", 0, 1, 'L')
    
    pdf.set_font('Arial', '', 8)
    pdf.set_fill_color(245, 245, 245)
    
    pdf.set_font('Arial', 'B', 8)
    pdf.cell(30, 6, "Year", 1, 0, 'C', fill=True)
    pdf.cell(50, 6, "Required Premium", 1, 0, 'C', fill=True)
    pdf.cell(50, 6, "Accumulated Balance", 1, 1, 'C', fill=True)
    pdf.set_font('Arial', '', 8)
    
    for index, row in schedule_df.iterrows():
        if pdf.get_y() > 260:
            pdf.add_page()
            pdf.set_font('Arial', 'B', 8)
            pdf.cell(30, 6, "Year", 1, 0, 'C', fill=True)
            pdf.cell(50, 6, "Required Premium", 1, 0, 'C', fill=True)
            pdf.cell(50, 6, "Accumulated Balance", 1, 1, 'C', fill=True)
            pdf.set_font('Arial', '', 8)

        yr = f"Year {int(row['Year'])}"
        if 'Shielded Premium' in row:
            prem = f"R {row['Shielded Premium']:,.2f}"
            bal = f"R {row['Shielded Value (Smart Plan)']:,.2f}"
        elif 'Escalating Premium' in row:
             prem = f"R {row['Escalating Premium']:,.2f}"
             bal = f"R {row['Projected Balance']:,.2f}"
        else:
             prem = "-"
             bal = "-"

        pdf.cell(30, 6, yr, 1, 0, 'C')
        pdf.cell(50, 6, prem, 1, 0, 'C')
        pdf.cell(50, 6, bal, 1, 1, 'C')

    # THE PROFESSIONAL DISCLAIMER
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 6)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 4, "IMPORTANT LEGAL DISCLAIMER & INDEMNITY", 0, 1, 'L')
    pdf.set_font('Arial', '', 5)
    
    disclaimer_text = (
        "1. STRATEGIC TOOL ONLY: This report serves as a quantitative decision-support tool for strategic planning. Cottington Capital is not a registered Financial Services Provider (FSP) "
        "and does not provide personalized investment, tax, or legal advice. "
        "2. PROJECTION METHODOLOGY: All figures are mathematical projections based on user-provided inputs and constant rates of return. Actual market returns vary. "
        "'Real Value' is estimated using the Fisher Equation. "
        "3. LIMITATION OF LIABILITY: By using this report, you acknowledge that Cottington Capital shall not be liable for any direct or consequential damages "
        "resulting from the use of this data. You assume full responsibility for any financial decisions made. "
        "4. PROFESSIONAL CONSULTATION: You are strongly advised to consult with a qualified actuary or financial advisor before making investment decisions."
    )
    
    pdf.multi_cell(0, 3, disclaimer_text)

    return pdf.output(dest='S').encode('latin-1')

# --- LOGIC 1: WEALTH PROJECTOR ---
def calculate_projection(principal, contribution, rate, inflation, years, freq_option, timing_option):
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

# --- LOGIC 2: SMART GOAL SEEKER ---
def calculate_smart_goal(target_amount, initial, rate, inflation, years, freq_option, timing_option):
    freq_map = {"Monthly": 12, "Quarterly": 4, "Semi-Annually": 2, "Yearly": 1}
    m = freq_map[freq_option]
    total_periods = int(years * m)
    r_per = (rate / 100) / m
    
    real_target_value = target_amount / ((1 + inflation/100)**years)
    fv_lump = initial * ((1 + r_per) ** total_periods)
    remaining_goal = target_amount - fv_lump
    
    if remaining_goal <= 0:
        return 0.0, 0.0, pd.DataFrame(), real_target_value

    test_pmt = 1.0
    test_balance = 0.0
    
    for period in range(1, total_periods + 1):
        if period > 1 and (period - 1) % m == 0:
            test_pmt *= (1 + inflation / 100)
            
        if timing_option == "Start of Period (Advance)":
            test_balance += test_pmt
            test_balance += (test_balance * r_per)
        else:
            test_balance += (test_balance * r_per)
            test_balance += test_pmt
            
    multiplier = remaining_goal / test_balance
    start_pmt = multiplier
    
    data = []
    balance = initial
    curr_pmt = start_pmt
    
    for period in range(1, total_periods + 1):
        if period > 1 and (period - 1) % m == 0:
            curr_pmt *= (1 + inflation / 100)
            
        if timing_option == "Start of Period (Advance)":
            balance += curr_pmt
            balance += (balance * r_per)
        else:
            balance += (balance * r_per)
            balance += curr_pmt
            
        if period % m == 0:
            data.append({
                "Year": period // m, 
                "Escalating Premium": round(curr_pmt, 2),
                "Projected Balance": round(balance, 2)
            })
            
    return start_pmt, real_target_value, pd.DataFrame(data), real_target_value

# --- MAIN UI ---
st.title("🏛️ COTTINGTON CAPITAL")

tab1, tab2 = st.tabs(["Wealth Projector (Forward)", "Goal Seeker (Reverse)"])

# --- TAB 1 ---
with tab1:
    st.markdown("#### The Inflation Shield Projector")
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        p_initial = st.number_input("Starting Capital (R)", value=0.0, step=1000.0, key="p1")
        p_contrib = st.number_input("Monthly Contribution (R)", value=1000.0, step=100.0, key="p2")
    with col2:
        p_rate = st.number_input("Market Return (%)", value=10.0, step=0.1, format="%.2f", key="p3")
        p_inf = st.number_input("Inflation / CPI (%)", value=6.0, step=0.1, format="%.2f", key="p4")

    col3, col4 = st.columns(2)
    with col3:
        p_years = st.number_input("Duration (Years)", value=10, step=1, key="p5")
        p_freq = st.selectbox("Frequency", ("Monthly", "Quarterly", "Semi-Annually", "Yearly"), key="p6")
    with col4:
        p_time = st.selectbox("Timing", ("Start of Period (Advance)", "End of Period (Arrears)"), key="p7")

    st.write("---")
    if st.button("Run Projection"):
        df, v_nom, v_real, v_shield = calculate_projection(p_initial, p_contrib, p_rate, p_inf, p_years, p_freq, p_time)
        st.session_state['proj_res'] = {'df': df, 'v_nom': v_nom, 'v_real': v_real, 'v_shield': v_shield, 'loss': v_nom - v_real}

    if 'proj_res' in st.session_state:
        res = st.session_state['proj_res']
        m1, m2, m3 = st.columns(3)
        with m1: st.metric("Nominal Value", f"R {res['v_nom']:,.0f}")
        with m2: st.metric("Real Buying Power", f"R {res['v_real']:,.0f}")
        with m3: st.metric("Inflation Loss", f"- R {res['loss']:,.0f}", delta_color="inverse")
        
        st.line_chart(res['df'], x="Year", y=["Nominal Value (Bank Balance)", "Real Buying Power"], color=["#d4af37", "#ff4b4b"])
        
        st.subheader("📄 Report Generator")
        c_name = st.text_input("Client Name", "Valued Client", key="c_name_1")
        
        inputs_1 = {"Initial Investment": f"R {p_initial:,.2f}", "Contribution": f"R {p_contrib:,.2f}", "Return": f"{p_rate}%", "Inflation": f"{p_inf}%", "Duration": f"{p_years} Years"}
        metrics_1 = {"Nominal Value": f"R {res['v_nom']:,.2f}", "Real Buying Power": f"R {res['v_real']:,.2f}", "Inflation Loss": f"- R {res['loss']:,.2f}", "Potential with Shield": f"R {res['v_shield']:,.2f}"}
        advice_1 = f"To neutralize inflation, an 'Annual Escalation' strategy is recommended. By increasing contributions annually to match inflation ({p_inf}%), the projected Nominal Value increases to R {res['v_shield']:,.0f}."
        
        if st.button("Download Projection Report"):
            pdf_bytes = create_pdf("Wealth Projection", c_name, inputs_1, metrics_1, res['df'], advice_1)
            st.download_button("📥 Download PDF", pdf_bytes, f"Cottington_Projection_{c_name}.pdf", "application/pdf")

# --- TAB 2 ---
with tab2:
    st.markdown("#### The Target Architect (Escalation Enabled)")
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        g_target = st.number_input("Target Wealth Amount (R)", value=1000000.0, step=10000.0, key="g1")
        g_initial = st.number_input("Existing Capital (R)", value=0.0, step=1000.0, key="g2")
    with col2:
        g_rate = st.number_input("Expected Return (%)", value=10.0, step=0.1, key="g3")
        g_inf = st.number_input("Escalation / Inflation (%)", value=6.0, step=0.1, key="g_inf")

    col3, col4 = st.columns(2)
    with col3:
        g_years = st.number_input("Time to Goal (Years)", value=10, step=1, key="g4")
        g_freq = st.selectbox("Contribution Frequency", ("Monthly", "Quarterly", "Semi-Annually", "Yearly"), key="g5")
    with col4:
        g_time = st.selectbox("Payment Timing", ("Start of Period (Advance)", "End of Period (Arrears)"), key="g6")

    st.write("---")
    
    if st.button("Calculate Smart Premium"):
        start_pmt, real_target, g_df, real_val = calculate_smart_goal(g_target, g_initial, g_rate, g_inf, g_years, g_freq, g_time)
        st.session_state['goal_res'] = {'pmt': start_pmt, 'df': g_df, 'real_target': real_target}

    if 'goal_res' in st.session_state:
        gres = st.session_state['goal_res']
        
        st.info(f"💡 **REALITY CHECK:** Your goal of **R {g_target:,.0f}** will only have the purchasing power of **R {gres['real_target']:,.0f}** in today's money due to inflation.")
        
        st.subheader("Required Action Plan")
        st.metric(label=f"Starting {g_freq} Contribution", value=f"R {gres['pmt']:,.2f}")
        st.caption(f"Note: This premium will increase by {g_inf}% every year to keep it affordable at the start.")
        
        st.line_chart(gres['df'], x="Year", y="Projected Balance", color="#d4af37")

        st.subheader("📄 Report Generator")
        c_name_2 = st.text_input("Client Name", "Valued Client", key="c_name_2")
        
        inputs_2 = {"Target Goal": f"R {g_target:,.2f}", "Existing Capital": f"R {g_initial:,.2f}", "Return": f"{g_rate}%", "Escalation": f"{g_inf}%", "Time Horizon": f"{g_years} Years"}
        metrics_2 = {
            "STARTING PREMIUM": f"R {gres['pmt']:,.2f}",
            "Target Nominal Value": f"R {g_target:,.2f}",
            "Target Real Value": f"R {gres['real_target']:,.2f} (Buying Power)"
        }
        advice_2 = f"To achieve the target capital of R {g_target:,.0f} within {g_years} years, we recommend a 'Smart Start' strategy. You begin with a contribution of R {gres['pmt']:,.2f}, which increases by {g_inf}% annually. This reduces your upfront burden while ensuring the goal is met."
        
        if st.button("Download Goal Strategy"):
            pdf_bytes_2 = create_pdf("Goal Seek", c_name_2, inputs_2, metrics_2, gres['df'], advice_2)
            st.download_button("📥 Download PDF", pdf_bytes_2, f"Cottington_Goal_{c_name_2}.pdf", "application/pdf")
