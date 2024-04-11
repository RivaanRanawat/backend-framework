from collections import defaultdict

class Request:
    def __init__(self, environ):
        self.queries = defaultdict()
        print(environ)
        for key, value in environ.items():
            setattr(self, key.replace(".", "_").lower(), value)