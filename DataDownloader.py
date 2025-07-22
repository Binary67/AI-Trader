import os
import pandas as pd
import numpy as np
import yfinance as yf


class DataDownloader:
    def __init__(self,
                 UseDummy: bool = False,
                 CacheDir: str = "Cache") -> None:
        self.UseDummy = UseDummy
        self.CacheDir = CacheDir
        os.makedirs(self.CacheDir, exist_ok=True)

    def DownloadData(self,
                     Ticker: str,
                     StartDate: str,
                     EndDate: str,
                     Interval: str) -> pd.DataFrame:
        if self.UseDummy:
            return self.GenerateDummyData(StartDate, EndDate, Interval)
        return self._GetRealData(Ticker, StartDate, EndDate, Interval)

    def _GetRealData(self,
                     Ticker: str,
                     StartDate: str,
                     EndDate: str,
                     Interval: str) -> pd.DataFrame:
        FileName = f"{Ticker}_{StartDate}_{EndDate}_{Interval}.csv"
        FilePath = os.path.join(self.CacheDir, FileName)
        if os.path.isfile(FilePath):
            return pd.read_csv(FilePath, index_col=0, parse_dates=True)
        Data = yf.Ticker(Ticker).history(
            start=StartDate,
            end=EndDate,
            interval=Interval
        )
        Data.to_csv(FilePath)
        return Data

    def GenerateDummyData(self,
                          StartDate: str,
                          EndDate: str,
                          Interval: str,
                          InitialPrice: float = 100.0,
                          Mu: float = 0.0001,
                          Sigma: float = 0.01) -> pd.DataFrame:
        Dates = pd.date_range(start=StartDate, end=EndDate, freq=Interval)
        Steps = len(Dates)
        Returns = np.random.normal(loc=Mu, scale=Sigma, size=Steps)
        Prices = [InitialPrice]
        for Ret in Returns[1:]:
            Prices.append(Prices[-1] * np.exp(Ret))
        Frame = pd.DataFrame({'Close': Prices}, index=Dates)
        Frame['Open'] = Frame['Close']
        Frame['High'] = Frame['Close']
        Frame['Low'] = Frame['Close']
        Frame['Volume'] = np.random.randint(1000, 10000, size=Steps)
        return Frame
