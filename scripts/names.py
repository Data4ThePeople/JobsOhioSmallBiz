"""Company-name normalization and conservative matching, shared by the
scripts. Adapted from the hospital matcher in SterileWater: strip legal
suffixes and noise words, compare the discriminating tokens, refuse to guess
on a tie."""
import re

_NOISE = {
    "the", "of", "and", "a", "an", "dba", "fka", "aka",
    "inc", "incorporated", "llc", "lc", "ltd", "limited", "lp", "llp", "plc", "pllc",
    "co", "corp", "corporation", "company", "companies", "holdings", "holding",
    "usa", "us", "america", "americas", "north", "international", "intl", "enterprises",
}
_PUNCT = re.compile(r"[^a-z0-9\s]")
_WS = re.compile(r"\s+")


def normalize_name(name):
    """Lowercase, strip punctuation, fold '&' to 'and', drop legal suffixes.

    >>> normalize_name("The Sherwin-Williams Company")
    'sherwin williams'
    >>> normalize_name("AMAZON.COM.DEDC, LLC")
    'amazon com dedc'
    """
    if not name:
        return ""
    s = name.lower().replace("&", " and ").replace("'", "").replace("’", "")
    s = s.replace(".com", " com")
    s = _PUNCT.sub(" ", s)
    toks = [t for t in _WS.sub(" ", s).strip().split() if t not in _NOISE]
    return " ".join(toks)


def name_tokens(name):
    return frozenset(normalize_name(name).split())


def score(a, b):
    """Jaccard overlap of discriminating tokens, in [0, 1]."""
    ta, tb = name_tokens(a), name_tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def best_match(name, candidates, threshold=0.6):
    """Best (key, score) among candidates [(key, name)], or None when nothing
    clears the threshold or the top two tie."""
    if not candidates:
        return None
    scored = sorted(((k, score(name, n)) for k, n in candidates), key=lambda t: t[1], reverse=True)
    top_k, top_s = scored[0]
    if top_s < threshold:
        return None
    if len(scored) > 1 and scored[1][1] >= top_s - 1e-9 and scored[1][0] != top_k:
        return None
    return top_k, top_s


def program_family(label, value=None):
    """Fold the many spellings of JobsOhio program names into one label per
    program. `value` (dollars) resolves the two 2021 months where the
    Inclusion column touched a neighbor: Inclusion grants cap at $50,000."""
    L = re.sub(r"[^a-z&]+", " ", (label or "").lower()).strip()
    L = L.replace("jobsohio", "").strip()
    if not L:
        return "Unknown"
    if "inclusion" in L and ("osip" in L or "revitalization" in L):
        return "Inclusion Grant" if (value or 0) <= 50000 else ("Spec Development (OSIP)" if "osip" in L else "Revitalization Grant")
    if "inclusion" in L or "small business" in L or "joig" in L:
        return "Inclusion Grant"
    if "osip" in L or "spec development" in L or "ohse" in L or "ose" == L.split()[-1]:
        return "Spec Development (OSIP)"
    if "vibrant" in L:
        return "Vibrant Community Grant"
    if "workforce" in L or "jow" in L.split():
        return "Workforce Grant"
    if "revitalization" in L or "jorg" in L:
        if "loan" in L:
            return "Revitalization Loan"
        if "phase" in L or " ii" in " " + L or L.endswith(" 2") or "gphase" in L or "lphase" in L:
            return "Revitalization Grant Phase II"
        return "Revitalization Grant"
    if "research" in L or "r&d" in L or "jordg" in L or L in ("development grant",):
        return "Research & Development Grant"
    if "economic" in L or "jog" in L.split() or L.replace(" ", "") in ("grant", "economicdevelopmentgrant"):
        return "Economic Development Grant"
    if "growth" in L or "jol" in L.split() or L == "loan":
        return "Growth Fund Loan"
    if "aerospace" in L:
        return "Aerospace and Defense Opportunity Grant"
    if "talent" in L:
        return "Talent Acquisition"
    if "other" in L:
        return "Other Loan" if "loan" in L else "Other Grant"
    return "Unknown: " + label
