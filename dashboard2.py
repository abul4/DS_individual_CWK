import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
from bokeh.layouts import row
from bokeh.plotting import figure, show


# Read Excel file
store_data = pd.read_excel('../data_science_individual_CWK/Global Superstore lite.xlsx', sheet_name=0)

# Total Sales
total_sales = store_data['Sales'].sum() / 1e6  # in millions

# Total Profit
total_profit = store_data['Profit'].sum() / 1e3  # in thousands

# Total Orders
total_orders = store_data['Order ID'].nunique()

# Dashboard Title
st.title("Global Superstore Dashboard")

# Increase the margin around each box to create space between them
box_style_with_margin = "border-radius: 10px; padding: 10px; border: 4px solid darkorange; width: 250px; font-size: 20px; margin: 10px 10px 20px 10px;"

# Use columns for layout management with increased padding
col1, col2, col3 = st.columns([1, 1, 1])

# Box Styling
box_style = "border-radius: 10px; padding: 10px; border: 4px solid darkorange; width: 250px; font-size: 20px; margin: 10px 20px;"

# Box 1: Total Sales
with col1:
    st.markdown(f'<div style="{box_style}">'
                f'<p style="margin: 20px 0; font-size: 24px;">Total Sales</p>'
                f'<p style="margin: 0; font-size: 32px;">${total_sales:.2f}M</p>'
                f'</div>', unsafe_allow_html=True)

# Box 2: Total Profit
with col2:
    st.markdown(f'<div style="{box_style}">'
                f'<p style="margin: 20px 0; font-size: 24px;">Total Profit</p>'
                f'<p style="margin: 0; font-size: 32px;">${total_profit:.2f}K</p>'
                f'</div>', unsafe_allow_html=True)

# Box 3: Total Orders
with col3:
    st.markdown(f'<div style="{box_style}">'
                f'<p style="margin: 20px 0; font-size: 24px;">Total Orders</p>'
                f'<p style="margin: 0; font-size: 32px;">{total_orders}</p>'
                f'</div>', unsafe_allow_html=True)

    

# Title styling
title_style = "font-size: 28px;"

# Reduce the size of the title
st.markdown(f'<style>h1 {{ {title_style} }}</style>', unsafe_allow_html=True)