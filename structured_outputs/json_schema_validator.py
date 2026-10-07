# data and schema is passed
# if schema type is object, the. passed data should be Dict
# and schema should contain 'required' key which is an array
# required and properties together

import re

def validate_schema(data, schema) :
    errors = []
    _validate(data, schema, "", errors)
    return errors

def _validate(data, schema, path, errors) : 
   
    schema_type = schema.get("type") # string / number / object / arrays etc
    #print(f" ============ schema  =  {schema_type}============== ")

    if schema_type == "object" :
        if not isinstance(data, dict):
            errors.append(f"{path}: expected dict, got{type(data).__name__}")
            return

        for key in schema.get("required", []):
            if key not in data:
                errors.append(f"{path}.{key} : required field missing")

        properties = schema.get("properties", {})
        for key, value in data.items() :
            if key in properties :
                _validate(value, properties[key], f"{path}.{key}", errors)

    #schema["type"]     what we expect: "array"
    #data               what we received: perhaps a list, string, number, etc.
    elif schema_type == "array" :
        if not isinstance(data, list):
            errors.append(f"{path} expected list, got {type(data).__name__}")
            return 
        minItems = schema.get("minItems", 0)
        maxItems = schema.get("maxItems", float("inf"))
        if len(data) < minItems :
            errors.append(f"{path}: array has {len(data)} items, minimum is {minItems}")
        if len(data) > maxItems :
            errors.append(f"{path}: array has {len(data)} items, maximum is {maxItems}")

        #now basic array validation sare done, moving on to Array Items
        items_schema = schema.get("items", {})
        for i, item in enumerate(data) :
            _validate(item, items_schema, f"{path}[{i}]", errors)

    elif schema_type == "string" :
        if not isinstance(data, str) :
            errors.append(f"{path}: expected string, got {type(data).__name__}")
            return
        enum_values = schema.get("enum")
        if enum_values and data not in enum_values :
            errors.append(f"{path}: '{data}' not in allowed values {enum_values}")
            
        pattern = schema.get("pattern")
        if pattern is not None and re.search(pattern, data) is None :
            errors.append(f"{path}: '{data}' does not match pattern '{pattern}'")
        

    elif schema_type == "number" :
        if isinstance(data, bool) or not isinstance(data, (int, float)) :
            errors.append(f"{path}: expected number, got {type(data).__name__}")
            return

        minimum = schema.get("minimum")
        maximum = schema.get("maximum")

        if minimum is not None and data < minimum :
            errors.append(f"{path}: {data} is less than minimum {minimum}")
        if maximum is not None and data > maximum: 
            errors.append(f"{path}: {data} is greater than maximum {maximum}")

    elif schema_type == "boolean" :
        if not isinstance(data, bool):
            errors.append(f"{path}: expected boolean, got {type(data).__name__}")

    elif schema_type == "integer":
        if not isinstance(data, int) or isinstance(data, bool):
            errors.append(f"{path}: expected integer, got {type(data).__name__}")

    elif "oneOf" in schema :

        matches = 0
        
        for option_schema in schema["oneOf"] : 
            option_errors = []

            _validate(data, option_schema, path, option_errors)

            if not option_errors:
                matches+=1

        if matches != 1:
            errors.append(
            f"{path}: data must match exactly one oneOf schema; "
            f"matched {matches}")

    elif "anyOf" in schema :

        matches = 0

        for option_schema in schema["anyOf"] :
            option_errors = []
            _validate(data, option_schema, path, option_errors)

            if not option_errors:
                matches +=1
       
        if matches <= 0:
            errors.append(
            f"{path}: data must match at least one anyOf schema; "
            f"matched {matches}")

    elif "allOf" in schema :
    
        for option_schema in schema["allOf"] :
            option_errors = []
            _validate(data, option_schema, path, option_errors)
            if option_errors:
                errors.extend(option_errors)




    
        



            


        

        
