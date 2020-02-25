import json

import asyncio
from .models import ChatMessage, Thread
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import PlayMateUser as User


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connect', event)
        other_user =  self.scope['url_route']['kwargs']['pk']
        me = self.scope['url_route']['kwargs']['id']

        me = User.objects.get(id=me)
        thread_obj = await self.get_thread(me, other_user)
        self.thread_obj = thread_obj
        chat_room = f'thread_{thread_obj.id}'
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name  # defualt
        )

        await self.send({
            "type": 'websocket.accept'
        })

        # await asyncio.sleep(10)
        # await self.send({
        #     'type': 'websocket.send',
        #     'text': 'Hello world'
        # })

    async def websocket_receive(self, event):
        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            msg = loaded_dict_data.get('message')
            isTyping = loaded_dict_data.get('isTyping')
            sender = loaded_dict_data.get('sender')
            status = loaded_dict_data.get('status')
            timestamp = loaded_dict_data.get('timestamp')
            me = self.scope['url_route']['kwargs']['id']
            user = User.objects.get(id=me) #self.scope['user']
            phone_number = 'Anonymous'
            if user.is_authenticated:
                phone_number = user.phone_number
            myResponse = {
                'message': msg,
                'sender': sender, # ME
                # "second_phone": receiver_phone,
                'status': status,
                'timestamp': timestamp
            }
            if not isTyping:

                await self.create_chat_message(msg, user)
            # brodcast the message event to be sent
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type': 'chat_message',
                    'text':  json.dumps(myResponse)
                }
            )

    async def chat_message(self, event):
        # send the actual message
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    async def websocket_disconnect(self, event):
        print('disconnected', event)

    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]

    @database_sync_to_async
    def create_chat_message(self, msg, me):
        thread_obj = self.thread_obj
        return ChatMessage.objects.create(thread=thread_obj, user=me, message=msg)
