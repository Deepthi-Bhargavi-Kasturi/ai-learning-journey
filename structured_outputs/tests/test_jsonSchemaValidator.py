import json
from pathlib import Path
from json_schema_validator import validate_schema
import pytest

#to fecth all the JSON files under tests folder
test_folder = Path("tests")
test_json_files = test_folder.glob('*.json')

def load_json(file):
    #path = Path(file)
    return json.loads(Path(file).read_text())

#schema = load_json("schemas/sustainability_report_schema.json")

test_cases = [
    (
        "tests/sustainability_valid_report.json",
        "schemas/sustainability_report_schema.json",
    ),
    (
        "tests/sustainability_invalid_report.json",
        "schemas/sustainability_report_schema.json",
    ),
    (
        "tests/polymorphic_sustainability_valid_rpt.json",
        "schemas/polymorphic_handling_schema_01.json",
    ),
    (
        "tests/polymorphic_sustainability_valid_rpt_v2.json",
        "schemas/polymorphic_handling_schema_01.json",
    ),
]

@pytest.mark.parametrize("data_file, schema_file", test_cases, ids=[
        "basic-sustainability-report",
        "basic-sustainability-invalid-report",
        "polymorphic-product-report",
        "polymorphic-service-report",
    ])
def test_report(data_file, schema_file):

    data = load_json(data_file)
    schema = load_json(schema_file)
    errors = validate_schema(data, schema)

    assert errors == [], f"{data_file} failed: {errors}"
            
    # if "invalid" in data_file:
    #     assert errors, f"{data_file} should fail validation"
    # else:
    #     assert errors == [], f"{data_file} failed: {errors}"



        

    

    
