from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
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
    driver = login_and_scrape()

    # load company id from israeli_companies_id.csv into a list
    with open('israeli_companies_id.csv', mode='r') as file:
        reader = csv.reader(file)
        id_list = [row[0] for row in reader]

    links_with_in = []  # Define list outside loop to avoid scoping issues

    for company in id_list:
        links_with_in = []  # Define list outside loop to avoid scoping issues
        driver.get(
            f"https://www.linkedin.com/search/results/people/?currentCompany=%5B%22{company}%22%5D&geoUrn=%5B%22101620260%22%5D&origin=FACETED_SEARCH&sid=B0D")
        # wait for the page to load
        driver.implicitly_wait(30)
        # Find the <ul> element with the class 'reusable-search__entity-result-list'
        result_list = driver.find_elements(
            By.CSS_SELECTOR, "ul.reusable-search__entity-result-list")
        if result_list:
            result_list = result_list[0]
        else:
            continue
        # Find all elements with class 'app-aware-link' within the result_list
        app_aware_links = result_list.find_elements(
            By.CLASS_NAME, "app-aware-link")

        # Store links containing "/in/" into a list
        for link in app_aware_links:
            href = link.get_attribute("href")
            if href and "/in/" in href:
                links_with_in.append(href)

        # Keep unique links
        links_with_in = list(set(links_with_in))

        # Write links to a CSV file without header
        with open('bad_linkedin_links2.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            for l in links_with_in:
                writer.writerow([l])
                print([l])
                exit()
    print("Links with '/in/' written to bad_linkedin_links.csv")


def clean_and_write():
    driver = login_and_scrape()
    time.sleep(40)

    # Load links from bad_linkedin_links.csv into a list
    with open('bad_linkedin_links.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        links = [row[0] for row in reader]

    # Open linkedin_links.csv in append mode ('a')
    with open('linkedin_links.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        for l in links:
            driver.get(l)
            driver.implicitly_wait(20)
            url = driver.current_url
            print([url])

            # Write the URL to the CSV file
            writer.writerow([url])

    # Remove empty lines from the CSV
    with open('linkedin_links.csv', mode='r') as file:
        lines = file.readlines()
    with open('linkedin_links.csv', mode='w') as file:
        for line in lines:
            if line.strip():
                file.write(line)

    print("Cleaned links written to linkedin_links.csv")


if __name__ == "__main__":
    scrape_links()
    # clean_and_write()
