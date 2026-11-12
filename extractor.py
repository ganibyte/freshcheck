from llm import ask_json


def extract_claims(answer):
    prompt = f"""List every factual claim in this text.
Return ONLY a JSON list. Each item must have:
"text" (the claim) and
"type" (one of: pricing, version, law, leadership, stable).

Text:
{answer}"""
    claims = ask_json(prompt)
    return claims if isinstance(claims, list) else []