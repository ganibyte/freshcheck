from scorer import freshness_score
print(freshness_score("contradict", "version", "high"))  # expect (5, '🔴 Outdated')
print(freshness_score("agree", "version", "high"))       # expect (95, '🟢 Fresh')
print(freshness_score("conflict", "law", "low"))         # expect (50, '🟡 Uncertain')
print(freshness_score("unknown", "law", "low"))          # expect (50, '🟡 Unverified')