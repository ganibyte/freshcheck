import os, json, re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI(base_url=os.getenv("BIFROST_URL"), api_key="dummy")
MODEL = os.getenv("MODEL")
FALLBACKS = [m.strip() for m in os.getenv("FALLBACK_MODELS", "").split(",") if m.strip()]

def ask_llm(prompt):
    kwargs = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "extra_headers": {"x-bf-cache-key": "freshcheck"},
    }
    if FALLBACKS:
        kwargs["extra_body"] = {"fallbacks": FALLBACKS}
    r = client.chat.completions.create(**kwargs)
    return r.choices[0].message.content

def ask_json(prompt):
    text = ask_llm(prompt)
    text = re.sub(r"```json|```", "", text).strip()
    try:
        return json.loads(text)
    except Exception:
        return None