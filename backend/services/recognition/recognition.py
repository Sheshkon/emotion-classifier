import base64

from django.conf import settings

import cv2
import numpy as np
import face_recognition
from skimage import io


from services.models.model import FacialEmotionModel

facec = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
model = FacialEmotionModel(settings.SERVICES_ROOT + '/models/model.json', settings.SERVICES_ROOT + '/models/model.h5')
font = cv2.FONT_HERSHEY_SIMPLEX


def get_faces_emotions(path, mode='face_recognition'):
    fr = io.imread(path)
    gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)

    if mode == 'openCV':
        faces = facec.detectMultiScale(gray_fr, 1.3, 5)

    elif mode == 'face_recognition':
        faces = face_recognition.face_locations(fr[:, :, ::-1])
        faces = [(face[3], face[0], face[1] - face[3], face[2] - face[0]) for face in faces]

    for (x, y, w, h) in faces:
        fc = gray_fr[y:y + h, x:x + w]
        roi = cv2.resize(fc, (48, 48))
        roi = roi / 255.0

        pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])

        cv2.putText(fr, pred, (x, y), font, 1, (255, 255, 0), 1)
        cv2.rectangle(fr, (x, y), (x + w, y + h), (255, 0, 0), 2)

    fr = cv2.cvtColor(fr, cv2.COLOR_RGB2BGR)

    _, jpeg = cv2.imencode('.jpg', fr)

    byte_encode = jpeg.tobytes()
    b64_encode = base64.b64encode(byte_encode).decode('utf-8')

    return b64_encode
