from collections import defaultdict

class Request:
    def __init__(self, environ):
        print(environ)
        self.queries = defaultdict()
        for key, value in environ.items():
            setattr(self, key.replace(".", "_").lower(), value)
        

        # if you only want self.body to exist when
        # the request method is not GET
        if self.request_method != 'GET':
            self.body = environ['wsgi.input'].read().decode()
        
        # extracting query
        if self.query_string:
            req_queries = self.query_string.split('&')
            
            for query in req_queries:
                query_key, query_val = query.split('=')
                self.queries[query_key] = query_val