import re
from cStringIO import StringIO

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

from PyPDF2 import PdfFileMerger

from routing import create_pdf
from proxy import get_pdf


def layout(raw):
    match = re.match(r'\w_(\w{2})_(\w*)', raw)
    if match:
        return ' '.join(match.groups())

def hello_world(request):
    body = request.json_body
    merger = PdfFileMerger()
    if body.get('outputFormat') == 'pdf':
        # append the pdf from MapFish print
        merger.append(get_pdf(request))

        # append the routing direction
        steps = body.get('routing')
        if steps is not None:
            merger.append(create_pdf(steps, size=layout(body.get('layout'))))

        output = StringIO()
        merger.write(output)
        output.seek(0)
        return Response(body_file=output, content_type='application/pdf')

if __name__ == '__main__':
    config = Configurator()
    config.add_route('hello', '/hello/{name}')
    config.add_view(hello_world, route_name='hello')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()

