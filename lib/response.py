class Response:
    def __init__(self, status_code=404, status='Missing Not Found', text='Route not found!'):
        self.status_code = int(status_code)
        self.status = status
        self.text = text
    
    def as_wsgi(self, start_response):
        status = f"{self.status_code} {self.status}"
        start_response(status, headers=[])
        return [f'{self.text}'.encode()]

    def send(self, text, status_code, status):
        self.text = text
        self.status_code = status_code
        self.status = status
        