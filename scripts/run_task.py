from app.core.graph import build_graph

if __name__ == "__main__":
    graph = build_graph()

    task = input("Enter task: ")

    result = graph.invoke({
        "task": task,
        "plan": [],
        "current_step": 0,
        "context": [],
        "patch": None,
        "review": None,
        "approved": False,
        "logs": []
    })

    print("\n=== FINAL RESULT ===\n")
    print("Approved:", result["approved"])
    print("\nPatch:\n", result["patch"])
    print("\nLogs:\n", "\n".join(result["logs"]))
