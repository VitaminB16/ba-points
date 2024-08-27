from ba_points.src.src import get_prices_tier_points


def main():
    df = get_prices_tier_points()
    return df


if __name__ == "__main__":
    df = main()
    print(
        df.sort_values("tier_points_per_pound", ascending=False)
        .reset_index(drop=True)
        .head(20)
    )
    breakpoint()
