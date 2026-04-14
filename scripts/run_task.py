from app.core.graph import build_graph
from app.llm.rule_selector import RuleSelector

if __name__ == "__main__":
    # Select rules based on config and auto-detection
    selector = RuleSelector(project_path=".")
    active_rules = selector.select_rules_interactively(accept_defaults=True)

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
        "logs": [],
        "active_rules": active_rules
    })

    print("\n=== FINAL RESULT ===\n")
    print("Approved:", result["approved"])
    print("\nPatch:\n", result["patch"])
    print("\nLogs:\n", "\n".join(result["logs"]))
