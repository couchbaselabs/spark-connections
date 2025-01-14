import json
import os

# Directory to store the generated documents
output_dir = "./"
os.makedirs(output_dir, exist_ok=True)

# Generate 1000 sample JSON documents
for i in range(1, 1001):
    doc = {
        "id": f"doc_{i}",
        "name": f"Sample Document {i}",
        "value": i,
        "tags": [f"tag{i%5}", f"category{i%3}"],
        "timestamp": "2025-01-09T00:00:00Z"
    }
    file_path = os.path.join(output_dir, f"doc_{i}.json")
    with open(file_path, "w") as f:
        json.dump(doc, f)

print(f"Generated 1000 documents in {output_dir}")
