from request import Request
from response import Response
from parse import parse
import types
import inspect

SUPPORTED_REQ_METHODS = {'GET', 'POST', 'DELETE'}

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
        
        print(self.routes)
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
    
    def route(self, path=None, middlewares=[]):
        def wrapper(handler):
            if isinstance(handler, type): # making sure it is only class
                # filtering out all the inbuilt dunder methods and variables
                class_members = inspect.getmembers(handler, 
                                                   lambda x: inspect.isfunction(x) 
                                                   and not (x.__name__.startswith('__') 
                                                            and x.__name__.endswith('__')))
                
                for fn_name, fn_handler in class_members:
                    fn_name = fn_name.upper()
                    if fn_name not in SUPPORTED_REQ_METHODS:
                        continue # can throw an error, ill just ignore that method
                    
                    # not returning self.route_common() cuz we are 
                    # looping over potentically multiple methods
                    # if we return, loop will end and other functions might
                    # not get registered
                    self.route_common(fn_handler, fn_name, f'/{(path or handler.__name__)}'.lower(), middlewares)
            else:
                raise '@route can only be used for classes'
            
            return handler
        return wrapper
        