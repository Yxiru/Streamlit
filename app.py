# dashboard.py
import streamlit as st
import pandas as pd
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
