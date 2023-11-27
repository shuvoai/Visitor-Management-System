from channels.generic.websocket import AsyncWebsocketConsumer
import random
import time
import json
import asyncio


class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # params = self.scope["url_route"]["kwargs"]
        # self.room_name = params["room_name"]
        # self.room_group_name = self.room_name+"_notifications"
        self.room_group_name = "notifications"
        # await self.channel_layer.group_add("notification_group", self.channel_name)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        notification = "test"
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "notification_sender", "notification": notification}
        )

    async def notify_groups(self, notification):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "notification_sender",
                "notification": notification
            }
        )

    async def notification_sender(self, event):
        message = event["message"]
        await self.send(
            text_data=json.dumps(
                {"message": message}
            ))
    # async def broadcast(self):
    #    await self.send(text_data=json.dumps({"message": "this sis dummy ddata"}))

    # async def disconnect(self, close_code):
    #    await self.channel_layer.group_discard("notification_group", self.channel_layer)
