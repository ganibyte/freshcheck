# 🔍 FreshCheck

**Don't trust old AI answers. Check if they're still true.**

FreshCheck is a verification layer for LLM answers. Paste any AI answer, and it marks each claim as Fresh, Uncertain or Outdated, with a freshness score, a corrected fact and a source link.

Built for the Tavily #01 Stale-answer detector track, combined with the Bifrost gateway.

## The problem

LLMs are trained on old data but answer with full confidence. They often give outdated facts about pricing, software versions, laws and company leaders. Users trust these answers and make wrong decisions.

## How it works

1. The user pastes an AI answer.
2. The LLM extracts each factual claim and tags its type (pricing, version, law, leadership, stable).
3. Stable claims are skipped.
4. Tavily searches the live web for each risky claim.
5. The LLM judges the claim against the search results.
6. Python calculates a freshness score from 0 to 100.
7. The app shows a colored table with the correction and a source link.

Score labels: 🟢 70 to 100 Fresh, 🟡 40 to 69 Uncertain, 🔴 0 to 39 Outdated.

## Tools used

- **Tavily API**: live web search to verify claims
- **Bifrost**: LLM gateway for all model calls, with fallback models
- **Google Gemini**: the LLM, through Bifrost
- **Streamlit**: the web interface
- **Python**

## How AI is used

- The LLM extracts claims, tags their type and judges each claim against the evidence.
- Tavily retrieves live sources for verification.
- Bifrost routes all model calls and switches to a backup model if the first one fails.

## Run it locally

1. Install Python 3.10+ and Node.js.
2. Clone the repo and install packages:
   ```
   pip install -r requirements.txt
   ```
3. Start Bifrost in a separate terminal and add your LLM provider key in the dashboard at http://localhost:8080:
   ```
   npx -y @maximhq/bifrost
   ```
4. Create a `.env` file:
   ```
   TAVILY_API_KEY=your_tavily_key
   BIFROST_URL=http://localhost:8080/openai/v1
   MODEL=gemini/gemini-flash-lite-latest
   FALLBACK_MODELS=TODO_your_fallback_model
   ```
5. Run the app:
   ```
   streamlit run app.py
   ```

## Screenshots

TODO: add screenshots/result.png and screenshots/bifrost-fallback.png here

## Future ideas

- Chrome extension that checks answers inside chatbots
- An API other apps can call
- A "shelf life" for each type of fact, learned over time
