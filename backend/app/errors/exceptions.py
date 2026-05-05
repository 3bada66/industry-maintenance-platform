from fastapi import HTTPException


class ErrorCodeException(HTTPException):
    def __init__(self, status_code: int, error_code: str):
        self.error_code = error_code
        super().__init__(status_code=status_code, detail=error_code)
