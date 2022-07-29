from django.http import HttpResponse
from django.template import loader
from channels.layers import get_channel_layer

def index(request):
    """Loads the index of the listener page"""
    template = loader.get_template('index.html')
    context = {"available_clients": getClients()}
    return HttpResponse(template.render(context, request))


def getClients():
    """Get a list of clients available for connection"""
    return list(get_channel_layer().groups.keys())
