# python_assignment

Importing necessary libraries: import requests from bs4 import BeautifulSoup import csv

Function scraping_product_list(url):
This function is responsible for scraping the product information from the Amazon search result pages.

Function scraping_product_details(url):
This function is responsible for scraping additional product details from the individual product pages.

The code exports the data to two separate CSV files. The first CSV file, amazon_products_part1.csv, contains the product-related information, including 'Product URL', 'Product Name', 'Product Price', 'Rating', and 'Number of Reviews'. The second CSV file, amazon_products_part2.csv, contains the product details, such as 'Description', 'ASIN', 'Product Description', and 'Manufacturer'.
