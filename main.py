import pandas as pd
from ba_points.src.api_scraper import get_destinations_prices


def main():
    results = get_destinations_prices()
    df = pd.DataFrame(results)
    return df


if __name__ == "__main__":
    df = main()
    df.to_csv("data/api_prices.csv", index=False)
