from app.core.state import AgentState
from app.retrieval.vector_store import VectorStore


def retriever_node(state: AgentState) -> AgentState:
    vector_store = VectorStore()

    # Query based on current task step
    query = state["task"]
    if state["plan"] and state["current_step"] < len(state["plan"]):
        query = state["plan"][state["current_step"]]

    docs = vector_store.similarity_search(query, k=5)
    state["context"] = [doc.page_content for doc in docs]
    state["logs"].append(f"Retrieved {len(docs)} context documents")

    return state
