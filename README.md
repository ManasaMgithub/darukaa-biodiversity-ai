# 🌍 Darukaa Earth — AI Biodiversity Intelligence System

An AI-powered biodiversity and environmental intelligence system that analyzes interconnected environmental conditions and generates **evidence-backed, multi-metric recommendations** using Retrieval-Augmented Generation (RAG).

The system is designed for the **Darukaa.Earth AI Biodiversity Intelligence Challenge**, with a focus on scientific grounding, environmental reasoning, knowledge retrieval, and conversational intelligence.

---

## 🚀 Live Demo

**Live Application:** `Coming soon`

**GitHub Repository:** `https://github.com/YOUR_USERNAME/darukaa-biodiversity-ai`

---

## 🎯 Problem Statement

Environmental problems are rarely caused by a single factor.

For example:

* Low rainfall can create water stress.
* Low soil organic carbon can reduce soil quality and water retention.
* Continuous monoculture can simplify habitat structure and reduce biodiversity.
* These factors can interact and amplify ecosystem stress.

A useful biodiversity intelligence system therefore needs to reason across multiple environmental variables instead of producing isolated or generic recommendations.

---

## 💡 Solution

Darukaa Earth is an AI environmental intelligence system that:

1. Accepts environmental conditions through natural-language or structured input.
2. Detects important environmental variables.
3. Identifies missing information and asks clarification questions.
4. Retrieves relevant scientific knowledge using semantic search.
5. Uses retrieved evidence as grounding for the analysis.
6. Performs multi-metric environmental reasoning.
7. Generates specific recommendations with:

   * Scientific reasoning
   * Impacted environmental metrics
   * Time horizon
   * Supporting evidence
8. Displays the retrieved scientific evidence and similarity scores.

The goal is to behave more like an **AI environmental scientist** than a generic chatbot.

---

## 🧠 Core Features

### Multi-Metric Environmental Reasoning

The system connects environmental variables such as:

* Soil organic carbon
* Rainfall
* Soil moisture
* Land use
* Crop diversity
* Habitat diversity
* Biodiversity
* Water availability

Example reasoning:

```text
Low rainfall
      ↓
Water stress
      ↓
Low soil organic carbon
      ↓
Reduced moisture retention
      ↓
Greater ecosystem stress
      ↓
Higher biodiversity pressure
```

---

### 🔎 Retrieval-Augmented Generation (RAG)

The system does not rely only on the language model.

Scientific knowledge is stored in a vector database and retrieved using semantic similarity.

```text
User Query
    ↓
Gemini Embedding
    ↓
Pinecone Vector Search
    ↓
Relevant Scientific Evidence
    ↓
Gemini Reasoning
    ↓
Grounded Recommendation
```

This allows recommendations to be linked to retrieved scientific sources.

---

### 💬 Conversational Intelligence

The system maintains environmental context during the conversation.

For incomplete queries, it asks for missing information such as:

* Soil organic carbon
* Rainfall pattern
* Land use or crop system

Example:

```text
User:
"My biodiversity is declining."

System:
"What is the approximate soil organic carbon level?"
"What is the rainfall pattern?"
"What is the current land use or crop system?"
```

The collected information is then used as the environmental state for analysis.

---

### 📚 Evidence-Backed Recommendations

Each recommendation contains:

* Action
* Scientific reasoning
* Impacted environmental metrics
* Time horizon
* Supporting evidence

The model is instructed not to invent studies, numerical estimates, citations, or URLs that are not present in the retrieved knowledge.

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │       User          │
                    │ Natural Language /  │
                    │ Structured Input    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Streamlit UI     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Conversation &      │
                    │ Environment State   │
                    └──────────┬──────────┘
                               │
                     Missing Factors?
                        │          │
                      Yes          No
                       │            │
                       ▼            ▼
                Clarification    Query Builder
                Questions             │
                                      ▼
                            ┌──────────────────┐
                            │ Gemini Embedding │
                            └────────┬─────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │ Pinecone Vector  │
                            │ Knowledge Base   │
                            └────────┬─────────┘
                                     │
                                     ▼
                            Retrieved Evidence
                                     │
                                     ▼
                            ┌──────────────────┐
                            │ Gemini Flash     │
                            │ Reasoning        │
                            └────────┬─────────┘
                                     │
                                     ▼
                         Multi-Metric Analysis
                                     │
                                     ▼
                     Evidence-Backed Recommendations
```

---

## 🗂️ Project Structure

```text
darukaa-biodiversity-ai/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── data/
│   └── knowledge.txt
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── conversation.py
│   ├── ingestion.py
│   ├── prompts.py
│   ├── reasoning.py
│   └── retriever.py
│
├── tests/
│   └── test_input.py
│
├── docs/
│
└── .github/
    └── workflows/
        └── ci.yml
```

---

## 🔬 Knowledge Base

The current knowledge base contains evidence related to:

* Soil organic cover and biodiversity
* Agricultural diversification
* Water availability and dryland ecosystems
* Land degradation and biodiversity
* Agroforestry and soil carbon
* Multi-metric biodiversity reasoning
* Evidence and uncertainty

Scientific sources include:

### FAO — Conservation Agriculture

https://www.fao.org/conservation-agriculture/in-practice/soil-organic-cover/en/

### IPCC — Special Report on Climate Change and Land

https://www.ipcc.ch/srccl/

### FAO AGRIS — Soil Carbon and Plant Diversity

**Soil carbon stock in relation to plant diversity of homegardens in Kerala, India**

https://agris.fao.org/search/en/providers/122535/records/65df9ab96eef00c2cea32487

---

## 🧰 Technology Stack

| Component            | Technology                |
| -------------------- | ------------------------- |
| Frontend             | Streamlit                 |
| Programming Language | Python 3.11               |
| Generative AI        | Google Gemini             |
| Embeddings           | Gemini Embedding          |
| Vector Database      | Pinecone                  |
| RAG                  | Semantic vector retrieval |
| Testing              | Pytest                    |
| Version Control      | Git + GitHub              |
| CI                   | GitHub Actions            |
| Deployment           | Streamlit Community Cloud |

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/darukaa-biodiversity-ai.git
cd darukaa-biodiversity-ai
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=darukaa-biodiversity
```

Do not commit `.env` to GitHub.

### 5. Ingest the knowledge base

```bash
python -m src.ingestion
```

### 6. Run tests

```bash
pytest
```

### 7. Start the application

```bash
streamlit run app.py
```

The application will open locally at:

```text
http://localhost:8501
```

---

## 🔄 Knowledge Ingestion

The ingestion pipeline:

```text
knowledge.txt
     ↓
Text processing
     ↓
Chunk creation
     ↓
Gemini embeddings
     ↓
Pinecone vectors
     ↓
Metadata + source information
```

Each stored knowledge chunk includes information that allows the application to show the retrieved evidence and its source.

---

## 🤖 Reasoning Pipeline

When the user provides a complete environmental situation:

```text
1. Detect environmental variables
2. Build combined environmental query
3. Generate query embedding
4. Search Pinecone
5. Retrieve top relevant evidence
6. Construct evidence context
7. Send grounded context to Gemini
8. Generate multi-metric environmental analysis
9. Display recommendations and supporting evidence
```

The reasoning prompt explicitly instructs the model to:

* Use retrieved knowledge as factual grounding.
* Analyze multiple variables together.
* Explain environmental mechanisms.
* Avoid generic recommendations.
* Include measurable metrics.
* Include time horizons.
* Avoid unsupported numerical claims.
* Distinguish direct evidence from derived reasoning.
* State when evidence is insufficient.

---

## 🧪 Example

### Input

```text
My farm has SOC 0.3%, low rainfall and wheat monoculture.
Biodiversity is declining.
```

### Detected Factors

```text
Soil Organic Carbon: 0.3%
Rainfall: Low
Land Use: Wheat monoculture
```

### Example Recommendation

```text
Action:
Implement cover crops and crop residue management.

Scientific reasoning:
Cover crops protect the soil surface, utilize residual soil
moisture, improve soil properties and reduce monoculture continuity.

Impacted metrics:
- Soil organic carbon
- Soil moisture
- Soil structure
- Vegetation cover
- Agroecosystem biodiversity

Time horizon:
Short term to Medium term

Evidence:
FAO Conservation Agriculture — Soil Organic Cover
```

The application also displays the retrieved scientific evidence and semantic similarity scores.

---

## 🔐 Security

API keys are stored through environment variables and are intentionally excluded from version control.

The following files must never contain committed credentials:

```text
.env
.streamlit/secrets.toml
```

For cloud deployment, secrets should be configured through the hosting platform rather than committed to the repository.

---

## 🚀 Deployment

The application is designed for deployment on **Streamlit Community Cloud**.

Deployment configuration:

```text
GitHub Repository
       ↓
Streamlit Community Cloud
       ↓
Install requirements.txt
       ↓
Configure secrets
       ↓
Run app.py
       ↓
Live Streamlit URL
```

Streamlit Community Cloud supports deployment directly from GitHub repositories and provides a secrets interface for environment variables and API credentials.

---

## 🔁 CI/CD

GitHub Actions is used for continuous integration.

The workflow performs automated checks on repository changes, including:

```text
Git Push
   ↓
GitHub Actions
   ↓
Checkout repository
   ↓
Setup Python
   ↓
Install dependencies
   ↓
Run tests
   ↓
Validate application
```

Successful changes can then be reflected in the deployed Streamlit application through the GitHub-connected deployment workflow.

Streamlit Community Cloud monitors the connected GitHub repository and updates the deployed application when repository changes are pushed.

---

## 📊 Evaluation Focus

The project is designed around the challenge's major evaluation areas:

| Area                        | Implementation                                    |
| --------------------------- | ------------------------------------------------- |
| Reasoning                   | Multi-metric environmental interactions           |
| Scientific Grounding        | FAO, IPCC and research evidence                   |
| Knowledge Design            | Pinecone vector knowledge base                    |
| Conversational Intelligence | Missing-factor detection and environmental state  |
| Output Clarity              | Structured recommendations and measurable metrics |

---

## 🌱 Future Improvements

Possible future extensions include:

* Geographic/spatial environmental analysis
* Weather and climate API integration
* Larger scientific document corpus
* Satellite-derived land-use information
* Biodiversity indicator datasets
* Location-specific recommendations
* More advanced temporal environmental analysis
* Additional structured environmental inputs

---

## 👥 Project

**Darukaa Earth — AI Biodiversity Intelligence System**

Built as a submission for the Darukaa.Earth AI Biodiversity Intelligence Challenge.
