import os
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage


# -----------------------------
# LOAD ENV
# -----------------------------
load_dotenv()

INDEX_PATH = "./faiss_index"

embeddings = HuggingFaceBgeEmbeddings()

llm = ChatGroq(
    api_key='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',
    model="llama3-70b-8192"
)


# -----------------------------
# LOAD FAISS INDEX
# -----------------------------
def load_index():
    return FAISS.load_local(
        INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )


# -----------------------------
# RAG PIPELINE
# -----------------------------
def ask_documents(query: str, k: int = 4):
    vectorstore = load_index()

    docs = vectorstore.similarity_search(query, k=k)

    context = "\n\n".join([d.page_content for d in docs])

    messages = [
        SystemMessage(content="""
        You are a helpful assistant.
        Answer ONLY using the provided context.
        If context is insufficient, say you don't know.
        """),
        HumanMessage(content=f"""
Context:
{context}

Question:
{query}
""")
    ]

    response = llm.invoke(messages)

    return {
        "query": query,
        "answer": response.content,
        "sources": [
            {
                "content": d.page_content[:200],
                "metadata": d.metadata
            }
            for d in docs
        ]
    }


# -----------------------------
# CLI MODE (RUN HERE)
# -----------------------------
def run_cli():
    print("\n📚 RAG SYSTEM READY (type 'exit' to quit)\n")

    while True:
        query = input("Ask a question: ")

        if query.lower() in ["exit", "quit"]:
            print("Goodbye 👋")
            break

        result = ask_documents(query)

        print("\n🤖 Answer:\n")
        print(result["answer"])

        print("\n📌 Sources:")
        for s in result["sources"]:
            print("-", s["content"][:100])

        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    run_cli()