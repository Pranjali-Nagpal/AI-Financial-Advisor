import streamlit as st
import finance_analysis as fa
import ai_advisor as ai
import visualization as viz
import utils
import os

# --- Page configuration ---
st.set_page_config(
    page_title="AI Financial Advisor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Load CSS from file ---
def load_css():
    css_file = 'style.css' if os.path.exists('style.css') else 'styles.css'
    try:
        with open(css_file, 'r') as f:
            css = f.read()
            st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found. Make sure 'style.css' is in the same directory.")

load_css()

# --- Initialize Session State ---
if "user_data" not in st.session_state:
    st.session_state.user_data = None
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None
if "generated_advice" not in st.session_state:
    st.session_state.generated_advice = None
if "goal_plan" not in st.session_state:
    st.session_state.goal_plan = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_query" not in st.session_state:
    st.session_state.user_query = ""

# --- HEADER SECTION ---
st.markdown("""
<div style="text-align: center; margin-bottom: 1rem; margin-top: 0rem;">
    <h1 style="color: #6C5CE7 !important; font-weight: 800; font-size: 3rem; margin-bottom: 0.2rem;">🌐 AI Financial Advisor</h1>
    <p style="color: #64748b !important; font-size: 1.1rem; margin-bottom: 1.5rem;">Your Personal AI-Powered Financial Planning Assistant</p>
</div>
<div class="main-banner">
    <h2 class="banner-title" style="color: #FFFFFF !important;">Take Control of Your Financial Future</h2>
    <p class="banner-sub" style="color: #FFFFFF !important;">Get personalized financial advice, investment strategies, and goal planning powered by AI</p>
</div>
""", unsafe_allow_html=True)

# "What You Can Do" Row
st.markdown("<h3 class='section-title'>💼 What You Can Do</h3>", unsafe_allow_html=True)
col_a, col_b, col_c, col_d = st.columns(4)
with col_a:
    st.markdown("<div class='white-card'><h4 class='card-title' style='color: #6C5CE7 !important;'>📊 Financial Health</h4><p class='card-text'>Track income, expenses, savings, and debts with interactive visualizations.</p></div>", unsafe_allow_html=True)
with col_b:
    st.markdown("<div class='white-card'><h4 class='card-title' style='color: #6C5CE7 !important;'>📝 Personalized Advice</h4><p class='card-text'>Get actionable recommendations and advice tailored to your financial profile.</p></div>", unsafe_allow_html=True)
with col_c:
    st.markdown("<div class='white-card'><h4 class='card-title' style='color: #6C5CE7 !important;'>🎯 Goal Planning</h4><p class='card-text'>Create detailed plans for your short-term and long-term financial goals.</p></div>", unsafe_allow_html=True)
with col_d:
    st.markdown("<div class='white-card'><h4 class='card-title' style='color: #6C5CE7 !important;'>💬 AI Chat Support</h4><p class='card-text'>Get instant answers to your financial questions anytime with AI.</p></div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.markdown(" ") 
    
    profile = st.selectbox("Current Stage", ["Student", "Professional", "Retiree"])
    
    if profile == "Student":
        income = st.number_input("Monthly Allowance / Stipend (₹)", min_value=0, value=10000, step=1000)
        part_time = st.selectbox("Do you have part-time income?", ["No", "Yes"], help="Select if you have additional income from part-time work")
        if part_time == "Yes":
            extra_income = st.number_input("Part-time Income (₹)", min_value=0, value=5000, step=1000)
            income += extra_income
            
    elif profile == "Professional":
        income = st.number_input("Monthly Income / Salary (₹)", min_value=0, value=60000, step=1000)
        
    else: # Retiree
        income = st.number_input("Monthly Pension / Fixed Income (₹)", min_value=0, value=40000, step=1000)
        
    expenses = st.number_input("Monthly Expenses (₹)", min_value=0, value=3000, step=1000)
    existing_savings = st.number_input("Existing Savings (₹)", min_value=0, value=5000, step=5000)
    debts = st.number_input("Total Outstanding Debts (₹)", min_value=0, value=100, step=1000)
    
    goals_input = st.text_area("Financial Goals (comma separated)", value="Emergency Fund, Buying a Car")
    goals = [goal.strip() for goal in goals_input.split(",") if goal.strip()]
    
    risk_tolerance = st.selectbox("Risk Tolerance", ["Low", "Medium", "High"], index=1)
    
    st.session_state.user_data = {
        "profile": profile,
        "income": income,
        "expenses": expenses,
        "existing_savings": existing_savings,
        "debts": debts,
        "goals": goals,
        "risk_tolerance": risk_tolerance
    }
    
    generate_btn = st.button("Financial Analysis & Advice", type="primary", use_container_width=True)

    
    # --- ABOUT TOOL SECTION ---
    st.markdown("---")
    with st.expander("ℹ️ About this Tool"):
        st.markdown("""
        **AI Financial Advisor** is an intelligent wealth management platform designed to help you track, plan, and optimize your personal finances.
        
        **Use Cases:**
        * **Students:** Budgeting and debt management.
        * **Professionals:** Tax optimization and aggressive wealth building.
        * **Retirees:** Capital preservation and safe withdrawal strategies.
        
        **Core Technologies:**
        * **Frontend UI:** Streamlit & Custom CSS
        * **Data Visualization:** Matplotlib & Seaborn
        * **AI Engine:** Google Gemini 2.5 Flash
        * **Language:** Python 3
        """)

# --- WORKFLOW TRIGGER ---
if generate_btn:
    with st.spinner("Analyzing your financial data..."):
        st.session_state.analysis_data = fa.analyze_finances(st.session_state.user_data)
        st.session_state.generated_advice = ai.generate_financial_advice(
            st.session_state.user_data, 
            st.session_state.analysis_data
        )
    st.success("Analysis Complete! Scroll down to see your personalized plan.")

# --- MAIN CONTENT AREA ---
if st.session_state.user_data and st.session_state.user_data['income'] > 0:
    
    if st.session_state.analysis_data:
        ad = st.session_state.analysis_data
        ud = st.session_state.user_data
        
        # Added !important to inline styling here
        st.markdown('<div class="main-banner"><h2 class="banner-title" style="color: #FFFFFF !important;">🧮 Your Financial Summary</h2></div>', unsafe_allow_html=True)
        
        def metric_card(title, value, subtext="", alert=False):
            border_style = "border: 1px solid rgba(239, 68, 68, 0.5);" if alert else ""
            return f"""
            <div class="card-metric" style="{border_style}">
                <h3 class="metric-value">{value}</h3>
                <p class="metric-label">{title}</p>
                <p class="metric-subtext">{subtext}</p>
            </div>
            """

        st.markdown("<h3 class='section-title'>Overview</h3>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1: st.markdown(metric_card("Monthly Income", f"₹{ud['income']:,.0f}", "Total Cash Inflow"), unsafe_allow_html=True)
        with col2: st.markdown(metric_card("Monthly Savings", f"₹{ad['savings']:,.0f}", "Available to invest"), unsafe_allow_html=True)
        with col3: st.markdown(metric_card("Savings Ratio", f"{ad['savings_ratio']*100:.1f}%", "Target: > 20%"), unsafe_allow_html=True)
        with col4: st.markdown(metric_card("Inv. Capacity", f"₹{ad['investment_capacity']:,.0f}", "Monthly potential"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(metric_card("Total Net Worth", f"₹{ad['total_net_worth']:,.0f}", "Assets minus Liabilities"), unsafe_allow_html=True)
        with col2: st.markdown(metric_card("Existing Savings", f"₹{ud['existing_savings']:,.0f}", "Current liquid cash"), unsafe_allow_html=True)
        with col3: st.markdown(metric_card("Emergency Target", f"₹{ad['emergency_fund']:,.0f}", "6 Months of expenses"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("<h3 class='section-title'>Financial Health Indicators</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Emergency Fund Progress**")
            ef_progress = min((ud['existing_savings'] / ad['emergency_fund']) * 100 if ad['emergency_fund'] > 0 else 100, 100)
            st.progress(int(ef_progress) / 100)
            st.caption(f"Goal: ₹{ad['emergency_fund']:,.0f}")
            
        with col2:
            st.write("**Debt Management Health**")
            dti_health = max(100 - (ad['debt_to_income_ratio'] * 200), 0)
            st.progress(int(dti_health) / 100)
            if ad.get('high_debt_alert', False):
                st.error("⚠️ High debt load detected.")
            else:
                st.caption("Debt levels are manageable.")
        
        st.markdown("<br><br>", unsafe_allow_html=True)

        if st.session_state.generated_advice:
            # Added !important to inline styling here
            st.markdown('<div class="main-banner"><h2 class="banner-title" style="color: #FFFFFF !important;">💡 AI Strategic Plan</h2></div>', unsafe_allow_html=True)
            
            advice_sections = utils.split_advice_sections(st.session_state.generated_advice)
            
            if not advice_sections:
                st.markdown(f"""
                    <div class='card-advice'>
                        <h4 class='card-title'>Strategic Overview</h4>
                        <div class='card-content'>{st.session_state.generated_advice}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                grid_col1, grid_col2 = st.columns(2)
                for i, (title, content) in enumerate(advice_sections):
                    with grid_col1 if i % 2 == 0 else grid_col2:
                        st.markdown(f"""
                            <div class='card-advice'>
                                <h4 class='card-title'>{title}</h4>
                                <div class='card-content'>{content}</div>
                            </div>
                        """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)

        # Added !important to inline styling here
        st.markdown('<div class="main-banner"><h2 class="banner-title" style="color: #FFFFFF !important;">📈 Financial Overview Visualizations</h2></div>', unsafe_allow_html=True)
        st.markdown("<div class='white-card' style='padding: 20px;'>", unsafe_allow_html=True)
        fig = viz.plot_advised_financial_overview(ud, ad)
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown("<h3 class='section-title'>🎯 Advanced Goal Planning</h3>", unsafe_allow_html=True)
        
        user_instructions = st.text_area(
            "Your Specific Instructions:",
            placeholder="e.g., I want to save 30% of income directly, Pay debt as fast as possible, Reach goal in 2 years, Invest only in stocks, etc.",
            height=80,
            help="Enter your specific financial instructions that will be prioritized above all else"
        )
        
        advanced_plan_btn = st.button("🚀 Generate Advanced Goal Plan", use_container_width=True)
        
        if advanced_plan_btn:
            if not user_instructions.strip():
                st.warning("Please enter your specific instructions for advanced planning")
            else:
                with st.spinner("Creating advanced plan with your specific instructions..."):
                    st.session_state.goal_plan = ai.generate_goal_plan(
                        st.session_state.user_data,
                        st.session_state.analysis_data,
                        user_instructions
                    )
                    
        if st.session_state.goal_plan:
            st.markdown("---")
            # Added !important to inline styling here
            st.markdown('<div class="main-banner"><h2 class="banner-title" style="color: #FFFFFF !important;">🎯 Goal-Oriented Planning</h2></div>', unsafe_allow_html=True)
            
            sections = utils.split_goal_sections(st.session_state.goal_plan)
            
            if not sections:
                st.markdown(f"""
                    <div class='card-advice'>
                        <h4 class='card-title'>Action Plan Overview</h4>
                        <div class='card-content'>{st.session_state.goal_plan}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                col1, col2 = st.columns(2)
                for i, (title, content_html) in enumerate(sections):
                    with col1 if i % 2 == 0 else col2:
                        st.markdown(f"""
                            <div class='card-advice'>
                                <h4 class='card-title'>{title if title else "Insight"}</h4>
                                <div class='card-content'>{content_html}</div>
                            </div>
                        """, unsafe_allow_html=True)
            
        st.markdown("---")

        st.markdown("<h3 class='section-title'>💬 Ask Your AI Advisor</h3>", unsafe_allow_html=True)
        
        chat_col1, chat_col2 = st.columns([2, 1])
        
        with chat_col1:
            chat_container = st.container()
            with chat_container:
                for msg in st.session_state.chat_history:
                    if msg.get('user'):
                        st.markdown(f'<div class="user-message"><b>You:</b> {msg["user"]}</div>', unsafe_allow_html=True)
                    if msg.get('bot'):
                        st.markdown(f'<div class="bot-message">🤖 <b>Advisor:</b> {msg["bot"]}</div>', unsafe_allow_html=True)
            
            st.text_input("Type your question here...", key="user_query")
            
            ask_col1, ask_col2, ask_col3 = st.columns([1, 2, 1])
            with ask_col2:
                ask_btn = st.button("💬 Send Message", use_container_width=True)
            
            if ask_btn:
                if not st.session_state.user_query.strip():
                    st.warning("Please enter a question before sending.")
                elif not st.session_state.user_data or st.session_state.user_data.get("income", 0) == 0:
                    st.error("Please enter your financial details in the sidebar before using the chatbot.")
                elif not st.session_state.analysis_data:
                    st.error("Please generate your financial analysis first.")
                else:
                    with st.spinner("Analyzing your question..."):
                        try:
                            response = ai.finance_chatbot_response(
                                st.session_state.user_data,
                                st.session_state.analysis_data,
                                st.session_state.user_query
                            )
                            st.session_state.chat_history.append({
                                "user": st.session_state.user_query,
                                "bot": response
                            })
                            st.session_state.user_query = ""
                            st.rerun()
                        except Exception as e:
                            st.error(f"Chatbot Error: {e}")
                            
        with chat_col2:
            st.markdown("""
            <div class='white-card' style='text-align: left;'>
                <h4 class='card-title'>💡 Chat Tips</h4>
                <ul class='card-content'>
                    <li>Ask about specific mutual funds or SIPs</li>
                    <li>"How can I reduce my debt faster?"</li>
                    <li>"What is an emergency fund?"</li>
                    <li>Plan for specific goals like a car or house</li>
                    <li>Understand tax-saving strategies</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)