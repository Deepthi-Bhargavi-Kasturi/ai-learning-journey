## 10 November 2026 — Comparing extraction outputs and calculating accuracy

**Focus:** Understand how to compare expected and predicted product data and calculate accuracy.

### What I tried

I looped through product records and their fields, then passed individual values to `accuracy_score()`. The values included strings, numbers, lists, and `None`.

### Errors and what they taught me

- `list(None)` fails because `None` is not iterable.
- `list("Bose")` splits the string into characters; it does not represent one brand label.
- `accuracy_score(True, False)` fails because the function expects collections, not individual Boolean values.
- Mixing list-valued fields with string placeholders causes incompatible classification inputs.
- A sparse array stores nonzero values efficiently. My evaluator does not need sparse arrays; regular lists are sufficient.

### What I understand now

I need to separate **comparison** from **aggregation**:

1. Match products by ID.
2. Compare corresponding values using my agreed rules.
3. Collect the Boolean results.
4. Calculate accuracy from those results.

For **per-field accuracy**, collect the same field’s match results across all products. For example, brand matches might be `[True, True, False]`. Comparing these with `[True, True, True]` gives brand accuracy.

Collecting all field results within one product measures that product’s field accuracy. A product passes **exact match** only when every expected field matches and there are no extra keys.

A missing key must remain distinguishable from a key explicitly containing null.

### Where help was needed

I initially treated `accuracy_score()` as a general-purpose comparator. I needed help understanding that it expects supported classification inputs. My evaluator must first decide whether each mixed-type field matches.

### Where I stopped

The collection-based Boolean comparison works. I identified that I need to group results by field across products rather than calculate each field’s score separately within a product.


**Reference:** [scikit-learn accuracy_score documentation](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html)

# 5th November 2026

- Working on measuring exact match 
- learning about accuracy_score()
- learnt about score() and difference between accuracy_score() and score()

Ref:
https://scikit-learn.org/stable/modules/model_evaluation.html#accuracy-score
https://www.geeksforgeeks.org/machine-learning/difference-between-score-and-accuracy_score-methods-in-scikit-learn/

# 4th November 2026

OpenAI structured outputs

- Documentation [link](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses) for API call details and parameters to be passed

For practice, I have used LLM - chat interface. Once code in place, I will call real time API and check the final result.

## Definition checks suggested by Codex:

| Case | Expected interpretation under these proposals |
| - | - |
| Sold by TechMart. Brand Acme. | brand is Acme, not TechMart. |
| Product weight 1.5 kg. Shipping weight 2 kg. | weight is 1.5 and weight_unit is kg. |
| Product dimensions 30 × 20 × 2 cm. Box 40 × 30 × 10 cm. | dimensions comes from the product measurement. |
| Warranty one year. Returns accepted for 30 days. | warranty_months is 12; the return period is excluded. |
| Black laptop. Also available in silver. | color describes the black advertised variant. |
| Originally ₹1,999, now ₹1,499. | original_price is 1999 and listed_price is 1499. |

<u>**Prompt**</u>: Extract product details from: The Bose NEW QuietComfort Wireless Noise Cancelling Headphones sold by TechMart, are premium over-ear Bluetooth headphones featuring legendary active noise cancellation that lets you switch between Quiet Mode (full ANC) and Aware Mode (ambient sound). They deliver high-fidelity audio with an adjustable EQ for personalised bass, mid-range, and treble control, backed by up to 24 hours of battery life and a quick 15-minute charge that adds 2.5 hours of playback. Weighing just 238 g with shipping weight 300 g, they come with plush earcup cushions and a padded headband for all-day comfort, Bluetooth 5.0 with a 10-metre range, and multi-device connectivity — available in seven colours including Black, White, and Petal Pink. It comes with one year warranty. Returns accepted for 30 days.

```json
{
"name": "Bose NEW QuietComfort Wireless Noise Cancelling Headphones",

"brand": "Bose",

"dimensions": null,

"original_price": null,

"listed_price": null,

"currency": null,

"color": ["black", "white", "petal pink"],

"weight": 238,

"weight_unit": "g",

"material": null,

"warranty_months": 12,

"categories": ["Headphones"],

"features": ["Active noise cancellation","Quiet Mode and Aware Mode","High-fidelity audio",
"Adjustable EQ for bass, mid-range, and treble","Up to 24 hours of battery life",
"15-minute charge adds 2.5 hours of playback","Plush earcup cushions","Padded headband",
"Bluetooth 5.0", "10-metre Bluetooth range","Multi-device connectivity"
]

}

```

&#x20; <u>**Case**</u>: It is priced originally ₹1,999, now ₹1,499

- My Prediction: {"original_price": 1999,"listed_price": 1499, “currency” : “Rupees”}

- LLM Prediction:&#x20;

  - "original_price": 1999,\
    &#x20; "listed_price": 1499,\
    &#x20; "currency": "Rupees"

Prompt: The Apple 2026 MacBook Neo 13″ is a sleek, lightweight laptop powered by the A18 Pro chip built for AI and Apple Intelligence, packed into a durable aluminium body available in four vibrant colours — Silver, Blush, Citrus, and Indigo. It features a stunning 33.02 cm (13″) Liquid Retina display with a 2408×1506 resolution, up to 500 nits of brightness, and support for a billion colours, paired with 8GB DDR5 unified memory, 256GB SSD storage, and a 1080p FaceTime HD camera. Weighing just 1.22 kg and offering up to 16 hours of battery life, it's designed for students and everyday users who need all-day performance without compromise.&#x20;



```json
My Prediction:
{

"name": "Apple 2026 MacBook Neo 13",

"brand": "Apple",

"dimensions": null --33.02 cm (13″),

"original_price": null,

"listed_price": null,

"currency": null,

"color": ["silver", "blush", "citrus", "indigo"],

"weight": 1.22,

"weight_unit": "kg",

"material": "aluminium",

"warranty_months": null,

"categories": ["Laptop"],

"features": ["sleek, lightweight laptop","A18 Pro chip","stunning 33.02 cm (13″) Liquid Retina display",

"2408×1506 resolution","500 nits of brightness",

"8GB DDR5 unified memory","256GB SSD storage","1080p FaceTime HD camera",

"up to 16 hours of battery life"

]

}
```

Note: `dimensions` is null because screen size and resolution do not establish the laptop’s physical dimensions.

<u>**Prompt**</u>: The ISDIN Fotoprotector Fusion Water Magic Color SPF 50 is a next-generation tinted facial sunscreen from the Spanish skincare brand ISDIN, designed for those who want sun protection and a natural, radiant finish in a single step. Formulated with an ultralight, water-based texture, it absorbs instantly into the skin without leaving any greasy residue — making it ideal for everyday use, even on oily or acne-prone skin. With SPF 50 and PA++++ broad-spectrum protection, it shields against both UVA and UVB rays to prevent sunburn, dark spots, hyperpigmentation, and premature ageing. The formula is enriched with Hyaluronic Acid for deep, lasting hydration and features a universal medium tint that blurs imperfections and evens out the skin tone for a healthy 'no-makeup' look. It is oil-free, non-comedogenic, hypoallergenic, and fragrance-free, with Safe-Eye Tech that ensures no stinging around the eyes — making it suitable for all skin types, including sensitive skin. Weighing just 52 g and available in a 50 ml tube, it's a travel-friendly everyday essential that beautifully replaces both your moisturiser and foundation.

```json
Model generated output:

{
  "name": "ISDIN Fotoprotector Fusion Water Magic Color SPF 50",
  "brand": "ISDIN",
  "dimensions": null,
  "original_price": null,
  "listed_price": null,
  "currency": null,
  "color": ["medium"],
  "weight": 52,
  "weight_unit": "g",
  "material": null,
  "warranty_months": null,
  "categories": ["Sunscreen"],
  "features": [
    "Tinted facial sunscreen",
    "Ultralight, water-based texture",
    "Fast absorption without greasy residue",
    "SPF 50 and PA++++",
    "Broad-spectrum UVA and UVB protection",
    "Hyaluronic Acid for hydration",
    "Universal medium tint",
    "Blurs imperfections and evens skin tone",
    "Oil-free",
    "Non-comedogenic",
    "Hypoallergenic",
    "Fragrance-free",
    "Safe-Eye Tech",
    "Suitable for all skin types, including sensitive skin"
  ]
}
```
