import pandas as pd


def calculate_tier_points(destination_num_nights_dict):
    df = pd.read_csv("data/prices_tier_points_sorted.csv")
    # df.columns: ["arr_city_name", "price", "tier_points", "tier_points_per_pound", "number_of_nights"]
    city_nights = list(zip(df["arr_city_name"], df["number_of_nights"]))
    mask = [
        (city, nights) in destination_num_nights_dict.items()
        for city, nights in city_nights
    ]
    df = df[mask]
    # Keep the rows with the highest tier_points_per_pound
    df = df.sort_values("tier_points_per_pound", ascending=False)
    df = df.drop_duplicates("arr_city_name")
    df = df.reset_index(drop=True)
    df.to_csv("tmp/filtered.csv", index=False)
    return df


if __name__ == "__main__":
    df = calculate_tier_points(
        {
            "Istanbul": 6,
            "Bucharest": 2,
            "Reykjavik": 3,
            "Sofia": 2,
            "Luxembourg": 2,
            "Billund": 2,
            "Dublin": 2,
            "Basel": 2,
            "Mykonos": 2,
            "Hamburg": 2,
            "Pisa": 2,
        }
    )
    print(df)
    breakpoint()
