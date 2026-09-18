from google import genai
from pinecone import Pinecone

from src.config import (
    GEMINI_API_KEY,
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
)

# Gemini
gemini = genai.Client(api_key=GEMINI_API_KEY)

# Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)


def create_embedding(text):
    """Create an embedding for the user's query."""
    result = gemini.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return result.embeddings[0].values


def retrieve_knowledge(query, top_k=4):
    """Retrieve the most relevant biodiversity knowledge."""

    query_embedding = create_embedding(query)

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    retrieved_chunks = []

    for match in results["matches"]:
        metadata = match.get("metadata", {})

        retrieved_chunks.append(
            {
                "score": match.get("score",0),
                "text": metadata.get("text") or metadata.get("content", ""),
                "source": metadata.get(
                    "source",
                    "Darukaa Earth Knowledge Base"
                ),
            }
        )

    return retrieved_chunks


if __name__ == "__main__":

    query = """
    My farm has low rainfall, low soil organic carbon
    and wheat monoculture. Biodiversity is declining.
    """

    results = retrieve_knowledge(query)

    print("\nRetrieved Knowledge:\n")

    for i, result in enumerate(results, 1):
        print(f"--- Result {i} ---")
        print(f"Similarity: {result['score']:.4f}")
        print(result["text"])
        print()