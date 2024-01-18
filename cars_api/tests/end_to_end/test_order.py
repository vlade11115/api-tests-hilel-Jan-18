import os

import requests

API_URL = os.getenv("API_URL")


def test_new_order():
    body = {}
    r = requests.post(f"{API_URL}/api/orders/", json=body)
    assert r.status_code == 201
    assert r.json()["order"]["url"].startswith("https://pay.mbnk.biz")
