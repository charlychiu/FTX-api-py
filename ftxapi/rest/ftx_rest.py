import asyncio
import aiohttp
import time
import json
import datetime

from ..utils.custom_logger import CustomLogger

class FtxRest:
    def __init__(self, API_KEY=None, API_SECRET=None, subaccount=None, host='https://ftx.com/api', loop=None,
             logLevel='INFO', parse_float=float, *args, **kwargs):
        self.loop = loop or asyncio.get_event_loop()
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET
        self.subaccount = subaccount
        self.host = host
        self.parse_float = parse_float
        self.logger = CustomLogger('FtxRest', logLevel=logLevel)
    
    def generate_auth_headers(self, path, method='POST', body=None):
        """
        Generate headers for a signed payload
        """
        import hmac
        ts = int(time.time() * 1000)
        signature_payload = f'{ts}{method}/api/{path}'.encode() # TODO optimize, get path directly
        if body != None:
            signature_payload += body.encode()
        signature = hmac.new(self.API_SECRET.encode(), signature_payload, 'sha256').hexdigest()
        
        prepared_headers = {
            "FTX-KEY": self.API_KEY,
            "FTX-SIGN": signature,
            "FTX-TS": str(ts),
        }
        
        if self.subaccount != None:
            prepared_headers['FTX-SUBACCOUNT'] = self.subaccount
        
        return prepared_headers
        
    async def fetch(self, endpoint, params=""):
        """
        Send a GET request to the ftx api

        @return reponse
        """
        url = '{}/{}{}'.format(self.host, endpoint, params)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                text = await resp.text()
                if resp.status != 200:
                    raise Exception('GET {} failed with status {} - {}'.format(url, resp.status, text))
                parsed = json.loads(text, parse_float=self.parse_float)
                return parsed

    async def fetch_auth(self, endpoint, params=""):
        url = '{}/{}{}'.format(self.host, endpoint, params)
        headers = self.generate_auth_headers(endpoint, 'GET')
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                text = await resp.text()
                if resp.status != 200:
                    raise Exception('GET {} failed with status {} - {}'.format(url, resp.status, text))
                parsed = json.loads(text, parse_float=self.parse_float)
                return parsed
            
   
    
    async def post(self, endpoint, data={}, params=""):
        """
        Send a pre-signed POST request to the ftx api

        @return response
        """
        url = '{}/{}'.format(self.host, endpoint)
        sData = json.dumps(data)
        print(sData)
        headers = self.generate_auth_headers(endpoint, 'POST', sData)
        async with aiohttp.ClientSession() as session:
            async with session.post(url + params, headers=headers, json=data) as resp:
                text = await resp.text()
                if resp.status < 200 or resp.status > 299:
                    raise Exception('POST {} failed with status {} - {}'.format(url, resp.status, text))
                parsed = json.loads(text, parse_float=self.parse_float)
                return parsed