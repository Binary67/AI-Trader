from DataDownloader import DataDownloader


def main() -> None:
    Downloader = DataDownloader(UseDummy=True)
    Data = Downloader.DownloadData('AAPL', '2020-01-01', '2020-01-10', '1d')
    print(Data.head())


if __name__ == '__main__':
    main()
