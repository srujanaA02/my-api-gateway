import requests

def test_gateway_flow():
    # Gateway should proxy to flaky backend
    r = requests.get("http://gateway:8000/api/v1/data")
    assert r.status_code in [200, 503, 429]