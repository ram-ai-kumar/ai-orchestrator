from langchain_community.llms import Ollama
from app.core.state import AgentState


def reviewer_node(state: AgentState) -> AgentState:
    llm = Ollama(model="deepseek-r1")

    prompt = f"""
You are a strict senior code reviewer.

Review this patch:

{state["patch"]}

Check:
- correctness
- edge cases
- security risks
- completeness

Respond ONLY in this format:

APPROVED

OR

REJECTED: <reason>
"""

    response = llm.invoke(prompt)

    state["review"] = response
    state["approved"] = "APPROVED" in response

    if state["approved"]:
        state["logs"].append("Reviewer approved patch")
        # Advance to next step if approved and more steps remain
        if state["current_step"] < len(state["plan"]) - 1:
            state["current_step"] += 1
            state["approved"] = False  # Reset for next iteration
            state["logs"].append(f"Advancing to step {state['current_step']}")
    else:
        state["logs"].append("Reviewer rejected patch")

    return state
