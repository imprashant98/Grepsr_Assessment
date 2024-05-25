### Updated Setup and Testing Instructions Using Swagger UI

#### Step-by-Step Setup

1. **Clone the Repository**:

   ```sh
   git clone (https://github.com/imprashant98/Grepsr_Assessment)
   cd Grepsr_Assessment
   ```

2. **Install Dependencies**:

   ```sh
   pip install -r requirements.txt
   ```

3. **Run the Application**:

   ```sh
   uvicorn main:app --reload
   ```

4. **Access Swagger UI**:
   - Open a web browser and navigate to `http://127.0.0.1:8000/docs` to access the Swagger UI provided by FastAPI.

#### Example Input and Output Using Swagger UI

**Input HTML Block**:

```json
{
  "html_content": "<div><h1 class='product-title'>Example Product</h1><p class='price'>$19.99</p><p class='description'>This is a great product.</p></div>"
}
```

**Corresponding JSON Output**:

```json
{
  "attributes": ["Product Name", "Price", "Description"],
  "selectors": {
    "product_name": { "css_selector": "h1[class='product-title']" },
    "price": { "css_selector": "p[class='price']" },
    "description": { "css_selector": "p[class='description']" }
  }
}
```

This code sets up a FastAPI application that uses the `google/flan-t5-large` model to extract attributes from HTML content. The Swagger UI provided by FastAPI at `http://127.0.0.1:8000/docs` can be used to test the `/extract_attributes` endpoint by providing the HTML content and receiving the extracted attributes and their corresponding CSS selectors.
