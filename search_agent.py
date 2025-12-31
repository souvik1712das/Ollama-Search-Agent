import requests
import json
import sys
from datetime import datetime

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
SEARXNG_URL = "http://127.0.0.1:8888/search"
MODEL = "llama3.2"

def query_ollama(prompt, system_prompt=None):
    """
    Sends a prompt to the Ollama API and returns the response.
    """
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
    """
    Searches SearXNG for the given query and returns the results.
    Tries multiple engines if one fails.
    """
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
    """
    Asks Ollama to interpret the user's query and formulate a search query.
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    system_prompt = (
        f"You are a helpful assistant. Today's date is {current_date}. "
        "Your goal is to interpret the user's query and formulate a concise search query for a search engine. "
        "If the user asks for 'recent' or 'latest' information, use the current year/month from today's date. "
        "Output ONLY the search query, nothing else."
    )
    return query_ollama(user_input, system_prompt)

def summarize_results(user_query, search_results):
    """
    Asks Ollama to summarize the search results in the context of the user's query.
    """
    if not search_results:
        return "No search results found."

    # Prepare context from search results (limit to top 5 to avoid context window issues)
    context = ""
    print("\n--- Search Results Context ---")
    for i, result in enumerate(search_results[:5]):
        title = result.get('title', 'No Title')
        content = result.get('content', 'No Content')
        url = result.get('url', 'No URL')
        
        print(f"[{i+1}] {title} ({url})")
        # print(f"    Snippet: {content}\n") # Optional: print snippet if needed, but might be verbose
        
        context += f"Result {i+1}:\nTitle: {title}\nSnippet: {content}\nURL: {url}\n\n"
    print("------------------------------\n")

    system_prompt = (
        "You are a helpful assistant. You MUST answer the user's query using ONLY the provided search results below. "
        "Do not use your pre-trained knowledge to answer the question if the information is available in the search results. "
        "If the search results contain the answer, summarize them clearly. "
        "If the search results do not contain the answer, state that you could not find the information in the search results. "
        "Include the source (URL) for your answer."
    )
    
    prompt = f"User Query: {user_query}\n\nSearch Results:\n{context}\n\nPlease provide a summary answer:"
    return query_ollama(prompt, system_prompt)

def main():
    print("--- Ollama + SearXNG Search Agent ---")
    print(f"Ollama URL: {OLLAMA_URL}")
    print(f"SearXNG URL: {SEARXNG_URL}")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        if not user_input.strip():
            continue

        print("Thinking...")
        
        # 1. Interpret Query
        search_query = interpret_query(user_input)
        if not search_query:
            print("Failed to interpret query.")
            continue
        
        print(f"Searching for: {search_query}")

        # 2. Search SearXNG
        results = search_searxng(search_query)
        if not results:
            print("No results found or error connecting to SearXNG.")
            # Fallback: ask Ollama directly without context? Or just report no results.
            # Let's just report no results for now.
        else:
            print(f"Found {len(results)} results. Summarizing...")
            
            # 3. Summarize Results
            summary = summarize_results(user_input, results)
            print(f"\nAgent: {summary}\n")

if __name__ == "__main__":
    main()
