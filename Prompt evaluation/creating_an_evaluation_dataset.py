from utils import generate_dataset
import json

# Testing the Dataset Generation
dataset = generate_dataset()
print(dataset)

# Save the dataset to a JSON file
with open('dataset.json', 'w') as f:
    json.dump(dataset, f, indent=2)