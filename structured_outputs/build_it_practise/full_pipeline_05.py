from pydantic_style_class_to_schema_converter import SchemaField, model_to_schema, python_type_to_schema
from json_schema_validator import validate_schema
from build_constraint_decoding import demonstrate_constraint_decoding


import json

from extraction_pipeline_04 import extract_with_retry

def run_demo() :
    print("="*60)
    print(" Structured Output pipeline Demo ")
    print("="*60)


    print("\n ----- Schema Defnition ----- \n")
    #Pydantic model -> generating schema

    print(model_to_schema("t", {"nums": SchemaField(list, items=SchemaField(int))}))
    grid_schema = model_to_schema("t", {"grid": SchemaField(list, items=SchemaField(list, items=SchemaField(float)))})
    print(model_to_schema("t", {"tags": SchemaField(list)}))

    #added this to have items and its type as dynamic
    # categories = {
    #     "items" : SchemaField(str)
    # }
    #cleanup
    items_field = SchemaField(str)

    product_fields = {
        "product" : SchemaField(str),
        "price" : SchemaField(float, minimum = 0),
        "in_stock" : SchemaField(bool),
        "categories" : SchemaField(list, required=False, items = items_field)
    }
    generated_schema = model_to_schema("product", product_fields)
    print(json.dumps(generated_schema, indent=2))
    print(json.dumps(grid_schema, indent=2))



    print("\n--- Schema Validation ---")
    tests = [
        ("{'product': 'Sony', 'price': 10, 'in_stock': true}", "single quotes"),
        ('{"product": "Sony", "price": 10, "in_stock": true,}', "trailing comma"),
        ('```json\n{"product": "Sony", "price": 10, "in_stock": true}\n```', "markdown fence"),
        ('{"product": "Sony", "price": 10, "in_stock": True}', "Python True"),
        ('{"product": "Sony", "price": -5, "in_stock": true}', "negative price"),
        ('{"product": "Sony", "in_stock": true}', "missing price"),
        ('{"product": "Sony", "price": 10}', "missing in_stock"),
        ('{"product": "Sony", "price": "348", "in_stock": true}', "price as string"),
        ('{"product": "Sony", "price": 10, "in_stock": "true"}', "in_stock as string"),
        ('{"product": "Sony", "price": 10, "in_stock": true, "categories": ["audio", 5]}', "number in categories"),
        ('{"product": "Sony", "price": 10, "in_stock": true, "color": "black"}', "extra key"),
        ('{"product": "Sony", "price": true, "in_stock": true}', "price is true"),
        ('[]', "list instead of object"),
        ('{"product": "Sony", "price": 348}', "Minimum criteria not met")
    ]

    for data, label in tests :

        #this step was not added in exercise, and with out this I am seeing a standard error FAIL : [': expected dict, got str'] across Test Cases -- because isinstance(data, dict) returns FALSE
        #and further even correcting the parsed is giving the same result
        try :
            parsed = json.loads(data)
        except json.JSONDecodeError as e :
            print(f"{label} : JSON parser error -- {e}")
            continue
        errors = validate_schema(parsed, generated_schema)
        status = "PASS" if not errors else f"FAIL : {errors}"
        print(f" {label} : {status}")
        # input()

    #output:
    # --- Schema Validation ---
    # single quotes : JSON parser error -- Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
    # trailing comma : JSON parser error -- Extra data: line 1 column 51 (char 50)x --  Illegal trailing comma before end of object: line 1 column 50 (char 49)
    # markdown fence : JSON parser error -- Expecting value: line 1 column 1 (char 0)
    # Python True : JSON parser error -- Expecting value: line 1 column 46 (char 45)
    # negative price : FAIL : ['.price: -5 is less than minimum 0']
    # missing price : FAIL : ['.price : required field missing']
    # missing in_stock : FAIL : ['.in_stock : required field missing']
    # price as string : FAIL : ['.price: expected number, got str']
    # in_stock as string : FAIL : ['.in_stock: expected boolean, got str']
    # number in categories : FAIL : ['.categories[1]: expected string, got int']
    # extra key : FAIL : ['.color : Additional field in data']
    # price is true : FAIL : ['.price: expected number, got bool']
    # list instead of object : FAIL : [': expected dict, got list']

    print(validate_schema({"grid": [[1.5, 2.5], [3.0]]}, grid_schema))   # ? []
    print(validate_schema({"grid": [[1.5, "x"]]}, grid_schema))          # ? ['.grid[0][1]: expected number, got str']
    print(validate_schema({"grid": [1.5]}, grid_schema))                 # ? ['.grid[0] expected list, got float']

    print("\n--- Constrained Decoding Simulation ---")
    demonstrate_constraint_decoding(generated_schema)


    print("\n--- Extraction Pipeline ---")
    texts = [
        "The Sony WH-1000XM5 headphones are priced at $348 and currently available.",
        "The new MacBook Pro 16-inch laptop costs $2499 but is sold out.",
        "This is a random sentence with no product info.",
    ]

    for text in texts :
        print(f"\n Input: {text[:60]}...")
        result = extract_with_retry(text, generated_schema)
        if result is not None :
            print(f" Output :{json.dumps(result)}")
        else :
            print(f"Output: FAILED after retries")



    


    


if __name__ == "__main__" :
    run_demo()