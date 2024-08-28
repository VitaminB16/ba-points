import requests
import pandas as pd
from ba_points.config.vars import DESTINATIONS_PRICES_URL, CABIN_CODES


def get_cabin_code_prices(cabin_code="M", number_of_nights=7):
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {
        "fq": f"departure_city:LON AND trip_type:RT AND number_of_nights:{number_of_nights} AND cabin:{cabin_code}"
    }
    response = requests.get(DESTINATIONS_PRICES_URL, headers=headers, params=params)
    results = response.json()
    results = results["grouped"]["arr_city_name"]["doclist"]["docs"]
    return results


def get_destinations_prices(number_of_nights=7):
    results = []
    for cabin_code in CABIN_CODES:
        print(f"Getting prices for cabin code: {cabin_code}")
        result = get_cabin_code_prices(cabin_code, number_of_nights)
        results.extend(result)
    df = pd.DataFrame(results)
    return df


def get_tier_points():
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
    except ImportError:
        print("Selenium not installed. Using cached data.")
        df = pd.read_csv("data/tier_points.csv")
        return df

    url = "https://www.headforpoints.com/2024/03/24/how-many-tier-points-does-each-british-airways-flight-earn/"
    driver = webdriver.Chrome()
    driver.get(url)
    table = driver.find_element(By.TAG_NAME, "table")
    df = pd.read_html(table.get_attribute("outerHTML"))[0]
    driver.quit()
    # Rename columns
    df.columns = [
        "arr_city_name",
        "economy_lowest",
        "economy_low",
        "economy_flex",
        "wtp",
        "ce/cw",
        "first",
    ]
    df = df.drop(columns=["economy_low", "economy_flex"])
    df = df.rename(
        columns={"economy_lowest": "M", "wtp": "W", "ce/cw": "C", "first": "F"}
    )
    # Pivot longer
    df = df.melt(id_vars=["arr_city_name"], var_name="cabin", value_name="tier_points")
    df = df.dropna().reset_index(drop=True)
    df["tier_points"] = df["tier_points"].astype(int)
    df.to_csv("data/tier_points.csv", index=False)
    return df
