from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, \
                  abort, jsonify
import re
import random
import string
import urllib
import requests

mod = Blueprint('core', __name__)


@mod.route('/')
def index():
  return (render_template('core/index.html', nav='readme'))

@mod.route('/uptime_check', methods=['GET'])
def uptime_check():
  return (render_template('core/uptime_check.html', nav='uptime_check'))


@mod.route('/uptime_check', methods=['POST'])
def check_key():
  if request.is_json:
    req = request.get_json()
    try:
      content_matchers = req['contentMatchers'][0]
      content = content_matchers['content']
      matcher = content_matchers['matcher']
      if matcher != 'MATCHES_REGEX' and matcher != 'MATCHES_STRING':
        return jsonify({'error': 'invalid matcher, only MATCHES_REGEX and MATCHES_STRING supported'}), 400
      http_check = req['httpCheck']
      path = http_check['path']
      port = http_check['port']
      request_method = http_check['requestMethod']
      if request_method != 'GET':
        return jsonify({'error': 'invalid method, only GET supported'}), 400
      use_ssl = http_check['useSsl']
      headers = http_check.get('headers', {})

      monitoredResource = req['monitoredResource']
      host = monitoredResource['host']
    except (KeyError, IndexError) as e:
      return jsonify({"error":'No necessary keys in JSON'}), 400

    
    result = dict()
    protocol = 'https' if use_ssl else 'http'
    if path.startswith('/'):
      path = path[1:]
    url = f'{protocol}://{host}:{port}/{path}'
    try:
      resp = requests.get(url, headers=headers)
    except requests.exceptions.RequestException:
      return jsonify({'error': 'There was an exception during sending the request. Your host might be down.'}), 400

    if matcher == 'MATCHES_STRING':
      check_passed = content in resp.text
    elif matcher == 'MATCHES_REGEX':
      check_passed = re.search(content, resp.text) is not None



    result = {
      "uptimeCheckResults": [
        {
          "checkPassed": check_passed,
          "httpStatus": resp.status_code,
          "requestLatency": resp.elapsed.total_seconds()
        }
      ]
    }
    return jsonify(result)
  else:
    return jsonify({'error': 'only JSON accepted'}), 400