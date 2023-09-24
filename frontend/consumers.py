import json
from channels.generic.websocket import AsyncWebsocketConsumer


class SensorDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Perform cleanup if needed
        pass

    async def receive(self, text_data):
        # Handle received data if needed
        # For example, you can echo the received data back to the client
        await self.send(text_data)
