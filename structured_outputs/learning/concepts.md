# Concepts

Reusable notes from the product extraction exercise, through 2 November 2026. This is a starting summary to review and rewrite in my own words. Statements about work completed belong in [journal.md](journal.md).

## Schema generation, extraction, validation, and evaluation

These are separate responsibilities:

1. **Schema generation:** describe the output contract as JSON Schema.
2. **Extraction:** ask the model to turn a description into structured data.
3. **Validation:** check the returned structure, types, and declared constraints.
4. **Evaluation:** compare extracted values with human-written expected answers.

A valid numeric price can still be the wrong price. Schema validation cannot establish that the model chose the correct fact from the description.

My handwritten generator and Pydantic are alternative ways to produce a schema. Using an API does not require replacing my generator with Pydantic.

## Required versus nullable versus default

- **Required:** the key must be supplied.
- **Nullable:** the value may be null.
- **Default:** the value used when a field is omitted.

In Pydantic V2:

```python
brand: str | None = Field()
```

The key is required; its value may be a string or None.

```python
brand: str | None = None
```

The key may be omitted; its default is None.

An absent key, JSON null, and the string "null" are three different things. Python represents JSON null as None.

## Field types and defaults in Pydantic

The structure is `field_name: allowed_type = field_configuration`.

The first positional argument to `Field()` supplies a default value. Types belong in the annotation after the colon.

```python
features: list[str] | None = Field()
```

This declares a required field accepting a list of strings or None. `Field(list[str])` instead supplies a type expression as the default, which was the cause of one warning I encountered.

A comma after the complete assignment expression creates a tuple:

```python
name: str = Field(),
```

This is not the same as `name: str = Field()`. Commas between arguments inside a function call serve a different purpose.

## JSON Schema keywords

| Keyword | Meaning |
| --- | --- |
| type | Kind of value: string, number, integer, array, object, etc. |
| properties | Rules for named object fields |
| required | Keys that must appear |
| items | Rules for each array element |
| enum | Allowed complete values at that position |
| anyOf | At least one alternative must match |
| minimum / maximum | Numeric bounds |
| additionalProperties | Rules for undeclared keys |
| description | Documentation that can also guide the model |

An enum beside an array constrains the entire array. An enum inside items constrains each element. Requiring an array while enumerating only string values creates conflicting requirements.

`$defs` holds reusable definitions; `$ref` points to one. Pydantic used these for my currency and weight-unit enums. A `title` is metadata, not a required output field.

## Enums and validation

Python Enum or Literal types can express allowed values in Pydantic and generate the corresponding JSON Schema restrictions.

Adding an enum through json_schema_extra changes schema metadata; it does not by itself create the same runtime Pydantic validation rule.

## Meaning, normalization, and structural constraints

- **Meaning:** which information belongs in a field? Example: product weight rather than shipping weight.
- **Normalization:** how should equivalent information be represented? Example: kilograms becomes kg; colors become lowercase.
- **Constraint:** which values are structurally permitted? Example: warranty_months is a nonnegative integer or null.

Descriptions guide extraction but do not automatically enforce their wording. Enforce suitable rules through types, constraints, or separate checks; assess factual choices against labels.

Normalization must preserve meaning and be applied consistently in expected answers. If converting 238 g to kilograms, the exact value is 0.238 kg, not 0.23 kg. Whether to convert at all is a separate policy decision.

## Missing information is not an explicit absence

For warranty:

| Source | Expected interpretation |
| --- | --- |
| One-year warranty | 12 months |
| Explicitly no warranty | 0 months |
| Warranty not discussed | null |

A product may have a market price without the supplied description stating it. Extraction should use the supplied evidence rather than guess missing facts.

MRP means Maximum Retail Price. The exercise separates an explicitly identified original/reference price from the current advertised purchase price.

## Serialization and parsing

Serialization converts data into a format for storage or transmission. JSON is one format.

Actual data such as a list of strings can be serialized to JSON. A Python type expression such as list[str] is not itself ordinary JSON data.

Parsing reads serialized text into usable data. JSON text, a Python dictionary, and a Pydantic model instance are different representations.

## What model_validate_json does

`Product.model_validate_json(response_text)` parses JSON text, validates against Product, and returns a Product instance. Invalid input raises a ValidationError.

Printing that instance shows a Python representation such as `brand=None` and an enum member. It is not the original API response text.

Preserve both the raw response and any validated representation. Pydantic can coerce compatible values by default; this can hide raw type errors if evaluation only examines the converted object. Choose strict checks deliberately and verify their behavior with representative inputs.

## SDK calls and structured output

An SDK wraps HTTP requests, handling endpoint details, request encoding, and authentication. A client method is still making an API request even when no REST URL appears in my code.

In the Gemini Interactions call used in this exercise, the generated schema is passed under response_format.schema, alongside the JSON MIME type. Provider support for JSON Schema may be narrower than the full specification.

Schema in a prompt is an instruction; schema passed through a supported structured-output setting also supplies a generation constraint. Neither proves factual extraction accuracy.

## Evaluation metrics

| Metric | Working definition for this exercise |
| --- | --- |
| Exact match | Completely correct examples divided by all attempted examples |
| Per-field accuracy | Correct predictions for one field divided by its evaluated examples |
| Overall field accuracy | Correct expected field slots divided by all expected field slots |
| Record type compliance | Examples with all required keys and allowed field types divided by all attempted examples |
| Schema compliance | Compliance with the full contract, including bounds, enums, and extra-key rules |

With 50 complete examples and 13 required fields, there are 650 expected field slots. Invalid JSON and request failures remain accounted for rather than disappearing from the denominator.

Ignore JSON whitespace and object key order. Decide list ordering, normalization, and equality rules before scoring. A negative number may pass a number type check while failing a minimum constraint.

## Error analysis and answer keys

Human-written expected outputs are the answer key. Check them against the contract too; label mistakes can make a correct prediction look wrong.

Useful error categories are hallucination, omission, wrong value, format error, type error, and missing field. They can overlap, so document a primary-category policy or allow multiple labels explicitly.

Cross-tab field versus error category and field versus description tag. Include denominators; overlapping tags are not parts of a single total. Read individual failures to understand what aggregate accuracy hides.

Write labels independently of predictions where possible. For feature lists, equivalent paraphrases may fail exact comparison: decide the extraction and scoring policy before treating such differences as factual failures.

## Journal, concepts, and references

- Journal: what I tried, observed, misunderstood, and will do next.
- Concepts: reusable explanations and examples worth retaining.
- Physical notes can be rough. Explaining them to an LLM can help organize digital notes, but I should review every claim and retain my reasoning.
- A digital reference inbox can assign labels such as R1; physical notes can refer to those labels instead of copying URLs.

## References

- [Course learning routine](https://aiengineeringfromscratch.com/how-to-learn)
- [Structured outputs lesson](https://aiengineeringfromscratch.com/lesson?path=phases%2F11-llm-engineering%2F03-structured-outputs&learningPath=applied-ai-engineer)
- [Exercise guide and working notes](https://chatgpt.com/space/page_8ecc6a5c0a5c81918e039615c5fe60fb)
- [Pydantic Field reference](https://docs.pydantic.dev/latest/api/fields/#pydantic.fields.Field)
- [Pydantic default values](https://docs.pydantic.dev/latest/concepts/fields/#default-values)
- [Pydantic JSON parsing](https://docs.pydantic.dev/latest/concepts/json/)
- [Pydantic strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/)
- [JSON Schema objects](https://json-schema.org/understanding-json-schema/reference/object)
- [JSON Schema arrays](https://json-schema.org/understanding-json-schema/reference/array)
- [JSON Schema enum](https://json-schema.org/understanding-json-schema/reference/enum)
- [Gemini structured outputs](https://ai.google.dev/gemini-api/docs/structured-output)

