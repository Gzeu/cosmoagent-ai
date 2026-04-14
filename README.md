# 🤖 CosmoAgent AI

> Multimodal AI Agent combining cosmic insights, MultiversX blockchain intelligence, and automated workflows for the MyShell ShellAgent platform.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![MultiversX](https://img.shields.io/badge/MultiversX-SDK-green)](https://multiversx.com)
[![MyShell](https://img.shields.io/badge/MyShell-ShellAgent-purple)](https://myshell.ai)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## Overview

CosmoAgent is a multimodal AI agent that merges two domains:
- **Cosmic Intelligence** - Astronomical facts, stellar classifications, space data
- **Blockchain Intelligence** - MultiversX account queries, EGLD market data, network stats

Built for the **MyShell ShellAgent** platform with support for Mistral, Claude, Grok, and Ollama LLM backends.

## Structure

```
cosmoagent-ai/
├── agent/
│   └── cosmo_agent.py    # Main agent: CosmoAgent, tools, memory
├── requirements.txt
└── README.md
```

## Features

- **AgentMemory** - Sliding window conversation memory (20 turns)
- **BlockchainTool** - Query MultiversX accounts, EGLD price, network stats
- **CosmicInsightTool** - Daily cosmic facts, stellar age calculations
- **Multi-LLM Support** - Mistral / Claude / Grok / Ollama
- **Async Architecture** - Full async/await for non-blocking tool calls
- **Keyword Routing** - Smart routing to appropriate tools based on user intent

## Quick Start

```bash
git clone https://github.com/Gzeu/cosmoagent-ai.git
cd cosmoagent-ai
pip install -r requirements.txt
python agent/cosmo_agent.py
```

## Example Interactions

```
You: What is the EGLD price?
CosmoAgent: EGLD Market Data:
{
  "token": "EGLD",
  "price_usd": 42.5,
  "market_cap": 1170000000
}

You: Tell me something cosmic
CosmoAgent: Cosmic Insight: The observable universe contains an estimated 2 trillion galaxies.

You: Get account erd1abc...
CosmoAgent: MultiversX Account Info: { ... }
```

## Configuration

```python
config = CosmoAgentConfig(
    llm_provider="mistral",  # mistral | claude | grok | ollama
    llm_model="mistral-large-latest",
    multiversx_network="mainnet",
    temperature=0.7
)
agent = CosmoAgent(config)
```

## Roadmap

- [ ] Full MyShell ShellAgent workflow integration
- [ ] Real LLM API calls (Mistral, Claude, Grok)
- [ ] NFT data queries from MultiversX
- [ ] NASA/ESA API integration for real space data
- [ ] Voice interface support
- [ ] Multi-agent orchestration with OpenClaw

## License

MIT License - see [LICENSE](LICENSE)

---
Built by [@Gzeu](https://github.com/Gzeu) | AI Agents · MultiversX · MyShell
