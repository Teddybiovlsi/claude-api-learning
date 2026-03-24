import json
from utils import run_eval

with open("dataset.json", "r") as f:
    dataset = json.load(f)

results = run_eval(dataset)
print(json.dumps(results, indent=2))

with open("results.json", "w") as f:
    json.dump(results, f, indent=2)