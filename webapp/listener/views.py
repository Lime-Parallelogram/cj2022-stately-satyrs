from channels.layers import get_channel_layer
from django.http import HttpResponse
from django.template import loader
from listener.models import Client


def index(request):
    """Loads the index of the listener page"""
    template = loader.get_template('index.html')
    context = {"available_clients": getClients()}
    return HttpResponse(template.render(context, request))


def getClients():
    """Get a list of clients available for connection"""
    return list(get_channel_layer().groups.keys())


def client_info(request):
    """Loads the specific userdata"""
    username = request.GET.get("username", "")
    mac_address = request.GET.get("mac_address", "")

    template = loader.get_template('client_data.html')

    context = {"client_data": Client.objects.filter(username=username, mac_address=mac_address).values().first()}

    return HttpResponse(template.render(context, request))
