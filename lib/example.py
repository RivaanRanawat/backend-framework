from main import SlowAPI

slow_api = SlowAPI()

@slow_api.get()
def thisissonice(request, response):
    print(request)
    response.status_code = 404
    response.status = 'Missing Not Found'
    response.text = 'Yo wassup my man'