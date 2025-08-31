import json

def parse_json_response(response_str):
    try:
        cleaned = response_str.strip()
        if cleaned.startswith('```'):
            cleaned = cleaned[7:]  # Remove ```json
        if cleaned.endswith('```'):
            cleaned = cleaned[:-3]  # Remove ```
        cleaned = cleaned.replace('\\n', '\n')
        cleaned = cleaned.replace('\\"', '"')
        cleaned = cleaned.replace('\\\\', '\\')
        result = json.loads(cleaned.strip())
        return result
    except json.JSONDecodeError as e:
        print(f"JSON parsing failed: {e}")
        print(f"Cleaned string: {repr(cleaned)}")
        return None

# Helper Functions