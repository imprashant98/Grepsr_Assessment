from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import torch
import re

# Initialize FastAPI
app = FastAPI()

# Initialize the language model (CPU only)
torch.random.manual_seed(0)
model_id = "google/flan-t5-large"
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)
pipe = pipeline("text2text-generation", model=model,
                tokenizer=tokenizer, device=-1)

# Define the request model


class HTMLBlock(BaseModel):
    html_content: str

# Helper function to extract attributes using the language model


def extract_attributes(html_content):
    prompt = (
        "Please extract the meaningful attributes relevant to e-commerce contexts from the provided HTML block representing as a ecommerce website:\n"
        f"{html_content}\n\n"
        "Example attributes include: Price, Ratings, Image URL, Descriptions, Name and so on.\n"
        "Please identify only the relevant attributes and separate them by commas."
    )

    output = pipe(prompt, max_length=300)
    generated_text = output[0]['generated_text']

    if isinstance(generated_text, list):
        generated_text = ', '.join(generated_text)

    attributes_list = re.findall(r'\b\w+\b', generated_text)

    # Define relevant attributes along with their similar words and case sensitivity
    relevant_attributes = {
        "Product Name": {"product-name", "name", "title", "product"},
        "Description": {"description", "descriptions", "details", "info"},
        "Image": {"image", "picture", "photo", "img", "images"},
        "Price": {"price", "cost", "amount"},
        "Discount": {"discount", "sale", "offer"},
        "Category": {"category", "type", "classification"}
    }

    filtered_attributes = []

    # Iterate through extracted attributes and check against relevant attributes
    for attr in attributes_list:
        for relevant_attr, similar_words in relevant_attributes.items():
            if attr.strip().lower() in similar_words:
                filtered_attributes.append(relevant_attr)
                break  # Move to the next extracted attribute

    # Remove duplicates
    filtered_attributes = list(set(filtered_attributes))
    return filtered_attributes


# Helper function to identify CSS selectors using regex
def identify_selectors(html_content, attributes):
    selectors = {}
    for attribute in attributes:
        attribute = attribute.strip().lower().replace(' ', '_')
        # Remove special characters and format attribute for CSS selector
        css_selector = re.sub(r'[^a-zA-Z0-9\-_]', '', attribute)
        css_selector = f"p[class*='{css_selector}']"
        selectors[attribute] = {"css_selector": css_selector}
    return selectors

# FastAPI endpoint


@app.post("/extract_attributes")
async def extract_attributes_endpoint(html_block: HTMLBlock):
    try:
        extracted_text = extract_attributes(html_block.html_content)
        if isinstance(extracted_text, str):
            attributes = [extracted_text.strip()]
        elif isinstance(extracted_text, list):
            attributes = [attr.strip() for attr in extracted_text]
        else:
            raise ValueError("Unexpected type for extracted_text")
        selectors = identify_selectors(html_block.html_content, attributes)
        return {"attributes": attributes, "selectors": selectors}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
