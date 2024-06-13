import streamlit as st
import base64
from openai import OpenAI
import os
from dotenv import load_dotenv

st.set_page_config(
    layout="wide"
)

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image

def analyze_image(image_data: str) -> str:
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
    MODEL = "gpt-4o"

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": prompt_instruction},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}
            ]}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content

# Streamlit UI
st.sidebar.title("Food Order Carbon Footprint Calculator")
uploaded_file = st.sidebar.file_uploader("Upload an image of your food order", type=["jpg", "jpeg", "png"])

if st.sidebar.button("Calculate"):
    if uploaded_file is not None:
        # Save the uploaded file
        with open("uploaded_image.png", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Encode the image
        base64_image = encode_image("uploaded_image.png")

        # Analyze the image
        result = analyze_image(base64_image)

        # Display the results
        col1, col2 = st.columns(2)
        with col1:
            st.image("uploaded_image.png", caption='Uploaded Food Order', use_column_width=True)
        with col2:
            st.markdown(result)
    else:
        st.sidebar.error("Please upload an image to proceed.")
