import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


def scrape_selenium():
    url = "https://www.britishairways.com/travel/low-price-finder/public/en_gb"
    driver = webdriver.Chrome()
    driver.get(url)
    destination_class = "destListBox"
    cabin_mode_class = "select#cabinFilter.input-primary"
    submit_button_class = "input.button.btn-primary.small-button.translate"
    region_tab_class = "regionTab"
    accept_buttone_id = "ensAcceptAll"
    accept_button = driver.find_element(By.ID, accept_buttone_id)
    time.sleep(2)
    accept_button.click()
    time.sleep(2)
    submit_button = driver.find_element(By.CSS_SELECTOR, submit_button_class)
    cabin_mode_selector = driver.find_element(By.CSS_SELECTOR, cabin_mode_class)
    cabin_modes = cabin_mode_selector.find_elements(By.TAG_NAME, "option")
    region_tabs = driver.find_elements(By.CLASS_NAME, region_tab_class)

    cabin_modes_list = [cabin_mode.text for cabin_mode in cabin_modes]
    region_tabs_list = [region_tab.text for region_tab in region_tabs]

    results = []
    previous_results = []

    for region_tab in region_tabs:
        for cabin_mode in cabin_modes:
            time.sleep(1)
            region_tab.click()
            time.sleep(1)
            cabin_mode.click()
            time.sleep(1.5)
            submit_button.click()
            time.sleep(2)
            # Get the prices and destinations
            destination_elements = driver.find_elements(
                By.CLASS_NAME, destination_class
            )
            current_results = []
            for destination_element in destination_elements:
                try:
                    destination = destination_element.text
                    city, tail = destination.split("\n")
                    price = int(
                        tail.replace("from", "")
                        .replace("£", "")
                        .replace("return", "")
                        .replace("each-way", "")
                        .strip()
                    )
                    entry = {
                        "city": city,
                        "price": price,
                        "cabin_mode": cabin_mode.text,
                    }
                    current_results.append(entry)
                except Exception as e:
                    continue
            time.sleep(2)
            current_df = pd.DataFrame(current_results, columns=["city", "price"])
            previous_df = pd.DataFrame(previous_results, columns=["city", "price"])
            if current_df.equals(previous_df):
                print(f"Skipping {region_tab.text} - {cabin_mode.text}")
                continue
            results.extend(current_results)
            previous_results = current_results

    # Write the results to a CSV file
    df = pd.DataFrame(results)
    df = df.sort_values(by=["city", "cabin_mode"])
    df.to_csv("data/prices.csv", index=False)


if __name__ == "__main__":
    scrape_selenium()
