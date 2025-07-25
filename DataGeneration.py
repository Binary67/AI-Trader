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

    def DataDownloader(
        self,
        TickerSymbol,
        StartDate,
        EndDate,
        Interval="1d",
        UseDummyData=False,
    ):
        CachePath = self._GetCachePath(
            TickerSymbol,
            StartDate,
            EndDate,
            Interval,
        )
        if UseDummyData:
            Days = (
                pd.to_datetime(EndDate) - pd.to_datetime(StartDate)
            ).days
            Data = self._GenerateDummyData(Days=Days)
            Data.to_csv(CachePath)
            return Data
        if CachePath.exists():
            Data = pd.read_csv(CachePath, index_col=0, parse_dates=True)
            return Data
        Data = yf.download(
            TickerSymbol,
            start=StartDate,
            end=EndDate,
            interval=Interval,
        )
        if not Data.empty:
            Data.to_csv(CachePath)
        return Data

    def SaveCache(self, Data, TickerSymbol, StartDate, EndDate, Interval="1d"):
        CachePath = self._GetCachePath(
            TickerSymbol,
            StartDate,
            EndDate,
            Interval,
        )
        Data.to_csv(CachePath)

    def _GenerateDummyData(
        self,
        StartPrice=100,
        Mu=0.001,
        Sigma=0.01,
        Days=252,
    ):
        Dt = 1.0 / Days
        Returns = np.random.normal(
            loc=Mu * Dt,
            scale=Sigma * np.sqrt(Dt),
            size=Days,
        )
        Price = [StartPrice]
        for R in Returns:
            Price.append(Price[-1] * np.exp(R))
        Index = pd.date_range(
            start=pd.Timestamp.today(),
            periods=Days,
            freq="D",
        )
        Data = pd.DataFrame(index=Index)
        Data["Open"] = Price[:-1]
        PriceArray = np.array(Price[1:])
        OpenArray = np.array(Price[:-1])
        HighMultiplier = np.random.uniform(1.0, 1.02, size=Days)
        LowMultiplier = np.random.uniform(0.98, 1.0, size=Days)
        Data["High"] = (
            np.maximum(OpenArray, PriceArray) * HighMultiplier
        )
        Data["Low"] = (
            np.minimum(OpenArray, PriceArray) * LowMultiplier
        )
        Data["Close"] = PriceArray
        Data["Adj Close"] = PriceArray
        Data["Volume"] = np.random.randint(100000, 1000000, size=Days)
        return Data
