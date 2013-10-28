from cStringIO import StringIO
import requests

def get_pdf(request, url="http://map.geoportail.lu/print"):
    # FIXME: forward headers ?
    # FIXME: forward GET params ?
    session = requests.Session()
    session.headers['Referer'] = request.referer 
    r = session.post(url + "/create.json?url=", data=request.body)
    # FIXME: errors checking
    pdf = r.json().get('getURL')
    r = session.get(url + pdf)
    # FIXME: errors checking
    return StringIO(r.content)
