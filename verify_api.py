import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    try:
        r = requests.get("http://localhost:8000/health/")
        print(f"Health Check: {r.status_code} - {r.json()}")
    except Exception as e:
        print(f"Health Check Failed: {e}")

def test_chat():
    question = "What are the top 5 complaint types?"
    try:
        r = requests.post(f"{BASE_URL}/chat/", json={"message": question})
        if r.status_code == 200:
            print(f"Chat Response: {r.json()}")
        else:
            print(f"Chat Failed: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Chat Request Error: {e}")

if __name__ == "__main__":
    test_health()
    test_chat()
