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
        response = Response(404, 'Error Not Found')
        
        return response.as_wsgi(start_response)

    def get(self):
        def wrapper(handler):
            path_name = handler.__name__
            self.routes[path_name] = handler
            return handler

        return wrapper