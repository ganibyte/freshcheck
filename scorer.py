def freshness_score(verdict, claim_type, confidence):
    base = {"agree": 100, "conflict": 50, "contradict": 0}.get(verdict)
    if base is None:           # unknown
        return 50, "🟡 Unverified"

    if claim_type in ("pricing", "version") and base == 100:
        base -= 10             # fast-changing facts get less trust
    if confidence == "high":
        base += 5

    score = max(0, min(100, base))
    if score >= 70:
        label = "🟢 Fresh"
    elif score >= 40:
        label = "🟡 Uncertain"
    else:
        label = "🔴 Outdated"
    return score, label