from fastapi.testclient import TestClient
from main import app
from parse import ParseSii
from unittest.mock import patch
from exceptions import NotFound
import pytest


class TestService:

    @pytest.fixture()
    def client(self):
        with TestClient(app) as test_client:
            yield test_client

    def test_main_service(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"server": "Works"}

    def test_uf_service_not_valid_date(self, client):
        response = client.get("/uf/20-13-2013")
        assert response.status_code == 400
        assert response.json() == {"detail": "date format is incorrect, try dd-mm-yyy"}

    def test_uf_service_minimum_date(self, client):
        response = client.get("/uf/20-12-2012")
        assert response.status_code == 400
        assert response.json() == {"detail": "The minimum date that can be consulted is 01-01-2013"}

    def test_uf_service_date_out_range(self, client):
        response = client.get("/uf/31-02-2013")
        assert response.status_code == 400
        assert response.json() == {"detail": "day is out of range for month"}

    @patch.object(ParseSii, "get_sii_information")
    @patch("redis.Redis.get")
    def test_uf_service_not_found_value_date_1(self, mock_redis_get, mock_parse, client):
        mock_parse.side_effect = NotFound('Uf from specific date does not exists')
        mock_redis_get.return_value = None
        response = client.get("/uf/01-05-2023")
        assert response.status_code == 400
        assert response.json() == {"detail": "Uf from specific date does not exists"}

    @patch.object(ParseSii, "get_uf_sii")
    @patch("redis.Redis.get")
    def test_uf_service_not_found_value_date_2(self, mock_redis_get, mock_parse, client):
        mock_parse.side_effect = NotFound('Uf from specific date does not exists')
        mock_redis_get.return_value = None
        response = client.get("/uf/01-05-2024")
        assert response.status_code == 400
        assert response.json() == {"detail": "Uf from specific date does not exists"}

    @patch.object(ParseSii, "parse_html")
    @patch("redis.Redis.get")
    def test_uf_service_exception_parse_html(self, mock_redis_get, mock_parse, client):
        mock_parse.side_effect = Exception('ERROR cannot be parser this content')
        mock_redis_get.return_value = None
        response = client.get("/uf/01-05-2023")
        assert response.status_code == 500
        assert response.json() == {"detail": "ERROR cannot be parser this content"}

    @patch.object(ParseSii, "get_uf_sii")
    @patch("redis.Redis.get")
    def test_uf_service_price_does_not_exist(self, mock_redis_get, mock_parse, client):
        mock_parse.return_value = None
        mock_redis_get.return_value = None
        response = client.get("/uf/01-05-2024")
        assert response.status_code == 400
        assert response.json() == {"detail": "Uf from specific date does not exists"}

    @patch.object(ParseSii, "get_uf_sii")
    @patch("redis.Redis.get")
    @patch("redis.Redis.setex")
    def test_uf_service_successfully(self, mock_redis_set, mock_redis_get, mock_parse, client):
        mock_parse.return_value = 35851.62
        mock_redis_get.return_value = None
        mock_redis_set.return_value = {"01-05-2023": 35851.62}
        response = client.get("/uf/01-05-2023")
        assert response.status_code == 200
        assert response.json() == {"uf": 35851.62}

    @patch("redis.Redis.get")
    def test_uf_service_successfully_cache(self, mock_redis_get, client):
        mock_redis_get.return_value = "35864.7"
        response = client.get("/uf/02-05-2023")
        assert response.status_code == 200
        assert response.json() == {"uf": 35864.7}
