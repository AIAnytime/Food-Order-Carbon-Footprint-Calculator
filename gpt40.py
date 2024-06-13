from openai import OpenAI
import os
from dotenv import load_dotenv
import base64

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image

image_path = "img.jpg"

base64_image = encode_image(image_path)

prompt_instruction = """
You are an intelligent assistant whose task is to analyze the food order and calculate the carbon footprint.

**Instructions**:
1. **Identify the Food Items**:
   - Determine if each food item is vegetarian or non-vegetarian.
   - List each food item with its classification (veg/non-veg).

2. **Calculate Carbon Emissions**:
   - Use India-specific carbon emission factors to calculate the carbon emissions for each food item.
   - Provide the carbon emission factors used for each food item.

3. **Provide a Breakdown**:
   - Detail the carbon emissions for each food item separately.
   - Summarize the total carbon emissions for the entire order.

4. **Summarize the Results in brief**:
   - Include a brief summary of the order.
   - Mention the type (veg/non-veg).
   - State the total carbon emissions.
   - Provide a breakdown of the emissions.
"""

client = OpenAI()

MODEL="gpt-4o"

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": prompt_instruction},
        {"role": "user", "content": [
            #{"type": "text", "text": "What's the area of the shape in this image?"},
            {"type": "image_url", "image_url": {
                "url": f"data:image/png;base64,{base64_image}"}
            }
        ]}
    ],
    temperature=0.7,
)
print(response.choices[0].message.content)
