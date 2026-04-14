import os
from pathlib import Path
from langchain_core.documents import Document


class CodeIndexer:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def index_directory(self, directory, extensions=[".py", ".js", ".ts"]):
        documents = []
        for root, _, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    path = Path(root) / file
                    try:
                        with open(path, 'r') as f:
                            content = f.read()
                        doc = Document(
                            page_content=content,
                            metadata={"source": str(path)}
                        )
                        documents.append(doc)
                    except Exception as e:
                        print(f"Failed to read {path}: {e}")
        self.vector_store.add_documents(documents)
        return len(documents)
