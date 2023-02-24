import json
import logging

from channels.generic.websocket import WebsocketConsumer

from services.recognition.recognition import from_b64_to_image, live_video_get_faces_emotions

logger = logging.getLogger('main')


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected!'
        }))
        logger.info('connection established')

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        recieved_frame = text_data_json['frame']

        try:
            frame = from_b64_to_image(recieved_frame)
            result = live_video_get_faces_emotions(frame)
        except Exception as e:
            return

        self.send(text_data=json.dumps({
            'type': 'classifier',
            'result': result
        }))

    def disconnect(self, code):
        logger.info('disconnected')
