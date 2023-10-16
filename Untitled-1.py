from bs4 import BeautifulSoup
import requests
import csv
url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
products = []

for product in soup.find_all('div', class_='s-include-content-margin'):
    product_url = product.find('a', class_='a-link-normal')['href']
    product_name = product.find('span', class_='a-size-base-plus a-color-base a-text-normal').text
    product_price = product.find('span', class_='a-price-whole').text
    rating = product.find('span', class_='a-icon-alt').text
    num_reviews = product.find('span', class_='a-size-base').text

    products.append({
        'Product URL': product_url,
        'Product Name': product_name,
        'Product Price': product_price,
        'Rating': rating,
        'Number of Reviews': num_reviews
    })
def extract_additional_info(product_url):
    response = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    description = soup.find('div', id='productDescription').text.strip()
    asin = soup.find('th', string='ASIN').find_next('td').text.strip()
    product_description = soup.find('div', id='feature-bullets').text.strip()
    manufacturer = soup.find('th', string='Manufacturer').find_next('td').text.strip()

    return {
        'Description': description,
        'ASIN': asin,
        'Product Description': product_description,
        'Manufacturer': manufacturer
    }
for product in products:
    additional_info = extract_additional_info(product['Product URL'])
    product.update(additional_info)
import csv
file_name = 'amazon_products.csv'
field_names = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews',
               'Description', 'ASIN', 'Product Description', 'Manufacturer']
with open(file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=field_names)
    writer.writeheader()
    for product in products:
        writer.writerow(product)
import csv

file_name = 'amazon_products.csv'
field_names = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews',
               'Description', 'ASIN', 'Product Description', 'Manufacturer']

with open(file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=field_names)
    writer.writeheader()
    for product in products:
        writer.writerow(product)
