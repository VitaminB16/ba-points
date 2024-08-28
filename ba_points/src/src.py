from ba_points.src.api_scraper import get_destinations_prices, get_tier_points


def get_prices_tier_points(number_of_nights=1):
    destination_prices = get_destinations_prices(number_of_nights=number_of_nights)
    tier_points = get_tier_points()
    df = destination_prices.merge(
        tier_points, on=["arr_city_name", "cabin"], how="left"
    )
    df = df.query("tier_points.notnull()")
    points_per_pound = 2 * df["tier_points"] / df["lowest_price"]
    df = df.assign(tier_points_per_pound=round(points_per_pound, 2))
    df.to_csv("data/prices_tier_points.csv", index=False)
    return df
