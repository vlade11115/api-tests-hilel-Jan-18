import json

import responses
from rest_framework.test import APITransactionTestCase


class TestOrders(APITransactionTestCase):
    fixtures = []

    @responses.activate
    def test_new_order(self):
        body = {}
        responses.add(responses.POST, "https://api.monobank.ua/api/merchant/invoice/create", json={"pageUrl": "foo"})
        r = self.client.post("/api/orders/", json.dumps(body), content_type="application/json")
        assert r.status_code == 201
        assert r.json()["order"]["url"] == "foo"
