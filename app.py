import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Track4 Dashboard", layout="wide")
st.title("Tech Industry Financial Analysis (5 Companies)")
st.subheader("Data Source: WRDS Compustat 2015-2023")

# ----------------------
#  Load Data
# ----------------------
df = pd.read_csv("tech_finance_5firms.csv")

# ----------------------
#  Sidebar
# ----------------------
st.sidebar.header("Control Panel")
companies = st.sidebar.multiselect(
    "Select Companies",
    df["tic"].unique(),
    default=["AAPL", "MSFT", "INDUSTRY"]
)

year_range = st.sidebar.slider(
    "Year Range",
    2015, 2023, (2015, 2023)
)

indicator = st.sidebar.selectbox(
    "Select Indicator",
    ["profit_margin", "roe", "roa", "revt", "debt_asset"]
)

# ----------------------
#  Filter Data
# ----------------------
filt = df[
    (df["tic"].isin(companies)) &
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1])
]

# ----------------------
#  Table
# ----------------------
st.subheader("Data Table")
st.dataframe(filt.round(2), use_container_width=True)

# ----------------------
#  Line Chart
# ----------------------
st.subheader("Trend Chart")
fig1 = px.line(filt, x="year", y=indicator, color="tic", markers=True)
st.plotly_chart(fig1, use_container_width=True)

# ----------------------
#  Scatter Plot
# ----------------------
st.subheader("ROE vs Profit Margin")
fig2 = px.scatter(filt, x="roe", y="profit_margin", color="tic", size="revt")
st.plotly_chart(fig2, use_container_width=True)

# ----------------------
#  Radar Chart
# ----------------------
st.subheader("2023 Financial Radar")
latest = df[df["year"] == 2023]
rad_comp = st.multiselect("Compare Radar", latest["tic"].unique(), default=["AAPL", "MSFT"])
rad_data = latest[latest["tic"].isin(rad_comp)]

fig3 = go.Figure()
for _, r in rad_data.iterrows():
    fig3.add_trace(go.Scatterpolar(
        r=[r.profit_margin, r.roe, r.roa, 100 - r.debt_asset],
        theta=["Profit Margin", "ROE", "ROA", "Low Debt"],
        fill="toself", name=r.tic
    ))

st.plotly_chart(fig3, use_container_width=True)

st.success("✅ All data from WRDS | Interactive Dashboard | ACC102 Track4")
