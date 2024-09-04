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
@st.cache_data
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

    # Cards for Summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Number of Products", df.shape[0])
    
    with col2:
        st.metric("Number of Unique Categories", df['category'].nunique())
    
    with col3:
        st.metric("Average Discount Percentage", f"{df['discount_percentage'].mean():.2f}%")

    # Pie Chart and Bar Chart Side by Side
    st.write("### Product Distribution")

    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### Distribution of Products by Category (Pie Chart)")
        category_counts = df['category'].value_counts()
        fig_pie, ax_pie = plt.subplots(figsize=(8, 8))
        ax_pie.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', colors=sns.color_palette('viridis', len(category_counts)))
        ax_pie.set_title('Product Category Distribution')
        st.pyplot(fig_pie)

    with col2:
        st.write("#### Distribution of Products by Category (Bar Chart)")
        fig_bar, ax_bar = plt.subplots(figsize=(8, 8))
        sns.barplot(x=category_counts.index, y=category_counts.values, ax=ax_bar, palette='viridis')
        ax_bar.set_title('Product Category Distribution')
        ax_bar.set_xlabel('Category')
        ax_bar.set_ylabel('Number of Products')
        ax_bar.tick_params(axis='x', rotation=45)
        st.pyplot(fig_bar)

elif options == "EDA":
    st.header("Exploratory Data Analysis (EDA)")

    # Price Distribution
    st.write("### Price Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['price'], bins=50, kde=True, ax=ax, color='blue')
    ax.set_title('Price Distribution')
    ax.set_xlabel('Price (KES)')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

    # Discount Percentage Distribution
    st.write("### Discount Percentage Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['discount_percentage'], bins=50, kde=True, ax=ax, color='green')
    ax.set_title('Discount Percentage Distribution')
    ax.set_xlabel('Discount Percentage (%)')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

    # Top 10 Products with Highest Discounts
    st.write("### Top 10 Products with Highest Discounts")
    top_discounts = df.sort_values(by='discount_percentage', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(x='discount_percentage', y='product_name', data=top_discounts, ax=ax, palette='coolwarm')
    ax.set_title('Top 10 Products with Highest Discounts')
    ax.set_xlabel('Discount Percentage (%)')
    ax.set_ylabel('Product')
    st.pyplot(fig)

    # Top 10 Cheapest Products
    st.write("### Top 10 Cheapest Products")
    cheapest_products = df.sort_values(by='price', ascending=True).head(10)
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(x='price', y='product_name', data=cheapest_products, ax=ax, palette='coolwarm')
    ax.set_title('Top 10 Cheapest Products')
    ax.set_xlabel('Price (KES)')
    ax.set_ylabel('Product')
    st.pyplot(fig)

    # Top 10 Most Expensive Products
    st.write("### Top 10 Most Expensive Products")
    most_expensive_products = df.sort_values(by='price', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(x='price', y='product_name', data=most_expensive_products, ax=ax, palette='coolwarm')
    ax.set_title('Top 10 Most Expensive Products')
    ax.set_xlabel('Price (KES)')
    ax.set_ylabel('Product')
    st.pyplot(fig)

    # Price vs. Discount Percentage
    st.write("### Price vs. Discount Percentage")
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.scatterplot(x='price', y='discount_percentage', hue='category', data=df, ax=ax, palette='Set1')
    ax.set_title('Price vs. Discount Percentage')
    ax.set_xlabel('Price (KES)')
    ax.set_ylabel('Discount Percentage (%)')
    ax.legend(loc='upper right')
    st.pyplot(fig)

    # Original Price vs. Discounted Price
    st.write("### Original Price vs. Discounted Price")
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.scatterplot(x='original_price', y='price', hue='category', data=df, ax=ax, palette='Set1')
    ax.set_title('Original Price vs. Discounted Price')
    ax.set_xlabel('Original Price (KES)')
    ax.set_ylabel('Discounted Price (KES)')
    ax.legend(loc='upper right')
    st.pyplot(fig)

    st.pyplot(fig)

elif options == "Category Analysis":
    st.header("Product Analysis by Category")

    # Select Category
    category = st.selectbox("Select a category", df['category'].unique())
    filtered_df = df[df['category'] == category]

    st.write(f"### Summary for Category: {category}")
    
    # Cards for Category Summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Products", filtered_df.shape[0])
    
    with col2:
        st.metric("Average Price", f"KES {filtered_df['price'].mean():.2f}")
    
    with col3:
        st.metric("Average Discount Percentage", f"{filtered_df['discount_percentage'].mean():.2f}%")

    # Price Distribution by Category
    st.write("#### Price Distribution for Selected Category")
    fig, ax = plt.subplots()
    sns.histplot(filtered_df['price'], bins=50, kde=True, ax=ax)
    ax.set_title('Price Distribution')
    ax.set_xlabel('Price (KES)')
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
