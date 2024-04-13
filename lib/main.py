from request import Request
from response import Response
from parse import parse
import types

# Has to be a callable so can be this:

# def app(environ, start_response):
#     print(environ)
#     response_body = b"Hello, World!"
#     status = "200 OK"
#     start_response(status, headers=[])
#     return iter([response_body])

# OR

class SlowAPI:
    def __init__(self, middlewares=[]):
        self.routes = dict()
        self.middleware_for_specific_routes = dict()
        self.middlewares = middlewares
    
    def __call__(self, environ, start_response):
        request = Request(environ)
        response = Response()

        for path, handler_dict in self.routes.items():
            for request_method, handler in handler_dict.items():
                # extracting {name}=Rivaan out of '/person/Rivaan'
                # - will give an empty object <Result () {}> if path matches
                # but theres no params
                # - will give a dictionary if path matches and theres params
                res = parse(path, request.path_info)
                
                if request.request_method == request_method and res is not None:
                    # run the global middleware
                    for middleware in self.middlewares:
                        if isinstance(middleware, types.FunctionType):
                            middleware(request)
                        else:
                            raise 'You can only pass functions as middleware!'
                    
                    # run the route specific middlewares
                    route_mw_list = self.middleware_for_specific_routes[path][request_method]

                    for mw in route_mw_list:
                        if isinstance(mw, types.FunctionType):
                            mw(request)
                        else:
                            raise 'You can only pass functions as middleware!'

                    handler(request, response, **res.named)
                    return response.as_wsgi(start_response)
        
        # return default response, error 404, route not found
        return response.as_wsgi(start_response)

    def get(self, path=None, middlewares=[]):
        def wrapper(handler):
            return self.route_common(handler, 'GET', path, middlewares)
        return wrapper
    
    # more routes
    def post(self, path=None, middlewares = []):
        def wrapper(handler):
            return self.route_common(handler, 'POST', path, middlewares)
        return wrapper
    
    def delete(self, path=None, middlewares = []):
        def wrapper(handler):
            return self.route_common(handler, 'DELETE', path, middlewares)
        return wrapper

    def route_common(self, handler, method_name, path, middlewares):
        # routing
        # {
        #   '/nice': {
        #       'GET': handler,
        #       'POST': handler2,
        #       'MIDDLEWARES': [fn, fn1, fn2]
        #   }
        # }
        path_name = path or f'/{handler.__name__}'
        if path_name not in self.routes:
            self.routes[path_name] = {}
            
        self.routes[path_name][method_name] = handler

        # middlewares
        # {
        #   '/nice': {
        #       'GET': [mw1],
        #       'POST': [mw2,mw3,mw4],
        #       'DELETE': []
        #   }
        # }
        if path_name not in self.middleware_for_specific_routes:
            self.middleware_for_specific_routes[path_name] = dict()
        
        self.middleware_for_specific_routes[path_name][method_name] = middlewares
        
        return handler
        