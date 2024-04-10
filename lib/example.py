from main import SlowAPI

slow_api = SlowAPI()

@slow_api.get()
def thisissonice(request, response):
    print(request)
    print(response)
    print('HELLO WORLD!')