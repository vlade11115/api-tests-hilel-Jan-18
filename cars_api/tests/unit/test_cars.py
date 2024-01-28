import json

from rest_framework.test import APITransactionTestCase


class TestCarsAPI(APITransactionTestCase):
    fixtures = ["cars"]

    def test_cars_list(self):
        response = self.client.get("/api/cars/")
        assert response.status_code == 200
        assert response.json()["results"] == [
            {
                "id": 1,
                "year": 2010,
                "car_type": {"id": 1, "price": 42, "brand": "BMW", "name": "X5"},
                "color": "Red",
            }
        ]

    def test_create_car_bad_request(self):
        r = self.client.post("/api/cars/", {})
        assert r.status_code == 400

    def test_create_car(self):
        request_body = {"year": 2015, "car_type": 1, "color": "Green"}
        r = self.client.post("/api/cars/", json.dumps(request_body), content_type="application/json")
        assert r.status_code == 201
        assert r.json() == {
            "car": {
                "id": 2,
                "year": 2015,
                "car_type": {"brand": "BMW", "id": 1, "name": "X5", "price": 42},
                "color": "Green",
            }
        }

    def test_create_car_not_found_car_type(self):
        r = self.client.post(
            "/api/cars/", json.dumps({"year": 2015, "car_type": 100, "color": "Green"}), content_type="application/json"
        )
        assert r.status_code == 404
