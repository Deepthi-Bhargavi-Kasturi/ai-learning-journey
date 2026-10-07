#define a class
class SchemaField :

    #constructor - assigning starting values to the newly created objects
    def __init__(self, field_type, required=True, default=None, enum=None, minimum=None, maximum=None):
        self.field_type = field_type
        self.required = required
        self.default = default
        self.enum = enum
        self.minimum = minimum
        self.maximum = maximum

# creating schema object
def python_type_to_schema(field) :

    #str is type and in schema : we write type as string
    type_map = {
        str : "string",
        int : "integer",
        float : "number",
        bool : "boolean"
    }

    #initialize schema to empty object - this will be generated schema at the end
    schema = {}

    if field.field_type in type_map :
        schema["type"] = type_map[field.field_type]
    elif field.field_type == list :
        schema["type"] = "array"
        schema["items"] = {"type": "string"}
    elif isinstance(field.field_type, dict) :
        schema = field.field_type

    if field.enum :
        schema["enum"] = field.enum
    if field.minimum is not None : 
        schema["minimum"] = field.minimum
    if field.maximum is not None : 
        schema["maximum"] = field.maximum

    return schema


def model_to_schema(name, fields) : 
    properties = {}
    required = []

    for field_name, field in fields.items() :
        properties[field_name] = python_type_to_schema(field)

        if field.required :
            required.append(field_name)


    return {
        "type" : "object",
        "properties" : properties,
        "required" : required
    }