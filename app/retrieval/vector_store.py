from langchain_community.vectorstores import Chroma
from app.llm.ollama_client import get_embeddings


class VectorStore:
    def __init__(self, persist_directory="./data/chroma"):
        self.embeddings = get_embeddings()
        self.vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings
        )

    def add_documents(self, documents):
        self.vectorstore.add_documents(documents)

    def similarity_search(self, query, k=5):
        return self.vectorstore.similarity_search(query, k=k)
