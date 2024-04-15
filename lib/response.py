import re
from pypugjs import simple_convert

class Response:
    def __init__(self, status_code=404, status='Missing Not Found', 
                 text='Route not found!', template_extension = 'html'):
        self.status_code = int(status_code)
        self.status = status
        self.text = text
        self.headers = []

        # taking this from init so that response can be modified
        # in the middleware
        self.template_extension = template_extension.lower()
    
    def as_wsgi(self, start_response):
        status = f"{self.status_code} {self.status}"
        start_response(status, headers=self.headers)
        return [self.text.encode()]

    def send(self, text, status_code, status):
        self.text = text
        self.status_code = status_code
        self.status = status
    
    # template engine
    # support for only simple HTML and PUG files
    # for example, if you add a list and ul to pug file
    # it work (show it)
    # you can work on that yourself using regex.
    def render(self, template_name, context={}):
        path = f"{template_name}.{self.template_extension}"
        try:
            fp = open(path, 'r')
            template = fp.read()
        except:
            raise f"{template_name}.{self.template_extension} file not found"
        
        if self.template_extension == 'html':
            # Substitute placeholders with context values
            for key, value in context.items():
                template = re.sub(r'{{\s*' + re.escape(key) + r'\s*}}', str(value), template)
        else:
            for key, value in context.items():
                template = re.sub(r'\#\{' + key + r'\}', str(value), template)
            
            template = simple_convert(template) # returns html
        
        self.headers.append(('Content-Type', 'text/html'))
        self.text = template
        self.status_code = 200
        self.status = 'OK'
        