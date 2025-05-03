import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Sri Lanka Humanitarian Funding Dashboard", layout="wide")

# Load data (simple direct import like matplotlib version)
df = pd.read_csv("cleaned_funding_data.csv")
df["Required_Funding_USD"] /= 1e6
df["Received_Funding_USD"] /= 1e6

# Sidebar filters
st.sidebar.title("\U0001F50D Filters")
year_range = st.sidebar.slider("Select Year Range", int(df["year"].min()), int(df["year"].max()), (2002, 2022))
sector_options = ["All"] + sorted(df["Sector"].unique().tolist())
selected_sectors = st.sidebar.multiselect("Select Sectors", options=sector_options, default=["All"])

# Filter data
filtered_df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]
if "All" not in selected_sectors:
    filtered_df = filtered_df[filtered_df["Sector"].isin(selected_sectors)]

# Metrics
st.title("\U0001F1F1\U0001F1F0 Sri Lanka Humanitarian Funding Dashboard (2002–2022)")
st.markdown("Analyze sector-wise funding trends and gaps for Sri Lanka's humanitarian appeals. *Data Source: Humanitarian Response Plans*")

st.subheader("\U0001F4CA Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Required", f"${filtered_df['Required_Funding_USD'].sum():,.1f}M")
col2.metric("Total Received", f"${filtered_df['Received_Funding_USD'].sum():,.1f}M")
gap = filtered_df['Required_Funding_USD'].sum() - filtered_df['Received_Funding_USD'].sum()
col3.metric("Funding Gap", f"${gap:,.1f}M", delta=f"{(gap / filtered_df['Required_Funding_USD'].sum()) * 100:.1f}%")
col4.metric("Average Funding %", f"{filtered_df['Funding_Percent'].mean():.1f}%")

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Funding by Sector", "📌 Sector Comparison", "📈 Time Trends"])

with tab1:
    st.subheader("Funding by Sector")

    sector_totals = filtered_df.groupby("Sector")[["Required_Funding_USD", "Received_Funding_USD"]].sum().reset_index()
    sector_totals = sector_totals.sort_values("Required_Funding_USD", ascending=True)

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.bar(
            sector_totals,
            x="Required_Funding_USD",
            y="Sector",
            orientation="h",
            title="Total Required Funding by Sector",
            labels={"Required_Funding_USD": "Funding (Millions USD)", "Sector": "Sector"},
            text_auto=".1f"
        )
        fig1.update_layout(height=600)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.bar(
            sector_totals,
            x="Received_Funding_USD",
            y="Sector",
            orientation="h",
            title="Total Received Funding by Sector",
            labels={"Received_Funding_USD": "Funding (Millions USD)", "Sector": "Sector"},
            text_auto=".1f"
        )
        fig2.update_layout(height=600)
        st.plotly_chart(fig2, use_container_width=True)


with tab2:
    st.subheader("Funding Requirements vs Received by Sector")
    bar_df = filtered_df.groupby("Sector")[["Required_Funding_USD", "Received_Funding_USD"]].sum().reset_index()
    bar_df = bar_df.sort_values("Required_Funding_USD", ascending=False)

    fig = px.bar(
        bar_df.melt(id_vars="Sector"),
        x="Sector",
        y="value",
        color="variable",
        barmode="group",
        text_auto=".1f",
        labels={"value": "USD (Millions)", "variable": ""},
        title="Funding Requirements vs Received by Sector"
    )
    fig.update_layout(xaxis_tickangle=-45, height=500)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Total Funding Over the Years")
    trend_df = filtered_df.groupby("year")[["Required_Funding_USD", "Received_Funding_USD"]].sum().reset_index()

    fig = px.line(
        trend_df.melt(id_vars="year"),
        x="year",
        y="value",
        color="variable",
        markers=True,
        labels={"value": "USD (Millions)", "variable": ""},
        title="Funding Trends Over Time"
    )
    fig.update_traces(line_width=2)
    st.plotly_chart(fig, use_container_width=True)
