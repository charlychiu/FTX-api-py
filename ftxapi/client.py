"""
This module exposes the core ftx clients which includes both a rest interface client
"""

from .rest.ftx_rest import FtxRest

REST_HOST = 'https://ftx.com/api'

class Client:
    """
    The ftx client exposes rest objects
    """

    def __init__(self, API_KEY=None, API_SECRET=None, rest_host=REST_HOST, logLevel='INFO', *args, **kwargs):
        self.rest = FtxRest(API_KEY=API_KEY, API_SECRET=API_SECRET, host=rest_host, logLevel=logLevel, *args, **kwargs)