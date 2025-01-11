import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Apply dark theme for the dashboard
st.set_page_config(page_title="Restaurant Data Dashboard", layout="wide")
st.markdown(
    """<style>
        body {
            background-color: #2c2c2c;
            color: white;
        }
        .stMetric-label {
            color: white;
        }
    </style>""",
    unsafe_allow_html=True
)

# Load and clean the data
file_path = 'restaurant_data.csv'
data = pd.read_csv(file_path)

# Data Cleaning
data = data.dropna()  # Remove missing values
data = data[data['OrderAmount'] > 0]  # Remove invalid order amounts
data = data[data['WaitTime'] > 0]  # Remove invalid wait times
data['CustomerSatisfaction'] = data['CustomerSatisfaction'].clip(lower=1, upper=5)  # Clip satisfaction ratings

# Title and Description
st.title("Restaurant Analysis Dashboard")
st.write("An interactive dashboard to analyze restaurant data including key metrics, cuisine distribution, payment methods, and wait times.")

# Add slicers
st.sidebar.header("Filters")
selected_cuisine = st.sidebar.multiselect("Select Cuisine Type", options=data['CuisineType'].unique(), default=data['CuisineType'].unique())
selected_payment = st.sidebar.multiselect("Select Payment Method", options=data['PaymentMethod'].unique(), default=data['PaymentMethod'].unique())

# Filter data based on slicers
data = data[(data['CuisineType'].isin(selected_cuisine)) & (data['PaymentMethod'].isin(selected_payment))]

# KPI Section
st.subheader("Key Performance Indicators (KPIs)")
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_order = data['OrderAmount'].mean()
    st.metric("Average Order Amount", f"${avg_order:.2f}")

with col2:
    avg_wait = data['WaitTime'].mean()
    st.metric("Average Wait Time", f"{avg_wait:.2f} min")

with col3:
    avg_satisfaction = data['CustomerSatisfaction'].mean()
    st.metric("Avg Customer Satisfaction", f"{avg_satisfaction:.2f}/5")

with col4:
    top_cuisine = data['CuisineType'].value_counts().idxmax()
    st.metric("Most Popular Cuisine", top_cuisine)

# Cuisine Type Distribution
st.subheader("Cuisine Type Distribution")
col5, col6 = st.columns(2)

with col5:
    cuisine_counts = data['CuisineType'].value_counts()
    fig1, ax1 = plt.subplots()
    colors = sns.color_palette("dark")
    ax1.pie(cuisine_counts, labels=cuisine_counts.index, autopct='%1.1f%%', colors=colors, startangle=140)
    ax1.axis('equal')
    st.pyplot(fig1)

# Payment Methods Distribution
with col6:
    payment_counts = data['PaymentMethod'].value_counts()
    fig2, ax2 = plt.subplots()
    sns.barplot(x=payment_counts.index, y=payment_counts.values, hue=payment_counts.index, palette="dark", ax=ax2, legend=False)
    ax2.set_title("Payment Methods")
    ax2.set_ylabel("Number of Payments")
    ax2.set_xlabel("Payment Method")
    st.pyplot(fig2)

# Wait Time Analysis
st.subheader("Wait Time Analysis")
col7, col8 = st.columns(2)

with col7:
    fig3, ax3 = plt.subplots()
    sns.histplot(data['WaitTime'], bins=20, kde=True, color="skyblue", ax=ax3)
    ax3.set_title("Distribution of Wait Times")
    ax3.set_xlabel("Wait Time (min)")
    ax3.set_ylabel("Frequency")
    st.pyplot(fig3)

with col8:
    fig4, ax4 = plt.subplots()
    sns.boxplot(x=data['CuisineType'], y=data['WaitTime'], hue=data['CuisineType'], palette="dark", ax=ax4, legend=False)
    ax4.set_title("Wait Time by Cuisine Type")
    ax4.set_xlabel("Cuisine Type")
    ax4.set_ylabel("Wait Time (min)")
    st.pyplot(fig4)

# Footer
st.write("---")
st.write("Dashboard created with Streamlit. Data source: Cleaned restaurant dataset.")
