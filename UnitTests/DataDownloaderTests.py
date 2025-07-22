import unittest
from unittest.mock import patch
import pandas as pd
from DataDownloader import DataDownloader


class DataDownloaderTests(unittest.TestCase):
    def test_dummy_data_generation(self):
        Downloader = DataDownloader(UseDummy=True)
        Data = Downloader.DownloadData(
            'TEST',
            '2020-01-01',
            '2020-01-05',
            '1d'
        )
        self.assertFalse(Data.empty)
        self.assertIn('Close', Data.columns)

    def test_real_data_download_and_cache(self):
        SampleFrame = pd.DataFrame({'Close': [1, 2, 3]})
        with patch('yfinance.Ticker.history', return_value=SampleFrame):
            Downloader = DataDownloader(UseDummy=False)
            Data = Downloader.DownloadData(
                'AAPL',
                '2020-01-01',
                '2020-01-05',
                '1d'
            )
            self.assertFalse(Data.empty)
            DataCached = Downloader.DownloadData(
                'AAPL',
                '2020-01-01',
                '2020-01-05',
                '1d'
            )
            self.assertFalse(DataCached.empty)


if __name__ == '__main__':
    unittest.main()
