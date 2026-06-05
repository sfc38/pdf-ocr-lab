def _levenshtein(a, b) -> int:
    m, n = len(a), len(b)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev, dp[0] = dp[:], i
        for j in range(1, n + 1):
            dp[j] = prev[j - 1] if a[i - 1] == b[j - 1] else 1 + min(prev[j], dp[j - 1], prev[j - 1])
    return dp[n]


def cer(prediction: str, reference: str) -> float:
    """Character Error Rate: edit distance at char level / reference length. Lower = better."""
    ref = reference.strip()
    if not ref:
        return 0.0
    return round(_levenshtein(prediction.strip(), ref) / len(ref), 4)


def wer(prediction: str, reference: str) -> float:
    """Word Error Rate: edit distance at word level / reference word count. Lower = better."""
    ref_words = reference.strip().split()
    if not ref_words:
        return 0.0
    return round(_levenshtein(prediction.strip().split(), ref_words) / len(ref_words), 4)


def jaccard(text_a: str, text_b: str) -> float:
    """Jaccard word overlap: |A ∩ B| / |A ∪ B|. Higher = more agreement between engines."""
    a = set(text_a.lower().split())
    b = set(text_b.lower().split())
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return round(len(a & b) / len(a | b), 4)
