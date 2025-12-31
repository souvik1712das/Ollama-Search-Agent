from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
from datetime import datetime
import os

app = FastAPI()

# CORS for development flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
SEARXNG_URL = "http://127.0.0.1:8888/search"
MODEL = "llama3.2"

class SearchRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    summary: str
    search_query: str
    results: list

def query_ollama(prompt, system_prompt=None):
    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    if system_prompt:
        data["system"] = system_prompt

    try:
        response = requests.post(OLLAMA_URL, json=data)
        response.raise_for_status()
        return response.json().get("response", "")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama: {e}")
        return None

def search_searxng(query):
    engines = ["duckduckgo", "brave", "wikipedia", "bing", "google"]
    
    for engine in engines:
        print(f"Trying engine: {engine}...")
        params = {
            "q": query,
            "format": "json",
            "language": "en",
            "engines": engine
        }
        try:
            response = requests.get(SEARXNG_URL, params=params)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            if results:
                return results
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to SearXNG with {engine}: {e}")
            continue
            
    return []

def interpret_query(user_input):
    current_date = datetime.now().strftime("%Y-%m-%d")
    system_prompt = (
        f"You are a helpful assistant. Today's date is {current_date}. "
        "Your goal is to interpret the user's query and formulate a concise search query for a search engine. "
        "If the user asks for 'recent' or 'latest' information, use the current year/month from today's date. "
        "Output ONLY the search query, nothing else."
    )
    return query_ollama(user_input, system_prompt)

def summarize_results(user_query, search_results):
    if not search_results:
        return "No search results found."

    context = ""
    for i, result in enumerate(search_results[:5]):
        title = result.get('title', 'No Title')
        content = result.get('content', 'No Content')
        url = result.get('url', 'No URL')
        context += f"Result {i+1}:\nTitle: {title}\nSnippet: {content}\nURL: {url}\n\n"

    system_prompt = (
        "You are a helpful assistant. You MUST answer the user's query using ONLY the provided search results below. "
        "Do not use your pre-trained knowledge to answer the question if the information is available in the search results. "
        "If the search results contain the answer, summarize them clearly. "
        "If the search results do not contain the answer, state that you could not find the information in the search results. "
        "Include the source (URL) for your answer."
    )
    
    prompt = f"User Query: {user_query}\n\nSearch Results:\n{context}\n\nPlease provide a summary answer:"
    return query_ollama(prompt, system_prompt)

@app.post("/api/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    print(f"Received query: {request.query}")
    
    # 1. Interpret
    search_query = interpret_query(request.query)
    if not search_query:
        raise HTTPException(status_code=500, detail="Failed to interpret query with Ollama")
    
    print(f"Interpreted as: {search_query}")

    # 2. Search
    results = search_searxng(search_query)
    
    # 3. Summarize
    summary = summarize_results(request.query, results)
    
    return {
        "summary": summary,
        "search_query": search_query,
        "results": results[:5] # Return top 5 to frontend
    }

# Mount static files (Frontend)
# We mount this LAST so API routes take precedence
app.mount("/", StaticFiles(directory="backend/static", html=True), name="static")
