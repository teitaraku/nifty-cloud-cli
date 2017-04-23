import os
import configparser
import requests
from datetime import datetime
import hmac, hashlib, base64
from itertools import zip_longest

class NiftyCloudRequest():
    def __init__(self, action):
        self.action = action
        config = configparser.SafeConfigParser()
        config.read('../config.ini')
        self.endpoint = os.getenv("ENDPOINT", config.get('common', 'ENDPOINT'))
        self.access_key = os.getenv("ACCESS_KEY", config.get('user', 'ACCESS_KEY'))
        self.secret_key = os.getenv("SECRET_ACCESS_KEY", config.get('user', 'SECRET_ACCESS_KEY'))

    def request(self, payload):
        request_url = self.endpoint + '?Action=' + self.action
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%dT%H:%M:%S") + ".%03dZ" % (now.microsecond // 1000)
        string_to_sign = self.action + timestamp
        digester = hmac.new(bytes(self.secret_key, 'UTF-8'), bytes(string_to_sign, 'UTF-8'), hashlib.sha1)
        signature = base64.b64encode(digester.digest())
        payload.update({'AccessKeyId': self.access_key})
        payload.update({'SignatureVersion': '0'})
        payload.update({'Signature': signature})
        payload.update({'Timestamp': timestamp})

        return requests.get(request_url, params=payload)
