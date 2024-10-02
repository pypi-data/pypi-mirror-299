class KeapException(Exception):
    pass


class KeapForbiddenException(KeapException):
    pass


class KeapUnauthorizedException(KeapException):
    pass


class KeapTokenExpiredException(KeapException):
    pass

class KeapXMLRPCException(KeapException):
    def __init__(self, url=None, errcode=None, errmsg=None, headers=None):
        self.url = url
        self.errcode = errcode
        self.errmsg = errmsg
        self.headers = headers
        super().__init__(f"XML-RPC Protocol Error {errcode}: {errmsg}")

    def __str__(self):
        return (f"KeapXMLRPCException: URL: {self.url}, Error Code: {self.errcode}, "
                f"Error Message: {self.errmsg}, Headers: {self.headers}")