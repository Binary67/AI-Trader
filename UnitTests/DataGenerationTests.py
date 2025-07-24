import pandas as pd
import tempfile
from unittest import TestCase
from unittest.mock import patch

from DataGeneration import DataGeneration


class DataGenerationTests(TestCase):
    def setUp(self):
        self.TempDir = tempfile.TemporaryDirectory()
        self.Generator = DataGeneration(self.TempDir.name)

    def tearDown(self):
        self.TempDir.cleanup()

    def test_DataDownloader_uses_cache(self):
        SampleData = pd.DataFrame({"Close": [1, 2, 3]}, index=pd.date_range("2020-01-01", periods=3))
        with patch("DataGeneration.yf.download", return_value=SampleData) as MockDownload:
            Data = self.Generator.DataDownloader("TEST", "2020-01-01", "2020-01-03", "1d")
            self.assertTrue(MockDownload.called)
        with patch("DataGeneration.yf.download") as MockDownload:
            Data2 = self.Generator.DataDownloader("TEST", "2020-01-01", "2020-01-03", "1d")
            self.assertFalse(MockDownload.called)
        pd.testing.assert_frame_equal(Data2, SampleData, check_freq=False)

    def test_GenerateDummyData_length(self):
        Data = self.Generator.GenerateDummyData(StartPrice=10, Days=10)
        self.assertEqual(len(Data), 11)
        self.assertEqual(Data.iloc[0]["Close"], 10)
