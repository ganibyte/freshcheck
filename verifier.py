import os
from tavily import TavilyClient
from dotenv import load_dotenv
from llm import ask_json

load_dotenv(override=True)
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def verify_claim(claim_text):
    # 1. Search the live web
    try:
        res = tavily.search(query=claim_text, max_results=3)
        results = res.get("results", [])
        print("Tavily returned", len(results), "results")
    except Exception as e:
        print("Tavily error:", repr(e)[:200])
        results = []

    if not results:
        return {"verdict": "unknown", "corrected_fact": "No sources found",
                "source_url": "", "confidence": "low"}

    evidence = "\n\n".join(
        f"Source: {r['url']}\n{r['content']}" for r in results
    )

    # 2. Ask the LLM to judge
    prompt = f"""Claim: {claim_text}

Web search results:
{evidence}

Is the claim still true today based ONLY on these results?
Return ONLY JSON with:
"verdict": "agree", "conflict", or "contradict"
"corrected_fact": the up-to-date fact (short)
"source_url": the best source URL
"confidence": "high" or "low" """

    out = ask_json(prompt)
    if not isinstance(out, dict):
        return {"verdict": "unknown", "corrected_fact": "Could not judge",
                "source_url": results[0]["url"], "confidence": "low"}
    return out