import joblib

# Load the model dictionary
model_path = "models/crop_model.pkl"
crop_model = joblib.load(model_path)

# Print top-level info
print("Type of object:", type(crop_model))
print("Keys in dictionary:", crop_model.keys())
print("\nContents preview:\n")

# Loop through all items to inspect
for key, value in crop_model.items():
    print(f"Key: {key}")
    print(f" Type: {type(value)}")
    if isinstance(value, dict):
        print(f"  Dict keys: {list(value.keys())}")
    elif hasattr(value, "classes_"):  # LabelEncoder or classifier
        print(f"  Classes: {getattr(value, 'classes_', None)}")
    else:
        print(f"  Value preview: {str(value)[:100]}")  # first 100 chars
    print("-" * 50)
