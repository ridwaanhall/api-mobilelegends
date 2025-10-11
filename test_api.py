"""Quick test to verify FastAPI endpoints"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(name, url, expected_status=200):
    try:
        response = requests.get(url)
        status = "✅" if response.status_code == expected_status else "❌"
        print(f"{status} {name}: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict):
                print(f"   Keys: {list(data.keys())[:5]}")
        return response.status_code == expected_status
    except Exception as e:
        print(f"❌ {name}: Error - {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing FastAPI Endpoints\n")
    
    tests = [
        ("Health Check", f"{BASE_URL}/health"),
        ("API Root", f"{BASE_URL}/api/"),
        ("Hero List (EN)", f"{BASE_URL}/api/hero-list/"),
        ("Hero List (RU)", f"{BASE_URL}/api/hero-list/?lang=ru"),
        ("Win Rate Calc", f"{BASE_URL}/api/win-rate/?match-now=100&wr-now=50&wr-future=75"),
        ("Docs Page", f"{BASE_URL}/docs"),
    ]
    
    results = []
    for name, url in tests:
        result = test_endpoint(name, url)
        results.append(result)
    
    print(f"\nResults: {sum(results)}/{len(results)} tests passed")
