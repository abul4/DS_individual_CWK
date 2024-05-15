import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
from bokeh.layouts import row
from bokeh.plotting import figure, show
import plotly.graph_objects as go

# Read Excel file
store_data = pd.read_excel('Global Superstore lite.xlsx', sheet_name=0)

# Extract year from Order Date
store_data['Order Date'] = pd.to_datetime(store_data['Order Date'])
store_data['Order Year'] = store_data['Order Date'].dt.year

# Get unique values for slicers and add 'All' options
years = sorted(store_data['Order Year'].unique())
years.insert(0, 'All Years')

ship_modes = store_data['Ship Mode'].unique().tolist()
ship_modes.insert(0, 'All Modes')

regions = store_data['Region'].unique().tolist()
regions.insert(0, 'All Regions')

# Dashboard Title
st.markdown(
    """
    <h1 style='text-align: center; color: darkorange; font-family: Arial, sans-serif; font-size: 36px;'>
        Global Superstore Sales and Performance Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)

# Box Styling
box_style = """
    border-radius: 10px;
    padding: 10px;
    border: 4px solid darkorange;
    width: 250px;
    font-size: 20px;
    color: white;
    background-color: black;
    """
title_style = "font-size: 28px;"

# Filter Section Heading
st.sidebar.header("Filter Data")

# Dropdown slicers
selected_year = st.sidebar.selectbox('Select Year', years)
selected_ship_mode = st.sidebar.selectbox('Select Ship Mode', ship_modes)
selected_region = st.sidebar.selectbox('Select Region', regions)

# Filter data based on selected options
filtered_data = store_data.copy()

if selected_year != 'All Years':
    filtered_data = filtered_data[filtered_data['Order Year'] == selected_year]

if selected_ship_mode != 'All Modes':
    filtered_data = filtered_data[filtered_data['Ship Mode'] == selected_ship_mode]

if selected_region != 'All Regions':
    filtered_data = filtered_data[filtered_data['Region'] == selected_region]

# Total Sales
total_sales = filtered_data['Sales'].sum() / 1e6  # in millions

# Total Profit
total_profit = filtered_data['Profit'].sum() / 1e3  # in thousands

# Total Orders
total_orders = filtered_data['Order ID'].nunique()

# Use columns for layout management with increased padding
col1, spacer1, col2, spacer2, col3 = st.columns([1, 0.5, 1, 0.5, 1])

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

# Reduce the size of the title
st.markdown(f'<style>h1 {{ {title_style} }}</style>', unsafe_allow_html=True)

# Visualization for top 6 products with sales and profit
st.markdown("## Top 6 Products by Sales and Profit")

# Combined Sales and Profit Chart
top_products = filtered_data.groupby('Product Name').agg({'Sales': 'sum', 'Profit': 'sum'}).nlargest(6, 'Sales').round()

fig_combined = px.bar(top_products, x=top_products.index, y=['Sales', 'Profit'], barmode='group',
                      color_discrete_sequence=["#FF8C00", "#FFA07A"],
                      title="Top 6 Products by Sales and Profit")

fig_combined.update_layout(xaxis_title="Product Name", yaxis_title="Amount", legend_title="Metric")

st.plotly_chart(fig_combined, use_container_width=True)

# Doughnut Chart for Orders by Segment
st.markdown("## Orders by Segment")

# Calculate the number of orders for each segment using filtered data
orders_by_segment = filtered_data['Segment'].value_counts()

# Define colors for the segments
colors = ['#FF8C00', '#FF7043', '#FFA07A']

# Create doughnut chart using Plotly
fig_doughnut = px.pie(orders_by_segment, 
                      names=orders_by_segment.index, 
                      values=orders_by_segment.values,
                      hole=0.4, 
                      color_discrete_sequence=colors,
                      height=300,  # Decrease the size of the chart
                      width=300)  # Decrease the size of the chart

fig_doughnut.update_traces(textposition='inside', textinfo='percent+label')

st.plotly_chart(fig_doughnut, use_container_width=True)

# Pie Chart for Sales and Profit by Category
st.markdown("## Sales and Profit by Category")

# Group by category and sum sales and profit
category_data = filtered_data.groupby('Category').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()

# Create an initial figure for the selected metric
fig_pie = go.Figure()

# Add dropdown buttons to switch between sales and profit
fig_pie.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="Sales",
                     method="update",
                     args=[{"values": [category_data['Sales']], "labels": [category_data['Category']]},
                           {"title": "Sales by Category", "showlegend": True}]),
                dict(label="Profit",
                     method="update",
                     args=[{"values": [category_data['Profit']], "labels": [category_data['Category']]},
                           {"title": "Profit by Category", "showlegend": True}]),
            ]),
            direction="down",
        )
    ]
)
# Decrease the size of the chart
fig_pie.update_layout(width=400, height=400)

# Change the color to different shades of orange
fig_pie.update_traces(marker=dict(colors=['#FFA07A', '#FF8C00', '#FF6347', '#FF4500', '#FF7F50']))

# Initialize with Sales data
fig_pie.add_trace(go.Pie(labels=category_data['Category'], values=category_data['Sales'],
                         marker=dict(colors=px.colors.sequential.Oranges)))

# Update layout for initial plot
fig_pie.update_layout(title_text='Sales by Category')

st.plotly_chart(fig_pie, use_container_width=True)

# Group by year and sum metrics
yearly_data = filtered_data.groupby('Order Year').agg({'Sales': 'sum', 'Profit': 'sum', 'Order ID': 'nunique'}).reset_index()
yearly_data.rename(columns={'Order ID': 'Total Orders'}, inplace=True)

fig = px.line(yearly_data, x='Order Year', y=['Sales', 'Profit', 'Total Orders'],
              title='Total Sales, Profit, and Orders by Year',
              markers=True)

st.plotly_chart(fig)

# Aggregate sales and profit data by country
countrysales = filtered_data.groupby('Country')[['Sales', 'Profit']].sum().reset_index()

# Create a Plotly figure with dropdown buttons
fig = px.choropleth(countrysales, 
                    locations='Country', 
                    locationmode='country names', 
                    color='Sales', 
                    hover_name='Country', 
                    color_continuous_scale='rainbow', 
                    title='Sales per Country',
                    template='ggplot2')

# Update the layout to include the dropdown menu
fig.update_layout(
    title_font_size=28,
    updatemenus=[
        dict(
            buttons=list([
                dict(label='Sales',
                     method='update',
                     args=[{'z': [countrysales['Sales']], 
                            'colorscale': 'rainbow'},
                           {'title': 'Sales per Country'}]),
                dict(label='Profit',
                     method='update',
                     args=[{'z': [countrysales['Profit']], 
                            'colorscale': 'rainbow'},
                           {'title': 'Profit per Country'}])
            ]),
            direction='down',
            showactive=True,
        )
    ]
)

# Plot the chart in Streamlit
st.plotly_chart(fig)










