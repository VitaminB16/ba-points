import pandas as pd
from ba_points.src.src import get_prices_tier_points


def main(number_of_nights=1):
    df = get_prices_tier_points(number_of_nights=number_of_nights)
    return df


if __name__ == "__main__":
    dfs = []
    for number_of_nights in range(1, 8):
        df = main(number_of_nights=number_of_nights)
        df["number_of_nights"] = number_of_nights
        dfs.append(df)
    df = pd.concat(dfs)
    df = df.sort_values("tier_points_per_pound", ascending=False)
    df = df.reset_index(drop=True)
    print(df.head(20))
    df.to_csv("data/prices_tier_points_sorted.csv", index=False)
    breakpoint()
