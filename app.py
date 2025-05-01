# dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Sri Lanka Humanitarian Funding Dashboard", layout="wide")

# Title and intro
st.title("Sri Lanka Humanitarian Funding Dashboard")
st.markdown("Analyze sector-wise funding and requirements for Sri Lanka's 2022 humanitarian appeal.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_funding_data.csv")
    return df

df = load_data()

# Sidebar
st.sidebar.header("Filter Data")

# Sector filter
sectors = df['Sector'].unique()
selected_sector = st.sidebar.selectbox("Select Sector", options=["All"] + list(sectors))

# Funding % slider
percent_range = st.sidebar.slider("Filter by Funding %", 0.0, 500.0, (0.0, 150.0), step=5.0)

# Apply filters
filtered_df = df.copy()
if selected_sector != "All":
    filtered_df = filtered_df[filtered_df['Sector'] == selected_sector]

filtered_df = filtered_df[
    (filtered_df['Funding_Percent'] >= percent_range[0]) &
    (filtered_df['Funding_Percent'] <= percent_range[1])
]


st.subheader("Funding vs Requirements (USD)")
fig1, ax1 = plt.subplots()
ax1.bar(filtered_df['Sector'], filtered_df['Required_Funding_USD'], label="Requirements")
ax1.bar(filtered_df['Sector'], filtered_df['Received_Funding_USD'], label="Funding")
ax1.set_ylabel("USD")
ax1.set_xticklabels(filtered_df['Sector'], rotation=45, ha='right')
ax1.legend()
st.pyplot(fig1)


st.subheader("📊 Funding vs Requirements by Sector (USD)")

# Sort and use filtered data
plot_df = filtered_df.sort_values(by='Required_Funding_USD', ascending=False)

# Set bar positions
x = np.arange(len(plot_df['Sector']))
width = 0.35

# Plot grouped bars
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(x - width/2, plot_df['Required_Funding_USD'], width, label='Requirements', color='tomato')
ax.bar(x + width/2, plot_df['Received_Funding_USD'], width, label='Funding', color='seagreen')

# Format axes
ax.set_ylabel("USD")
ax.set_title("Funding vs Requirements by Sector")
ax.set_xticks(x)
ax.set_xticklabels(plot_df['Sector'], rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.5)

# Show plot
st.pyplot(fig)
