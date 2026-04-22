import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Advanced Financial Dashboard", layout="wide")

# ----------------------
# ----------------------
st.title("📊 Advanced Financial Comparison Dashboard")
st.subheader("AAPL vs MSFT: Interactive Financial Analysis")

# ----------------------
# ----------------------
df_aapl = pd.read_csv("data_aapl.csv")
df_msft = pd.read_csv("data_msft.csv")

# ----------------------
# ----------------------
st.sidebar.header("Portfolio Weights")
weight_aapl = st.sidebar.slider("AAPL Weight (%)", 0, 100, 50, 1)
weight_msft = 100 - weight_aapl
st.sidebar.metric("MSFT Weight (%)", weight_msft)

# ----------------------
# ----------------------
st.sidebar.header("Metric Selection")
selected_metrics = st.sidebar.multiselect(
    "Choose Metrics to Display",
    ["net_profit_margin", "debt_asset_ratio", "asset_turnover", "roe", "current_ratio"],
    default=["net_profit_margin", "roe"]
)

# ----------------------
# ----------------------
latest_year = max(df_aapl['year'])
aapl_latest = df_aapl[df_aapl['year'] == latest_year].iloc[0]
msft_latest = df_msft[df_msft['year'] == latest_year].iloc[0]

weighted_margin = (aapl_latest['net_profit_margin'] * weight_aapl + msft_latest['net_profit_margin'] * weight_msft) / 100
weighted_debt = (aapl_latest['debt_asset_ratio'] * weight_aapl + msft_latest['debt_asset_ratio'] * weight_msft) / 100
weighted_roe = (aapl_latest['roe'] * weight_aapl + msft_latest['roe'] * weight_msft) / 100

# ----------------------
# ----------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Weighted Net Profit Margin", f"{weighted_margin:.1f}%")
with col2:
    st.metric("Weighted Debt-to-Asset Ratio", f"{weighted_debt:.1f}%")
with col3:
    st.metric("Weighted ROE", f"{weighted_roe:.1f}%")

# ----------------------
# ----------------------
st.subheader("📈 Financial Trend Comparison")
fig, ax = plt.subplots(figsize=(12, 6))
for metric in selected_metrics:
    ax.plot(df_aapl['year'], df_aapl[metric], marker='o', label=f"AAPL {metric}")
    ax.plot(df_msft['year'], df_msft[metric], marker='s', label=f"MSFT {metric}")
ax.set_title("Financial Metrics Trend (2015-2023)")
ax.set_xlabel("Year")
ax.set_ylabel("Value")
ax.legend()
ax.grid(True, alpha=0.3)
st.pyplot(fig)

# ----------------------
# ----------------------
st.subheader("⚡ Efficiency vs Profitability")
fig2, ax2 = plt.subplots(figsize=(8, 6))
ax2.scatter(df_aapl['asset_turnover'], df_aapl['net_profit_margin'], color='blue', label='AAPL', s=80, alpha=0.7)
ax2.scatter(df_msft['asset_turnover'], df_msft['net_profit_margin'], color='orange', label='MSFT', s=80, alpha=0.7)

combined_turnover = (aapl_latest['asset_turnover'] * weight_aapl + msft_latest['asset_turnover'] * weight_msft) / 100
combined_margin = (aapl_latest['net_profit_margin'] * weight_aapl + msft_latest['net_profit_margin'] * weight_msft) / 100
ax2.scatter(combined_turnover, combined_margin, color='green', label='Weighted Portfolio', s=120, marker='*')
ax2.set_xlabel("Asset Turnover")
ax2.set_ylabel("Net Profit Margin (%)")
ax2.set_title("Efficiency vs Profitability with Weighted Portfolio")
ax2.legend()
ax2.grid(True, alpha=0.3)
st.pyplot(fig2)

# ----------------------
# ----------------------
st.subheader("📊 Annual Revenue Comparison")
selected_year = st.selectbox("Select Year", sorted(df_aapl['year'].unique()))
aapl_rev = df_aapl[df_aapl['year'] == selected_year]['revenue'].values[0]
msft_rev = df_msft[df_msft['year'] == selected_year]['revenue'].values[0]

fig3, ax3 = plt.subplots(figsize=(6, 4))
ax3.bar(['AAPL', 'MSFT'], [aapl_rev, msft_rev], color=['blue', 'orange'])
ax3.set_title(f"Revenue Comparison: {selected_year}")
ax3.set_ylabel("Revenue (USD)")
st.pyplot(fig3)

# ----------------------
# ----------------------
st.subheader("📋 Raw Financial Data")
col1, col2 = st.columns(2)
with col1:
    st.dataframe(df_aapl[['year'] + selected_metrics].round(2))
with col2:
    st.dataframe(df_msft[['year'] + selected_metrics].round(2))