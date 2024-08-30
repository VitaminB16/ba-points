import pandas as pd
from ba_points.src.api_scraper import get_destinations_prices, get_tier_points


def get_prices_tier_points(number_of_nights=1):
    if not isinstance(number_of_nights, (list, range, tuple)):
        number_of_nights = [number_of_nights]

    dfs = []
    for number_of_nights in range(1, 8):
        _df = get_destinations_prices(number_of_nights=number_of_nights)
        _df["number_of_nights"] = number_of_nights
        dfs.append(_df)
    dfs = pd.concat(dfs)
    destination_prices = dfs.reset_index(drop=True)

    tier_points = get_tier_points()

    df = destination_prices.merge(
        tier_points, on=["arr_city_name", "cabin"], how="left"
    )
    df = df.query("tier_points.notnull()")
    points_per_pound = 2 * df["tier_points"] / df["lowest_price"]
    df = df.assign(tier_points_per_pound=round(points_per_pound, 2))
    df = df.sort_values("tier_points_per_pound", ascending=False)
    df.to_csv("data/prices_tier_points.csv", index=False)
    return df
