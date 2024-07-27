import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape a single page and return products and the next page URL
def scrape_page(url, seen_products):
    response = requests.get(url)
    products = []
    
    if response.status_code == 200:
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find all product items on the page
        product_items = soup.find_all('li', class_='item product product-item')

        for item in product_items:
            # Extract product name
            product_name_tag = item.select_one('strong.product.name.product-item-name a')
            product_name = product_name_tag.text.strip() if product_name_tag else "No name found"

            # Extract product price
            product_price_tag = item.select_one('.price-box .price')
            product_price = product_price_tag.text.strip() if product_price_tag else "No price found"

            # Create a unique identifier for the product
            product_id = (product_name, product_price)
            
            # Add product if it has not been seen before
            if product_id not in seen_products:
                seen_products.add(product_id)
                products.append(product_id)

        # Find the link to the next page
        next_page_tag = soup.select_one('li.pages-item-next a')
        if next_page_tag:
            next_page_url = next_page_tag['href']
            return products, next_page_url
        else:
            return products, None
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return products, None

# Main function to control the scraping process
def main():
    base_url = "URL_OF_THE_CATALOG_PAGE"  # Replace with the catalog URL
    next_page_url = base_url
    all_products = []
    seen_products = set()  # Set to keep track of seen products

    while next_page_url:
        print(f"Scraping page: {next_page_url}")
        products, next_page_url = scrape_page(next_page_url, seen_products)
        all_products.extend(products)

    # Create a DataFrame from the list of products
    df = pd.DataFrame(all_products, columns=['Product Name', 'Product Price'])

    # Specify the file path
    file_path = r"YOUR_PATH_TO_SAVE_EXCEL_FILE\products.xlsx"  # Replace with your desired file path
    
    # Export the DataFrame to an Excel file
    df.to_excel(file_path, index=False)

    print(f"Data has been exported to '{file_path}'")

if __name__ == "__main__":
    main()
