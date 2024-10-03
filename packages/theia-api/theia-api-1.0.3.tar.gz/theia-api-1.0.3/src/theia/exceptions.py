
from typing import Any
from theia.enums import ErrCode
from fastapi import HTTPException
from starlette import status


class TheiaException(HTTPException):

    def __init__(self, detail: Any = None,
                       status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
                       headers: dict = None,
                       is_trace: bool = False,
                       errcode: ErrCode = None):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.is_trace = is_trace
        self.code = status_code
        if isinstance(detail, str):
            self.detail = None
            self.message = detail
        else:
            self.detail = detail
            self.message = ErrCode.get_code_msg(self.code)

        if errcode:
            self.code = errcode.code
            self.message = self.message or errcode.msg

class AuthException(TheiaException):

    def __init__(self,
                 detail: Any = None,
                 status_code=status.HTTP_401_UNAUTHORIZED,
                 errcode: ErrCode = ErrCode.AUTH):
        TheiaException.__init__(self, detail=detail, status_code=status_code, errcode=errcode)


#  class MaxTimoutException()
