from DataGeneration import DataGeneration


def main():
    Generator = DataGeneration()
    Data = Generator.DataDownloader(
        "AAPL",
        "2020-01-01",
        "2024-12-31",
        "1d",
        UseDummyData=True,
    )

    print(Data.head())


if __name__ == "__main__":
    main()
