import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver 
import time

# Part 1: Scraping Product Listings
def scrape_product_listings(base_url, page_count):
    all_data = []

    for page_num in range(1, page_count+1):
        url = f'{base_url}&page={page_num}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        for product in soup.find_all('div', class_='s-item__info'):
            product_url = product.find('a', class_='s-item__link')['href']
            product_name = product.find('h3', class_='s-item__title').text
            product_price = product.find('span', class_='s-item__price').text
            try:
                rating = product.find('span', class_='s-item__rating--stars').text
                num_reviews = product.find('span', class_='s-item__reviews-count').text
            except AttributeError:
                rating = 'N/A'
                num_reviews = 'N/A'

            all_data.append([product_url, product_name, product_price, rating, num_reviews])

        time.sleep(2)  # Add a delay to be respectful of the website's resources

    return all_data

# Part 2: Extract Additional Information
def scrape_product_details(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        description = soup.find('div', id='productDescription').text
    except AttributeError:
        description = 'N/A'
    try:
        asin = soup.find('th', text='ASIN').find_next('td').text
    except AttributeError:
        asin = 'N/A'
    try:
        product_description = soup.find('div', id='feature-bullets').text
    except AttributeError:
        product_description = 'N/A'
    try:
        manufacturer = soup.find('th', text='Brand').find_next('td').text
    except AttributeError:
        manufacturer = 'N/A'

    return [description, asin, product_description, manufacturer]

# Main Function
def main():
    # Part 1: Scrape Product Listings
    base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'
    page_count = 20  # Set the number of pages to scrape
    product_listings = scrape_product_listings(base_url, page_count)

    # Part 2: Scrape Additional Information
    detailed_data = []
    for product_data in product_listings:
        product_url = product_data[0]
        detailed_info = scrape_product_details(product_url)
        detailed_data.append(product_data + detailed_info)

    # Save Data to CSV
    with open('product_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews',
                         'Description', 'ASIN', 'Product Description', 'Manufacturer'])
        for row in detailed_data:
            writer.writerow(row)

if __name__ == '__main__':
    main()
url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

driver = webdriver.Chrome()
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')

# resultset = soup.find_all('div', {'data-component-type': 's-result-item'})
resultset = soup.find_all('div', {'data-component-type': 's-search-result'})

product_names = []
product_urls = []
product_prices = []
product_ratings = []
product_review_counts = []

for item in soup.find_all("div", class_="s-result-item"):
    name = item.find("span", class_="a-size-medium a-color-base a-text-normal")
    if name is not None:
        name = name.text
    else:
        name = ""

    url = item.find("a", class_="a-link-normal a-text-normal")
    if url is not None:
        url = url["href"]
    else:
        url = ""

    price = item.find("span", class_="a-offscreen")
    if price is not None:
        price = price.text
    else:
        price = ""

    rating = item.find("span", class_="a-icon-alt")
    if rating is not None:
        rating = rating.text
    else:
        rating = ""

    review_count = item.find("div", class_="a-section a-text-center")
    if review_count is not None:
        review_count = review_count.text
    else:
        review_count = ""

    product_names.append(name)
    product_urls.append(url)
    product_prices.append(price)
    product_ratings.append(rating)
    product_review_counts.append(review_count)

for i in range(len(product_names)):
    print(i, ") Product Name: ", product_names[i], "\n")
    print("product_urls: ", product_urls[i], "\n")
    print("product_prices: ", product_prices[i], "\n")
    print("product_ratings: ", product_ratings[i], "\n")
    print("product_review_counts: ", product_review_counts[i], "\n")


rows = list(zip(product_names, product_urls, product_prices,
            product_ratings, product_review_counts))

filename = "products3.csv"
header = ['Product Name', 'URL',  'Price', 'Rating', 'Review Count']

with open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)