import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
from src.graphs.graph_builder import GraphBuilder
from src.llms.groqllm import GroqLLM
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")

app = FastAPI()


# ---------- Request Models (matching LangGraph BlogState inputs) ----------

class BlogRequest(BaseModel):
    """Request model for topic-only blog generation."""
    topic: str = Field(..., description="The topic to generate a blog about")


class BlogTranslateRequest(BaseModel):
    """Request model for blog generation with translation."""
    topic: str = Field(..., description="The topic to generate a blog about")
    current_language: str = Field(
        ..., description="Target language for translation (e.g. hindi, french, english)"
    )


# ---------- Routes ----------

@app.post("/blogs")
async def create_blog(request: BlogRequest):
    """Generate a blog on a given topic."""
    groq_llm = GroqLLM()
    llm = groq_llm.get_llm()

    graph_builder = GraphBuilder(llm)
    graph = graph_builder.setup_graph(usecase="topic")
    state = graph.invoke({"topic": request.topic})

    return {"data": state}


@app.post("/blogs/translate")
async def create_translated_blog(request: BlogTranslateRequest):
    """Generate a blog on a given topic and translate it to the specified language."""
    groq_llm = GroqLLM()
    llm = groq_llm.get_llm()

    graph_builder = GraphBuilder(llm)
    graph = graph_builder.setup_graph(usecase="language")
    state = graph.invoke({
        "topic": request.topic,
        "current_language": request.current_language,
    })

    return {"data": state}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)