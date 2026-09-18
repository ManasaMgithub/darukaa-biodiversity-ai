from google import genai
from pinecone import Pinecone
from src.config import GEMINI_API_KEY, PINECONE_API_KEY, PINECONE_INDEX_NAME

# Gemini client
gemini = genai.Client(api_key=GEMINI_API_KEY)

# Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)


def create_embedding(text):
    """Create Gemini embedding for a text chunk."""
    result = gemini.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return result.embeddings[0].values


def load_knowledge():
    """Read the biodiversity knowledge file."""
    with open("data/knowledge.txt", "r", encoding="utf-8") as file:
        return file.read()


def split_into_chunks(text):
    """Split knowledge into topic-based chunks."""
    sections = text.split("\n\nTOPIC:")

    chunks = []

    for section in sections:
        section = section.strip()

        if not section:
            continue

        if not section.startswith("TOPIC:"):
            section = "TOPIC:" + section

        chunks.append(section)

    return chunks

def extract_source(chunk):
    """
    Extract the source name from a knowledge chunk.
    """
    if "SOURCE:" in chunk:
        after_source = chunk.split("SOURCE:", 1)[1].strip()
        source_name = after_source.split("\n")[0].strip()

        if source_name:
            return source_name

    if "SUPPORTING SOURCES:" in chunk:
        return "FAO / IPCC"

    return "Darukaa Earth Knowledge Base"

def ingest():
    """Embed and upload knowledge chunks to Pinecone."""

    knowledge = load_knowledge()
    chunks = split_into_chunks(knowledge)

    # Remove old knowledge before uploading the final dataset
    index.delete(delete_all=True)

    vectors = []
    for i, chunk in enumerate(chunks):

        print(f"Embedding chunk {i + 1}/{len(chunks)}...")

        embedding = create_embedding(chunk)

        vectors.append(
            {
                "id": f"knowledge-{i}",
                "values": embedding,
                "metadata": {
                    "source": extract_source(chunk),
                    "text": chunk
                }
            }
        )

    index.upsert(vectors=vectors)

    print(f"\nSuccessfully uploaded {len(vectors)} knowledge chunks.")


if __name__ == "__main__":
    ingest()