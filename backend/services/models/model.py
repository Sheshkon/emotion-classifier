from keras.models import model_from_json


class FacialEmotionModel:

    EMOTIONS = ("Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral")

    def __init__(self, model_json_file, model_weights_file):
        json_file = open(model_json_file, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.loaded_model = model_from_json(loaded_model_json)
        self.loaded_model.load_weights(model_weights_file)

    def predict_emotion(self, img):
        self.preds = self.loaded_model.predict(img)
        return FacialEmotionModel.EMOTIONS[self.preds.argmax()]
