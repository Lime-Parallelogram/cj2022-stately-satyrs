from django.http import HttpResponse
from django.template import loader


def index(request):
    """TODO"""
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))
