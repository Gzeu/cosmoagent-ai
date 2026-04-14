"""
CosmoAgent - Multimodal AI Agent for MyShell ShellAgent Platform
Combines cosmic insights, blockchain intelligence, and automated workflows.
"""

import os
import json
import asyncio
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import httpx


@dataclass
class AgentMemory:
    """Short-term memory for the agent session."""
    conversation: List[Dict[str, str]] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    max_turns: int = 20

    def add(self, role: str, content: str):
        self.conversation.append({"role": role, "content": content, "timestamp": datetime.utcnow().isoformat()})
        if len(self.conversation) > self.max_turns:
            self.conversation = self.conversation[-self.max_turns:]

    def get_context(self) -> List[Dict[str, str]]:
        return [{"role": m["role"], "content": m["content"]} for m in self.conversation]


@dataclass
class CosmoAgentConfig:
    name: str = "CosmoAgent"
    version: str = "0.1.0"
    llm_provider: str = "mistral"  # mistral | claude | grok | ollama
    llm_model: str = "mistral-large-latest"
    multiversx_network: str = "mainnet"
    multiversx_gateway: str = "https://gateway.multiversx.com"
    myshell_api_key: str = ""
    temperature: float = 0.7
    max_tokens: int = 2048


class BlockchainTool:
    """Tool for querying MultiversX blockchain data."""

    def __init__(self, gateway: str):
        self.gateway = gateway
        self.client = httpx.AsyncClient(timeout=30)

    async def get_account(self, address: str) -> Dict:
        try:
            r = await self.client.get(f"{self.gateway}/address/{address}")
            return r.json().get("data", {}).get("account", {})
        except Exception as e:
            return {"error": str(e)}

    async def get_token_price(self, token: str = "EGLD") -> Dict:
        try:
            r = await self.client.get(f"https://api.multiversx.com/economics")
            data = r.json()
            return {"token": token, "price_usd": data.get("price", 0), "market_cap": data.get("marketCap", 0)}
        except Exception as e:
            return {"error": str(e)}

    async def get_network_stats(self) -> Dict:
        try:
            r = await self.client.get(f"{self.gateway}/network/status/4294967295")
            return r.json().get("data", {}).get("status", {})
        except Exception as e:
            return {"error": str(e)}


class CosmicInsightTool:
    """Tool for generating cosmic/astronomical insights."""

    COSMIC_FACTS = [
        "The observable universe contains an estimated 2 trillion galaxies.",
        "A neutron star's magnetic field is about 1 trillion times stronger than Earth's.",
        "Light from the Sun takes approximately 8 minutes and 20 seconds to reach Earth.",
        "The Milky Way galaxy is approximately 100,000 light-years in diameter.",
        "Black holes can spin at up to 99% the speed of light.",
    ]

    def get_daily_insight(self) -> str:
        import random
        return random.choice(self.COSMIC_FACTS)

    def calculate_stellar_age(self, star_type: str) -> str:
        lifetimes = {
            "O": "~1-10 million years",
            "B": "~10-100 million years",
            "A": "~100 million - 1 billion years",
            "F": "~1-3 billion years",
            "G": "~3-10 billion years (like our Sun)",
            "K": "~10-30 billion years",
            "M": "~1 trillion years",
        }
        return lifetimes.get(star_type.upper(), f"Unknown star type: {star_type}")


class CosmoAgent:
    """Main CosmoAgent class - Multimodal AI Agent."""

    def __init__(self, config: Optional[CosmoAgentConfig] = None):
        self.config = config or CosmoAgentConfig()
        self.memory = AgentMemory()
        self.blockchain = BlockchainTool(self.config.multiversx_gateway)
        self.cosmic = CosmicInsightTool()
        self.tools = {
            "get_account": self._tool_get_account,
            "get_egld_price": self._tool_get_egld_price,
            "cosmic_insight": self._tool_cosmic_insight,
            "stellar_age": self._tool_stellar_age,
        }

    async def _tool_get_account(self, address: str) -> str:
        data = await self.blockchain.get_account(address)
        return json.dumps(data, indent=2)

    async def _tool_get_egld_price(self) -> str:
        data = await self.blockchain.get_token_price("EGLD")
        return json.dumps(data, indent=2)

    async def _tool_cosmic_insight(self) -> str:
        return self.cosmic.get_daily_insight()

    async def _tool_stellar_age(self, star_type: str) -> str:
        return self.cosmic.calculate_stellar_age(star_type)

    def _build_system_prompt(self) -> str:
        return (
            f"You are {self.config.name}, a multimodal AI agent with expertise in "
            "cosmic astronomy, MultiversX blockchain intelligence, and automated workflows. "
            "You run on the MyShell ShellAgent platform. "
            "Available tools: get_account(address), get_egld_price(), cosmic_insight(), stellar_age(star_type). "
            "Always provide accurate, helpful responses combining cosmic insights with blockchain data."
        )

    async def chat(self, user_message: str) -> str:
        """Process a user message and return a response."""
        self.memory.add("user", user_message)

        # Simple tool routing based on keywords
        response = await self._route_and_respond(user_message)
        self.memory.add("assistant", response)
        return response

    async def _route_and_respond(self, message: str) -> str:
        msg_lower = message.lower()

        if any(k in msg_lower for k in ["account", "wallet", "address", "erd1"]):
            # Extract erd1 address if present
            words = message.split()
            address = next((w for w in words if w.startswith("erd1")), None)
            if address:
                data = await self._tool_get_account(address)
                return f"MultiversX Account Info:\n```json\n{data}\n```"

        if any(k in msg_lower for k in ["price", "egld", "market", "crypto"]):
            data = await self._tool_get_egld_price()
            return f"EGLD Market Data:\n```json\n{data}\n```"

        if any(k in msg_lower for k in ["star", "stellar", "galaxy", "cosmic", "universe", "space"]):
            insight = await self._tool_cosmic_insight()
            return f"Cosmic Insight: {insight}"

        return (
            f"Hi! I'm {self.config.name} v{self.config.version}. "
            "I can help you with: cosmic insights, MultiversX blockchain data, and automated workflows. "
            "Try asking about EGLD price, an erd1 wallet address, or a cosmic topic!"
        )


async def main():
    agent = CosmoAgent()
    print(f"Starting {agent.config.name} v{agent.config.version}...")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["quit", "exit"]:
            break
        response = await agent.chat(user_input)
        print(f"\nCosmoAgent: {response}\n")


if __name__ == "__main__":
    asyncio.run(main())
