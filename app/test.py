#testing the ollama (llama2:latest) model connection
import requests

OLLAMA_URL = "http://localhost:11434"

def test_connection():
    try:
        # Verify server status
        response = requests.get(f"{OLLAMA_URL}")
        if response.status_code == 200:
            print("✅ Ollama server is ready on localhost:11434")
        else:
            print(f"⚠️ Ollama server is ready but with code: {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot connect to Ollama server with Exception: {e}")

test_connection()