
import json
from json_schema_validator import validate_schema
import pathlib


def simulate_llm_extraction(text, schema, attempt) :

    if not text :
        text = '{"product": "Sony", "price": 348}'

    if "headphones" in text.lower() or "sony" in text.lower() :
        if attempt == 0 :
            return '{"product": "Sony WH-1000XM5", "price": 348.00, "in_stock": true, "categories": ["audio", "headphones"]}'
        return '{"product": "Sony WH-1000XM5", "price": 348.00, "in_stock": true}'

    if "laptop" in text.lower() :
        return '{"product": "MacBook Pro 16", "price": 2499.00, "in_stock": false, "categories": ["computers"]}'

    return '{"product": "Unknown", "price": 0, "in_stock": false}'





#make an LLM call and validate output against schema
def extract_with_retry(text, schema, max_retries = 3) :
    # print(schema)
    for attempt in range(max_retries) :
        raw = simulate_llm_extraction(text, schema, attempt)
        #print(f"LLM Output {raw}")

        #load the output and check if it is JSON
        try :
            data = json.loads(raw)
        except json.JSONDecodeError as e :
            print(f" Attempt {attempt + 1}: JSON parse error -- {e}")

        #validate output against schema
        errors = validate_schema(data, schema)

        if not errors :
           return data
        print(raw)
        print(f" Attempt {attempt + 1} Schema Validation errors -- {errors}")

    return None

        
#define a schema
product_schema = {
    "type" : "object",
    "properties" : {
        "product" : {"type" : "string"},
        "price" : {"type" : "number", "minimum" : 0},
        "in_stock" : {"type" : "boolean"},
        "categories" : {"type" : "array", "items" : {"type" : "string"}}
    },
    "required" : ["product", "price", "in_stock", "categories" ]
}
#print(product_schema)

#Tests I ran
tests = [
    ("{'product': 'Sony', 'price': 10, 'in_stock': true}", "single quotes"),
    ('{"product": "Sony", "price": 10, "in_stock": true,}', "trailing comma"),
    ('```json\n{"product": "Sony", "price": 10, "in_stock": true}\n```', "markdown fence"),
    ('{"product": "Sony", "price": 10, "in_stock": True}', "Python True"),
    ('{"product": "Sony", "price": -5, "in_stock": true}', "negative price"),
    ('{"product": "Sony", "price": 10}', "missing in_stock"),
    ('{"product": "Sony", "price": "348", "in_stock": true}', "price as string"),
    ('{"product": "Sony", "price": 10, "in_stock": "true"}', "in_stock as string"),
    ('{"product": "Sony", "price": 10, "in_stock": true, "categories": ["audio", 5]}', "number in categories"),
    ('{"product": "Sony", "price": 10, "in_stock": true, "color": "black"}', "extra key"),
    ('{"product": "Sony", "price": true, "in_stock": true}', "price is true"),
    ('[]', "list instead of object"),
]

if __name__ == "__main__" :
    res = extract_with_retry('',product_schema,3)
    print(res)