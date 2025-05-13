**System Prompt**
You are an expert AI assistant creating high-quality training data to fine-tune another LLM. The target LLM will specialize in **mapping raw real estate data from various formats to a standardized canonical JSON schema (`CanonicalRecord`)**.

**Your Task:**
Given a RAW PROPERTY DATA SNIPPET and its ORIGINAL SOURCE TYPE and ORIGINAL SOURCE IDENTIFIER, you must generate a fine-tuning example in a specific conversational JSON format. The example should contain:
1.  A "user" turn:
    *   Clear instructions for the target LLM, including the request to output ONLY the mapped JSON.
    *   The complete `CanonicalRecord` JSON schema definition.
    *   The RAW PROPERTY DATA SNIPPET.
    *   Information about the `ORIGINAL_SOURCE_TYPE` and `ORIGINAL_SOURCE_IDENTIFIER`.
2.  A "model" turn:
    *   The ideal, gold-standard JSON output string, perfectly conforming to the `CanonicalRecord` schema, accurately mapped from the RAW PROPERTY DATA SNIPPET.

**CanonicalRecord Schema Definition (for Real Estate):**
```json
{
  "title": "CanonicalRecord",
  "type": "object",
  "properties": {
    "canonical_record_id": {"type": "string", "description": "Unique identifier for this canonical record.", "examples": ["cre-SOME_UUID"]},
    "original_source_identifier": {"type": "string", "description": "Identifier of the original source (e.g., URL, filename + row index)."},
    "original_source_type": {"type": "string", "description": "Type of the original source adapter ('api', 'file', 'scrape')."},
    "entity_type": {"type": "string", "enum": ["RealEstateListing", "NewsArticle", "Other"], "default": "Other", "description": "Classification of the source entity."},
    "mapping_model_version": {"type": ["string", "null"], "description": "Version identifier of the ML model used for mapping."},
    "mapping_timestamp": {"type": "string", "format": "date-time", "description": "Timestamp (UTC) when the mapping was performed."},
    "address": {
      "title": "Address", "type": ["object", "null"],
      "properties": {
        "street_address": {"type": ["string", "null"]}, "city": {"type": ["string", "null"]},
        "state_province": {"type": ["string", "null"]}, "postal_code": {"type": ["string", "null"]},
        "country": {"type": ["string", "null"], "default": "USA"}
      }
    },
    "features": { /* ... (full features schema as before) ... */ },
    "listing": { /* ... (full listing schema as before) ... */ },
    "agent": { /* ... (full agent schema as before) ... */ },
    "description": {"type": ["string", "null"]},
    "image_urls": {"type": ["array", "null"], "items": {"type": "string", "format": "uri"}},
    "raw_source_data": {"type": ["object", "null"], "description": "Original source data record (JSON representation)."}
  },
  "required": ["original_source_identifier", "original_source_type", "entity_type"]
}
```

**Output Format (JSON):**
Your entire output must be a single JSON object matching this structure:
```json
{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "You are a data mapping assistant. Your task is to map the provided 'Raw Property Data Snippet' to the 'CanonicalRecord Schema Definition'. \n\nRULES:\n- Your entire response must be ONLY the mapped JSON object string, conforming strictly to the CanonicalRecord schema.\n- Do NOT include any explanatory text before or after the JSON object.\n- Set 'original_source_type' to: <ORIGINAL_SOURCE_TYPE_PROVIDED_TO_YOU>\n- Set 'original_source_identifier' to: <ORIGINAL_SOURCE_IDENTIFIER_PROVIDED_TO_YOU>\n- Set 'entity_type' to 'RealEstateListing'.\n- For the 'raw_source_data' field in the output, include the exact 'Raw Property Data Snippet' you were given.\n- Perform necessary data transformations (e.g., string prices to numbers, parse dates, extract address components).\n- If information for a canonical field is not present, use `null` or omit optional fields as per the schema.\n\nCanonicalRecord Schema Definition:\n<PASTE_THE_FULL_JSON_SCHEMA_STRING_HERE>\n\nOriginal Source Type: <ORIGINAL_SOURCE_TYPE_PROVIDED_TO_YOU>\nOriginal Source Identifier: <ORIGINAL_SOURCE_IDENTIFIER_PROVIDED_TO_YOU>\n\nRaw Property Data Snippet:\n<RAW_PROPERTY_DATA_SNIPPET_JSON_STRING_HERE>\n\nNow, provide ONLY the mapped JSON object string:\n\n"
        }
      ]
    },
    {
      "role": "model",
      "parts": [
        {
          "text": "<GOLD_STANDARD_CANONICALRECORD_JSON_STRING>"
        }
      ]
    }
  ]
}
```

**Instructions for You (the Data Generator LLM):**
*   You will be given:
    1.  `ORIGINAL_SOURCE_TYPE`: e.g., "api", "file", "scrape"
    2.  `ORIGINAL_SOURCE_IDENTIFIER`: e.g., "https://dummyjson.com/products/1", "property_data.csv-row-5", "https://www.baania.com/..."
    3.  `RAW_PROPERTY_DATA_SNIPPET`: The actual JSON/dictionary data extracted from the source.
*   **Construct the "user" text:** Carefully substitute the placeholders `<ORIGINAL_SOURCE_TYPE_PROVIDED_TO_YOU>`, `<ORIGINAL_SOURCE_IDENTIFIER_PROVIDED_TO_YOU>`, `<PASTE_THE_FULL_JSON_SCHEMA_STRING_HERE>`, and `<RAW_PROPERTY_DATA_SNIPPET_JSON_STRING_HERE>` in the user prompt template.
*   **Construct the "model" text:** This part must be a **JSON string** representing the fully mapped `CanonicalRecord`.
    *   Set `original_source_type` and `original_source_identifier` in the JSON string to the values provided.
    *   Set `entity_type` to "RealEstateListing".
    *   Set `canonical_record_id` to a placeholder like "cre-GENERATED-UUID".
    *   Set `raw_source_data` in the JSON string to the `RAW_PROPERTY_DATA_SNIPPET` you were given.
    *   Meticulously map all other fields. Perform transformations. Use `null` for missing optional data.
*   Ensure the "model" part is a valid JSON string that, when parsed, conforms to the `CanonicalRecord` schema.

---
**Now, I will provide you with the input parts. Generate the fine-tuning example JSON using the JSON MAPPING meta-prompt.**

**INPUT FOR YOU (THE GENERATOR LLM):**

1.  `ORIGINAL_SOURCE_TYPE`: "scrape"
2.  `ORIGINAL_SOURCE_IDENTIFIER`: "https://www.baania.com/some-property-link-v2"
3.  `RAW_PROPERTY_DATA_SNIPPET` (as a JSON string for easy insertion into the user prompt):
    ```json
    {
      "projectName": "The Oasis Residence",
      "propertyType": "Condominium",
      "priceInfo": {
        "amount": 7800000,
        "unit": "THB"
      },
      "location": {
        "building": "Tower A",
        "street": "Sukhumvit Soi 31",
        "district": "Wattana",
        "city": "Bangkok",
        "postalCode": "10110"
      },
      "attributes": {
        "num_bedrooms": "2 Bedrooms",
        "num_bathrooms": "2",
        "area": "75 SQ.M.",
        "floor": "15th"
      },
      "title": "Luxury 2 Bed Condo, High Floor, Sukhumvit",
      "full_description": "Modern luxury condominium unit on a high floor in Tower A of The Oasis Residence. Offers stunning city views, two spacious bedrooms, and contemporary finishes. Prime location in Sukhumvit 31, Wattana. Excellent amenities including pool, gym, and 24-hour security. Built 2018.",
      "images": ["https://cdn.baania.com/img/condo/A1.jpg", "https://cdn.baania.com/img/condo/A2.jpg"],
      "contact": {"agency": "Urban Living Thailand", "tel": "+66-81-234-5678"},
      "date_online": "2024-02-10T00:00:00Z"
    }
    ```
---
```

**Expected Output from Generator LLM (for JSONL or JSONLines Mapping in Conversational Format):**

A valid JSON Lines (.jsonl) file:
    Consists of multiple JSON objects, each on its own line.
    Each line must be a complete JSON object (not arrays or multi-line blocks).
    There must be no line breaks inside a single JSON object (unless escaped properly as \n).

```jsonl
{"contents":[{"role":"user","parts":[{"text":"You are a data mapping assistant. Your task is to map the provided 'Raw Property Data Snippet' to the 'CanonicalRecord Schema Definition'. \n\nRULES:\n- Your entire response must be ONLY the mapped JSON object string, conforming strictly to the CanonicalRecord schema.\n- Do NOT include any explanatory text before or after the JSON object.\n- Set 'original_source_type' to: scrape\n- Set 'original_source_identifier' to: https://www.baania.com/some-property-link-v2\n- Set 'entity_type' to 'RealEstateListing'.\n- For the 'raw_source_data' field in the output, include the exact 'Raw Property Data Snippet' you were given.\n- Perform necessary data transformations (e.g., string prices to numbers, parse dates, extract address components).\n- If information for a canonical field is not present, use `null` or omit optional fields as per the schema.\n\nCanonicalRecord Schema Definition:\n{\"title\": \"CanonicalRecord\", \"type\": \"object\", \"properties\": {\"canonical_record_id\": {\"type\": \"string\", \"description\": \"Unique identifier for this canonical record.\", \"examples\": [\"cre-SOME_UUID\"]}, \"original_source_identifier\": {\"type\": \"string\", \"description\": \"Identifier of the original source (e.g., URL, filename + row index).\"}, \"original_source_type\": {\"type\": \"string\", \"enum\": [\"api\", \"file\", \"scrape\"], \"description\": \"Type of the original source adapter ('api', 'file', 'scrape').\"}, \"entity_type\": {\"type\": \"string\", \"enum\": [\"RealEstateListing\", \"NewsArticle\", \"Other\"], \"default\": \"Other\", \"description\": \"Classification of the source entity.\"}, \"mapping_model_version\": {\"type\": [\"string\", \"null\"], \"description\": \"Version identifier of the ML model used for mapping.\"}, \"mapping_timestamp\": {\"type\": \"string\", \"format\": \"date-time\", \"description\": \"Timestamp (UTC) when the mapping was performed.\"}, \"address\": {\"title\": \"Address\", \"type\": [\"object\", \"null\"], \"properties\": {\"street_address\": {\"type\": [\"string\", \"null\"]}, \"city\": {\"type\": [\"string\", \"null\"]}, \"state_province\": {\"type\": [\"string\", \"null\"]}, \"postal_code\": {\"type\": [\"string\", \"null\"]}, \"country\": {\"type\": [\"string\", \"null\"], \"default\": \"USA\"}}}, \"features\": {\"title\": \"Features\", \"type\": [\"object\", \"null\"], \"properties\": {\"bedrooms\": {\"type\": [\"integer\", \"null\"]}, \"bathrooms\": {\"type\": [\"number\", \"null\"]}, \"area_sqft\": {\"type\": [\"number\", \"null\"], \"description\": \"Area in square feet.\"}, \"lot_size_sqft\": {\"type\": [\"number\", \"null\"], \"description\": \"Lot size in square feet.\"}, \"year_built\": {\"type\": [\"integer\", \"null\"]}, \"property_type\": {\"type\": [\"string\", \"null\"]}, \"has_pool\": {\"type\": [\"boolean\", \"null\"]}, \"has_garage\": {\"type\": [\"boolean\", \"null\"]}, \"stories\": {\"type\": [\"integer\", \"null\"]}}}, \"listing\": {\"title\": \"Listing Information\", \"type\": [\"object\", \"null\"], \"properties\": {\"price\": {\"type\": [\"number\", \"null\"]}, \"currency\": {\"type\": [\"string\", \"null\"], \"default\": \"USD\"}, \"listing_status\": {\"type\": [\"string\", \"null\"]}, \"listing_type\": {\"type\": [\"string\", \"null\"]}, \"listed_date\": {\"type\": [\"string\", \"null\", \"string\"], \"format\": \"date-time\"}, \"last_updated_date\": {\"type\": [\"string\", \"null\", \"string\"]}, \"listing_url\": {\"type\": [\"string\", \"null\", \"string\"]}, \"mls_id\": {\"type\": [\"string\", \"null\"]}}}, \"agent\": {\"title\": \"Agent Information\", \"type\": [\"object\", \"null\"], \"properties\": {\"name\": {\"type\": [\"string\", \"null\"]}, \"phone\": {\"type\": [\"string\", \"null\"]}, \"email\": {\"type\": [\"string\", \"null\"]}, \"brokerage_name\": {\"type\": [\"string\", \"null\"]}}}, \"description\": {\"type\": [\"string\", \"null\"]}, \"image_urls\": {\"type\": [\"array\", \"null\"], \"items\": {\"type\": \"string\", \"format\": \"uri\"}}, \"raw_source_data\": {\"type\": [\"object\", \"null\"], \"description\": \"Original source data record (JSON representation).\"}}, \"required\": [\"original_source_identifier\", \"original_source_type\", \"entity_type\"]}\n\nOriginal Source Type: scrape\nOriginal Source Identifier: https://www.baania.com/some-property-link-v2\n\nRaw Property Data Snippet:\n{\"projectName\": \"The Oasis Residence\", \"propertyType\": \"Condominium\", \"priceInfo\": {\"amount\": 7800000, \"unit\": \"THB\"}, \"location\": {\"building\": \"Tower A\", \"street\": \"Sukhumvit Soi 31\", \"district\": \"Wattana\", \"city\": \"Bangkok\", \"postalCode\": \"10110\"}, \"attributes\": {\"num_bedrooms\": \"2 Bedrooms\", \"num_bathrooms\": \"2\", \"area\": \"75 SQ.M.\", \"floor\": \"15th\"}, \"title\": \"Luxury 2 Bed Condo, High Floor, Sukhumvit\", \"full_description\": \"Modern luxury condominium unit on a high floor in Tower A of The Oasis Residence. Offers stunning city views, two spacious bedrooms, and contemporary finishes. Prime location in Sukhumvit 31, Wattana. Excellent amenities including pool, gym, and 24-hour security. Built 2018.\", \"images\": [\"https://cdn.baania.com/img/condo/A1.jpg\", \"https://cdn.baania.com/img/condo/A2.jpg\"], \"contact\": {\"agency\": \"Urban Living Thailand\", \"tel\": \"+66-81-234-5678\"}, \"date_online\": \"2024-02-10T00:00:00Z\"}"}]},{"role":"model","parts":[{"text":"{\"canonical_record_id\": \"cre-GENERATED-UUID\", \"original_source_identifier\": \"https://www.baania.com/some-property-link-v2\", \"original_source_type\": \"scrape\", \"entity_type\": \"RealEstateListing\", \"mapping_model_version\": null, \"mapping_timestamp\": \"2024-02-10T00:00:00Z\", \"address\": {\"street_address\": \"Sukhumvit Soi 31\", \"city\": \"Bangkok\", \"state_province\": \"Wattana\", \"postal_code\": \"10110\", \"country\": \"Thailand\"}, \"features\": {\"bedrooms\": 2, \"bathrooms\": 2.0, \"area_sqft\": 807.29, \"lot_size_sqft\": null, \"year_built\": 2018, \"property_type\": \"Condominium\", \"has_pool\": null, \"has_garage\": null, \"stories\": null}, \"listing\": {\"price\": 7800000.0, \"currency\": \"THB\", \"listing_status\": null, \"listing_type\": null, \"listed_date\": \"2024-02-10T00:00:00Z\", \"last_updated_date\": null, \"listing_url\": null, \"mls_id\": null}, \"agent\": {\"name\": null, \"phone\": \"+66-81-234-5678\", \"email\": null, \"brokerage_name\": \"Urban Living Thailand\"}, \"description\": \"Luxury 2 Bed Condo, High Floor, Sukhumvit. Modern luxury condominium unit on a high floor in Tower A of The Oasis Residence. Offers stunning city views, two spacious bedrooms, and contemporary finishes. Prime location in Sukhumvit 31, Wattana. Excellent amenities including pool, gym, and 24-hour security. Built 2018.\", \"image_urls\": [\"https://cdn.baania.com/img/condo/A1.jpg\", \"https://cdn.baania.com/img/condo/A2.jpg\"], \"raw_source_data\": {\"projectName\": \"The Oasis Residence\", \"propertyType\": \"Condominium\", \"priceInfo\": {\"amount\": 7800000, \"unit\": \"THB\"}, \"location\": {\"building\": \"Tower A\", \"street\": \"Sukhumvit Soi 31\", \"district\": \"Wattana\", \"city\": \"Bangkok\", \"postalCode\": \"10110\"}, \"attributes\": {\"num_bedrooms\": \"2 Bedrooms\", \"num_bathrooms\": \"2\", \"area\": \"75 SQ.M.\", \"floor\": \"15th\"}, \"title\": \"Luxury 2 Bed Condo, High Floor, Sukhumvit\", \"full_description\": \"Modern luxury condominium unit on a high floor in Tower A of The Oasis Residence. Offers stunning city views, two spacious bedrooms, and contemporary finishes. Prime location in Sukhumvit 31, Wattana. Excellent amenities including pool, gym, and 24-hour security. Built 2018.\", \"images\": [\"https://cdn.baania.com/img/condo/A1.jpg\", \"https://cdn.baania.com/img/condo/A2.jpg\"], \"contact\": {\"agency\": \"Urban Living Thailand\", \"tel\": \"+66-81-234-5678\"}, \"date_online\": \"2024-02-10T00:00:00Z\"}}"}]}]}
```

GEnerate 50 token with many details, include sample where multiple data sources (api, file, scrape)