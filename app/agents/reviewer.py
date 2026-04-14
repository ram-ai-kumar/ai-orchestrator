from langchain_ollama import OllamaLLM
from app.core.state import AgentState
from app.llm.prompt_builder import PromptBuilder


def reviewer_node(state: AgentState) -> AgentState:
    llm = OllamaLLM(model="deepseek-r1")

    # Build system prompt with active rules
    prompt_builder = PromptBuilder()
    system_prompt = prompt_builder.build_system_prompt(state.get("active_rules", []))

    prompt = f"""
{system_prompt}

You are a strict senior code reviewer enforcing production quality.

PATCH:
{state["patch"]}

CHECK THE FOLLOWING:

1. Correctness
- Does the change achieve the intended goal?
- Are there logical errors?

2. Safety
- Any security risks?
- Any unsafe assumptions?

3. Scope
- Are changes minimal?
- Any unrelated modifications?

4. Robustness
- Edge cases handled?
- Null/empty handling?

5. Maintainability
- Readability preserved?
- No unnecessary complexity?

DECISION RULES:

APPROVE if:
- Change is correct, safe, and minimal

REJECT if:
- Any correctness issue
- Any unnecessary change
- Any unclear behavior

OUTPUT FORMAT (STRICT):

APPROVED

OR

REJECTED: <clear, specific reason>
"""

    response = llm.invoke(prompt).strip()

    if response.startswith("APPROVED"):
        state["approved"] = True
        state["review"] = "Approved"
        state["current_step"] += 1
    else:
        state["approved"] = False
        state["review"] = response

    state["logs"].append(f"Reviewer: {state['review']}")

    return state
