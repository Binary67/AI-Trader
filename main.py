from DataGeneration import DataGeneration


def main():
    Generator = DataGeneration()
    Data = Generator.DataDownloader(
        "AAPL",
        "2022-01-01",
        "2022-01-10",
        "1d",
        UseDummyData=True,
    )

    print(Data.head())


if __name__ == "__main__":
    main()
