"""
Demonstrate Post-Fine-Tuning Evaluation with these metrics:
1. JSON Syntactic Validity
2. Pydantic Schema Conformance
"""

# --- JSON Syntactic Validity ---
# HOW: parse generated json string with json.loads()
# METRIC: Percentage of generated outputs that are valid JSON
# IMPORTANCE: Fundamental. If it's not valid JSON, it's useless.

# ---  Pydantic Schema Conformance (CanonicalRecord Validation Rate) ---
# HOW: If the generated output is valid JSON, try to instantiate your CanonicalRecord Pydantic model with the parsed dictionary: CanonicalRecord(**parsed_generated_json).
# METRIC: Percentage of syntactically valid JSON outputs that also conform to the CanonicalRecord Pydantic schema (correct field names, data types, required fields present, enum values correct).
# IMPORTANCE: Crucial for ensuring the output is usable by downstream systems. Pydantic's ValidationError will give details on why it failed.
