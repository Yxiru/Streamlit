import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Sri Lanka Humanitarian Funding Dashboard", layout="wide")

# Load data
df = pd.read_csv("cleaned_funding_data.csv")
df["Required_Funding_USD"] /= 1e6
df["Received_Funding_USD"] /= 1e6

# Setting the Sidebar filters
st.sidebar.title("\U0001F50D Filters")
year_range = st.sidebar.slider("Select Year Range", int(df["year"].min()), int(df["year"].max()), (2002, 2022))
sector_options = ["All"] + sorted(df["Sector"].unique().tolist())
selected_sectors = st.sidebar.multiselect("Select Sectors", options=sector_options, default=["All"])

# Data Filters
filtered_df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]
if "All" not in selected_sectors:
    filtered_df = filtered_df[filtered_df["Sector"].isin(selected_sectors)]

# Key Metrics
st.title("Sri Lanka Humanitarian Funding Dashboard (2002–2022)")
st.markdown("Analyze sector-wise funding trends and gaps for Sri Lanka's humanitarian appeals. *Data Source: Humanitarian Response Plans*")

st.subheader("\U0001F4CA Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Required", f"${filtered_df['Required_Funding_USD'].sum():,.1f}M")
col2.metric("Total Received", f"${filtered_df['Received_Funding_USD'].sum():,.1f}M")
gap = filtered_df['Required_Funding_USD'].sum() - filtered_df['Received_Funding_USD'].sum()
col3.metric("Funding Gap", f"${gap:,.1f}M", delta=f"{(gap / filtered_df['Required_Funding_USD'].sum()) * 100:.1f}%")
col4.metric("Average Funding %", f"{filtered_df['Funding_Percent'].mean():.1f}%")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Funding by Sector",
    "📌 Sector Comparison",
    "📈 Time Trends",
    "📉 Funding Gap",
    "⚖️ Funding Efficiency",
    "🥧 Sector Funding Share"
])


with tab1:
    st.subheader("Funding by Sector")

    # Group by sector
    sector_grouped = filtered_df.groupby("Sector")[["Required_Funding_USD", "Received_Funding_USD"]].sum().reset_index()

    # Left: Required Funding (sorted independently)
    required_sorted = sector_grouped.sort_values("Required_Funding_USD", ascending=True)
    fig1 = px.bar(
        required_sorted,
        x="Required_Funding_USD",
        y="Sector",
        orientation='h',
        text="Required_Funding_USD",
        labels={"Required_Funding_USD": "Funding (Millions USD)"},
        title="Total Required Funding by Sector"
    )
    fig1.update_traces(marker_color="skyblue", texttemplate='%{text:.1f}', textposition='outside')
    fig1.update_layout(yaxis=dict(categoryorder='total ascending'))

    # Right: Received Funding (sorted independently)
    received_sorted = sector_grouped.sort_values("Received_Funding_USD", ascending=True)
    fig2 = px.bar(
        received_sorted,
        x="Received_Funding_USD",
        y="Sector",
        orientation='h',
        text="Received_Funding_USD",
        labels={"Received_Funding_USD": "Funding (Millions USD)"},
        title="Total Received Funding by Sector"
    )
    fig2.update_traces(marker_color="lightskyblue", texttemplate='%{text:.1f}', textposition='outside')
    fig2.update_layout(yaxis=dict(categoryorder='total ascending'))

    # Show side-by-side
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig1, use_container_width=True)
    col2.plotly_chart(fig2, use_container_width=True)


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

with tab4:
    st.subheader("Funding Gap by Sector")
    gap_df = filtered_df.groupby("Sector")[["Required_Funding_USD", "Received_Funding_USD"]].sum().reset_index()
    gap_df["Funding_Gap"] = gap_df["Required_Funding_USD"] - gap_df["Received_Funding_USD"]
    gap_df = gap_df.sort_values("Funding_Gap", ascending=False)

    fig = px.bar(
        gap_df,
        x="Funding_Gap",
        y="Sector",
        orientation="h",
        text="Funding_Gap",
        labels={"Funding_Gap": "Gap (Millions USD)"},
        title="Funding Gap by Sector"
    )
    fig.update_traces(marker_color="indianred", texttemplate='%{text:.1f}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.subheader("Funding Efficiency by Sector")

    # Compute efficiency
    efficiency_df = filtered_df.groupby("Sector")[["Required_Funding_USD", "Received_Funding_USD"]].sum().reset_index()
    efficiency_df["Funding_Percent"] = (efficiency_df["Received_Funding_USD"] / efficiency_df["Required_Funding_USD"]) * 100
    efficiency_df = efficiency_df.sort_values("Funding_Percent", ascending=False)

    # Plot
    fig = px.bar(
        efficiency_df,
        x="Funding_Percent",
        y="Sector",
        orientation="h",
        text="Funding_Percent",
        labels={"Funding_Percent": "Funding Efficiency (%)"},
        title="Funding Efficiency by Sector"
    )
    fig.update_traces(marker_color="seagreen", texttemplate='%{text:.1f}%', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

with tab6:
    st.subheader("Sector Share of Total Funding")

    #Adding the radio button for selecting data type
    funding_type = st.radio(
        "Select Funding Type to Display:",
        options=["Received Funding", "Required Funding"],
        index=0,
        horizontal=True
    )

    # Group data
    pie_df = filtered_df.groupby("Sector")[["Required_Funding_USD", "Received_Funding_USD"]].sum().reset_index()
    pie_df = pie_df[(pie_df["Received_Funding_USD"] > 0) | (pie_df["Required_Funding_USD"] > 0)]

    # Plot based on selection
    if funding_type == "Received Funding":
        fig = px.pie(
            pie_df,
            names="Sector",
            values="Received_Funding_USD",
            title="Proportional Share of Received Funding by Sector",
            hole=0.4,
            height=600
        )
    else:
        fig = px.pie(
            pie_df,
            names="Sector",
            values="Required_Funding_USD",
            title="Proportional Share of Required Funding by Sector",
            hole=0.4,
            height=600
        )

    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)



# Detailed Data Table View
st.subheader("📋 Detailed Data View")
st.dataframe(
    filtered_df.sort_values("Funding_Percent", ascending=False),
    column_config={
        "year": st.column_config.NumberColumn(format="%d"),
        "Required_Funding_USD": st.column_config.NumberColumn(
            "Required (M USD)",
            format="$%.2f"
        ),
        "Received_Funding_USD": st.column_config.NumberColumn(
            "Received (M USD)",
            format="$%.2f"
        ),
        "Funding_Percent": st.column_config.ProgressColumn(
            "Funding %",
            format="%.1f%%",
            min_value=0,
            max_value=200
        )
    },
    hide_index=True,
    use_container_width=True
)


    # Footer
st.caption("""
**Note:** All monetary values in millions USD.  
Data covers humanitarian appeals from 2002-2022.
""")