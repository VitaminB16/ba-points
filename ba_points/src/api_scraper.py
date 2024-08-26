import requests
from ba_points.config.vars import DESTINATIONS_PRICES_URL, CABIN_CODES


def get_cabin_code_prices(cabin_code="M"):
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {
        "fq": f"departure_city:LON AND trip_type:RT AND number_of_nights:7 AND cabin:{cabin_code}"
    }
    response = requests.get(DESTINATIONS_PRICES_URL, headers=headers, params=params)
    results = response.json()
    header = results["responseHeader"]
    results = results["grouped"]["arr_city_name"]["doclist"]["docs"]
    return results


def get_destinations_prices():
    results = []
    for cabin_code in CABIN_CODES:
        print(f"Getting prices for cabin code: {cabin_code}")
        result = get_cabin_code_prices(cabin_code)
        results.extend(result)
    return results
