import pandas as pd
from ba_points.src.api_scraper import get_destinations_prices, get_tier_points


def main():
    destination_prices = get_destinations_prices()
    tier_points = get_tier_points()
    df = destination_prices.merge(
        tier_points, on=["arr_city_name", "cabin"], how="left"
    )
    df = df.query("tier_points.notnull()")
    return df


if __name__ == "__main__":
    df = main()
    df.to_csv("data/prices_tier_points.csv", index=False)
