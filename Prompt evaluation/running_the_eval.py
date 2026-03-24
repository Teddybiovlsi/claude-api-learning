import json
from utils import run_eval

with open("dataset.json", "r") as f:
    dataset = json.load(f)

results = run_eval(dataset)