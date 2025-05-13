"""
Demonstrate Model explainability and resoning with
Traceable Prompting / Chain-of-Thought (CoT) Prompting
"""

from vertex import generate, CustomModel

# Structure the prompt to include reasoning steps, or ask the model to generate
# intermediate rationales

model = CustomModel.BORBANN_PIPELINE_4

result = generate(
    model,
    """Explain how to generate output in a format that can be easily parsed by downstream 
    systems in \"reasoning steps\" key then output the canonical record.""",
)

print(result)

# Save result
with open("explainability.json", "w", encoding="utf-8") as f:
    f.write(result)
