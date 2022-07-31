import json
from datetime import datetime, timedelta

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Client


class AudioStreamConsumer(AsyncWebsocketConsumer):
    """Accept audio via websockets and retransmit to clients"""

    async def connect(self):
        """On connection"""
        self.room_group_name = self.scope["url_route"]["kwargs"]["client_ID"]
        self.is_listener = True if ("/listen/" in str(self.scope["path"])) else False

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        """Leave the channel when a client disconnects"""
        # Leave room group
        name, mac = self.room_group_name.split("-")
        mac = ':'.join([mac[i:i+2] for i in range(0, len(mac), 2)])

        if not self.is_listener:
            print("Will now delete where:", name, mac)
            # await sync_to_async((await sync_to_async(Client.objects.get)(mac_address=mac, username=name)).delete)()
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        """Receive incoming data"""
        if text_data:
            print(text_data)
            json_data = json.loads(text_data)
            await self.update_ping(json_data)

            if len(self.channel_layer.groups[self.room_group_name]) > 1:
                await self.send(text_data="OK")
            else:
                await self.send(text_data="NO LISTENER")
        else:
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "stream_data", "bytes": bytes_data}
            )

    @sync_to_async
    def update_ping(self, jsonData):
        """Retrieve list of clients available for connection"""
        record = Client.objects.get_or_create(**jsonData)
        record[0].last_ping = datetime.now()
        Client.save(record[0])

    # Receive message from room group
    async def stream_data(self, event):
        """Stream data back out to the client"""
        if len(self.channel_layer.groups[self.room_group_name]) > 1:
            bytes = event["bytes"]

            # Send message to WebSocket
            await self.send(bytes_data=bytes)

        else:
            await self.send(text_data="NO LISTENER")


class DataConsumer(AsyncWebsocketConsumer):
    """Accept audio via websockets and retransmit to clients"""

    async def connect(self):
        """On connection"""
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        """Receive incoming data"""
        if text_data:
            if text_data[:5] == "DATA:":
                keyData = text_data[5:]
                name, mac = keyData.split("-")
                mac = ':'.join([mac[i:i+2] for i in range(0, len(mac), 2)])

                userDetail = await sync_to_async(Client.objects.get)(mac_address=mac, username=name)
                await self.send(json.dumps({"system": userDetail.system,
                                            "version": userDetail.version,
                                            "release": userDetail.release,
                                            "username": userDetail.username,
                                            "architecture": userDetail.architecture,
                                            "processor": userDetail.processor,
                                            "ip": userDetail.ip,
                                            "mac_address": userDetail.mac_address}))
            if text_data == "CLIENT LIST":
                print("Returning Client List")
                clientList = await self.get_clients_list()
                await self.send(json.dumps({"users": clientList}))

    @sync_to_async
    def get_clients_list(self):
        """Retrieve list of clients available for connection"""
        now = datetime.now()
        start_time = now - timedelta(minutes=2)
        clients = Client.objects.filter(last_ping__range=(start_time, now))
        outList = []
        for client in clients:
            outList.append(client.username + "-" + client.mac_address.replace(":", ""))

        return outList
