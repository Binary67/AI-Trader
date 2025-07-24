import os
from pathlib import Path
import pandas as pd
import numpy as np
import yfinance as yf


class DataGeneration:
    def __init__(self, CacheDir="Cache"):
        self.CacheDir = Path(CacheDir)
        self.CacheDir.mkdir(parents=True, exist_ok=True)

    def _GetCachePath(self, TickerSymbol, StartDate, EndDate, Interval):
        FileName = f"{TickerSymbol}_{StartDate}_{EndDate}_{Interval}.csv"
        Sanitized = FileName.replace(":", "-")
        return self.CacheDir / Sanitized

    def DataDownloader(self, TickerSymbol, StartDate, EndDate, Interval="1d"):
        CachePath = self._GetCachePath(TickerSymbol, StartDate, EndDate, Interval)
        if CachePath.exists():
            Data = pd.read_csv(CachePath, index_col=0, parse_dates=True)
            return Data
        Data = yf.download(TickerSymbol, start=StartDate, end=EndDate, interval=Interval)
        if not Data.empty:
            Data.to_csv(CachePath)
        return Data

    def SaveCache(self, Data, TickerSymbol, StartDate, EndDate, Interval="1d"):
        CachePath = self._GetCachePath(TickerSymbol, StartDate, EndDate, Interval)
        Data.to_csv(CachePath)

    def GenerateDummyData(self, StartPrice=100, Mu=0.001, Sigma=0.01, Days=252):
        Dt = 1.0 / Days
        Returns = np.random.normal(loc=Mu * Dt, scale=Sigma * np.sqrt(Dt), size=Days)
        Price = [StartPrice]
        for R in Returns:
            Price.append(Price[-1] * np.exp(R))
        Index = pd.date_range(start=pd.Timestamp.today(), periods=Days + 1, freq="D")
        return pd.DataFrame({"Close": Price}, index=Index)
