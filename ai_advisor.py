import streamlit as st
from config import setup_environment

# --- 1. Environment Configuration ---
try:
    client = setup_environment()
except ValueError as e:
    st.error(str(e))
    st.stop() 

# --- 2. AI Reasoning Module ---

def generate_financial_advice(user_data, analysis_data):
    """Provides holistic, AI-generated advice based on income, savings, and goals."""
    
    # Profile-specific prompts
    if user_data['profile'] == "Student":
        profile_prompt = "Focus on building good financial habits, managing education loans if any, and starting early investments."
    elif user_data['profile'] == "Working Professional":
        profile_prompt = "Focus on tax-saving strategies, aggressive wealth building, and balancing lifestyle inflation with savings."
    else:
        profile_prompt = "Focus on capital preservation, generating stable passive income, and safe withdrawal rates."

    prompt = f"""
You are an expert financial advisor. Generate a sectioned, structured, and actionable personal finance plan.

{profile_prompt}

User Data:
- Profile Type: {user_data['profile']}
- Monthly Income: ₹{user_data['income']}
- Monthly Expenses: ₹{user_data['expenses']}
- Total Debts: ₹{user_data['debts']}
- Existing Savings & Investments: ₹{user_data['existing_savings']}
- Estimated Monthly Savings: ₹{analysis_data['savings']}
- Total Net Worth: ₹{analysis_data['total_net_worth']}
- Debt-to-Income Ratio: {analysis_data['debt_to_income_ratio']*100:.1f}%
- Savings Ratio: {analysis_data['savings_ratio']*100:.2f}%
- Financial Goals: {', '.join(user_data.get('goals', ['Not specified']))}
- Risk Tolerance: {user_data['risk_tolerance']}
- Recommended Investment Allocation: {analysis_data['recommended_investment_allocation']}

Important: The user already has ₹{user_data['existing_savings']} in existing savings and investments.
Consider how to best utilize these existing funds alongside new monthly savings.

Instructions:
- Use sections with clear headers (e.g., Existing Savings Utilization:, Monthly Savings Strategy:, Debt Plan:, Investment Advice:, Goal Guidance:, Budgeting)
- Include specific advice on how to utilize existing savings
- Consider if existing savings should be used for debt repayment, emergency fund completion, or goal acceleration
- Include short, actionable bullet points in each section
- Tailor advice to the user's profile and risk tolerance
- Keep tone professional and easy to follow
- Avoid long paragraphs and executive summaries
- Do not use markdown, tables, or bold formatting

Output:
- Ready-to-read actionable plan that incorporates existing savings
"""
    try:
        # Using the updated SDK syntax and the 2.5 flash model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"Gemini API Error: {e}"


def generate_goal_plan(user_data, analysis_data, user_instructions):
    """Creates specific, step-by-step goal plans based on advanced user instructions."""
    
    prompt = f"""
    You are an expert financial planner. Create an advanced, step-by-step roadmap to achieve the user's financial goals while strictly adhering to their specific instructions.
    
    User Profile: {user_data['profile']}
    Monthly Income: ₹{user_data['income']}
    Current Savings: ₹{user_data['existing_savings']}
    Available Monthly Investment Capacity: ₹{analysis_data['savings']}
    Primary Goals: {', '.join(user_data.get('goals', ['Not specified']))}
    
    USER'S STRICT INSTRUCTIONS / CONSTRAINTS:
    "{user_instructions}"
    
    Use EXACTLY the following section headers to structure your response:
    Financial Impact Analysis:
    Revised Goal Timeline:
    Monthly Action Plan:
    Resource Allocation Strategy:
    Risk Assessment & Mitigation:
    
    Keep the advice highly actionable, use bullet points, and tailor everything to the strict instructions provided. Do not use bold markdown for the section headers.
    """
    try:
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini API Error: {e}"

def finance_chatbot_response(user_data, analysis_data, user_query):
    """Enables interactive, AI-powered conversations for ongoing financial queries."""
    
    # Dynamically build the context from the user's active session data
    context = f"""
    Profile: {user_data['profile']}
    Income: ₹{user_data['income']}
    Current Savings: ₹{user_data['existing_savings']}
    Total Debt: ₹{user_data['debts']}
    Risk Tolerance: {user_data['risk_tolerance']}
    """
    
    prompt = f"""
    You are a helpful and knowledgeable AI Financial Advisor assistant.
    Answer the user's question accurately, maintaining a professional yet approachable tone.
    Base your advice strictly on their financial context provided below.
    
    User Context:
    {context}
    
    User Query: {user_query}
    """
    try:
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        return response.text.strip()
    except Exception as e:
         return f"Gemini API Error: {e}"
