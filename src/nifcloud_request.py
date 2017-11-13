import os
import configparser
import requests
from datetime import datetime
import hmac, hashlib, base64
from itertools import zip_longest
from py_nifcloud.computing_client import ComputingClient

class NifCloudRequest():
    def __init__(self):
        config = configparser.SafeConfigParser()
        config.read('./config.ini')
        self.endpoint = os.getenv("ENDPOINT", config.get('common', 'ENDPOINT'))
        self.signature_version = os.getenv("SIGNATURE_VERSION", config.get('common', 'SIGNATURE_VERSION'))
        self.access_key = os.getenv("ACCESS_KEY", config.get('user', 'ACCESS_KEY'))
        self.secret_key = os.getenv("SECRET_ACCESS_KEY", config.get('user', 'SECRET_ACCESS_KEY'))
        self.client = ComputingClient(region_name="jp-east-1", access_key_id=self.access_key, secret_access_key=self.secret_key)

    def request(self, payload):
        return self.client.request(method="GET", query=payload)

    def __calc_version0(self, payload):
        action = payload['Action']
        timestamp = payload['Timestamp']
        cannonical_string = action + timestamp
        digester = hmac.new(bytes(self.secret_key, 'UTF-8'), bytes(cannonical_string, 'UTF-8'), hashlib.sha1)
        return base64.b64encode(digester.digest())

    def __calc_version1(self, payload):
        sorted_payload = sorted(payload.items())
        cannonical_string = ''
        for k, v in sorted_payload:
            cannonical_string = cannonical_string + k + v
        digester = hmac.new(bytes(self.secret_key, 'UTF-8'), bytes(cannonical_string, 'UTF-8'), hashlib.sha1)
        return base64.b64encode(digester.digest())
