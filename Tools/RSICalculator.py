from langchain_core.tools import tool
import pandas as pd


def CreateRsiTool(Data: pd.DataFrame):
    @tool
    def CalculateRsi(Period: int = 14) -> float:
        """Return the latest relative strength index using closing prices."""
        Delta = Data["Close"].diff()
        Gain = Delta.clip(lower=0)
        Loss = -Delta.clip(upper=0)
        AvgGain = Gain.rolling(window=Period, min_periods=Period).mean()
        AvgLoss = Loss.rolling(window=Period, min_periods=Period).mean()
        Rs = AvgGain / AvgLoss
        Rsi = 100 - (100 / (1 + Rs))
        return float(Rsi.iloc[-1])

    return CalculateRsi
