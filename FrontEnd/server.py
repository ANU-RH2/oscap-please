from wsgiref.simple_server import make_server
from mako.template import Template

def renderTemplate(file):
    template = Template(filename = file, output_encoding = 'ascii')
    return template.render()

def app(environ, start_response):
    start_response('200 OK', [])
    path = environ['PATH_INFO'][1:]     # strip the leading slash
    return '' if path == 'favicon.ico' else [renderTemplate(path)]  # ignore request for favicon

if __name__ == '__main__':

    ##TODO: Allow user to specify output file name, add prompt if file already exists
    f = open('write2me.html', 'w+')
    template = Template(filename = 'date.mako', output_encoding = 'ascii')
    output = str(template.render())
    output = output.replace("\\r","").replace("\\n","").replace("b'","").replace("\\'","'")
    f.write(output)
    f.close()

    server = make_server('127.0.0.1', 8080, app)
    server.serve_forever()
