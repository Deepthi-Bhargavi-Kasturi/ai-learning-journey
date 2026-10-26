#mini json parser/state tracker

import re
import string
import json

#when we are validating against a schema, then the rules wont be generic right? It should change as per schema

def get_json_state(partial_json, schema) :
    stack = []
    stack_frame = [] #schema context

    #initial states set to False
    in_string = False
    escaped = False
    number_has_decimal = False
    isMatch = False
    in_number = False
    
    schemaKeys_CompletedMatch = []

    keys = re.findall(r'"([^"]+)"\s*:\s*\[', partial_json)
    key = keys[len(keys) - 1] if len(keys) >= 1 else keys

    for char in partial_json :
        #if its escaped - then reset flag and then continue with the loop

       
        if escaped :
            escaped = False
            continue

        #backslashes
        if char == "\\" and in_string :
            escaped = True
            continue

        if char == '"' :
            in_string = not in_string
            
            if stack_frame[-1]["kind"] == "object" :
                if stack_frame[-1]["expecting"] == "key_or_end" :
                    stack_frame[-1]["expecting"] = "writing_key"
                elif stack_frame[-1]["expecting"] == "value_start" :
                    stack_frame[-1]["expecting"] = "writing_value"
                elif stack_frame[-1]["expecting"] == "writing_value" :
                    stack_frame[-1]["expecting"] = "separator_or_end"
                elif stack_frame[-1]["expecting"] == "colon" :
                    stack_frame[-1]["expecting"] = "value_start"
                elif stack_frame[-1]["expecting"] == "new_key" :
                    stack_frame[-1]["expecting"] = "writing_key"
                elif stack_frame[-1]["expecting"] == "writing_key" :
                    stack_frame[-1]["expecting"] = "colon"
                else :
                    isMatch = bool(re.search(r':\s*"([^"]+)\s*"', partial_json))
                    # if isMatch: 
                    #     keys = re.findall(r'"([^"]+)\s*":\s*"[^"]+\s*"', partial_json)
                    #     if keys[-1] not in schemaKeys_CompletedMatch :
                    #         schemaKeys_CompletedMatch.append(keys[-1])
                
            continue

        
        if char == ':' :
            if stack_frame[-1]["kind"] == "object" :
                stack_frame[-1]["expecting"] = "value_start"
                    

        if char == ',' :
             if stack_frame[-1]["kind"] == "object" :
                stack_frame[-1]["expecting"] = "new_key" 
            
                  
        if char in list("0123456789") :
            in_number = True
            continue
        elif in_number and char == '.' :
            number_has_decimal = True
            continue
        elif in_number :
            in_number = False

        
        if number_has_decimal and char in [',', '}', ']'] :
            number_has_decimal = False
            #continue


        if not in_string and not number_has_decimal:

            if char == '{' :

                stack_frame.append({
                    "kind" : "object",
                    "schema" : key,
                    "in_object" : True,
                    "expecting" : "key_or_end"
                })

            elif char == '[' :
                if stack_frame[-1]["kind"] == "object" :
                    stack_frame[-1]["expecting"] = "writing_value"
                stack_frame.append({
                    "kind" : "array",
                    "schema" : key,
                    "minItems" : (find_key_value(schema, key))["minItems"],
                    "maxItems" : (find_key_value(schema, key))["maxItems"],
                    "itemsType" : (find_key_value(schema, key))["items"]["type"],
                    "count" : 0
                })
            elif char == '}' :
                if not stack_frame or stack_frame[-1]["kind"] != 'object' :
                    return {'valid so far' : False}
                stack_frame.pop()

            if stack_frame[-1]["kind"] == "array" :

                if stack_frame[-1]["itemsType"] == "object" :

                    if char == '}' :
                        itemsCount = stack_frame[-1]["count"]
                        itemsCount+=1
                        stack_frame[-1]["count"] = itemsCount
                    

            if char == ']' :
                if not stack_frame or stack_frame[-1]["kind"] != 'array' :
                    return {"valid so far": False}
                if stack_frame[-1]["count"]  < stack_frame[-1]["minItems"]  :
                    return {"valid so far": False}
                stack_frame.pop()

                
   
    return {
        'valid so far' : True,
        "in_string" : in_string,
        "number_has_decimal" : number_has_decimal,
        "completed_key_val_pair" : isMatch,
        "stack_frames" : stack_frame,
        "schema_keys_generated" : schemaKeys_CompletedMatch
    }

def next_valid_tokens(partial_json, schema) :

    stripped = partial_json.strip()

    keys = re.findall(r'"([^"]+)"\s*:', partial_json)
    print(f"partial json {partial_json}")
    lengthOfKeys = len(keys)
    key = keys[len(keys) - 1] if len(keys) >= 1 else keys
   
    if not stripped :
        return ["{"]

    try:
        #JSON is complete, return <EOS> token. And loads :JSON text into appropriate python value
        json.loads(stripped) 
        return ['<EOS>']
    except json.JSONDecodeError:
            pass

    last_char = stripped[-1] if stripped else ""

    currentState = get_json_state(stripped, schema)
    if currentState["valid so far"] != True:
        print("FAIL")
        return []
    stack = currentState.get("stack_frames", [])
    type = {}
    result = False


    if stack[-1]["kind"] == 'object' :

        if stack[-1]["expecting"] == "key_or_end" :
            result = find_keys(schema, key)
            if result :
                return ['"']
            return ["}", '"']
        elif stack[-1]["expecting"] == "end_of_key" :
            return ['"']
        elif stack[-1]["expecting"] == "colon" :
            
            keys = re.findall(r'"([^"]+)"\s*', partial_json)
            result = find_keys(schema, keys[-1])

            if result == False:
                return []


            return [':']
        elif stack[-1]["expecting"] == "new_key" :
            return ['"']
        elif stack[-1]["expecting"] == "value_start" :
            type = find_key_value(schema, key)
        elif stack[-1]["expecting"] == "writing_key" :
            return list(string.ascii_letters) + list("0123456789") + [" ", '"', "_", "-"]
        elif stack[-1]["expecting"] == "writing_value" :
            #schema enforcement
            type = find_key_value(schema, key) 
            if type.get('type', '') == "integer"  :
                return []
        elif stack[-1]["expecting"] == "separator_or_end" :
            result = find_keys(schema, key)
            if result :
                return [',']
            else :
                return ['}']
        elif stack[-1]["expecting"] == "new_key" :
            return ['"'] 
        else :
            return ['"']

    if type and type.get('type', '') == "string"  :
        if stack[-1]["expecting"] == "value_start" :
            return ['"']
        elif stack[-1]["expecting"] == "writing_value" :
            return list(string.ascii_letters) + list("0123456789") + [" ", '"', "_", "-"]
   

    if last_char == '[' :

        if stack[-1]["itemsType"] == "object" :
            return ["{"]
        if stack[-1]["itemsType"] == 'string' :
            return ['"']
        elif stack[-1]["itemsType"] == 'integer' :
            return list("0123456789")
        elif stack[-1]["itemsType"] == 'boolean' :
            return ["true", "false"]
        elif stack[-1]["itemsType"] == 'object' :
            return ["{"]
        else :
            return ['"', "null", "{"]
            

    if last_char == '"' : #we never know if it is a close string or opened string
        if currentState["in_string"] :
            return list(string.ascii_letters) + list("0123456789") + [" ", '"']
        
        if not currentState["in_string"] and stack and stack[-1]["kind"] == 'object' and currentState["completed_key_val_pair"] :
            return [',', "}"]
        elif not currentState["in_string"] and stack and stack[-1]["kind"] == 'object':
            return [":"]
        elif not currentState["in_string"] and stack and stack[-1]["kind"] == 'array':
            return ["]"]
        else :
            return [',', "}", ":"]
            
    elif last_char == ":" :
        
        typeFetched = find_key_value(schema, key)
        typeFetched = typeFetched.get('type', '') 

        if typeFetched == 'string' :
            return ['"']
        elif typeFetched == 'integer' or typeFetched == 'number' :
            return list("0123456789")
        elif typeFetched == 'boolean' :
            return ["true", "false"]
        elif typeFetched == 'array' :
            return ["["]
        else :
            return ['"', "null", "{"]

    elif last_char == ".":   
        return list("0123456789")

    elif last_char == ",":

        if stack and stack[-1]["kind"] == "array" :
            # An array needs another value.
            return ["{", "[", '"', "true", "false", "null"] + list("0123456789")

        elif stack and stack[-1]["kind"] == "object" :
            return ['"']
        else :
            # An object needs its next key.
            return ['"']

    elif last_char in '0123456789':
        typeFetched = find_key_value(schema, key)
        typeFetched = typeFetched.get('type', '') 

        output = []
        if typeFetched != "integer" :
            output = ['.']

        result = find_keys(schema, key)
        if currentState["number_has_decimal"] and stack and stack[-1]["kind"] == "object" :
            
            if result :
                return list("0123456789") + [","]

            return list("0123456789") + [",", "}"]
        elif stack and stack[-1]["kind"] == "object" : 
            if result :
                return list("0123456789") + [","]
            return output + list("0123456789") + [",", "}"]
        else :
            return output + list("0123456789") + [",", "}", "]"]
                
    elif last_char in "}]" :
           
            if not stack :
                return ["<EOS>"]
            if stack[-1]["kind"] == "object" :  
                if len(stack) == 1 :
                    return ["}"]
                return [",", "}"]
            if stack[-1]["kind"]  == "array" :
                schemaMaxArrayCount = stack[-1]["maxItems"]
                partialJsonItemsCount = stack[-1]["count"]
                if partialJsonItemsCount < schemaMaxArrayCount :
                    return ["]", ","]
                else :
                    return ["]"]
            
    elif last_char == "[" :

        typeFetched = find_key_value(schema, key)
        typeFetched = typeFetched.get('type', '') 

        if typeFetched == "object" :
            return ["{"]
        elif typeFetched == "boolean" :
            return ["true", "false"]
        elif typeFetched == "string" :
            return ['"']
        elif typeFetched == "integer" :
            return list("0123456789")
        elif typeFetched == "array" :
            return ["["]
        return [ "null", "]" ]
    else :
        return "any"

    


def demonstrate_constraint_decoding(schema) :
    partial_states = [
        '',
        '{',
        '{"product"',
        '{"product":',
        '{"product": "Sony"',
        '{"product": "Sony",',
        '{"product": "Sony", "price":',
        '{"product": "Sony", "price": 348',
        '{"product": "Sony", "price": 348}',
        '{"product": "Sony", "price": 348}'
    ]

    print(f"{'Partial JSON':<45} {'Valid Next Tokens'}")
    print("-" * 80)

    for state in partial_states :
        valid_next_tokens = next_valid_tokens(state, schema)
        display = state if state else "(empty)"
        print(f"{display:<45} {valid_next_tokens}")



def find_keys(schema, target_key=''):   
    array_keys = []
    schema_type = schema.get("type")

    if schema_type == "object" :
        keys =  schema.get("required", [])
        if target_key in keys and len(keys) > 1 :
            return True
        if target_key == [] and keys and len(keys) > 1 :
            return True

        properties = schema.get("properties", {})
        for value in properties.values() :

            if value.get("type", '') == 'array' :
                result = find_keys(value, target_key)
                return result
            
            

    # if schema_type == "string" :
    #     if schema != target_key :
            
    #     return False

    if schema_type == "array" :
        keys = schema["items"].get("required")
        if target_key in keys and keys.index(target_key) < len(keys) - 1:
            return True
        if target_key == [] and keys and len(keys) > 1 :
            return True
        
    return False

def find_key_value(schema, target_key=''):
    array_keys = []

    if isinstance(schema, dict):
        if target_key == [] :
            return schema["required"]
                
       
        if target_key in schema:
            return schema[target_key]

        for val in schema.values():
            if isinstance(val, (dict, list)):
                result = find_key_value(val, target_key)
                if result is not None:  # Found it deep inside
                    return result

    elif isinstance(schema, list):
        for item in schema:
            if isinstance(item, (dict, list)):
                result = find_key_value(item, target_key)
                if result is not None:
                    return result

        
    return None



                





if __name__ == "__main__":
    demonstrate_constraint_decoding()

    
        


