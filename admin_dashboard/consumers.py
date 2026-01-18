import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Pelanggan

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Print debug information
        print(f"DEBUG: Scope Session: {self.scope.get('session')}")
        # Check if user is authenticated
        if self.scope["user"].is_authenticated or 'pelanggan_id' in self.scope.get('session', {}):
            # Get user ID from session
            pelanggan_session_id = self.scope.get('session', {}).get('pelanggan_id')
            if pelanggan_session_id:
                # Convert to int if it's a string
                try:
                    self.user_id = int(pelanggan_session_id)
                except (ValueError, TypeError):
                    self.user_id = pelanggan_session_id
            else:
                # For admin users, we don't handle notifications here
                await self.close()
                return
                
            # Create a unique group name for this user
            self.group_name = f"user_{self.user_id}"
            
            # Join room group
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    # Receive message from WebSocket
    async def receive(self, text_data):
        # We don't expect to receive messages from the client in this implementation
        pass

    # Receive message from room group
    async def send_notification(self, event):
        # Send notification to WebSocket
        notification = event['notification']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'notification': notification
        }))