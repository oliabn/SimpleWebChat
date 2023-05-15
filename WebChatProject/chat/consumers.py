import json
import datetime

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    """Web socket event consumer"""
    async def connect(self):
        """Connect a user to chat"""

        # one room group for all
        self.room_group_name = "group_chat_gfg"
        await self.channel_layer.group_add(self.room_group_name,
                                           self.channel_name)
        # accept user connection
        await self.accept()

    async def disconnect(self, close_code):
        """Leave the room group"""

        await self.channel_layer.group_discard(self.room_group_name,
                                               self.channel_layer)

    async def receive(self, text_data):
        """Receive message from WebSocket"""

        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]

        # Sends an event to a group
        # event has "type": "sendMessage", where sendMessage is function below
        await self.channel_layer.group_send(self.room_group_name,
                                            {"type": "send_message",
                                             "message": message,
                                             "username": username, })

    async def send_message(self, event):
        """Receive message from the room group Event.
        It will be invoked for consumers that receive the event"""

        message = event["message"]
        username = event["username"]
        date = str(datetime.date.today())
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message,
                                              "username": username,
                                              "date": date, }))
