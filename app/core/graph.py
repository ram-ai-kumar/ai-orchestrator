from langgraph.graph import StateGraph, END
from app.core.state import AgentState

from app.agents.planner import planner_node
from app.agents.retriever import retriever_node
from app.agents.coder import coder_node
from app.agents.patch_applier import patch_applier_node
from app.agents.tester import tester_node
from app.agents.reviewer import reviewer_node


def build_graph():
    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("planner", planner_node)
    graph.add_node("retriever", retriever_node)
    graph.add_node("coder", coder_node)
    graph.add_node("patch_applier", patch_applier_node)
    graph.add_node("tester", tester_node)
    graph.add_node("reviewer", reviewer_node)

    # Entry
    graph.set_entry_point("planner")

    # Flow
    graph.add_edge("planner", "retriever")
    graph.add_edge("retriever", "coder")
    graph.add_edge("coder", "patch_applier")
    graph.add_edge("patch_applier", "tester")
    graph.add_edge("tester", "reviewer")

    # Conditional loop
    def review_router(state: AgentState):
        # If all steps completed
        if state["current_step"] >= len(state["plan"]):
            return END
        # If approved, go to next step (via coder)
        elif state["approved"]:
            return "coder"
        # If rejected, retry current step
        else:
            return "coder"

    graph.add_conditional_edges(
        "reviewer",
        review_router
    )

    return graph.compile()
