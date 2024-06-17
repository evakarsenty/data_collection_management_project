from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import PARAMETERS


def login_and_scrape():

    options = Options()
    # You may need to change this path to match the location of your Firefox binary
    options.binary_location = r"""C:/Program Files/Mozilla Firefox/firefox.exe"""
    # options.add_argument('headless')
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(10)
    driver.get("https://www.linkedin.com/login")

    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys(PARAMETERS.username)
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(PARAMETERS.password)

    sign_in_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    sign_in_btn.click()

    return driver


def scrape_links():
    NUM_PAGES = PARAMETERS.number_of_pages
    driver = login_and_scrape()

    for i in range(11, NUM_PAGES+1):
        driver.get(
            f"https://www.linkedin.com/search/results/companies/?companyHqGeo=%5B%22101620260%22%5D&companySize=%5B%22B%22%2C%22C%22%2C%22D%22%5D&origin=FACETED_SEARCH&page={i}&sid=pun")
        # Find all div elements with data-chameleon-result-urn attribute
        divs_with_urn = driver.find_elements(
            By.XPATH, "//div[@data-chameleon-result-urn]")

        # Print content of data-chameleon-result-urn attribute
        for div in divs_with_urn:
            urn_content = div.get_attribute("data-chameleon-result-urn")
            id = urn_content.split(":")[-1]
            # add id to a csv file
            with open('israeli_companies_id.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([id])
            print(
                "------------------------------Added id to csv file------------------------------")


if __name__ == "__main__":
    scrape_links()
