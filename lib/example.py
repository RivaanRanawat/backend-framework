from main import SlowAPI

slow_api = SlowAPI()

@slow_api.get('/')
def hello(request, response):
    print(request)
    response.send('Content is different', 200, 'OK')

@slow_api.get('/thisfortheboi/{name}')
def hello(request, response, name):
    print(request)
    print(name)
    response.send('Content is different', 200, 'OK')


@slow_api.get('/thisfortheboi')
def hello3(request, response):
    print(request)
    response.send('Content is different 23232', 200, 'OK')