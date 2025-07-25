import pandas as pd
from unittest import TestCase
from Tools.RSICalculator import CreateRsiTool


class RSICalculatorTests(TestCase):
    def test_CalculateRsi(self):
        Data = pd.DataFrame({"Close": [1, 2, 3, 4, 5, 4, 3, 4, 5, 6]})
        RsiTool = CreateRsiTool(Data)
        Result = RsiTool.invoke({"Period": 3})
        Delta = Data["Close"].diff()
        Gain = Delta.clip(lower=0)
        Loss = -Delta.clip(upper=0)
        AvgGain = Gain.rolling(window=3, min_periods=3).mean()
        AvgLoss = Loss.rolling(window=3, min_periods=3).mean()
        Rs = AvgGain / AvgLoss
        Expected = 100 - (100 / (1 + Rs)).iloc[-1]
        self.assertAlmostEqual(Result, Expected)
