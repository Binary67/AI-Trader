from DataGeneration import DataGeneration
from Agents.TraderAgent import TraderAgent


def Main():
    Generator = DataGeneration()
    Data = Generator.DataDownloader(
        "AAPL",
        "2020-01-01",
        "2024-12-31",
        "1d",
        UseDummyData=True,
    )

    Agent = TraderAgent(Data)
    Decision = Agent.Analyze("Provide a trading decision based on the data")
    print(Decision)


if __name__ == "__main__":
    Main()
