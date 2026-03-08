import matplotlib.pyplot as plt
import seaborn as sns

# Visualization: Detailed Advised Financial Health
def plot_advised_financial_overview(user_data, analysis_data):
    
    # Extracting core financial data
    expenses = user_data.get("expenses", 0)
    savings = analysis_data.get("savings", 0)
    emergency_fund_monthly = analysis_data.get("emergency_fund_monthly", 0)
    
    # Extracting investment allocation data safely
    investment_allocation = analysis_data.get("recommended_investment_allocation", {})
    high_interest = investment_allocation.get("High-Interest Savings / RD", 0)
    stocks = investment_allocation.get("Stocks / Equity Funds", 0)
    etfs = investment_allocation.get("ETFs / Balanced Funds", 0)
    risk_free = investment_allocation.get("Debt Mutual Funds / Bonds", 0)
    
    # Calculating totals
    total_investments = high_interest + stocks + etfs + risk_free
    remaining_savings = max(0, savings - (emergency_fund_monthly + total_investments))
    
    # Defining labels and corresponding values
    labels = [
        "Expenses", 
        "Emergency Fund", 
        "High-Interest / RD", 
        "Stocks / Equity", 
        "ETFs / Balanced", 
        "Debt / Bonds", 
        "Remaining Savings"
    ]
    
    values = [
        expenses, 
        emergency_fund_monthly, 
        high_interest, 
        stocks, 
        etfs, 
        risk_free, 
        remaining_savings
    ]
    
    # Filter out zero values so the charts don't look cluttered
    filtered_labels = [l for l, v in zip(labels, values) if v > 0]
    filtered_values = [v for v in values if v > 0]

    # Style definitions (Restored to exact original)
    colors = sns.color_palette("pastel", len(filtered_values))
    fig, ax = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor("#F9FAFB")
    
    # 1. Pie Chart Configuration
    wedges, texts, autotexts = ax[0].pie(
        filtered_values, labels=filtered_labels, autopct="%1.1f%%", 
        startangle=140, colors=colors, textprops={'fontsize': 9}
    )
    
    # Text styling for the pie chart
    for text in texts:
        text.set_color("#222222")
    for autotext in autotexts:
        autotext.set_color("#222222")
        autotext.set_fontweight("bold")
        
    ax[0].set_title("Savings & Investment Distribution", pad=35, fontweight="bold", fontsize=11, color="#222222")
    
    # 2. Bar Chart Configuration
    sns.set_style("whitegrid")
    sns.barplot(x=filtered_labels, y=filtered_values, ax=ax[1], palette="pastel")
    
    ax[1].set_facecolor("#FFFFFF")
    ax[1].grid(axis="y", linestyle="--", alpha=0.5)
    ax[1].set_ylabel("Amount (₹)", fontsize=10, fontweight="bold", color="#222222")
    ax[1].tick_params(axis="x", rotation=45, labelsize=9)
    ax[1].set_title("Component-wise Financial Impact", pad=35, fontweight="bold", fontsize=11, color="#222222")
    
    # Adding data labels on top of the bars
    for i, value in enumerate(filtered_values):
        ax[1].text(i, value + (max(filtered_values) * 0.02), f"₹{value:,.0f}", 
                   ha="center", fontsize=9, fontweight="bold", color="#222222")
        
    plt.tight_layout(rect=[0.05, 0.1, 0.95, 0.95])
    plt.subplots_adjust(wspace=0.4)
    
    return fig