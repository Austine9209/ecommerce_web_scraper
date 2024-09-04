# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 01:44:40 2024

@author: abaraka
"""

import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

# Create database engine
engine = create_engine('postgresql+psycopg2://postgres:admin@localhost/jumia_products')

# Load data from database
try:
    df = pd.read_sql('SELECT * FROM discounted_products', engine)
except Exception as e:
    print(f"Error loading data from database: {e}")
    raise

# Data Cleaning and Preprocessing
df['price'] = pd.to_numeric(df['price'].replace('[^\d.]', '', regex=True), errors='coerce')
df['original_price'] = pd.to_numeric(df['original_price'].replace('[^\d.]', '', regex=True), errors='coerce')

# Drop rows with NaN values in price or original_price columns
df.dropna(subset=['price', 'original_price'], inplace=True)

# Calculate Discount Percentage
df['discount_percentage'] = ((df['original_price'] - df['price']) / df['original_price']) * 100

# Basic Statistics
print(df.describe())

# Visualizations
try:
    # Distribution of Prices
    plt.figure(figsize=(10,6))
    sns.histplot(df['price'], bins=50, kde=True)
    plt.title('Price Distribution')
    plt.xlabel('Price (₦)')
    plt.ylabel('Frequency')
    plt.show()

    # Distribution of Discount Percentages
    plt.figure(figsize=(10,6))
    sns.histplot(df['discount_percentage'], bins=50, kde=True)
    plt.title('Discount Percentage Distribution')
    plt.xlabel('Discount Percentage (%)')
    plt.ylabel('Frequency')
    plt.show()

    # Top 10 Products with Highest Discounts
    top_discounts = df.sort_values(by='discount_percentage', ascending=False).head(10)
    plt.figure(figsize=(12,8))
    sns.barplot(x='discount_percentage', y='product_name', data=top_discounts)
    plt.title('Top 10 Products with Highest Discounts')
    plt.xlabel('Discount Percentage (%)')
    plt.ylabel('Product')
    plt.show()

    # Top 10 Cheapest Products
    cheapest_products = df.sort_values(by='price', ascending=True).head(10)
    plt.figure(figsize=(12,8))
    sns.barplot(x='price', y='product_name', data=cheapest_products)
    plt.title('Top 10 Cheapest Products')
    plt.xlabel('Price (₦)')
    plt.ylabel('Product')
    plt.show()

    # Top 10 Most Expensive Products
    most_expensive_products = df.sort_values(by='price', ascending=False).head(10)
    plt.figure(figsize=(12,8))
    sns.barplot(x='price', y='product_name', data=most_expensive_products)
    plt.title('Top 10 Most Expensive Products')
    plt.xlabel('Price (₦)')
    plt.ylabel('Product')
    plt.show()

    # Price vs. Discount Percentage
    plt.figure(figsize=(10,6))
    sns.scatterplot(x='price', y='discount_percentage', hue='category', data=df)
    plt.title('Price vs. Discount Percentage')
    plt.xlabel('Price (₦)')
    plt.ylabel('Discount (%)')
    plt.show()

    # Original Price vs. Discounted Price
    plt.figure(figsize=(10,6))
    sns.scatterplot(x='original_price', y='price', hue='category', data=df)
    plt.title('Original Price vs. Discounted Price')
    plt.xlabel('Original Price (₦)')
    plt.ylabel('Discounted Price (₦)')
    plt.show()

except Exception as e:
    print(f"Error during visualization: {e}")
