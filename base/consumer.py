# consumers.py
import json
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer
from .Algorithm import is_face_present


class SignalConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"video_call_{self.room_name}"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is not None:
            data = json.loads(text_data)
            if data['command'] == 'agora_signal':
                await self.handle_agora_signal(data['message'])
            # elif 'frame' in data and data['type'] == 'iris_detection_frame':
            #     print("frame received")
            #     frame_data = base64.b64decode(data['frame'])
            #     await self.send(text_data=json.dumps({
            #         'type': 'frame_processed',
            #         'message': 'Frame processed successfully',
            #     }))
            elif data['command'] == 'join_room':
                await self.channel_layer.group_send(self.room_group_name, {
                    'type': 'join.message',
                })

        elif bytes_data is not None:
                binary_data = bytes_data
                face_present = is_face_present(binary_data)

                if face_present:
                    print("Face is present in the frame.")
                else:
                    print("No face detected in the frame.")
                   
        else:
            print("Received message without text_data and bytes_data")
            
    async def join_message(self,event):
        await self.send(text_data=json.dumps({
        'type': 'joined',
        'text': 'hello, this is joined',
    }))


    async def handle_agora_signal(self, message):
        # Implement your Agora signaling logic here
        pass

    async def detect_iris_movement(self, video_frame):
        # Implement your iris detection logic here
        # You may use a machine learning library like TensorFlow or OpenCV
        # Return the result of the detection
        return 'Iris Detected'
