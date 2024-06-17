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


def clean_and_write():
    driver = login_and_scrape()
    time.sleep(40)

    # Load links from bad_linkedin_links.csv into a list
    with open('bad_linkedin_links.csv', mode='r') as file:
        reader = csv.reader(file)
        links = [row[0] for row in reader]
    file.close()

    # Open url.csv and loop over URLs
    f = open('output.csv', 'w')
    output_file = csv.writer(f)
    final = []
    for l in links:
        driver.get(l)
        driver.implicitly_wait(30)
        current_url = driver.current_url
        print(current_url)
        output_file.writerow([current_url])
        final.append(current_url)

        # add to txt
        with open('output.txt', 'a') as file2:
            file2.write(current_url + '\n')
    f.close()

    driver.quit()
    # write to txt
    with open('output2.txt', 'w') as f:
        for item in final:
            f.write(f"{item}\n")


if __name__ == "__main__":
    clean_and_write()
