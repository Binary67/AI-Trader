from langchain_core.tools import tool
import pandas as pd


def CreateEmaTool(Data: pd.DataFrame):
    @tool
    def CalculateEma(Span: int = 14) -> float:
        """Return the latest exponential moving average using closing prices."""
        return float(Data["Close"].ewm(span=Span, adjust=False).mean().iloc[-1])

    return CalculateEma
