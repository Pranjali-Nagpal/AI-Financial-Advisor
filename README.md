# 🌐 AI Financial Advisor

An intelligent, AI-powered wealth management and financial planning platform. This Streamlit web application helps users track their financial health, generate personalized investment strategies, and plan for short-term and long-term goals using advanced AI algorithms.

## 🤖 Key Features

* **📊 Financial Health Dashboard:** Track your monthly income, expenses, total net worth, and savings ratio in a clean, interactive UI.
* **💡 AI Strategic Plan:** Receive actionable, personalized financial advice tailored to your specific profile (Student, Professional, or Retiree), income, and risk tolerance.
* **📈 Data Visualizations:** Beautiful, component-wise charts (Pie and Bar charts) illustrating savings distribution and financial impact, powered by Matplotlib and Seaborn.
* **🎯 Advanced Goal Planning:** Input specific financial goals (e.g., "Buy a house," "Build an emergency fund") and receive a step-by-step AI-generated roadmap to achieve them.
* **💬 Interactive AI Chat Support:** A built-in financial chatbot that can answer follow-up questions about budgeting, taxes, mutual funds, and debt reduction.

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (with custom CSS for styling)
* **Backend / Logic:** Python 3
* **AI Engine:** Google Gemini AI API (`google-generativeai`)
* **Data Visualization:** Matplotlib, Seaborn, Pandas

## 📂 Project Structure

```text
AI_FINANCIAL_ADVISOR/
├── .env                    # Environment variables (API Keys - NOT tracked in Git)
├── .gitignore              # Files and directories ignored by Git
├── ai_advisor.py           # Handles communication with the Gemini AI model
├── app.py                  # Main Streamlit application and UI layout
├── config.py               # Application configuration and environment loading
├── finance_analysis.py     # Core mathematical logic and financial metric calculations
├── requirements.txt        # List of Python dependencies
├── style.css               # Custom CSS for UI styling (gradients, cards, banners)
├── utils.py                # Helper functions (text parsing, card formatting)
└── visualization.py        # Logic for generating Matplotlib/Seaborn charts
