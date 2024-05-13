import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

# Read Excel file
store_data = pd.read_excel('../data_science_individual_CWK/Global Superstore lite.xlsx', sheet_name=0)

# Total Sales
total_sales = store_data['Sales'].sum() / 1e6  # in millions
sales_trend = np.random.choice([-1, 1])  # Random trend for demonstration purposes

# Total Profit
total_profit = store_data['Profit'].sum() / 1e3  # in thousands
profit_trend = np.random.choice([-1, 1])  # Random trend for demonstration purposes

# Total Orders
total_orders = store_data['Order ID'].nunique()

# Total Ship Mode
ship_mode_counts = store_data['Ship Mode'].value_counts()

# Dashboard Title
st.title("Global Superstore Dashboard")

# Box Styling
box_style = "border-radius: 10px; padding: 20px; border: 2px solid darkgreen;"

# Box 1: Total Sales
with st.sidebar:
    st.markdown(f'<div style="{box_style} background-color: limegreen; color: limegreen; cursor: pointer;" onmouseover="this.style.backgroundColor=\'darkgreen\'; this.style.color=\'white\'" onmouseout="this.style.backgroundColor=\'limegreen\'; this.style.color=\'limegreen\'">', unsafe_allow_html=True)
    st.markdown(f"## Total Sales: ${total_sales:.2f}M")
    st.markdown('<i class="fas fa-arrow-up" style="color: green;"></i>' if sales_trend == 1 else '<i class="fas fa-arrow-down" style="color: red;"></i>')
    st.markdown('</div>', unsafe_allow_html=True)

# Box 2: Total Profit
with st.sidebar:
    st.markdown(f'<div style="{box_style} background-color: limegreen; color: limegreen; cursor: pointer;" onmouseover="this.style.backgroundColor=\'darkgreen\'; this.style.color=\'white\'" onmouseout="this.style.backgroundColor=\'limegreen\'; this.style.color=\'limegreen\'">', unsafe_allow_html=True)
    st.markdown(f"## Total Profit: ${total_profit:.2f}K")
    st.markdown('<i class="fas fa-arrow-up" style="color: green;"></i>' if profit_trend == 1 else '<i class="fas fa-arrow-down" style="color: red;"></i>')
    st.markdown('</div>', unsafe_allow_html=True)

# Box 3: Total Orders
with st.sidebar:
    st.markdown(f'<div style="{box_style} background-color: limegreen; color: limegreen; cursor: pointer;" onmouseover="this.style.backgroundColor=\'darkgreen\'; this.style.color=\'white\'" onmouseout="this.style.backgroundColor=\'limegreen\'; this.style.color=\'limegreen\'">', unsafe_allow_html=True)
    st.markdown(f"## Total Orders: {total_orders}")
    st.markdown('</div>', unsafe_allow_html=True)

# Box 4: Ship Mode Doughnut Chart
with st.sidebar:
    st.markdown(f'<div style="{box_style} background-color: limegreen; color: limegreen; cursor: pointer;" onmouseover="this.style.backgroundColor=\'darkgreen\'; this.style.color=\'white\'" onmouseout="this.style.backgroundColor=\'limegreen\'; this.style.color=\'limegreen\'">', unsafe_allow_html=True)
    st.markdown("## Total Ship Mode")
    fig = px.pie(values=ship_mode_counts, names=ship_mode_counts.index, hole=0.4)
    fig.update_traces(marker=dict(colors=['#3D9970', '#2CA02C', '#26B0A6', '#00AFB9']))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)