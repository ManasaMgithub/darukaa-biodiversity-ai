from google import genai
from src.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input="Explain biodiversity in one sentence."
)

print(interaction.output_text)