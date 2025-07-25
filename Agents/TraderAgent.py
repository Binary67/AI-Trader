import os
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent
from Tools.EMACalculator import CreateEmaTool
from Tools.RSICalculator import CreateRsiTool


class TraderAgent:
    def __init__(self, Data):
        self.Data = Data
        self.EmaTool = CreateEmaTool(self.Data)
        self.RsiTool = CreateRsiTool(self.Data)
        self.Model = AzureChatOpenAI(
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"],
            api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        )
        Prompt = (
            "You are a trading assistant. Use the tools provided to analyze the "
            "data and give a buy or sell recommendation."
        )
        self.Agent = create_react_agent(
            model=self.Model,
            tools=[self.EmaTool, self.RsiTool],
            prompt=Prompt,
        )

    def Analyze(self, Query: str) -> str:
        Result = self.Agent.invoke({"messages": [{"role": "user", "content": Query}]})
        Messages = Result.get("messages", [])
        if Messages:
            Last = Messages[-1]
            if hasattr(Last, "content"):
                return Last.content
            if isinstance(Last, dict):
                return Last.get("content", str(Last))
            return str(Last)
        return ""
