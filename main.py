from ba_points.src.src import get_prices_tier_points


def main(number_of_nights=1):
    df = get_prices_tier_points(number_of_nights=number_of_nights)
    return df


if __name__ == "__main__":
    df = main(number_of_nights=1)
    df = df.sort_values("tier_points_per_pound", ascending=False)
    df = df.reset_index(drop=True)
    print(df.head(50))
    df.to_csv("data/prices_tier_points_sorted.csv", index=False)
    breakpoint()
