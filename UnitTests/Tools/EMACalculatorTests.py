import pandas as pd
from unittest import TestCase
from Tools.EMACalculator import CreateEmaTool


class EMACalculatorTests(TestCase):
    def test_CalculateEma(self):
        Data = pd.DataFrame({"Close": [1, 2, 3, 4, 5]})
        EmaTool = CreateEmaTool(Data)
        Result = EmaTool.invoke({"Span": 3})
        Expected = Data["Close"].ewm(span=3, adjust=False).mean().iloc[-1]
        self.assertAlmostEqual(Result, Expected)
