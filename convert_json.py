import json

print(""" """)

# ✅ Remove Markdown JSON formatting
cleaned_text = text.replace("```json", "").replace("```", "").strip()

# ✅ Convert to dictionary
try:
    expense_data = json.loads(cleaned_text)
    print("✅ JSON Parsed Successfully:", expense_data)
except json.JSONDecodeError as e:
    print(f"❌ ERROR: Failed to parse JSON: {e}")
