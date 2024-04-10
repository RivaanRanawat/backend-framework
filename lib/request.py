class Request:
    def __init__(self, environ):
        print(environ)
        for key, value in environ.items():
            setattr(self, key.replace(".", "_").lower(), value)