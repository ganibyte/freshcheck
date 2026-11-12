import streamlit as st
from extractor import extract_claims
from verifier import verify_claim
from scorer import freshness_score

MAX_CHECKS = 8

st.set_page_config(page_title="FreshCheck", page_icon="🔍", layout="wide")
st.title("🔍 FreshCheck")
st.caption("Don't trust old AI answers. Check if they're still true.")

answer = st.text_area("Paste an AI answer here:", height=200)

if st.button("Check freshness"):
    if not answer.strip():
        st.warning("Please paste an answer first.")
        st.stop()

    with st.spinner("Finding claims..."):
        claims = extract_claims(answer)

    # keep only well-formed claims
    claims = [c for c in claims if isinstance(c, dict) and c.get("text")]

    if not claims:
        st.error("No claims found. Try a longer answer, or check that Bifrost is running.")
        st.stop()

    stable = [c for c in claims if c.get("type") == "stable"]
    risky = [c for c in claims if c.get("type") != "stable"]
    to_check = risky[:MAX_CHECKS]
    skipped = risky[MAX_CHECKS:]

    rows = []
    checked_scores = []
    progress = st.progress(0.0, text="Verifying claims...")

    for i, c in enumerate(to_check):
        result = verify_claim(c["text"])
        score, label = freshness_score(
            result.get("verdict"), c.get("type"), result.get("confidence"))
        checked_scores.append(score)
        rows.append({
            "Claim": c["text"],
            "Type": c.get("type", ""),
            "Status": label,
            "Score": score,
            "Correction": result.get("corrected_fact", ""),
            "Source": result.get("source_url", ""),
        })
        progress.progress((i + 1) / len(to_check), text=f"Verified {i + 1} of {len(to_check)}")

    progress.empty()

    for c in skipped:
        rows.append({"Claim": c["text"], "Type": c.get("type", ""),
                     "Status": "⏭️ Not checked (limit)", "Score": None,
                     "Correction": "-", "Source": ""})

    for c in stable:
        rows.append({"Claim": c["text"], "Type": "stable",
                     "Status": "⚪ Stable (skipped)", "Score": None,
                     "Correction": "-", "Source": ""})

    col1, col2, col3 = st.columns(3)
    if checked_scores:
        col1.metric("Overall freshness", f"{sum(checked_scores) // len(checked_scores)} / 100")
    else:
        col1.metric("Overall freshness", "n/a")
    col2.metric("Claims checked", len(checked_scores))
    col3.metric("Stable, skipped", len(stable))

    st.dataframe(
        rows,
        use_container_width=True,
        column_config={"Source": st.column_config.LinkColumn("Source")},
    )