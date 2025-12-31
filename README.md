# Ollama Search Agent

A powerful, private, and local search agent that combines **Ollama (Llama 3.2)** with **SearXNG** to provide AI-summarized search results. It features a modern **React** frontend with a premium glowing beam UI.

## Features

-   **AI-Powered Search**: Uses Llama 3.2 to interpret queries and summarize results.
-   **Privacy-Focused**: Uses SearXNG for metasearch, keeping your queries private.
-   **Multi-Engine Fallback**: Automatically tries DuckDuckGo, Brave, Bing, Google, and Wikipedia if one fails.
-   **Modern UI**: Beautiful React-based interface with glassmorphism and animations.
-   **Zero-Build Frontend**: No Node.js required! The frontend runs directly via CDN.
-   **CLI Mode**: Includes a command-line interface for quick terminal searches.

## Prerequisites

1.  **Ollama**: [Download Ollama](https://ollama.com/) and run `ollama serve`.
    -   Pull the model: `ollama pull llama3.2`
2.  **SearXNG**: A running instance of SearXNG (e.g., via Docker).
    -   Default URL: `http://localhost:8080` or `http://127.0.0.1:8888` (Configurable).
3.  **Python 3.8+**

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/OllamaSearchAgent.git
    cd OllamaSearchAgent
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Web Interface (Recommended)

1.  Start the backend server:
    ```bash
    uvicorn backend.main:app --reload
    ```
2.  Open your browser to: [http://localhost:8000](http://localhost:8000)

### CLI Mode

Run the script directly in your terminal:
```bash
python search_agent.py
```

## Configuration

You can adjust the `OLLAMA_URL` and `SEARXNG_URL` in `backend/main.py` and `search_agent.py` if your services are running on different ports.

## Demo

<img width="1919" height="713" alt="image" src="https://github.com/user-attachments/assets/40f66473-2369-4284-a03f-5ebf3cee3c24" />

<img width="1919" height="675" alt="image" src="https://github.com/user-attachments/assets/854f4dd8-be3f-4298-80ab-643517fca354" />

<img width="1914" height="551" alt="image" src="https://github.com/user-attachments/assets/64d85918-4df2-4aa4-bd0b-37ae3bbfa306" />

<img width="1919" height="784" alt="image" src="https://github.com/user-attachments/assets/77d6f661-2b10-4f2c-a552-e0a14943e5fc" />



## Author 

Souvik Das

## Last updated: 

31 December 2025 

## LinkedIn: 

https://www.linkedin.com/in/souvik-das-6ba904a2/
