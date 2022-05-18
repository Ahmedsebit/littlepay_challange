class ResponseError(Exception):
    
    def __init__(self, detail, status=None, error_code=None):
        super(ResponseError, self).__init__(detail)

        self.detail = detail
        self.status = status
        self.error_code = error_code
