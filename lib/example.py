from main import SlowAPI


def print_something(request):
    print(request, '\nahsahsashashas')
    print('This is soo coooool!')

slow_api = SlowAPI()

@slow_api.get('/', middlewares=[print_something])
def hello(request, response):
    print(request)
    response.send('Content is different', 200, 'OK')

@slow_api.get('/thisfortheboi/{name}')
def hello(request, response, name):
    print(request)
    print(name)
    response.send('Content is different', 200, 'OK')

@slow_api.get('/thisfortheboi')
@slow_api.post('/thisfortheboi')
def hello3(request, response):
    # print(request.body)
    response.send('Content is different 23232', 200, 'OK')

@slow_api.route('/illcallthissomething')
class NewRoute:
    def get(request, response):
        response.send('this work!!!!', 203, 'SOMETHIGN')
        print('cool shit')

    def post(request, response):
        response.send('i send something new', 200, 'OKOOKOKOKOK')
        print('cool shi2323n232 3t')
    
    def pleaseignore(request, response):
        response.send('hihihihi')