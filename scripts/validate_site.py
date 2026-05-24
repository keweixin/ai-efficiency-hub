from __future__ import annotations

import datetime
from html import unescape
from pathlib import Path
import json
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://www.bevoorra.business"
PUBLISHED_DATE = "2026-05-21"
TODAY = datetime.date.today().isoformat()
MIN_ARTICLES = 30
MIN_CJK = 1200
GSC_VERIFICATION_FILE = "google97d2ec5ca21ee27c.html"
GSC_VERIFICATION_BODY = "google-site-verification: google97d2ec5ca21ee27c.html"
ADS_TXT_LINE = "google.com, pub-7663008606677915, DIRECT, f08c47fec0942fa0"

REQUIRED_PAGES = [
    "index.html",
    "articles.html",
    "volume.html",
    "channels.html",
    "packing.html",
    "tools.html",
    "smoke-test.html",
    "about.html",
    "privacy.html",
    "contact.html",
]

FORBIDDEN_TERMS = [
    "AI效率资源站",
    "四六级",
    "简历",
    "保证省钱",
    "必省",
    "货代坑人",
    "隐藏条款",
    "上架建议",
    "建议定价",
    "面包多",
    "顿顿",
    "付款",
    "购买",
    "data-payment-link",
    "1234567890",
    "sellercentral.amazon.com/help",
    "旧 60cm",
    "从 60cm 调整到 40cm",
    "EMS 60cm",
]

OLD_SLUGS = [
    "cet-14-day-study-plan.html",
    "ai-resume-polish-guide.html",
    "prompt-four-part-formula.html",
    "automation-test-interview-roadmap.html",
    "gpt-claude-beginner-differences.html",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def cjk_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def strip_tags(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def html_files() -> list[Path]:
    root_pages = [
        path for path in sorted(ROOT.glob("*.html"))
        if not path.name.startswith("google")
    ]
    return root_pages + sorted((ROOT / "articles").glob("*.html"))


def local_target(from_path: Path, href: str) -> Path:
    path = unescape(href).split("#", 1)[0].split("?", 1)[0]
    return (from_path.parent / path).resolve()


def validate_articles(errors: list[str]) -> None:
    articles = sorted((ROOT / "articles").glob("*.html"))
    if len(articles) != MIN_ARTICLES:
        errors.append(f"expected {MIN_ARTICLES} article files, found {len(articles)}")

    titles: set[str] = set()
    descriptions: set[str] = set()
    for path in articles:
        text = read(path)
        body_match = re.search(r'<article class="article-body">(.*?)</article>', text, re.S)
        body = body_match.group(1) if body_match else text
        count = cjk_count(strip_tags(body))
        if count < MIN_CJK:
            errors.append(f"{path.relative_to(ROOT)} has only {count} CJK chars")
        if len(re.findall(r"<h2\b", text)) < 8:
            errors.append(f"{path.relative_to(ROOT)} has fewer than 8 h2 sections")
        if len(re.findall(r'<a href="https?://', text)) < 2:
            errors.append(f"{path.relative_to(ROOT)} has fewer than 2 external sources")
        for required in [
            '<link rel="canonical"',
            'property="og:title"',
            'name="twitter:card"',
            'name="robots"',
            'application/ld+json',
            'id="answer"',
            'id="checklist"',
            'id="faq"',
        ]:
            if required not in text:
                errors.append(f"{path.relative_to(ROOT)} missing {required}")
        title = re.search(r"<title>(.*?)</title>", text, re.S)
        description = re.search(r'<meta name="description" content="(.*?)"', text, re.S)
        if not title or title.group(1) in titles:
            errors.append(f"{path.relative_to(ROOT)} missing or duplicates title")
        elif title:
            titles.add(title.group(1))
        if not description or description.group(1) in descriptions:
            errors.append(f"{path.relative_to(ROOT)} missing or duplicates description")
        elif description:
            descriptions.add(description.group(1))


def validate_seo(errors: list[str]) -> None:
    for path in html_files():
        text = read(path)
        for required in [
            '<meta name="description"',
            '<meta name="robots"',
            '<link rel="canonical"',
            'property="og:title"',
            'property="og:url"',
            'name="twitter:card"',
            'application/ld+json',
        ]:
            if required not in text:
                errors.append(f"{path.relative_to(ROOT)} missing {required}")
        if path.parent.name == "articles":
            if f'"datePublished":"{PUBLISHED_DATE}"' not in text:
                errors.append(f"{path.relative_to(ROOT)} has wrong datePublished")
            if f'"dateModified":"{TODAY}"' not in text:
                errors.append(f"{path.relative_to(ROOT)} has wrong dateModified")

    home = read(ROOT / "index.html") if (ROOT / "index.html").exists() else ""
    js = read(ROOT / "assets" / "site.js") if (ROOT / "assets" / "site.js").exists() else ""
    if "articles.html?q={search_term_string}" in home and "params.get('q')" not in js:
        errors.append("SearchAction q parameter is not handled by article filter")
    if "params.get('group')" in js and "chips.some((chip) => chip.dataset.filter === activeGroup)" not in js:
        errors.append("article filter does not guard invalid group parameters")


def validate_links_and_images(errors: list[str]) -> None:
    for path in html_files():
        text = read(path)
        ids = set(re.findall(r'\bid="([^"]+)"', text))

        for href in re.findall(r'\bhref="([^"]+)"', text):
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            if href == "#main":
                continue
            file_part, _, anchor = href.partition("#")
            if file_part:
                target = local_target(path, file_part)
                try:
                    target.relative_to(ROOT)
                except ValueError:
                    errors.append(f"{path.relative_to(ROOT)} link escapes root: {href}")
                    continue
                if not target.exists():
                    errors.append(f"{path.relative_to(ROOT)} missing link target: {href}")
            elif anchor and anchor not in ids:
                errors.append(f"{path.relative_to(ROOT)} missing anchor: {href}")

        for img_tag in re.findall(r"<img\b[^>]*>", text):
            src_match = re.search(r'\bsrc="([^"]+)"', img_tag)
            if not src_match:
                errors.append(f"{path.relative_to(ROOT)} img missing src")
                continue
            src = src_match.group(1)
            if src.startswith(("http://", "https://")):
                errors.append(f"{path.relative_to(ROOT)} hotlinks image: {src}")
            target = local_target(path, src)
            if not target.exists():
                errors.append(f"{path.relative_to(ROOT)} missing image: {src}")
            for attr in ["alt", "width", "height", "loading", "decoding"]:
                if f"{attr}=" not in img_tag:
                    errors.append(f"{path.relative_to(ROOT)} img missing {attr}: {src}")

        for source in re.findall(r"<source\b[^>]*\bsrcset=\"([^\"]+)\"", text):
            if source.startswith(("http://", "https://")):
                errors.append(f"{path.relative_to(ROOT)} hotlinks source: {source}")
            target = local_target(path, source)
            if not target.exists():
                errors.append(f"{path.relative_to(ROOT)} missing source image: {source}")


def validate_sitemap_and_index(errors: list[str]) -> None:
    sitemap_path = ROOT / "sitemap.xml"
    if not sitemap_path.exists():
        errors.append("missing sitemap.xml")
        return
    sitemap = read(sitemap_path)
    if f"<lastmod>{TODAY}</lastmod>" not in sitemap:
        errors.append(f"sitemap lastmod is not current build date {TODAY}")
    if "<lastmod>2026-05-21</lastmod>" in sitemap and TODAY != "2026-05-21":
        errors.append("sitemap still contains old hard-coded lastmod 2026-05-21")
    article_urls = re.findall(rf"<loc>{re.escape(SITE_URL)}/articles/[^<]+</loc>", sitemap)
    if len(article_urls) != MIN_ARTICLES:
        errors.append(f"sitemap has {len(article_urls)} article urls")
    for page in REQUIRED_PAGES:
        expected = f"{SITE_URL}/{page}" if page != "index.html" else SITE_URL
        if expected not in sitemap:
            errors.append(f"sitemap missing {page}")
    for page in ["campus.html", "career.html", "404.html"]:
        if f"{SITE_URL}/{page}" in sitemap:
            errors.append(f"sitemap should not include {page}")
    for slug in OLD_SLUGS:
        if f"/articles/{slug}</loc>" in sitemap:
            errors.append(f"sitemap still contains old slug {slug}")

    search_index = ROOT / "assets" / "search-index.json"
    if not search_index.exists():
        errors.append("missing assets/search-index.json")
    else:
        data = json.loads(read(search_index))
        if len(data) != MIN_ARTICLES:
            errors.append(f"search index has {len(data)} items")
        for item in data:
            if not (ROOT / item["href"]).exists():
                errors.append(f"search index points to missing article {item['href']}")

    not_found = ROOT / "404.html"
    if not not_found.exists():
        errors.append("missing 404.html")
    elif 'name="robots" content="noindex, follow"' not in read(not_found):
        errors.append("404.html should be noindex, follow")


def validate_sensitive_terms(errors: list[str]) -> None:
    public_files = html_files()
    public_files += [
        ROOT / "assets" / "site.js",
        ROOT / "assets" / "search-index.json",
        ROOT / "sitemap.xml",
        ROOT / "robots.txt",
    ]
    for path in public_files:
        if not path.exists():
            continue
        text = read(path)
        for term in FORBIDDEN_TERMS:
            if term in text:
                errors.append(f"{path.relative_to(ROOT)} contains forbidden term: {term}")


def validate_tools(errors: list[str]) -> None:
    text = read(ROOT / "tools.html") if (ROOT / "tools.html").exists() else ""
    for marker in [
        "data-logistics-calculator",
        "data-sku-rows",
        "data-channel-results",
        "data-export-report",
        "data-lang-toggle",
        "data-save-status",
        "SoftwareApplication",
        "featureList",
        '"offers"',
        '"price":0',
        "DHL 5000",
        "EMS 6000",
        "标准空运 6000",
        "默认按 EMS 超过 40cm 口径提醒",
    ]:
        if marker not in text:
            errors.append(f"tools.html missing {marker}")
    if "默认按 EMS 40cm 口径提醒" in text:
        errors.append("tools.html still contains outdated EMS 40cm fallback copy")
    for forbidden in ["aggregateRating", '"review"']:
        if forbidden in text:
            errors.append(f"tools.html should not include unverified structured data marker {forbidden}")
    js = read(ROOT / "assets" / "site.js") if (ROOT / "assets" / "site.js").exists() else ""
    for marker in [
        "initCalculator",
        "initLanguage",
        "exportPdfReport",
        "JSPDF_SRC",
        "data-load-failed",
        "jsPDF load failed",
        "shipping-calculator-state-v1",
        "ShippingCalculatorLogic",
        "computeCalculatorData",
        "normalizeCalculatorRows",
        "shipmentCalc",
        "emsPieceCalc",
        "calcChannel",
        "saveStateNow",
        "readSavedState",
        "storageSet",
        "emsPieceWarning",
        "emsNoDimWarning",
        "airChannel",
        "5000",
        "6000",
        "40cm",
    ]:
        if marker not in js:
            errors.append(f"site.js missing calculator marker {marker}")
    for forbidden in [
        "chargeable += Math.max(volumePer, actualPer) * row.qty",
        "longest >= 40",
        "row.l >= 40",
    ]:
        if forbidden in js:
            errors.append(f"site.js still contains outdated calculator pattern {forbidden}")


def validate_calculator_logic(errors: list[str]) -> None:
    site_js = json.dumps(str(ROOT / "assets" / "site.js"))
    script = f"""
const siteJs = {site_js};
const noop = () => {{}};
global.window = {{
  localStorage: {{ getItem() {{ return null; }}, setItem() {{}}, removeItem() {{}} }},
  location: {{ pathname: '/tools.html' }},
  clearTimeout,
  setTimeout
}};
global.location = window.location;
global.document = {{
  documentElement: {{ lang: '', classList: {{ add: noop, remove: noop, toggle() {{ return false; }} }} }},
  body: {{ dataset: {{}} }},
  querySelectorAll() {{ return []; }},
  querySelector() {{ return null; }},
  addEventListener: noop,
  dispatchEvent: noop
}};
global.CustomEvent = function CustomEvent(type, init) {{ return {{ type, detail: init && init.detail }}; }};
require(siteJs);

const logic = window.ShippingCalculatorLogic;
if (!logic || typeof logic.compute !== 'function') throw new Error('ShippingCalculatorLogic.compute is missing');

function channel(report, key) {{
  const item = report.channelData.find((entry) => entry.key === key);
  if (!item) throw new Error('missing channel ' + key);
  return item;
}}
function close(actual, expected, label) {{
  if (Math.abs(actual - expected) > 0.01) {{
    throw new Error(`${{label}} expected ${{expected}}, got ${{actual}}`);
  }}
}}

const mixed = logic.compute([
  {{ name: 'bulky', qty: 1, l: 100, w: 50, h: 30, kg: 2 }},
  {{ name: 'heavy', qty: 1, l: 20, w: 20, h: 25, kg: 30 }}
], 6000);
close(channel(mixed, 'dhlChannel').chargeable, 32, 'DHL mixed shipment chargeable weight');
close(channel(mixed, 'airChannel').chargeable, 32, 'air mixed shipment chargeable weight');
close(channel(mixed, 'emsChannel').chargeable, 55, 'EMS piece long-side chargeable weight');

const exact40 = logic.compute([{{ name: 'edge', qty: 1, l: 40, w: 20, h: 20, kg: 1 }}], 6000);
close(channel(exact40, 'emsChannel').chargeable, 1, 'EMS exact 40cm should stay actual-weight only');

const over40 = logic.compute([{{ name: 'over', qty: 1, l: 40.1, w: 20, h: 20, kg: 1 }}], 6000);
close(channel(over40, 'emsChannel').chargeable, 2.67, 'EMS above 40cm should compare piece volume and actual');

const custom = logic.compute([{{ name: 'custom', qty: 1, l: 50, w: 50, h: 50, kg: 10 }}], 4000);
close(channel(custom, 'customChannel').divisor, 4000, 'custom divisor should be preserved');
close(channel(custom, 'customChannel').chargeable, 31.25, 'custom divisor chargeable weight');
"""
    try:
        completed = subprocess.run(
            ["node", "-e", script],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=20,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        errors.append(f"calculator runtime validation could not run: {exc}")
        return
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        errors.append(f"calculator runtime validation failed: {detail}")


def validate_required_pages(errors: list[str]) -> None:
    for page in REQUIRED_PAGES + ["404.html"]:
        if not (ROOT / page).exists():
            errors.append(f"missing page {page}")
    for old in ["campus.html", "career.html"]:
        if (ROOT / old).exists():
            errors.append(f"old page still exists: {old}")


def validate_required_static_files(errors: list[str]) -> None:
    for file_name in ["robots.txt", "sitemap.xml", "ads.txt", GSC_VERIFICATION_FILE]:
        if not (ROOT / file_name).exists():
            errors.append(f"missing static file {file_name}")

    ads = read(ROOT / "ads.txt").strip() if (ROOT / "ads.txt").exists() else ""
    if ADS_TXT_LINE not in ads:
        errors.append("ads.txt missing expected AdSense publisher line")

    verification = read(ROOT / GSC_VERIFICATION_FILE).strip() if (ROOT / GSC_VERIFICATION_FILE).exists() else ""
    if verification != GSC_VERIFICATION_BODY:
        errors.append(f"{GSC_VERIFICATION_FILE} has unexpected verification body")


def validate_analytics(errors: list[str]) -> None:
    for path in html_files():
        text = read(path)
        rel = path.relative_to(ROOT)
        for marker in ["window.va", "dataset.vercelAnalytics", "hostname", "localhost", "127.0.0.1", "/_vercel/insights/script.js"]:
            if marker not in text:
                errors.append(f"{rel} missing Vercel Analytics marker {marker}")
    privacy = read(ROOT / "privacy.html") if (ROOT / "privacy.html").exists() else ""
    if "Vercel Web Analytics" not in privacy or "cookie" not in privacy:
        errors.append("privacy.html missing Vercel Web Analytics privacy note")


def main() -> int:
    errors: list[str] = []
    validate_required_pages(errors)
    validate_required_static_files(errors)
    validate_articles(errors)
    validate_seo(errors)
    validate_links_and_images(errors)
    validate_sitemap_and_index(errors)
    validate_sensitive_terms(errors)
    validate_tools(errors)
    validate_calculator_logic(errors)
    validate_analytics(errors)
    if errors:
        print(f"FAILED: {len(errors)} issue(s)")
        for error in errors[:250]:
            print(f"- {error}")
        return 1
    print("PASS: site validation completed")
    print(f"- articles: {MIN_ARTICLES}")
    print(f"- minimum CJK chars per article: {MIN_CJK}")
    print("- SEO, links, images, sitemap, search index, static files, tools, and sensitive terms checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
