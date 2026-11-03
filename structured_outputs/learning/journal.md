Learning journal

Retrospective starting record through 2 November 2026, based on this chat and my updated exercise document. This summarizes reported work; it is not a fresh verification of the local implementation. Earlier sessions are grouped rather than assigned invented dates.

## Goal

Build an extraction evaluation suite for 50 product descriptions: human-written expected JSON, exact match, field-level accuracy, type compliance, and an explanation of the hardest fields.

I want to understand and implement the work myself. Assistance should begin with hints and questions when I am stuck. I also want practical habits that can carry into production work.

## 28 to 30 October 2026 — Output contract and missing information

**Worked on:** A handwritten product schema and the meaning of its fields.

**Changes and discoveries:**

- Distinguished array item constraints from enum constraints on the complete field.
- Separated original_price from listed_price to avoid overloading one price field.
- Made all 13 output keys required while allowing unknown values for applicable fields.
- Distinguished a missing key from a key containing null.
- Established that missing warranty information is unknown, while explicitly no warranty means zero months.
- Discussed field meanings, normalization, and separate weight–unit consistency checks.
- Created a reference Page with deliverables, small examples, and validation cases.

**Still to settle through examples:** Product-name boundaries, feature-list boundaries, list comparison order, category scope, and treatment of partial measurements.

## 30 October to 2 November 2026 — Schema generation and API integration

**Worked on:** My own SchemaField class, recursive schema generation, and later a Pydantic Product model.

**What I reported building:** A handwritten generator and validation functionality. The validation implementation has not been reviewed in this conversation.

**Observed obstacle:** NVIDIA free API calls were taking too long. Discussed usage-based APIs and moved to a Gemini SDK call.

**Learned:**

- My own schema dictionary can be supplied to a supported API; Pydantic is an alternative, not a requirement.
- The SDK handles the HTTP endpoint and request details.
- Pass the schema through response_format.schema for the Gemini Interactions call.
- My prompt variable was unused when the call passed product directly. A plain string containing {product} does not interpolate it.

**Troubleshooting record:**

| Symptom | What I learned or changed |
| --- | --- |
| Quoted attribute name in a Pydantic class | Class field identifiers are unquoted; dictionary keys are different. |
| enum passed directly to Field produced a deprecation warning | Use a validating enum/type declaration for allowed values rather than relying on extra schema metadata. |
| Tuple containing FieldInfo was not serializable | A trailing comma after Field(...) created a tuple. |
| list[str] default was not serializable | The first positional Field argument is the default; list item types belong in the annotation. |

**Credential follow-up:** A key appeared in shared code. Revoke and replace it, and load credentials outside source code. Completion has not been confirmed. Do not copy the key into notes or Git.

## 2 November 2026 — Pydantic schema and first observed extraction

**Schema observed:** Product.model_json_schema() generated all 13 required fields, reusable enum definitions, and nullable alternatives.

**Latest shared model:**

- Currency is one CurrencyEnum value or None, rather than an array.
- Weight unit uses WeightUnitEnum with kg and g.
- Categories and features are lists of strings or None.
- The shown model does not include an extra='forbid' configuration.
- Categories currently accept arbitrary strings; a restricted category enum is not present in the shared version.

**Dataset progress:** Selected three inputs: Bose headphones, Apple laptop, and ISDIN sunscreen. All omit price and warranty information. These are useful missing-information cases but do not yet cover those fields when present.

**Bose run observed:** Called Gemini, validated response text with Product.model_validate_json(), and printed a Product instance. It contained Bose as brand, weight 238.0 g, lowercase named colors, null prices and warranty, and a paraphrased feature list. Categories included both Headphones and Over-ear Headphones.

**Important distinction:** The printed Product instance is not raw JSON text. Structural validation success does not establish extraction accuracy.

### My handwritten prediction recorded in the Page

I added an expected Bose output and troubleshooting notes to the working document. That draft still needs review before it becomes the scoring reference:

- Several absent values are written as quoted "null"; actual JSON null is unquoted.
- Colors use title case, while my extraction rule asks for lowercase.
- Weight is written as 0.23 kg. Source weight is 238 g; exact conversion would be 0.238 kg. I still need a consistent preserve-or-convert policy.
- Name boundaries differ between my prediction and the model output. Resolve this using a labeling rule, not by accepting whichever the model produced.
- Feature lists differ in wording and granularity. Decide the expected policy before scoring.
- The example uses typographic quotation marks and is missing a separator after weight_unit; it needs valid JSON syntax before machine validation.

These are label-review findings, not measured model failures. No evaluation scores have been calculated in the shared work yet.

### Working document needs reconciliation

Some older guide text still describes currency as a non-nullable array, categories as enum-restricted, and extra keys as already rejected. That does not match the latest shared Pydantic model. The old warranty table wording also needs the explicit-no-warranty clarification. Preserve my original notes and reconcile these deliberately rather than treating every section as current.

## Current checkpoint

- [x] Defined an initial 13-field product contract.
- [x] Wrote and shared a handwritten schema generator.
- [x] Generated a schema from a Pydantic Product model.
- [x] Supplied three candidate descriptions.
- [x] Recorded a draft expected output for Bose in the Page.
- [x] Observed one Gemini extraction and a validated Product instance.
- [ ] Review the Bose reference answer against the agreed rules and validate its JSON.
- [ ] Check extra-key and category restrictions in the current model.
- [ ] Preserve raw responses separately from validated instances.
- [ ] Verify evaluator behavior on manually constructed predictions.
- [ ] Complete 50 human-labeled examples and run the evaluation.
- [ ] Calculate metrics and inspect error patterns.

## Next session

**First action:** Review the Bose expected answer from the source description, correcting syntax, null representation, and normalization without copying the model prediction.

**Then:** Validate the reference answer locally. Keep prediction, expected answer, and any unresolved labeling choices separate. Start implementing scoring with manually supplied outputs before scaling API calls.

## Note-taking habit going forward

I will keep rough physical notes, explain what I learned, and use an LLM to organize digital notes. I will review the result and check that I can explain every sentence.

At the end of a session, capture where I stopped and the next small action. Move reusable explanations into [concepts.md](concepts.md); do not transcribe every conversational step.

### Future entry template

- **Date and focus:**
- **My prediction or question:**
- **What I tried:**
- **What I observed:**
- **What changed in my understanding:**
- **Where help was needed:**
- **Where I stopped and next action:**
- **References or concept links:**

## References

- [Reusable concepts and documentation links](concepts.md)
- [Course lesson](https://aiengineeringfromscratch.com/lesson?path=phases%2F11-llm-engineering%2F03-structured-outputs&learningPath=applied-ai-engineer)
