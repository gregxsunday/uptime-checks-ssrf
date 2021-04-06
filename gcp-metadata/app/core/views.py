from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, \
                  abort, jsonify, make_response
import random
import string
from os import environ

mod = Blueprint('core', __name__)


key_charset = string.ascii_letters + string.digits + '-._'
key_length = int(environ.get('KEY_LENGTH', 64)) # real value 213
number_of_instances = int(environ.get('NO_INSTANCES', 4)) # real value 54
print(key_length, number_of_instances)
keys = [''.join(random.choices(key_charset, k=key_length)) for _ in range(number_of_instances)]


def resp_with_headers(body, request):
  if 'Metadata-Flavor' not in request.headers or request.headers['Metadata-Flavor'] != 'Google':
    return 'Missing Metadata-Flavor:Google header', 403
  resp = make_response(body)
  resp.headers["Content-Type"] = 'application/text'
  resp.headers["Metadata-Flavor"] = 'Google'
  resp.headers["Server"] = 'Metadata Server for VM'
  return resp

@mod.route('/')
def index():
  body = '''computeMetadata/'''
  return resp_with_headers(body, request)

@mod.route('/computeMetadata/')
def computeMetadata():
  body = '''v1/'''
  return resp_with_headers(body, request)

@mod.route('/computeMetadata/v1/')
def v1():
  body = '''instance/'''
  return resp_with_headers(body, request)


@mod.route('/computeMetadata/v1/instance/')
def instance():
  body = '''cpu-platform
service-accounts/'''
  return resp_with_headers(body, request)

@mod.route('/computeMetadata/v1/instance/cpu-platform')
def cpu_platform():
  body = '''Intel Broadwell'''
  return resp_with_headers(body, request)

@mod.route('/computeMetadata/v1/instance/service-accounts/')
def service_accounts():
  body = '''default/'''
  return resp_with_headers(body, request)

@mod.route('/computeMetadata/v1/instance/service-accounts/default/')
def default():
  body = '''token
scopes'''
  return resp_with_headers(body, request)

@mod.route('/computeMetadata/v1/instance/service-accounts/default/token')
def token():
  key = random.choice(keys)
  body = r'{"access_token":"' + key + '","expires_in":3600,"token_type":"Bearer"}'
  return resp_with_headers(body, request) 


@mod.route('/computeMetadata/v1/instance/service-accounts/default/scopes')
def scopes():
  body = '''https://www.googleapis.com/auth/devstorage.read_only
https://www.googleapis.com/auth/logging.write
https://www.googleapis.com/auth/monitoring.write
https://www.googleapis.com/auth/servicecontrol
https://www.googleapis.com/auth/service.management.readonly
https://www.googleapis.com/auth/trace.append'''
  return resp_with_headers(body, request) 
  