import base64

from django.conf import settings
import cv2
import numpy as np
import face_recognition

from services.models.model import FacialEmotionModel

facec = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
model = FacialEmotionModel(settings.SERVICES_ROOT + '/models/model.json', settings.SERVICES_ROOT + '/models/model.h5')
font = cv2.FONT_HERSHEY_COMPLEX


def get_faces_emotions(path, mode='face_recognition'):
    fr = cv2.imread(path)
    gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)

    if mode == 'openCV':
        faces = facec.detectMultiScale(gray_fr, 1.3, 5)

    elif mode == 'face_recognition':
        faces = face_recognition.face_locations(fr)
        faces = [(face[3], face[0], face[1] - face[3], face[2] - face[0]) for face in faces]

    if not len(faces):
        text = 'no faces'
        text_size = cv2.getTextSize(text, font, 1, 2)[0]
        text_x = (fr.shape[1] - text_size[0]) // 2
        text_y = (fr.shape[0] + text_size[1]) // 2
        put_text(fr, text_x, text_y, text)

    for (x, y, w, h) in faces:
        fc = gray_fr[y:y + h, x:x + w]
        roi = cv2.resize(fc, (48, 48))
        roi = roi / 255.0
        pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])

        put_text(fr, x, y, pred, scale_width=w)
        cv2.rectangle(fr, (x, y), (x + w, y + h), (0, 255, 0), 2)

    _, jpeg = cv2.imencode('.jpg', fr)

    byte_encode = jpeg.tobytes()
    b64_encode = base64.b64encode(byte_encode).decode('utf-8')

    return b64_encode


def put_text(fr, x, y, text, scale_width=None):

    scale = 1

    if scale_width:
        scale = get_optimal_font_scale(text, scale_width)
        text_size = cv2.getTextSize(text, font, scale, 2)[0]
        x += (scale_width - text_size[0]) // 2

    text_size = cv2.getTextSize(text, font, scale, 2)[0]

    sub_fr = fr[y - text_size[1]: y, x: x + text_size[0]]
    black_rect = np.ones(sub_fr.shape, dtype=np.uint8)

    res = cv2.addWeighted(sub_fr, 0.5, black_rect, 0.5, 1.0)
    fr[y - text_size[1]: y, x: x + text_size[0]] = res

    cv2.putText(fr, text, (x, y), font, scale, (255, 255, 255), 2)


def get_optimal_font_scale(text, width):
    for scale in reversed(range(0, 60, 1)):
        text_size = cv2.getTextSize(text, font, scale/10, 2)
        new_width = text_size[0][0]
        if new_width <= width:
            return scale/10
    return 1
