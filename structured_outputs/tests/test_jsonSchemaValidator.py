import json
from pathlib import Path
from json_schema_validator import validate_schema
import pytest

#to fecth all the JSON files under tests folder
test_folder = Path("tests")
test_json_files = test_folder.glob('*.json')

def load_json(file):
    path = Path(file)
    return json.loads(path.read_text())

schema = load_json("schemas/sustainability_report_schema.json")

@pytest.mark.parametrize("file_path", test_json_files, ids = lambda path: path.name)
def test_valid_report(file_path):

    data = load_json(file_path)
    errors = validate_schema(data, schema)
            
    assert errors == [], f"{file_path.name} failed: {errors}"
        

    

    