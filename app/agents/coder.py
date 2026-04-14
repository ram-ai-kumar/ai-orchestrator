from langchain_community.llms import Ollama
from app.core.state import AgentState


def coder_node(state: AgentState) -> AgentState:
    llm = Ollama(model="qwen2.5-coder")

    step = state["plan"][state["current_step"]]

    context_block = "\n\n".join(state.get("context", []))

    prompt = f"""
You are an expert software engineer.

Current task step:
{step}

Relevant context:
{context_block}

Rules:
- Generate ONLY a valid git diff patch
- Do NOT explain anything
- Do NOT output full files
- Only show changes

Return format:
--- a/file
+++ b/file
@@ ...
"""

    response = llm.invoke(prompt)

    state["patch"] = response
    state["logs"].append(f"Coder generated patch for step {state['current_step']}")

    return state
