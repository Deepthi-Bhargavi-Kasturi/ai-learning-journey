from exercises.pydantic_style_class_to_schema_converter import SchemaField, model_to_schema, python_type_to_schema

def test_string_field() :
    field = SchemaField(str)

    assert python_type_to_schema(field) == {
        "type": "string"
    }

def test_number_limits() :
    field = SchemaField(float, minimum = 0, maximum = 100) # it calls __init__ and assigns starting values to the object

    assert python_type_to_schema(field) == {
        "type" : "number",
        "minimum" : 0,
        "maximum" : 100
    }

def test_enum_field() :
    field = SchemaField(str, enum = ["draft", "reviewed", "published"])

    assert python_type_to_schema(field) == {
        "type" : "string",
        "enum" : ["draft", "reviewed", "published"]
    }

def test_sustainability_model() :
    fields = {
        "company_name": SchemaField(str),
        "reporting_year": SchemaField(
            int,
            minimum=2000,
            maximum=2100,
        ),
        "status": SchemaField(
            str,
            required=False,
            enum=["draft", "published"],
        ),
    }

    schema = model_to_schema("SustainabilityReport", fields)

    assert schema == {
        "type": "object",
        "properties": {
            "company_name": {"type": "string"},
            "reporting_year": {
                "type": "integer",
                "minimum": 2000,
                "maximum": 2100,
            },
            "status": {
                "type": "string",
                "enum": ["draft", "published"],
            },
        },
        "required": ["company_name", "reporting_year"],
    }