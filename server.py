import re
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

from routing import pdf


def layout(raw):
    match = re.match(r'\w_(\w{2})_(\w*)', raw)
    if match:
        return ' '.join(match.groups())

def hello_world(request):
    body = request.json_body
    steps = body.get('routing')
    if steps is not None:
        output = pdf(steps, size=layout(body.get('layout')))
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

