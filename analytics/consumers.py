from channels.generic.websocket import AsyncWebsocketConsumer
import random
import time
import json
import asyncio


class AnalyticsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # params = self.scope["url_route"]["kwargs"]
        # self.room_name = params["room_name"]
        # self.room_group_name = self.room_name+"_notifications"
        self.room_group_name = "analytics"
        print("connected")
        # await self.channel_layer.group_add("notification_group", self.channel_name)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def update_visitor_count(self, event):
        # When a new visitor instance is created, update the visitor count
        visitor_count = event["visitor_count"]
        await self.send(
            text_data=json.dumps(
                {"visitor_count": visitor_count}
            ))
