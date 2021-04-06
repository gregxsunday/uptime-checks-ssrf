import pytest
import unittest

from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_valid_json_with_regex(client):
    body = {
        "contentMatchers": [
            {
                "content": "",
                "matcher": "MATCHES_REGEX"
            }
        ],
        "displayName": "test",
        "httpCheck": {
            "path": "/",
            "port": 443,
            "requestMethod": "GET",
            "useSsl": True,
        },
        "monitoredResource": {
            "host": "google.com"
        }
    }
    resp = client.post('/check_key', json=body)
    assert resp.status_code == 200
    uptimeCheckResults = resp.get_json()['uptimeCheckResults'][0]
    assert uptimeCheckResults['checkPassed'] == True
    assert uptimeCheckResults['httpStatus'] == 200


def test_valid_json_with_string(client):
    body = {
        "contentMatchers": [
            {
                "content": "",
                "matcher": "MATCHES_REGEX"
            }
        ],
        "displayName": "test",
        "httpCheck": {
            "path": "/",
            "port": 443,
            "requestMethod": "GET",
            "useSsl": True,
        },
        "monitoredResource": {
            "host": "google.com"
        }
    }
    resp = client.post('/check_key', json=body)
    assert resp.status_code == 200
    uptimeCheckResults = resp.get_json()['uptimeCheckResults'][0]
    assert uptimeCheckResults['checkPassed'] == True
    assert uptimeCheckResults['httpStatus'] == 200

def test_valid_json_with_json_placeholder_string(client):
    # https://jsonplaceholder.typicode.com/posts
    body = {
        "contentMatchers": [
            {
                "content": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
                "matcher": "MATCHES_STRING"
            }
        ],
        "displayName": "test",
        "httpCheck": {
            "path": "/posts",
            "port": 443,
            "requestMethod": "GET",
            "useSsl": True,
        },
        "monitoredResource": {
            "host": "jsonplaceholder.typicode.com"
        }
    }
    resp = client.post('/check_key', json=body)
    assert resp.status_code == 200
    uptimeCheckResults = resp.get_json()['uptimeCheckResults'][0]
    assert uptimeCheckResults['checkPassed'] == True
    assert uptimeCheckResults['httpStatus'] == 200

def test_valid_json_with_json_placeholder_regex(client):
    # https://jsonplaceholder.typicode.com/posts
    body = {
        "contentMatchers": [
            {
                "content": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
                "matcher": "MATCHES_REGEX"
            }
        ],
        "displayName": "test",
        "httpCheck": {
            "path": "/posts",
            "port": 443,
            "requestMethod": "GET",
            "useSsl": True,
        },
        "monitoredResource": {
            "host": "jsonplaceholder.typicode.com"
        }
    }
    resp = client.post('/check_key', json=body)
    assert resp.status_code == 200
    uptimeCheckResults = resp.get_json()['uptimeCheckResults'][0]
    assert uptimeCheckResults['checkPassed'] == True
    assert uptimeCheckResults['httpStatus'] == 200

def test_valid_json_with_json_placeholder_regex_with_dot(client):
    # https://jsonplaceholder.typicode.com/posts
    body = {
        "contentMatchers": [
            {
                "content": "sunt aut fac.re repellat provident occaecati excepturi optio reprehenderit",
                "matcher": "MATCHES_REGEX"
            }
        ],
        "displayName": "test",
        "httpCheck": {
            "path": "/posts",
            "port": 443,
            "requestMethod": "GET",
            "useSsl": True,
        },
        "monitoredResource": {
            "host": "jsonplaceholder.typicode.com"
        }
    }
    resp = client.post('/check_key', json=body)
    assert resp.status_code == 200
    uptimeCheckResults = resp.get_json()['uptimeCheckResults'][0]
    assert uptimeCheckResults['checkPassed'] == True
    assert uptimeCheckResults['httpStatus'] == 200

def test_valid_json_with_json_placeholder_regex_with_dot_star(client):
    # https://jsonplaceholder.typicode.com/posts
    body = {
        "contentMatchers": [
            {
                "content": "sunt aut fac.*e repellat provident occaecati excepturi optio reprehenderit",
                "matcher": "MATCHES_REGEX"
            }
        ],
        "displayName": "test",
        "httpCheck": {
            "path": "/posts",
            "port": 443,
            "requestMethod": "GET",
            "useSsl": True,
        },
        "monitoredResource": {
            "host": "jsonplaceholder.typicode.com"
        }
    }
    resp = client.post('/check_key', json=body)
    assert resp.status_code == 200
    uptimeCheckResults = resp.get_json()['uptimeCheckResults'][0]
    assert uptimeCheckResults['checkPassed'] == True
    assert uptimeCheckResults['httpStatus'] == 200

def test_valid_json_with_json_placeholder_regex_with_range(client):
    # https://jsonplaceholder.typicode.com/posts
    body = {
        "contentMatchers": [
            {
                "content": "sunt aut fac[a-z]re repellat provident occaecati excepturi optio reprehenderit",
                "matcher": "MATCHES_REGEX"
            }
        ],
        "displayName": "test",
        "httpCheck": {
            "path": "/posts",
            "port": 443,
            "requestMethod": "GET",
            "useSsl": True,
        },
        "monitoredResource": {
            "host": "jsonplaceholder.typicode.com"
        }
    }
    resp = client.post('/check_key', json=body)
    assert resp.status_code == 200
    uptimeCheckResults = resp.get_json()['uptimeCheckResults'][0]
    assert uptimeCheckResults['checkPassed'] == True
    assert uptimeCheckResults['httpStatus'] == 200

def test_valid_json_with_json_placeholder_regex_with_range_negative(client):
    # https://jsonplaceholder.typicode.com/posts
    body = {
        "contentMatchers": [
            {
                "content": "sunt aut fac[^A-Z]re repellat provident occaecati excepturi optio reprehenderit",
                "matcher": "MATCHES_REGEX"
            }
        ],
        "displayName": "test",
        "httpCheck": {
            "path": "/posts",
            "port": 443,
            "requestMethod": "GET",
            "useSsl": True,
        },
        "monitoredResource": {
            "host": "jsonplaceholder.typicode.com"
        }
    }
    resp = client.post('/check_key', json=body)
    assert resp.status_code == 200
    uptimeCheckResults = resp.get_json()['uptimeCheckResults'][0]
    assert uptimeCheckResults['checkPassed'] == True
    assert uptimeCheckResults['httpStatus'] == 200