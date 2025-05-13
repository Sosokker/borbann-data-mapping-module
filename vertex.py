"""
Demonstrate how to generate output in a format that can be easily parsed by downstream systems.
"""

from enum import Enum

from google import genai
from google.genai import types

# pyright: reportArgumentType=false

# run `gcloud auth application-default login` and sync uv before running this script

DEFAULT_PROMPT_TEXT = "Demonstrate how to generate output in a format that can be easily parsed by downstream systems."


# I start with borbann-pipeline-2 because borbann-pipeline-1 failed to fine-tune due to incorrect jsonl file.
class CustomModel(str, Enum):
    BORBANN_PIPELINE_2 = (
        "projects/83228855505/locations/us-central1/endpoints/7340996035474358272"
    )
    BORBANN_PIPELINE_3 = (
        "projects/83228855505/locations/us-central1/endpoints/5289606405207097344"
    )
    BORBANN_PIPELINE_4 = (
        "projects/83228855505/locations/us-central1/endpoints/7800363197466148864"
    )


def generate(
    model: CustomModel,
    prompt: str = DEFAULT_PROMPT_TEXT,
) -> str:
    """Generate output of prompt using fine-tuned borbann-pipeline-4 model."""
    client = genai.Client(
        vertexai=True,
        project="83228855505",
        location="us-central1",
    )

    contents = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=8192,
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"
            ),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
        ],
    )

    output = []
    for chunk in client.models.generate_content_stream(
        model=model.value,
        contents=contents,
        config=generate_content_config,
    ):
        if chunk.text:
            output.append(chunk.text)

    result = "".join(output)
    return result
