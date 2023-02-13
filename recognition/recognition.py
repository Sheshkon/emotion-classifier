import cv2
import numpy as np
import face_recognition

from models.model import FacialEmotionModel

facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = FacialEmotionModel('../models/model_0_2.json', '../models/model_0_2.h5')
font = cv2.FONT_HERSHEY_SIMPLEX


def get_faces_emotions(path, mode='openCV'):
    fr = cv2.imread(path)
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

        cv2.putText(fr, pred, (x, y), font, 1, (255, 255, 0), 2)
        cv2.rectangle(fr, (x, y), (x + w, y + h), (255, 0, 0), 2)

    _, jpeg = cv2.imencode('.jpg', fr)
    cv2.imshow('result', fr)
    cv2.waitKey(0)

    byte_encode = jpeg.tobytes()
    return byte_encode

get_faces_emotions('../examples/img_11.png', mode='face_recognition')
