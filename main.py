from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup


property_url = "https://appbrewery.github.io/Zillow-Clone/"
response = requests.get(property_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Property Link
    property_links = soup.find_all("a", class_="property-card-link")

    links = [link.get("href") for link in property_links if link.get("href") is not None]

    # Price
    price_element = soup.find_all("span", {"data-test": "property-card-price"})

    prices = [price.text for price in price_element]
    cleaned_prices = [price.replace("+", "").replace("/mo", "").strip() for price in prices]

    # Address
    address_elements = soup.find_all("address", {"data-test": "property-card-addr"})
    # Extract and clean the addresses
    addresses = [
        " ".join(address.text.split()).replace("|", "").strip()
        for address in address_elements
    ]

    # Combine existing data
    listings = [
        {"address": addr, "price": price, "link": link}
        for addr, price, link in zip(addresses, cleaned_prices, links)
    ]
else:
    print(f"Failed to retrieve  data. Status code {response.status_code}")
    listings = []

form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdqP6jofyngwpX2HebkzEaquPfPBYUSDTJlEa0LuiL978-zDg/viewform?usp=sf_link"

driver = webdriver.Chrome()
driver.get(form_url)

for listing in listings:
    try:
        address_field = driver.find_element(By.XPATH, "(//input[@type='text'])[1]")
        address_field.send_keys(listing["address"])
        time.sleep(1)

        # Locate the price field and fill it
        price_field = driver.find_element(By.XPATH, "(//input[@type='text'])[2]")
        price_field.send_keys(listing["price"])
        time.sleep(1)

        # Locate the link field and fill it
        link_field = driver.find_element(By.XPATH, "(//input[@type='text'])[3]")
        link_field.send_keys(listing["link"])
        time.sleep(1)

        # Locate and click the submit button
        submit_button = driver.find_element(By.XPATH, "//span[text()='Submit']")
        submit_button.click()
        time.sleep(2)  # Wait for the submission to complete

        # Click on "Submit another response" to reload the form
        another_response_button = driver.find_element(By.XPATH, "//a[text()='Submit another response']")
        another_response_button.click()
        time.sleep(2)
    except Exception as e:
        print(f"Error submitting listing {listings}: {e}")
        break
# Close the browser
driver.quit()
