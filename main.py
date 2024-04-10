
# Has to be a callable so can be this:

# def app(environ, start_response):
#     print(environ)
#     response_body = b"Hello, World!"
#     status = "200 OK"
#     start_response(status, headers=[])
#     return iter([response_body])


# OR

class SlowAPI:
    def __call__(self, environ, start_response):
        print(environ)
        response_body = b"Hello, World!"
        status = "200 OK"
        start_response(status, headers=[])
        return [response_body]