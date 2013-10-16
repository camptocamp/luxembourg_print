from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

from routing import pdf

def hello_world(request):
    steps = request.json_body.get('desc')
    if steps is not None:
        # FIXME: parse 'layout' and set size
        output = pdf(steps, size='A4 portrait')
        return Response(output, content_type='application/pdf')
    else:
        return Response('fail')

if __name__ == '__main__':
    config = Configurator()
    config.add_route('hello', '/hello/{name}')
    config.add_view(hello_world, route_name='hello')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()

