PLACEHOLDERS = [
    "<username>", "%3Cusername%3E",
    "<email_address>", "<email>",
    "<phone_number>", "<phone>",
    "<domain>", "%3Cdomain%3E",
    "{username}", "<name>", "%3Cdomain.com%3E",
]


def build_urls(node, target, results=None):
    if results is None:
        results = []

    name = node.get("name", "Unknown")
    url = node.get("url")

    if url and isinstance(url, str):
        final = url
        for ph in PLACEHOLDERS:
            final = final.replace(ph, target)
        if final.startswith("http"):
            results.append({"name": name, "url": final})

    for child in node.get("children", []) or []:
        build_urls(child, target, results)

    return results
