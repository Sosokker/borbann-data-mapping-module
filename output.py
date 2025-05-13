"""
Demonstrate how to generate output in a format that can be easily parsed by downstream systems.
"""

from google import genai
from google.genai import types

# pyright: reportArgumentType=false


def generate():
    client = genai.Client(
        vertexai=True,
        project="83228855505",
        location="us-central1",
    )

    model = "projects/83228855505/locations/us-central1/endpoints/7800363197466148864"
    contents = [types.Content(role="user", parts=[])]

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

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")


generate()
