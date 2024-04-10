from request import Request
from response import Response

# Has to be a callable so can be this:

# def app(environ, start_response):
#     print(environ)
#     response_body = b"Hello, World!"
#     status = "200 OK"
#     start_response(status, headers=[])
#     return iter([response_body])

# OR

# Intended route:
# @api.get() OR @api.post() and hello will be the name of the route
# def hello(self, request, response):
#   pass

class SlowAPI:
    def __init__(self):
        self.routes = dict()
    
    def __call__(self, environ, start_response):
        request = Request(environ)
        print(request.path_info)
        response = Response()

        for path, handler_dict in self.routes.items():
            for request_method, handler in handler_dict.items():
                if request.request_method == request_method and path == request.path_info:
                    handler(request, response)
                    return response.as_wsgi(start_response)
        
        return response.as_wsgi(start_response)

    def get(self):
        def wrapper(handler):
            return self.route_common(handler, 'GET')
        return wrapper

    def route_common(self, handler, method_name):
        # {
        #   '/nice': {
        #       'GET': handler
        #   }
        # }
        path_name = f'/{handler.__name__}'
        if path_name not in self.routes:
            self.routes[path_name] = {}
            
        self.routes[path_name][method_name] = handler
        
        return handler
        