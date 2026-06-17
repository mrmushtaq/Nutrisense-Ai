from transformers import pipeline
from PIL import Image


class FoodPredictor:
    def __init__(self):
        self.model = pipeline(
            "image-classification",
            model="nateraw/food"
        )

    def predict(self, image_path):

        image = Image.open(image_path).convert("RGB")

        result = self.model(image)

        best = result[0]

        return {
            "food_name": best["label"],
            "confidence": round(best["score"] * 100, 2),
            "top_predictions": result[:5]
        }


predictor = FoodPredictor()


def predict_food(image_path):
    return predictor.predict(image_path)


def is_model_ready():
    return True


def get_model_info():
    return {
        "model_name": "nateraw/food",
        "type": "HuggingFace Food-101 pretrained model",
        "classes": 101,
        "status": "ready"
    }