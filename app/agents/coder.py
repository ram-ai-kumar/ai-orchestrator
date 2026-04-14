from langchain_ollama import OllamaLLM
from app.core.state import AgentState
from app.llm.prompt_builder import PromptBuilder


def coder_node(state: AgentState) -> AgentState:
    llm = OllamaLLM(model="qwen2.5-coder")

    # Build system prompt with active rules
    prompt_builder = PromptBuilder()
    system_prompt = prompt_builder.build_system_prompt(state.get("active_rules", []))

    step = state["plan"][state["current_step"]]

    context_block = "\n\n".join(state.get("context", []))

    prompt = f"""
{system_prompt}

You are an expert software engineer.

Current task step:
{step}

Relevant context:
{context_block}

RULES:
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
