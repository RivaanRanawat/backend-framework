from request import Request
from response import Response
from parse import parse

# Has to be a callable so can be this:

# def app(environ, start_response):
#     print(environ)
#     response_body = b"Hello, World!"
#     status = "200 OK"
#     start_response(status, headers=[])
#     return iter([response_body])

# OR

class SlowAPI:
    def __init__(self):
        self.routes = dict()
    
    def __call__(self, environ, start_response):
        request = Request(environ)
        response = Response()

        for path, handler_dict in self.routes.items():
            for request_method, handler in handler_dict.items():
                # extracting query
                req_queries = request.query_string.split('&')
                
                for query in req_queries:
                    query_key, query_val = query.split('=')
                    request.queries[query_key] = query_val

                # extracting {name}=Rivaan out of '/person/Rivaan'
                # - will give an empty object <Result () {}> if path matches
                # but theres no params
                # - will give a dictionary if path matches and theres params
                res = parse(path, request.path_info)
                
                if request.request_method == request_method and res is not None:
                    handler(request, response, **res.named)
                    return response.as_wsgi(start_response)
        
        # return default response, error 404, route not found
        return response.as_wsgi(start_response)

    def get(self, path=None):
        def wrapper(handler):
            return self.route_common(handler, 'GET', path)
        return wrapper

    def route_common(self, handler, method_name, path):
        # {
        #   '/nice': {
        #       'GET': handler,
        #       'POST': handler2,
        #   }
        # }
        path_name = path or f'/{handler.__name__}'
        if path_name not in self.routes:
            self.routes[path_name] = {}
            
        self.routes[path_name][method_name] = handler
        
        return handler
        