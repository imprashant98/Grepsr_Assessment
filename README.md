### Setup and Testing Instructions

#### Step-by-Step Setup

1. **Clone the Repository**:

   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**:

   ```sh
   pip install fastapi uvicorn transformers torch pydantic
   ```

3. **Run the Application**:
   ```sh
   uvicorn main:app --reload
   ```

#### Testing the API

- **Using Curl**:

  ```sh
  curl -X POST "http://127.0.0.1:8000/extract_attributes" -H "Content-Type: application/json" -d '{"html_content": "<div><h1 class=\"product-title\">Example Product</h1><p class=\"price\">$19.99</p><p class=\"description\">This is a great product.</p></div>"}'
  ```

- **Using Postman**:
  1. Open Postman.
  2. Set the request type to `POST`.
  3. Set the URL to `http://127.0.0.1:8000/extract_attributes`.
  4. In the "Body" tab, select "raw" and set the type to `JSON`.
  5. Enter the following JSON in the body:
     ```json
     {
       "html_content": "<div><h1 class=\"product-title\">Example Product</h1><p class=\"price\">$19.99</p><p class=\"description\">This is a great product.</p></div>"
     }
     ```
  6. Click "Send" to make the request.

#### Example Input and Output

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

This output indicates that the API has successfully extracted the relevant e-commerce attributes ("Product Name", "Price", "Description") from the HTML content and generated corresponding CSS selectors for these attributes. These selectors can be used to identify and manipulate the respective HTML elements in further processing steps.
