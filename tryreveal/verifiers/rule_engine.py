def needs_browser(rule):
    return bool(rule and rule.get("requires_js", False))


def score_with_rule(result, rule):
    body = result["body"]
    status = result["status"]

    if status == "error":
        return False, 0, "network"

    has_pos = any(p.lower() in body for p in rule.get("positive", []))
    has_neg = any(n.lower() in body for n in rule.get("negative", []))

    if has_neg:
        return False, 10, "rule-negative"
    if has_pos:
        return True, 90, "rule-positive"
    if status == 200:
        return True, 40, "rule-fallback-200"
    if status in (301, 302, 403):
        return True, 50, "rule-fallback-redirect"
    return False, 0, "rule-fallback-miss"
