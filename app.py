import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Load data
df = pd.read_csv("cleaned_funding_data.csv")

# Page config
st.set_page_config(page_title="Sri Lanka Humanitarian Funding Dashboard", layout="wide")

# Sidebar filters
st.sidebar.title("🔍 Filters")
year_range = st.sidebar.slider("Select Year Range", int(df["year"].min()), int(df["year"].max()), (2002, 2022))
# Create sector list with 'All' option
sector_options = ["All"] + sorted(df["Sector"].unique().tolist())
selected_sectors = st.sidebar.multiselect("Select Sectors", options=sector_options, default=["All"])

# Filter by year range first
filtered_df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

# Filter by selected sectors if 'All' is not selected
if "All" not in selected_sectors:
    filtered_df = filtered_df[filtered_df["Sector"].isin(selected_sectors)]

# Metrics
total_required = filtered_df["Required_Funding_USD"].sum()
total_received = filtered_df["Received_Funding_USD"].sum()
funding_gap = total_required - total_received
avg_funding_percent = filtered_df["Funding_Percent"].mean()

# Header
st.title("🇱🇰 Sri Lanka Humanitarian Funding Dashboard (2002–2022)")
st.markdown("Analyze sector-wise funding trends and gaps for Sri Lanka’s humanitarian appeals. *Data Source: Humanitarian Response Plans*")

# Metrics display
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Required", f"${total_required / 1e6:,.1f}M")
col2.metric("Total Received", f"${total_received / 1e6:,.1f}M")
col3.metric("Funding Gap", f"${funding_gap / 1e6:,.1f}M", delta=f"{(funding_gap / total_required) * 100:.1f}%")
col4.metric("Average Funding %", f"{avg_funding_percent:.1f}%")

# Tabs
tab1, tab2 = st.tabs(["📌 Sector Comparison", "📈 Time Trends"])

with tab1:
    st.subheader("Funding Requirements vs Received by Sector")
    sector_data = filtered_df.groupby("Sector")[["Required_Funding_USD", "Received_Funding_USD"]].sum().sort_values("Required_Funding_USD", ascending=False)

    fig, ax = plt.subplots(figsize=(12, 6))
    sector_data.plot(kind='bar', ax=ax)
    ax.set_ylabel("USD (Millions)")
    ax.set_title("Funding Requirements vs Received by Sector")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig)

with tab2:
    st.subheader("Trend of Total Funding Over the Years")
    trend_data = filtered_df.groupby("year")[["Required_Funding_USD", "Received_Funding_USD"]].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(trend_data["year"], trend_data["Required_Funding_USD"], marker='o', label="Required Funding")
    ax.plot(trend_data["year"], trend_data["Received_Funding_USD"], marker='o', label="Received Funding")
    ax.set_title("Total Required vs Received Funding Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Funding (USD)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
