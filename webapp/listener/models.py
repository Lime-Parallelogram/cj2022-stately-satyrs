from django.db import models


class Client(models.Model):
    """Used to store information about a client"""

    class Meta:
        unique_together = (('username', 'mac_address'),)

    system = models.CharField(max_length=120)
    version = models.CharField(max_length=200)
    release = models.CharField(max_length=200)
    username = models.CharField(max_length=50)
    architecture = models.CharField(max_length=10)
    processor = models.CharField(max_length=120)
    ip = models.CharField(max_length=20)
    mac_address = models.CharField(max_length=40)

    last_ping = models.DateTimeField(auto_now_add=True)
