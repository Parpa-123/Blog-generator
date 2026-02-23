# 📝 AI Blog Generator Agent

An agentic AI-powered blog generator built with **LangGraph**, **LangChain**, and **Groq (Llama 3.3 70B)**. It generates SEO-friendly blog titles and content from a topic, with optional multi-language translation — all served through a **FastAPI** backend.

---

## ✨ Features

- **AI Blog Generation** — Automatically generates creative, SEO-optimized blog titles and content for any given topic.
- **Multi-Language Translation** — Optionally translates generated blogs into **Hindi** or **French** using conditional graph routing.
- **LangGraph Workflow** — Uses a stateful, multi-step agent graph with nodes for title creation, content generation, routing, and translation.
- **LangSmith Tracing** — Built-in observability and tracing via LangSmith for debugging and monitoring.
- **FastAPI Backend** — Clean REST API with Pydantic request validation and auto-generated OpenAPI docs.

---

## 🏗️ Architecture

```
User Request
     │
     ▼
  FastAPI
     │
     ▼
 LangGraph State Machine
     │
     ├── Title Creation Node
     │        │
     │        ▼
     ├── Content Generation Node
     │        │
     │        ▼
     ├── Route Node (conditional)
     │        │
     │   ┌────┼────────┐
     │   ▼    ▼        ▼
     │ Hindi French  English
     │ Trans  Trans  (no-op)
     │   │    │        │
     └───┴────┴────────┘
              │
              ▼
         Response
```

---

## 📁 Project Structure

```
Project-2/
├── main.py                          # FastAPI app with API routes
├── pyproject.toml                   # Project metadata & dependencies
├── .env                             # Environment variables (API keys)
├── src/
│   ├── graphs/
│   │   └── graph_builder.py         # LangGraph state graph definitions
│   ├── nodes/
│   │   └── blog_node.py             # Node logic (title, content, translation, routing)
│   ├── states/
│   │   └── blogstate.py             # BlogState schema (TypedDict + Pydantic)
│   └── llms/
│       └── groqllm.py               # Groq LLM configuration
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.13+**
- **[uv](https://docs.astral.sh/uv/)** (recommended) or pip
- A **[Groq API Key](https://console.groq.com/)**
- A **[LangChain API Key](https://smith.langchain.com/)** (for LangSmith tracing)

### 1. Clone the Repository

```bash
git clone https://github.com/Parpa-123/Blog-generator.git
cd Blog-generator
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
LANGCHAIN_API_KEY=your_langchain_api_key_here
```

### 3. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### 4. Run the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`. Interactive docs are at `http://localhost:8000/docs`.

---

## 📡 API Endpoints

### `POST /blogs` — Generate a Blog

Generate a blog (title + content) for a given topic.

**Request:**
```json
{
  "topic": "Artificial Intelligence in Healthcare"
}
```

**Response:**
```json
{
  "data": {
    "topic": "Artificial Intelligence in Healthcare",
    "blog": {
      "title": "Revolutionizing Healthcare: The Power of AI",
      "content": "..."
    }
  }
}
```

---

### `POST /blogs/translate` — Generate & Translate a Blog

Generate a blog and translate it into a specified language (`hindi`, `french`, or `english`).

**Request:**
```json
{
  "topic": "Artificial Intelligence in Healthcare",
  "current_language": "hindi"
}
```

**Response:**
```json
{
  "data": {
    "topic": "Artificial Intelligence in Healthcare",
    "current_language": "hindi",
    "blog": {
      "title": "स्वास्थ्य सेवा में कृत्रिम बुद्धिमत्ता की क्रांति",
      "content": "..."
    }
  }
}
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| LLM | Groq — Llama 3.3 70B Versatile |
| Orchestration | LangGraph + LangChain |
| Backend | FastAPI + Uvicorn |
| Observability | LangSmith Tracing |
| Language | Python 3.13+ |

---
