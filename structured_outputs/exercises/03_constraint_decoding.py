# Implement a more realistic constrained decoding simulator. 
# Given a JSON Schema and a vocabulary of 100 tokens (letters, digits, punctuation, keywords), 
# walk through generation step by step, masking invalid tokens at each position. 
# Measure what percentage of the vocabulary is valid at each step.


#Exercise is to build a small imitation of how structured-output constrained decoding works

#Need:
#A JSON Schema - using ai-learning-journey/structured_outputs/tests/sustainability_valid_report.json
#A fake vocabulary of 100 possible tokens
#A partial JSON output
#Code that decides which tokens are allowed next


# Partial JSON + parser state + schema
#         ↓
# Find valid next tokens
#         ↓
# Mask/remove invalid tokens from the 100-token vocabulary
#         ↓
# Choose one valid token and continue

#SCHEMA RULES:
# Block } while required fields are still missing.
# Block , after the maximum number of array items.
# Restrict property names to keys defined in properties.
# Enforce enum values while generating strings.
# Add a final root } test state that returns ["<EOS>"].


#Create a fake Vocabulary of 100 tokens

import string
import re
from pathlib import Path
import json

jsonSchemaFile = Path("schemas/sustainability_report_schema.json")

STRUCTURAL_TOKENS = [
    "{", "}", "[", "]",
    '"', ":", ",", ".", "-", "_",
    " ", "\n", "<EOS>", "'", ";"
]

LOWERCASE_TOKENS = list(string.ascii_lowercase)

UPPERCASE_TOKENS = list(string.ascii_uppercase)

DIGIT_TOKENS = list("0123456789")

KEYWORD_TOKENS = ["true", "false", "null", "undefined"]

EXTRA_TOKENS = [
    "scope", "carbon", "solar", "wind", "audit",
    "draft", "published", "company", "report",
    "sustainability", "emission", "energy", "water",
     "world", "@", "#", "?", "=", "/",
]


VOCABULARY = (
        STRUCTURAL_TOKENS +
        LOWERCASE_TOKENS +
        UPPERCASE_TOKENS +
        DIGIT_TOKENS +
        KEYWORD_TOKENS +
        EXTRA_TOKENS
)

vocabulary_len = len(VOCABULARY)
print(vocabulary_len)


#First measure what percentage of the vocabulary is valid at each step

from build_constraint_decoding import next_valid_tokens

def calc_valid_token_percentage() :

    schemaObject = json.loads(jsonSchemaFile.read_text())

    partial_states = [
        '',
        '{',
        '{"unknown_key"',
        '{"company_name"',
        '{"company_name":',
        '{"company_name": "',
        '{"company_name": "GreenLeaf F',
        '{"company_name": "GreenLeaf Foods"',
        '{"company_name": "GreenLeaf Foods",',
        '{"company_name": "GreenLeaf Foods","',
        '{"company_name": "GreenLeaf Foods", "reporting_year":',
        '{"reporting_year": "',
        '{"company_name": "GreenLeaf Foods", "reporting_year": 2025',
        '{"company_name": "GreenLeaf Foods", "reporting_year": 2025, "total_emissions_tco2e": 12450.',
        '{"company_name": "GreenLeaf Foods", "reporting_year": 2025, "total_emissions_tco2e": 12450.75',
        '{"company_name": "GreenLeaf Foods", "reporting_year": 2025, "total_emissions_tco2e": 12450.75, "renewable_energy_percent": 62.5, "reporting_status": "reviewed","is_third_party_verified":',
        '{"company_name": "GreenLeaf Foods", "reporting_year": 2025, "total_emissions_tco2e": 12450.75, "renewable_energy_percent": 62.5, "reporting_status": "reviewed", "is_third_party_verified":true,',
        '{"company_name": "GreenLeaf Foods", "reporting_year": 2025, "total_emissions_tco2e": 12450.75, "renewable_energy_percent": 62.5, "reporting_status": "reviewed", "is_third_party_verified":true, "sites" : ',
        '{"company_name": "GreenLeaf Foods", "reporting_year": 2025, "total_emissions_tco2e": 12450.75, "renewable_energy_percent": 62.5, "reporting_status": "reviewed", "is_third_party_verified":true, "sites" : [}',
        '{"company_name": "GreenLeaf Foods", "reporting_year": 2025, "total_emissions_tco2e": 12450.75, "renewable_energy_percent": 62.5, "reporting_status": "reviewed", "is_third_party_verified":true, "sites" : []',
        '{"company_name": "GreenLeaf Foods", "reporting_year": 2025, "total_emissions_tco2e": 12450.75, "renewable_energy_percent": 62.5, "reporting_status": "reviewed", "is_third_party_verified":true, "sites" : [',
        '{"company_name": "GreenLeaf Foods", "reporting_year": 2025, "total_emissions_tco2e": 12450.75, "renewable_energy_percent": 62.5, "reporting_status": "reviewed", "is_third_party_verified":true, "sites" : [{',
        '{"company_name": "GreenLeaf Foods", "reporting_year": 2025, "total_emissions_tco2e": 12450.75, "renewable_energy_percent": 62.5, "reporting_status": "reviewed", "is_third_party_verified":true, "sites" : [{ "site_name": "Bengaluru Office","country": "India","annual_energy_kwh": 85000.0},{"site_name": "Chennai Factory","country": "India"',
        '{"company_name": "GreenLeaf Foods", "reporting_year": 2025, "total_emissions_tco2e": 12450.75, "renewable_energy_percent": 62.5, "reporting_status": "reviewed", "is_third_party_verified":true, "sites" : [{ "site_name": "Bengaluru Office","country": "India","annual_energy_kwh": 85000.0},{"site_name": "Chennai Factory","country": "India","annual_energy_kwh": 350500',
        '{"company_name": "GreenLeaf Foods", "reporting_year": 2025, "total_emissions_tco2e": 12450.75, "renewable_energy_percent": 62.5, "reporting_status": "reviewed", "is_third_party_verified":true, "sites" : [{ "site_name": "Bengaluru Office","country": "India","annual_energy_kwh": 85000.0},{"site_name": "Chennai Factory","country": "India","annual_energy_kwh": 350500}',
        '{"company_name": "GreenLeaf Foods", "reporting_year": 2025, "total_emissions_tco2e": 12450.75, "renewable_energy_percent": 62.5, "reporting_status": "reviewed", "is_third_party_verified":true, "sites" : [{ "site_name": "Bengaluru Office","country": "India","annual_energy_kwh": 85000.0},{"site_name": "Chennai Factory","country": "India","annual_energy_kwh": 350500}]',
        '{"company_name": "GreenLeaf Foods", "reporting_year": 2025, "total_emissions_tco2e": 12450.75, "renewable_energy_percent": 62.5, "reporting_status": "reviewed", "is_third_party_verified":true, "sites" : [{ "site_name": "Bengaluru Office","country": "India","annual_energy_kwh": 85000.0},{"site_name": "Chennai Factory","country": "India","annual_energy_kwh": 350500}]}'
            
    ]

    

    print(f"{'Valid Next Tokens %':<25} {'Valid Next Tokens'}")
    print("-" * 90)

    for state in partial_states :
        valid = next_valid_tokens(state, schemaObject)
        display = state if state else "(empty)"
        valid_next_tokens_per = f"{(len(valid)/vocabulary_len)*100:.2f} %"
        print(f"{valid_next_tokens_per:<35} {valid}")

        

    



if __name__ == "__main__" :
    calc_valid_token_percentage()