# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 01:44:40 2024

@author: abaraka
"""

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

# Create database engine
engine = create_engine('postgresql+psycopg2://postgres:admin@localhost/jumia_products')

# Load data from database
@st.cache
def load_data():
    try:
        df = pd.read_sql('SELECT * FROM discounted_products', engine)
        # Data Cleaning and Preprocessing
        df['price'] = pd.to_numeric(df['price'].replace('[^\d.]', '', regex=True), errors='coerce')
        df['original_price'] = pd.to_numeric(df['original_price'].replace('[^\d.]', '', regex=True), errors='coerce')
        df.dropna(subset=['price', 'original_price'], inplace=True)
        df['discount_percentage'] = ((df['original_price'] - df['price']) / df['original_price']) * 100
        return df
    except Exception as e:
        st.error(f"Error loading data from database: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

df = load_data()

# App Layout
st.title("E-commerce Product Analysis")

# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Select a section", ["Summary", "EDA", "Category Analysis"])

if options == "Summary":
    st.header("Summary of Products")

    # Basic Information
    st.write("### Basic Information")
    st.write(df.info())

    # Summary Statistics
    st.write("### Summary Statistics")
    st.write(df.describe())

    # Total Number of Products
    st.write("### Total Number of Products")
    st.write(df.shape[0])

    # Number of Unique Categories
    st.write("### Number of Unique Categories")
    st.write(df['category'].nunique())

elif options == "EDA":
    st.header("Exploratory Data Analysis (EDA)")

    # Price Distribution
    st.write("### Price Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df['price'], bins=50, kde=True, ax=ax)
    ax.set_title('Price Distribution')
    ax.set_xlabel('Price (₦)')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

    # Discount Percentage Distribution
    st.write("### Discount Percentage Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df['discount_percentage'], bins=50, kde=True, ax=ax)
    ax.set_title('Discount Percentage Distribution')
    ax.set_xlabel('Discount Percentage (%)')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

    # Top 10 Products with Highest Discounts
    st.write("### Top 10 Products with Highest Discounts")
    top_discounts = df.sort_values(by='discount_percentage', ascending=False).head(10)
    fig, ax = plt.subplots()
    sns.barplot(x='discount_percentage', y='product_name', data=top_discounts, ax=ax)
    ax.set_title('Top 10 Products with Highest Discounts')
    ax.set_xlabel('Discount Percentage (%)')
    ax.set_ylabel('Product')
    st.pyplot(fig)

    # Top 10 Cheapest Products
    st.write("### Top 10 Cheapest Products")
    cheapest_products = df.sort_values(by='price', ascending=True).head(10)
    fig, ax = plt.subplots()
    sns.barplot(x='price', y='product_name', data=cheapest_products, ax=ax)
    ax.set_title('Top 10 Cheapest Products')
    ax.set_xlabel('Price (₦)')
    ax.set_ylabel('Product')
    st.pyplot(fig)

    # Top 10 Most Expensive Products
    st.write("### Top 10 Most Expensive Products")
    most_expensive_products = df.sort_values(by='price', ascending=False).head(10)
    fig, ax = plt.subplots()
    sns.barplot(x='price', y='product_name', data=most_expensive_products, ax=ax)
    ax.set_title('Top 10 Most Expensive Products')
    ax.set_xlabel('Price (₦)')
    ax.set_ylabel('Product')
    st.pyplot(fig)

    # Price vs. Discount Percentage
    st.write("### Price vs. Discount Percentage")
    fig, ax = plt.subplots()
    sns.scatterplot(x='price', y='discount_percentage', hue='category', data=df, ax=ax)
    ax.set_title('Price vs. Discount Percentage')
    ax.set_xlabel('Price (₦)')
    ax.set_ylabel('Discount (%)')
    st.pyplot(fig)

    # Original Price vs. Discounted Price
    st.write("### Original Price vs. Discounted Price")
    fig, ax = plt.subplots()
    sns.scatterplot(x='original_price', y='price', hue='category', data=df, ax=ax)
    ax.set_title('Original Price vs. Discounted Price')
    ax.set_xlabel('Original Price (₦)')
    ax.set_ylabel('Discounted Price (₦)')
    st.pyplot(fig)

elif options == "Category Analysis":
    st.header("Product Analysis by Category")

    # Select Category
    category = st.selectbox("Select a category", df['category'].unique())
    filtered_df = df[df['category'] == category]

    st.write(f"### Summary for Category: {category}")
    
    # Total Products in Category
    st.write("#### Total Products")
    st.write(filtered_df.shape[0])

    # Average Price
    st.write("#### Average Price")
    st.write(filtered_df['price'].mean())

    # Average Discount
    st.write("#### Average Discount")
    st.write(filtered_df['discount_percentage'].mean())

    # Price Distribution by Category
    st.write("#### Price Distribution for Selected Category")
    fig, ax = plt.subplots()
    sns.histplot(filtered_df['price'], bins=50, kde=True, ax=ax)
    ax.set_title('Price Distribution')
    ax.set_xlabel('Price (₦)')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

    # Discount Distribution by Category
    st.write("#### Discount Distribution for Selected Category")
    fig, ax = plt.subplots()
    sns.histplot(filtered_df['discount_percentage'], bins=50, kde=True, ax=ax)
    ax.set_title('Discount Distribution')
    ax.set_xlabel('Discount Percentage (%)')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)
