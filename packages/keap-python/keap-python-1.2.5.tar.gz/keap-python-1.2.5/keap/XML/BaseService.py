from keap import Keap
from keap.exceptions import KeapXMLRPCException

try:
    from xmlrpclib import ServerProxy, Error
except ImportError:
    from xmlrpc.client import ServerProxy, Error


class BaseService:
    xmlrpc_url = 'https://api.infusionsoft.com/crm/xmlrpc/v1'
    _service = None
    client = None

    def __init__(self, keap: Keap):
        self.keap = keap
        self.get_xmlrpc_client()

    def get_xmlrpc_client(self):
        if not self.keap.token.access_token:
            raise Exception(f"No token set for client {self.keap.app_name}")
        uri = f"{self.xmlrpc_url}?access_token={self.keap.token.access_token}"
        self.client = ServerProxy(uri, use_datetime=self.keap.api_settings.USE_DATETIME,
                                  allow_none=self.keap.api_settings.ALLOW_NONE)
        self.client.error = Error
        return self.client

    def __getattr__(self, method):
        def function(*args):
            return self.call(method, *args)

        return function

    @property
    def service(self):
        return self._service if self._service else self.__class__.__name__

    def call(self, method, *args):
        call = getattr(self.client, f"{self.service}.{method}")
        try:
            return call(self.keap.token.access_token, *args)
        except self.client.error as e:
            e_dict = e.__dict__
            if 'faultCode' in e_dict:
                raise KeapXMLRPCException(None, e.faultCode, e.faultString, None)
            else:
                if 'url' in e_dict:
                    url = e_dict['url']
                else:
                    url = None
                if 'errcode' in e_dict:
                    errcode = e_dict['errcode']
                else:
                    errcode = None
                if 'errmsg' in e_dict:
                    errmsg = e_dict['errmsg']
                else:
                    errmsg = None
                if 'headers' in e_dict:
                    headers = e_dict['headers']
                else:
                    headers = []
                raise KeapXMLRPCException(url, errcode, errmsg, headers)

    def server(self):
        return self.client
