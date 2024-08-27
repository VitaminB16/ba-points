from ba_points.src.api_scraper import get_destinations_prices, get_tier_points


def get_prices_tier_points():
    destination_prices = get_destinations_prices()
    tier_points = get_tier_points()
    df = destination_prices.merge(
        tier_points, on=["arr_city_name", "cabin"], how="left"
    )
    df = df.query("tier_points.notnull()")
    points_per_pound = df["tier_points"] / df["rounded_lowest_each_way_price"]
    df = df.assign(tier_points_per_pound=round(points_per_pound, 2))
    df.to_csv("data/prices_tier_points.csv", index=False)
    return df
