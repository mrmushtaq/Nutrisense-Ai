from src.vision.prediction import predict_food


print("Loading model...\n")

result = predict_food("Apple.jpg")

print("Model loaded successfully ✅\n")

print("Prediction Result:\n")

print(f"Food Name: {result['food_name']}")
print(f"Confidence: {result['confidence']} %\n")

print("Top Predictions:")

for i, item in enumerate(result["top_predictions"], start=1):
    label = item["label"]
    score = item["score"] * 100

    print(f"{i}. {label} - {score:.2f}%")