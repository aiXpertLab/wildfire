![alt text](doc/logo.png)

# 🔥 Wildfire

**Wildfire is an agentic execution framework that rapidly propagates reasoning, actions, and state across tools, models, and workflows.**

Wildfire is designed to complement retrieval-centric frameworks (such as Haystack) by focusing on **execution, coordination, and propagation** once knowledge has been retrieved.

---

## Why Wildfire?

Modern LLM applications increasingly require more than retrieval and prompting — they require **agentic behavior**, **tool execution**, and **stateful reasoning** across multiple steps and systems.

Wildfire addresses this by providing a framework optimized for:

- Fast propagation of decisions and actions
- Multi-agent and multi-tool orchestration
- Explicit state and execution flow management
- Scalable, model-agnostic reasoning pipelines

---

## Conceptual Model

| Layer | Responsibility |
|------|---------------|
| Retrieval | Knowledge access (e.g. Haystack, vector DBs) |
| **Execution (Wildfire)** | Reasoning, actions, propagation |
| Tools | APIs, databases, services |
| Models | LLMs, VLMs, embedding models |

> **Haystack gathers the fuel. Wildfire ignites and spreads the intelligence.**

---

## Key Features

- **Agentic Execution Engine**  
  Coordinate autonomous and semi-autonomous agents with explicit execution control.

- **State Propagation**  
  Share and evolve state across agents, tools, and steps.

- **Tool-First Design**  
  Native support for tool calling, retries, fallbacks, and side-effects.

- **Model-Agnostic**  
  Works with OpenAI, Azure OpenAI, local models, and custom inference backends.

- **Composable Workflows**  
  Build execution graphs, not just linear chains.

---

## Example Use Cases

- Agent-based RAG systems (Haystack + Wildfire)
- Autonomous research and planning agents
- Multi-step reasoning with tool execution
- Workflow automation powered by LLMs
- Event-driven AI systems

---

## Minimal Example (Conceptual)

```python
from wildfire import Agent, Workflow

agent = Agent(
    model="gpt-4o",
    tools=[search, calculator, database]
)

workflow = Workflow(agent)
workflow.run(input="Investigate market trends and produce a summary report")
