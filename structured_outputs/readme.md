# Reference: 
https://aiengineeringfromscratch.com/lesson?path=phases%2F11-llm-engineering%2F03-structured-outputs&learningPath=applied-ai-engineer#ship-it


# Step 1: JSON Schema Validator - Output

- Pass data and schema to validate oif data adheres to Schema
- Verify Valid and Invalid Scenarios

test_jsonSchemaValidator.py::test_valid_report[sustanability_invalid_report.json] FAILED                                                                                                                                                [ 50%]
test_jsonSchemaValidator.py::test_valid_report[sustanability_valid_report.json] PASSED                                                                                                                                                  [100%]

================================================================================================================== FAILURES ===================================================================================================================
____________________________________________________________________________________________ test_valid_report[sustanability_invalid_report.json] _____________________________________________________________________________________________

file_path = PosixPath('tests/sustanability_invalid_report.json')

    @pytest.mark.parametrize("file_path", test_json_files, ids = lambda path: path.name)
    def test_valid_report(file_path):
    
        data = load_json(file_path)
        errors = validate_schema(data, schema)
    
>       assert errors == [], f"{file_path.name} failed: {errors}"
E       AssertionError: sustanability_invalid_report.json failed: ['.company_name: expected string, got int', '.reporting_year: expected integer, got bool', '.total_emissions_tco2e: -50 is less than minimum 0', '.renewable_energy_percent: 120 is greater than maximum 100', ".reporting_status: 'complete' not in allowed values ['draft', 'reviewed', 'published']", '.is_third_party_verified: expected boolean, got str', '.company_name: expected string, got int', '.reporting_year: expected integer, got bool', '.total_emissions_tco2e: -50 is less than minimum 0', '.renewable_energy_percent: 120 is greater than maximum 100', ".reporting_status: 'complete' not in allowed values ['draft', 'reviewed', 'published']", '.is_third_party_verified: expected boolean, got str', '.company_name: expected string, got int', '.reporting_year: expected integer, got bool', '.total_emissions_tco2e: -50 is less than minimum 0', '.renewable_energy_percent: 120 is greater than maximum 100', ".reporting_status: 'complete' not in allowed values ['draft', 'reviewed', 'published']", '.is_third_party_verified: expected boolean, got str', '.company_name: expected string, got int', '.reporting_year: expected integer, got bool', '.total_emissions_tco2e: -50 is less than minimum 0', '.renewable_energy_percent: 120 is greater than maximum 100', ".reporting_status: 'complete' not in allowed values ['draft', 'reviewed', 'published']", '.is_third_party_verified: expected boolean, got str', '.company_name: expected string, got int', '.reporting_year: expected integer, got bool', '.total_emissions_tco2e: -50 is less than minimum 0', '.renewable_energy_percent: 120 is greater than maximum 100', ".reporting_status: 'complete' not in allowed values ['draft', 'reviewed', 'published']", '.is_third_party_verified: expected boolean, got str']
E       assert ['.company_na...got str', ...] == []
E         
E         Left contains 30 more items, first extra item: '.company_name: expected string, got int'
E         
E         Full diff:
E         - []
E         + [
E         +     '.company_name: expected string, got int',...
E         
E         ...Full output truncated (35 lines hidden), use '-vv' to show

test_jsonSchemaValidator.py:22: AssertionError
============================================================================================================== warnings summary ===============================================================================================================
../../../../../Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/_pytest/python.py:124
  /Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/_pytest/python.py:124: PytestRemovedIn10Warning: Passing a non-Collection iterable to parametrize is deprecated.
  Test: test_jsonSchemaValidator.py::test_valid_report, argvalues type: map
  Please convert to a list or tuple.
  See https://docs.pytest.org/en/stable/deprecations.html#parametrize-iterators
    metafunc.parametrize(*marker.args, **marker.kwargs, _param_mark=marker)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================================================================================================== short test summary info ===========================================================================================================
FAILED test_jsonSchemaValidator.py::test_valid_report[sustanability_invalid_report.json] - AssertionError: sustanability_invalid_report.json failed: ['.company_name: expected string, got int', '.reporting_year: expected integer, got bool', '.total_emissions_tco2e: -50 is less than minimum 0', '.renewable_energy_percent: 120...
=================================================================================================== 1 failed, 1 passed, 1 warning in 0.07s ====================================================================================================