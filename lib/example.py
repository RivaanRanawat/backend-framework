from main import SlowAPI

slow_api = SlowAPI()

@slow_api.get('/thisfortheboi')
def hello(request, response):
    print(request)
    response.send('Content is different', 200, 'OK')