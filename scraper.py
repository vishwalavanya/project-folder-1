#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import urllib.parse
import sys


def get_search_url(search_term):
    # I am creating the base URL and search URL
    base_url = "https://mdcomputers.in/"
    encoded_term = urllib.parse.quote(search_term)
    return f"{base_url}?route=product/search&search={encoded_term}"


def fetch_page(url):
    # I am creating a browser-like request header
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        # I am fetching the webpage using a GET request
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as err:
        print(f"Sorry, could not fetch the page. Error: {err}")
        return None


def extract_products(html_content):
    # I am creating a BeautifulSoup object to parse the webpage
    soup = BeautifulSoup(html_content, "html.parser")
    products_found = []

    # I am finding all product containers from the webpage
    product_boxes = soup.find_all("div", class_="product-layout")

    for box in product_boxes:
        name_tag = box.find("h4")
        product_name = (
            name_tag.get_text(strip=True)
            if name_tag
            else "Name not available"
        )

        price_tag = box.find("span", class_="price-new")
        if not price_tag:
            price_tag = box.find("span", class_="price")

        product_price = (
            price_tag.get_text(strip=True)
            if price_tag
            else "Price not available"
        )

        if product_name != "Name not available":
            # I am storing the product name and price
            products_found.append({
                "name": product_name,
                "price": product_price
            })

    return products_found


def display_results(products, search_term):
    # I am creating the output section for the search results
    print("\n" + "=" * 60)
    print(f"Search Results for: {search_term}")
    print("=" * 60)

    if not products:
        print("No products found for your search term.")
        print("Please try a different keyword.")
        return

    print(f"Total products found: {len(products)}")
    print("-" * 60)

    for idx, item in enumerate(products, start=1):
        print(f"{idx}. {item['name']}")
        print(f"   Price: {item['price']}\n")


def main():
    # I am asking the user to enter the product search term
    user_input = input("Enter search term: ").strip()

    if not user_input:
        print("Error: Search term cannot be empty.")
        sys.exit(1)

    # I am creating the search URL and fetching the webpage
    search_url = get_search_url(user_input)
    print("\nFetching results from MDComputers...")

    page_html = fetch_page(search_url)

    if page_html is None:
        sys.exit(1)

    # I am extracting and displaying the product information
    product_list = extract_products(page_html)
    display_results(product_list, user_input)


# I am creating the standard Python entry point
if __name__ == "__main__":
    main()