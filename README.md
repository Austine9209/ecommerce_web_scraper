# Jumia Discounted Products Analysis

## Project Overview

This project involves scraping discounted product data from the Jumia e-commerce website, performing exploratory data analysis (EDA) on the scraped data, and creating a user interface to display the results. The project uses Python, Streamlit, Selenium, BeautifulSoup, pandas, SQLAlchemy, and PostgreSQL.

## Table of Contents

- [Project Overview](#project-overview)
- [Requirements](#requirements)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Visualizations](#visualizations)
- [Contributing](#contributing)
- [License](#license)



## Requirements

To run this project, you need the following dependencies:

- Python 3.x
- Selenium
- BeautifulSoup
- pandas
- SQLAlchemy
- psycopg2
- Streamlit
- PostgreSQL

You can install the required Python packages using pip:

```bash
pip install selenium beautifulsoup4 pandas sqlalchemy psycopg2 streamlit
```
## Usage

1. Run the Scraper:
   - To scrape data from Jumia and Amazon, run the scraping scripts:
     ```bash
     python scraper.py
     ```
     
2. Run the Streamlit App:
   - To start the Streamlit application and view the visualizations:
     ```bash
     streamlit run app.py
     ```
3. Access the Application:
   - Open a web browser and go to `http://localhost:8501` to interact with the Streamlit app.

## Project Structure

- `scraper.py`: A Python script to scrape discounted product data from Jumia and store it in a PostgreSQL database.
- `eda.py`: A Python script to perform exploratory data analysis (EDA) on the data stored in the PostgreSQL database.
- `app.py`: A Streamlit application to display the discounted products and allow filtering and sorting.

## Visualizations

### Summary
- Category Breakdown: A pie chart showing the distribution of products by category.
- Category Summary: Cards displaying key statistics (total products, average price, average discount) for selected categories.
- Price and Discount Distribution: Bar and pie charts providing insights into price and discount percentages.

### Exploratory Data Analysis (EDA)
- Price Distribution: Histogram showing the distribution of product prices.
- Discount Percentage Distribution: Histogram showing the distribution of discount percentages.
- Top 10 Products with Highest Discounts: Bar chart displaying products with the highest discount percentages.
- Top 10 Cheapest Products: Bar chart displaying the cheapest products.
- Top 10 Most Expensive Products: Bar chart displaying the most expensive products.
- Price vs. Discount Percentage: Scatter plot showing the relationship between price and discount percentage.
- Original Price vs. Discounted Price: Scatter plot comparing original and discounted prices.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.

## License
This project is licensed under the MIT License

```css
    Feel free to adjust any section or add additional information relevant to your project.
```

