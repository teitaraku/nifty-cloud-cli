import os
import configparser
import requests
from datetime import datetime
import hmac, hashlib, base64
from itertools import zip_longest

class NiftyCloudRequest():
    def __init__(self):
        config = configparser.SafeConfigParser()
        config.read('./config.ini')
        self.endpoint = os.getenv("ENDPOINT", config.get('common', 'ENDPOINT'))
        self.signature_version = os.getenv("SIGNATURE_VERSION", config.get('common', 'SIGNATURE_VERSION'))
        self.access_key = os.getenv("ACCESS_KEY", config.get('user', 'ACCESS_KEY'))
        self.secret_key = os.getenv("SECRET_ACCESS_KEY", config.get('user', 'SECRET_ACCESS_KEY'))

    def request(self, payload):
        request_url = self.endpoint# + '?Action=' + self.action
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%dT%H:%M:%S") + ".%03dZ" % (now.microsecond // 1000)

        payload.update({'AccessKeyId': self.access_key})
        payload.update({'SignatureVersion': self.signature_version})
        payload.update({'Timestamp': timestamp})

        if self.signature_version is '0':
            signature = self.__calc_version0(payload)
        elif self.signature_version is '1':
            signature = self.__calc_version1(payload)

        payload.update({'Signature': signature})

        response = requests.get(request_url, params=payload)
        print(response.url)
        return response

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
