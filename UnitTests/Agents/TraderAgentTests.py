import pandas as pd
from unittest import TestCase
from unittest.mock import patch, MagicMock
from Agents.TraderAgent import TraderAgent


class TraderAgentTests(TestCase):
    def test_Analyze_returns_agent_response(self):
        Data = pd.DataFrame({"Close": [1, 2, 3]})
        with patch("Agents.TraderAgent.create_react_agent") as MockCreate:
            MockGraph = MagicMock()
            MockGraph.invoke.return_value = {
                "messages": [{"role": "assistant", "content": "Buy"}]
            }
            MockCreate.return_value = MockGraph
            Agent = TraderAgent(Data)
            Response = Agent.Analyze("Should I buy?")
            self.assertEqual(Response, "Buy")
