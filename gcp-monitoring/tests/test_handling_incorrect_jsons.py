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
                "content": "a",
                "matcher": "MATCHES_REGEX"
            }
        ],
        "displayName": "test",
        "httpCheck": {
            "path": "/test",
            "port": 443,
            "requestMethod": "GET",
            "useSsl": True,
        },
        "monitoredResource": {
            "host": "google.com"
        }
    }
    resp = client.post('/check_key', json=body)
    assert resp.status_code < 400 or resp.status_code >= 500

def test_json_no_json(client):
    body = {
        "contentMatchers": [
            {
                "matcher": "MATCHES_REGEX"
            }
        ],
        "displayName": "test",
        "httpCheck": {
            "path": "/test",
            "port": 443,
            "requestMethod": "GET",
            "useSsl": True,
        },
        "monitoredResource": {
            "host": "google.com"
        }
    }
    resp = client.post('/check_key', data=body)
    assert resp.status_code == 400
    assert resp.get_json()['error'] == 'only JSON accepted'

def test_json_no_content(client):
    body = {
        "contentMatchers": [
            {
                "matcher": "MATCHES_REGEX"
            }
        ],
        "displayName": "test",
        "httpCheck": {
            "path": "/test",
            "port": 443,
            "requestMethod": "GET",
            "useSsl": True,
        },
        "monitoredResource": {
            "host": "google.com"
        }
    }
    resp = client.post('/check_key', json=body)
    assert resp.status_code == 400
    assert resp.get_json()['error'] == 'No necessary keys in JSON'

def test_json_no_matcher(client):
    body = {
        "contentMatchers": [
            {
                "matcher": "MATCHES_REGEX"
            }
        ],
        "displayName": "test",
        "httpCheck": {
            "path": "/test",
            "port": 443,
            "requestMethod": "GET",
            "useSsl": True,
        },
        "monitoredResource": {
            "host": "google.com"
        }
    }
    resp = client.post('/check_key', json=body)
    assert resp.status_code == 400
    assert resp.get_json()['error'] == 'No necessary keys in JSON'

def test_json_no_content_matchers(client):
    body = {
        "displayName": "test",
        "httpCheck": {
            "path": "/test",
            "port": 443,
            "requestMethod": "GET",
            "useSsl": True,
        },
        "monitoredResource": {
            "host": "google.com"
        }
    }
    resp = client.post('/check_key', json=body)
    assert resp.status_code == 400
    assert resp.get_json()['error'] == 'No necessary keys in JSON'

def test_json_no_path(client):
    body = {
        "contentMatchers": [
            {
                "content": "a",
                "matcher": "MATCHES_REGEX"
            }
        ],
        "displayName": "test",
        "httpCheck": {
            "port": 443,
            "requestMethod": "GET",
            "useSsl": True,
        },
        "monitoredResource": {
            "host": "google.com"
        }
    }
    resp = client.post('/check_key', json=body)
    assert resp.status_code == 400
    assert resp.get_json()['error'] == 'No necessary keys in JSON'

def test_json_no_port(client):
    body = {
        "contentMatchers": [
            {
                "content": "a",
                "matcher": "MATCHES_REGEX"
            }
        ],
        "displayName": "test",
        "httpCheck": {
            "path": "/test",
            "requestMethod": "GET",
            "useSsl": True,
        },
        "monitoredResource": {
            "host": "google.com"
        }
    }
    resp = client.post('/check_key', json=body)
    assert resp.status_code == 400
    assert resp.get_json()['error'] == 'No necessary keys in JSON'


def test_json_no_method(client):
    body = {
        "contentMatchers": [
            {
                "content": "a",
                "matcher": "MATCHES_REGEX"
            }
        ],
        "displayName": "test",
        "httpCheck": {
            "path": "/test",
            "port": 443,
            "useSsl": True,
        },
        "monitoredResource": {
            "host": "google.com"
        }
    }
    resp = client.post('/check_key', json=body)
    assert resp.status_code == 400
    assert resp.get_json()['error'] == 'No necessary keys in JSON'

def test_json_bad_method(client):
    body = {
        "contentMatchers": [
            {
                "content": "a",
                "matcher": "MATCHES_REGEX"
            }
        ],
        "displayName": "test",
        "httpCheck": {
            "path": "/test",
            "port": 443,
            "requestMethod": "POST",
            "useSsl": True,
        },
        "monitoredResource": {
            "host": "google.com"
        }
    }
    resp = client.post('/check_key', json=body)
    assert resp.status_code == 400
    assert resp.get_json()['error'] == 'invalid method, only GET supported'

def test_json_bad_matcher(client):
    body = {
        "contentMatchers": [
            {
                "content": "a",
                "matcher": "sadniuas"
            }
        ],
        "displayName": "test",
        "httpCheck": {
            "path": "/test",
            "port": 443,
            "requestMethod": "POST",
            "useSsl": True,
        },
        "monitoredResource": {
            "host": "google.com"
        }
    }
    resp = client.post('/check_key', json=body)
    assert resp.status_code == 400
    assert resp.get_json()['error'] == 'invalid matcher, only MATCHES_REGEX and MATCHES_STRING supported'

def test_json_no_use_ssl(client):
    body = {
        "contentMatchers": [
            {
                "content": "a",
                "matcher": "MATCHES_REGEX"
            }
        ],
        "displayName": "test",
        "httpCheck": {
            "path": "/test",
            "port": 443,
            "requestMethod": "GET"
        },
        "monitoredResource": {
            "host": "google.com"
        }
    }
    resp = client.post('/check_key', json=body)
    assert resp.status_code == 400
    assert resp.get_json()['error'] == 'No necessary keys in JSON'

def test_json_no_host(client):
    body = {
        "contentMatchers": [
            {
                "content": "a",
                "matcher": "MATCHES_REGEX"
            }
        ],
        "displayName": "test",
        "httpCheck": {
            "path": "/test",
            "port": 443,
            "requestMethod": "GET",
            "useSsl": True,
        },
        "monitoredResource": {
            
        }
    }
    resp = client.post('/check_key', json=body)
    assert resp.status_code == 400
    assert resp.get_json()['error'] == 'No necessary keys in JSON'

