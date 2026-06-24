import os, re, sys, urllib.request, urllib.parse

BASE = "C:/Users/roger/Desktop/Projetos/Teste-Croche/artes-cristas-copia"
ORIGIN = "https://arquivoscnc.online/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

downloaded = {}   # absolute_url -> local_relative_path (posix)
failed = []

def local_path_for(url):
    """Map a same-origin absolute URL to a local relative path (strip query)."""
    p = urllib.parse.urlparse(url)
    path = p.path
    if path.endswith("/") or path == "":
        path = path + "index.html"
    rel = path.lstrip("/")
    return rel

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def save(rel, data):
    dest = os.path.join(BASE, rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        f.write(data)

def download(url):
    if url in downloaded:
        return downloaded[url]
    rel = local_path_for(url)
    try:
        data = fetch(url)
    except Exception as e:
        failed.append((url, str(e)))
        return None
    save(rel, data)
    downloaded[url] = rel
    print("OK", rel)
    # If CSS, process its url() refs
    if rel.lower().endswith(".css"):
        process_css(url, rel, data)
    return rel

def process_css(css_url, css_rel, data):
    text = data.decode("utf-8", "replace")
    css_dir = os.path.dirname(css_rel)
    refs = re.findall(r"url\(\s*['\"]?([^'\")]+?)['\"]?\s*\)", text)
    refs += re.findall(r"@import\s+['\"]([^'\"]+)['\"]", text)
    changed = text
    for ref in set(refs):
        r = ref.strip()
        if r.startswith("data:") or r == "":
            continue
        abs_url = urllib.parse.urljoin(css_url, r)
        if not abs_url.startswith(ORIGIN):
            continue  # leave external CDN refs untouched
        new_rel = download(abs_url)
        if new_rel:
            # relative path from this css file to the asset
            relpath = os.path.relpath(
                os.path.join(BASE, new_rel.replace("/", os.sep)),
                os.path.join(BASE, css_dir.replace("/", os.sep)) if css_dir else BASE,
            ).replace(os.sep, "/")
            changed = changed.replace(ref, relpath)
    if changed != text:
        save(css_rel, changed.encode("utf-8"))

def main():
    with open(os.path.join(BASE, "index.html"), "r", encoding="utf-8", errors="replace") as f:
        html = f.read()

    # all same-origin asset URLs in attributes
    urls = set(re.findall(r'["\'](https://arquivoscnc\.online/[^"\'\s]+)["\']', html))
    # also srcset / unquoted occurrences
    urls |= set(re.findall(r'(https://arquivoscnc\.online/[^"\'\s<>\\]+\.(?:css|js|png|jpe?g|gif|webp|svg|ico|woff2?|ttf|eot)[^"\'\s<>\\]*)', html))

    for u in sorted(urls):
        download(u)

    # rewrite HTML: replace each downloaded absolute URL with relative local path
    new_html = html
    for url, rel in sorted(downloaded.items(), key=lambda kv: -len(kv[0])):
        new_html = new_html.replace(url, "./" + rel)

    with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
        f.write(new_html)

    print("\n=== DONE ===")
    print("downloaded:", len(downloaded))
    print("failed:", len(failed))
    for u, e in failed:
        print("  FAIL", u, e)

main()
