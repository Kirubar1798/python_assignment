import requests
from bs4 import BeautifulSoup
import csv

def scraping_product_list(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_list = []
    
    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    for product in products:
        product_data = {}
        product_url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal s-no-outline'}).get('href')
        product_name = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
        product_price = product.find('span', {'class': 'a-offscreen'}).text.strip()
        rating = product.find('span', {'class': 'a-icon-alt'}).text.strip().split()[0]
        num_reviews = product.find('span', {'class': 'a-size-base'}).text.strip()
        
        product_data['Product URL'] = product_url
        product_data['Product Name'] = product_name
        product_data['Product Price'] = product_price
        product_data['Rating'] = rating
        product_data['Number of Reviews'] = num_reviews
        
        product_list.append(product_data)
    
    return product_list

def scraping_product_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_details = {}
    
    try:
        description = soup.find('div', {'id': 'productDescription'}).text.strip()
    except AttributeError:
        description = ''
    
    try:
        asin = soup.find('th', text='ASIN').find_next('td').text.strip()
    except AttributeError:
        asin = ''
    
    try:
        product_description = soup.find('div', {'id': 'feature-bullets'}).text.strip()
    except AttributeError:
        product_description = ''
    
    try:
        manufacturer = soup.find('a', {'id': 'bylineInfo'}).text.strip()
    except AttributeError:
        manufacturer = ''
    
    product_details['Description'] = description
    product_details['ASIN'] = asin
    product_details['Product Description'] = product_description
    product_details['Manufacturer'] = manufacturer
    
    return product_details

base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'
product_list = []
for page in range(1, 21):
    url = base_url + str(page)
    product_list.extend(scraping_product_list(url))

# Scraping product details
product_details_list = []
counter = 0
for product in product_list[:200]:  # Limiting to 200 products
    counter += 1
    print(f"Scraping ProductURL: {product['Product URL']} ({counter}/{len(product_list[:200])})")
    product_details = scraping_product_details(product['Product URL'])
    product_details_list.append(product_details)

# Exporting data to CSV - Part 1
filename_part1 = 'amazon_products_part1.csv'
fieldnames_part1 = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews']

with open(filename_part1, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames_part1)
    writer.writeheader()
    
    for product in product_list[:200]:
        writer.writerow(product)

# Exporting data to CSV - Part 2
filename_part2 = 'amazon_products_part2.csv'
fieldnames_part2 = ['Description', 'ASIN', 'Product Description', 'Manufacturer']

with open(filename_part2, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames_part2)
    writer.writeheader()
    
    for details in product_details_list:
        writer.writerow(details)

print(f"{filename_part1} and {filename_part2} created.")
