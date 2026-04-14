from langchain_community.llms import Ollama
from app.core.state import AgentState
from app.llm.prompt_builder import PromptBuilder


def planner_node(state: AgentState) -> AgentState:
    llm = Ollama(model="qwen3.5")

    # Build system prompt with active rules
    prompt_builder = PromptBuilder()
    system_prompt = prompt_builder.build_system_prompt(state.get("active_rules", []))

    prompt = f"""
{system_prompt}

You are a senior software architect and task planner.

Your job is to convert a user request into a sequence of small, precise, executable coding steps.

INPUT TASK:
{state["task"]}

RULES:
- Break into 3–7 steps maximum
- Each step must be independently executable
- Each step must involve a concrete code action
- Avoid vague steps like "improve" or "optimize"
- Prefer file-level or function-level actions
- Respect existing architecture unless explicitly told otherwise

CONSTRAINTS:
- Do NOT write code
- Do NOT explain reasoning
- Do NOT repeat the task

OUTPUT FORMAT (STRICT):
1. <step>
2. <step>
3. <step>

EXAMPLE:
1. Identify the function handling authentication in auth.py
2. Refactor the function to extract validation logic into a separate helper
3. Update unit tests to cover the new helper function
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
