"""
Demonstrate Post-Fine-Tuning Evaluation with these metrics:
1. JSON Syntactic Validity
2. Pydantic Schema Conformance
"""

import json
from vertex import generate, CustomModel
from schemas.canonical import CanonicalRecord

prompts = []
json_validity_count = {
    CustomModel.BORBANN_PIPELINE_2: 0,
    CustomModel.BORBANN_PIPELINE_3: 0,
    CustomModel.BORBANN_PIPELINE_4: 0,
}
pydantic_validity_count = {
    CustomModel.BORBANN_PIPELINE_2: 0,
    CustomModel.BORBANN_PIPELINE_3: 0,
    CustomModel.BORBANN_PIPELINE_4: 0,
}

with open("data/evaluation/evaluation.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        obj = json.loads(line)
        for message in obj.get("contents", []):
            if message.get("role") == "user":
                for part in message.get("parts", []):
                    if "text" in part:
                        prompts.append(part["text"])

# --- JSON Syntactic Validity ---
# HOW: parse generated json string with json.loads()
# METRIC: Percentage of generated outputs that are valid JSON
# IMPORTANCE: Fundamental. If it's not valid JSON, it's useless.

for prompt in prompts:
    for model in CustomModel:
        result = generate(model, prompt)
        try:
            json.loads(result)
            json_validity_count[model] += 1
        except json.JSONDecodeError:
            pass

# ---  Pydantic Schema Conformance (CanonicalRecord Validation Rate) ---
# HOW: If the generated output is valid JSON, try to instantiate your CanonicalRecord Pydantic model with the parsed dictionary: CanonicalRecord(**parsed_generated_json).
# METRIC: Percentage of syntactically valid JSON outputs that also conform to the CanonicalRecord Pydantic schema (correct field names, data types, required fields present, enum values correct).
# IMPORTANCE: Crucial for ensuring the output is usable by downstream systems. Pydantic's ValidationError will give details on why it failed.

for prompt in prompts:
    for model in CustomModel:
        result = generate(model, prompt)
        try:
            json.loads(result)
            try:
                CanonicalRecord(**json.loads(result))
                pydantic_validity_count[model] += 1
            except ValueError as e:
                print(e)
        except json.JSONDecodeError:
            pass

# --- Print Results ---
print("JSON Syntactic Validity:")
for model in CustomModel:
    print(f"{model}: {json_validity_count[model] / len(prompts) * 100:.2f}%")

print("Pydantic Schema Conformance (CanonicalRecord Validation Rate):")
for model in CustomModel:
    print(
        f"{model}: {pydantic_validity_count[model] / json_validity_count[model] * 100:.2f}%"
    )

# --- Save results ---

with open("evaluation_results.json", "w", encoding="utf-8") as f:
    json.dump(
        {
            "json_validity_count": json_validity_count,
            "pydantic_validity_count": pydantic_validity_count,
        },
        f,
        indent=4,
    )
