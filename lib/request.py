from collections import defaultdict

class Request:
    def __init__(self, environ):
        print(environ)
        self.queries = defaultdict()
        for key, value in environ.items():
            setattr(self, key.replace(".", "_").lower(), value)
        
        # extracting query
        req_queries = self.query_string.split('&')
        
        for query in req_queries:
            query_key, query_val = query.split('=')
            self.queries[query_key] = query_val
        
        self.body = environ['wsgi.input'].read().decode()