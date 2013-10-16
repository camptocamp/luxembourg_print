import weasyprint

from jinja2 import Environment, FileSystemLoader

def format_duration(value):
    from datetime import timedelta
    return str(timedelta(minutes=value))

def format_distance(value):
    if value > 1000:
        return "%.2fkm" % (value / 1000.0)
    else:
        return "%dm" % (value)

environment = Environment(loader=FileSystemLoader('.'))
environment.filters['format_duration'] = format_duration
environment.filters['format_distance'] = format_distance

template = environment.get_template('routing.html')


def pdf(steps, **kwargs):
    html = template.render(steps=steps, **kwargs)
    return weasyprint.HTML(string=html).write_pdf()

