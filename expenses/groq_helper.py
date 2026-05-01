import json
import re
import requests
from django.conf import settings

CATEGORIES = ['Dairy', 'Vegetables', 'Household', 'Personal Care', 'Frozen Food', 'Grocery / Spices', 'Transport', 'Bills', 'Entertainment', 'Health', 'Other']

EXTRACT_PROMPT = f"""Extract all purchased items from this receipt/invoice/bill. For each item return:
- description: item name (short, clean)
- amount: final price paid for that item (number, use the Amount column not Price column)
- category: one of {', '.join(CATEGORIES)}
- quantity: number from Qty column (default 1)
- size: weight/volume if visible (e.g. "500ml", "1kg")
- mrp: original MRP if visible, else same as amount

Rules:
- Only extract individual line items, NOT subtotals, service charges, taxes (CGST/SGST/GST), tips, delivery fees, round-off, or grand totals
- Skip zero-value/complimentary items
- For restaurant bills, each dish/drink is a separate item with category "Other"
- If an item name spans multiple lines, combine them into one description

Return ONLY a JSON array. Example:
[{{"description":"Tandoori Paneer Tacos","amount":490,"category":"Other","quantity":1,"size":"","mrp":490}}]"""


def groq_chat(messages, max_tokens=1000):
    resp = requests.post(
        'https://api.groq.com/openai/v1/chat/completions',
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {settings.GROQ_API_KEY}'},
        json={'model': 'meta-llama/llama-4-scout-17b-16e-instruct', 'messages': messages, 'temperature': 0, 'max_tokens': max_tokens},
        timeout=60,
    )
    data = resp.json()
    if 'error' in data:
        raise Exception(data['error'].get('message', str(data['error'])))
    return data['choices'][0]['message']['content']


def parse_json(text):
    m = re.search(r'[\[{][\s\S]*[\]}]', text)
    return json.loads(m.group(0)) if m else None
