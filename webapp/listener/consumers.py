from channels.generic.websocket import AsyncWebsocketConsumer


class AudioStreamConsumer(AsyncWebsocketConsumer):
    """Accept audio via websockets and retransmit to clients"""

    async def connect(self):
        """On connection"""
        self.room_name = self.scope["url_route"]["kwargs"]["client_ID"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        """Leave the channel when a client disconnects"""
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        """Receive incoming data"""
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "stream_data", "bytes": bytes_data}
        )

    # Receive message from room group
    async def stream_data(self, event):
        """Stream data back out to the client"""
        bytes = event["bytes"]

        # Send message to WebSocket
        await self.send(bytes_data=bytes)
