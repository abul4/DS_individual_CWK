import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Read Excel file
store_data = pd.read_excel('../data_science_individual_CWK/Global Superstore lite.xlsx', sheet_name=0)

# Print the head of the DataFrame
print(store_data.head())

# Title of the dashboard
st.title("Your Data Science Dashboard")

# Add a sidebar for filters
st.sidebar.title("Filters")

# Select filter options
filter_options = st.sidebar.multiselect("Select Filter Options", ["Segment", "City", "State", "Country", "Market", "Region", "Category", "Sub Category"])

# Filter data based on selected options
filtered_data = store_data[filter_options]

# Display filtered data
st.write(filtered_data)

# Visualizations
st.subheader("Visualizations")

# Plot for sales by category
plt.figure(figsize=(10, 6))
sns.barplot(x="Category", y="Sales", data=store_data)
plt.xticks(rotation=45)
st.pyplot()

# Plot for sales by region
plt.figure(figsize=(10, 6))
sns.barplot(x="Region", y="Sales", data=store_data)
plt.xticks(rotation=45)
st.pyplot()