from langchain_community.llms import Ollama
from app.core.state import AgentState


def planner_node(state: AgentState) -> AgentState:
    llm = Ollama(model="qwen3.5")

    prompt = f"""
You are a senior software architect.

Break the following task into clear, actionable coding steps.

Task:
{state["task"]}

Rules:
- Keep steps small and precise
- Each step should be executable independently
- Focus on code changes

Return ONLY numbered steps.
"""

    response = llm.invoke(prompt)

    steps = [
        s.strip()
        for s in response.split("\n")
        if s.strip() and any(c.isdigit() for c in s[:3])
    ]

    state["plan"] = steps
    state["current_step"] = 0
    state["logs"].append("Planner created plan")

    return state
