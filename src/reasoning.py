from google import genai

from src.config import GEMINI_API_KEY
from src.retriever import retrieve_knowledge


gemini = genai.Client(api_key=GEMINI_API_KEY)


def build_context(results):
    context_parts = []

    for i, result in enumerate(results, 1):
        context_parts.append(
            f"""
EVIDENCE {i}

Source:
{result['source']}

Similarity:
{result['score']:.4f}

Retrieved Knowledge:
{result['text']}
"""
        )

    return "\n".join(context_parts)


def analyze_environment(user_query):
    """
    Retrieve relevant environmental knowledge and
    generate an evidence-grounded multi-metric analysis.
    """

    results = retrieve_knowledge(user_query, top_k=5)

    context = build_context(results)

    prompt = f"""
You are Darukaa Earth, an AI biodiversity and environmental
intelligence system.

Your task is to analyze an environmental situation using
multi-metric reasoning and retrieved scientific knowledge.

USER ENVIRONMENTAL SITUATION:
{user_query}


RETRIEVED KNOWLEDGE:
{context}


IMPORTANT RULES:

1. Use the retrieved knowledge as the factual grounding
   for your answer.

2. Analyze multiple environmental variables together.

3. Explain relationships between the variables instead of
   treating each variable independently.

4. Do NOT give generic recommendations such as
   "use sustainable practices" without explaining the
   specific action.

5. Every recommendation must contain:
   - Action
   - Scientific reasoning
   - Impacted environmental metrics
   - Time horizon
   - Supporting evidence

6. Only mention numerical improvement estimates if they
   are explicitly present in the retrieved knowledge.

7. Do NOT invent:
   - studies
   - authors
   - percentages
   - numerical results
   - citations
   - URLs

8. When citing evidence, use the source information that
   appears in the retrieved knowledge.

9. Clearly distinguish between:
   - Evidence directly supported by the knowledge base
   - Reasoning derived from combining the evidence

10. If evidence is insufficient for a specific claim,
    explicitly state that the knowledge base does not
    provide enough evidence.

11. Consider interactions such as:
    - soil health ↔ biodiversity
    - water availability ↔ ecosystem stress
    - land use ↔ habitat diversity
    - climate stress ↔ land degradation

12. Do not claim certainty when the evidence is limited.

13. Preserve measurement units exactly as provided by the user.
    For example, if soil organic carbon is given as 0.3%,
    display it as 0.3%, not 0.3.

14. Confidence rule:
    - Use "Medium" confidence when recommendations are
      supported by scientific evidence but site-specific
      information is limited.
    - Use "High" confidence only when the retrieved evidence
      strongly and directly supports the recommendation and
      sufficient site-specific information is available.
    - Use "Low" confidence when the available evidence is
      insufficient or highly indirect.


Return the response using exactly this structure:


ENVIRONMENTAL ASSESSMENT

Explain the main environmental situation and how the
identified variables interact.


DETECTED FACTORS

List the environmental variables detected from the
user's input.


MULTI-METRIC INTERACTIONS

Explain how the detected environmental factors influence
one another.

For each important interaction, explain the mechanism.


RECOMMENDATIONS

Recommendation 1

Action:
Give a specific intervention.

Scientific reasoning:
Explain why this intervention addresses the detected
environmental conditions.

Impacted metrics:
List the environmental metrics expected to be affected.

Time horizon:
Short term / Medium term / Long term.

Evidence:
Name the retrieved supporting source and explain what
the source supports.


Recommendation 2

Action:
Give a specific intervention.

Scientific reasoning:
Explain why this intervention addresses the detected
environmental conditions.

Impacted metrics:
List the environmental metrics expected to be affected.

Time horizon:
Short term / Medium term / Long term.

Evidence:
Name the retrieved supporting source and explain what
the source supports.


MEASURABLE METRICS TO MONITOR

List the environmental metrics that should be monitored
to determine whether the interventions are working.


EVIDENCE SOURCES

List the relevant retrieved sources and their URLs.


CONFIDENCE

Give:
High / Medium / Low

Explain briefly why this confidence level was selected.
"""


    interaction = gemini.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    return {
        "answer": interaction.output_text,
        "sources": results
    }


if __name__ == "__main__":

    query = """
    My farm has low rainfall, low soil organic carbon
    and wheat monoculture. Biodiversity is declining.
    """

    result = analyze_environment(query)

    print("\n")
    print(result["answer"])

    print("\n\nRETRIEVED SOURCES:")

    for source in result["sources"]:
        print(
            f"- {source['source']} "
            f"(similarity: {source['score']:.4f})"
        )