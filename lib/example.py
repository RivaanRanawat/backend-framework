from main import SlowAPI

slow_api = SlowAPI()

@slow_api.get()
def thisissonice(request, response):
    print(request)
    response.status_code = 200
    response.status = 'OK'
    response.text = 'This is alright!'