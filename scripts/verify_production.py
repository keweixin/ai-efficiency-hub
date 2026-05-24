from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen
import json
import re
import socket
import ssl
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET


SITE_URL = "https://www.bevoorra.business"
ROOT_DOMAIN_URL = "https://bevoorra.business"
HTTP_ROOT_DOMAIN_URL = "http://bevoorra.business"
HTTP_WWW_URL = "http://www.bevoorra.business"
ADS_TXT_LINE = "google.com, pub-7663008606677915, DIRECT, f08c47fec0942fa0"
GSC_VERIFICATION_FILE = "google97d2ec5ca21ee27c.html"
GSC_VERIFICATION_BODY = "google-site-verification: google97d2ec5ca21ee27c.html"
JSPDF_PATH = "assets/vendor/jspdf.umd.min.js"
MIN_ARTICLES = 30
FETCH_ATTEMPTS = 3
LOCAL_ASSET_MARKERS = ("assets/", "articles/", ".html", ".css", ".js", ".png", ".webp")
REQUIRED_SITEMAP_URLS = [
    SITE_URL,
    f"{SITE_URL}/articles.html",
    f"{SITE_URL}/tools.html",
    f"{SITE_URL}/smoke-test.html",
    f"{SITE_URL}/volume.html",
    f"{SITE_URL}/channels.html",
    f"{SITE_URL}/packing.html",
    f"{SITE_URL}/about.html",
    f"{SITE_URL}/privacy.html",
    f"{SITE_URL}/contact.html",
]


@dataclass
class FetchResult:
    url: str
    status: int
    final_url: str
    body: str


FETCH_CACHE: dict[str, FetchResult] = {}


class AssetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.assets: set[str] = set()

    def track_asset(self, value: str) -> None:
        candidate = value.strip().split()[0].rstrip(",")
        if not candidate or candidate.startswith(("mailto:", "#", "data:")):
            return
        if candidate.startswith(("http://", "https://")):
            if candidate.startswith(f"{SITE_URL}/") and any(marker in candidate for marker in LOCAL_ASSET_MARKERS):
                self.assets.add(candidate)
            return
        if any(marker in candidate for marker in LOCAL_ASSET_MARKERS):
            self.assets.add(candidate)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        for key in ("href", "src"):
            value = values.get(key)
            if value:
                self.track_asset(value)
        srcset = values.get("srcset")
        if srcset:
            for item in srcset.split(","):
                self.track_asset(item)
        if tag == "meta" and values.get("content"):
            meta_key = values.get("property") or values.get("name")
            if meta_key in {"og:image", "twitter:image"}:
                self.track_asset(values["content"])


def fetch(url: str, timeout: int = 25) -> FetchResult:
    if url in FETCH_CACHE:
        return FETCH_CACHE[url]
    request = Request(url, headers={"User-Agent": "ai-efficiency-hub-production-check/1.0"})
    last_error: Exception | None = None
    for attempt in range(1, FETCH_ATTEMPTS + 1):
        try:
            with urlopen(request, timeout=timeout, context=ssl.create_default_context()) as response:
                raw = response.read()
                charset = response.headers.get_content_charset() or "utf-8"
                result = FetchResult(url, response.status, response.geturl(), raw.decode(charset, errors="replace"))
                FETCH_CACHE[url] = result
                return result
        except HTTPError as error:
            raw = error.read()
            charset = error.headers.get_content_charset() or "utf-8"
            result = FetchResult(url, error.code, error.geturl(), raw.decode(charset, errors="replace"))
            FETCH_CACHE[url] = result
            return result
        except (URLError, TimeoutError, OSError) as error:
            last_error = error
            if attempt < FETCH_ATTEMPTS:
                time.sleep(1.5 * attempt)
                continue
    raise RuntimeError(f"{url} failed after {FETCH_ATTEMPTS} attempts: {last_error}") from last_error


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def schema_types(data: object) -> set[str]:
    found: set[str] = set()
    if isinstance(data, dict):
        value = data.get("@type")
        if isinstance(value, str):
            found.add(value)
        elif isinstance(value, list):
            found.update(item for item in value if isinstance(item, str))
        for item in data.values():
            found.update(schema_types(item))
    elif isinstance(data, list):
        for item in data:
            found.update(schema_types(item))
    return found


def parse_json_ld_types(body: str, label: str, errors: list[str]) -> set[str]:
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', body, re.S)
    require(bool(blocks), f"{label} missing JSON-LD block", errors)
    found: set[str] = set()
    for index, block in enumerate(blocks, start=1):
        try:
            data = json.loads(block)
        except json.JSONDecodeError as exc:
            errors.append(f"{label} has invalid JSON-LD block {index}: {exc}")
            continue
        found.update(schema_types(data))
    return found


def check_dns(errors: list[str]) -> None:
    for host in ("bevoorra.business", "www.bevoorra.business"):
        try:
            addresses = {item[4][0] for item in socket.getaddrinfo(host, 443, proto=socket.IPPROTO_TCP)}
        except OSError as exc:
            errors.append(f"DNS lookup failed for {host}: {exc}")
            continue
        require(bool(addresses), f"DNS lookup returned no addresses for {host}", errors)


def check_core_pages(errors: list[str]) -> None:
    expected_200 = [
        f"{SITE_URL}/",
        f"{SITE_URL}/tools.html",
        f"{SITE_URL}/smoke-test.html",
        f"{SITE_URL}/articles.html",
        f"{SITE_URL}/sitemap.xml",
        f"{SITE_URL}/robots.txt",
        f"{SITE_URL}/ads.txt",
        f"{SITE_URL}/{GSC_VERIFICATION_FILE}",
        f"{SITE_URL}/assets/site.js",
        f"{SITE_URL}/assets/styles.css",
        f"{SITE_URL}/_vercel/insights/script.js",
    ]
    for url in expected_200:
        result = fetch(url)
        require(result.status == 200, f"{url} returned {result.status}", errors)

    root = fetch(f"{ROOT_DOMAIN_URL}/")
    require(root.status == 200, f"{ROOT_DOMAIN_URL}/ returned {root.status}", errors)
    require(root.final_url.startswith(f"{SITE_URL}/"), f"root domain did not end at www domain: {root.final_url}", errors)

    for url in (f"{HTTP_ROOT_DOMAIN_URL}/", f"{HTTP_WWW_URL}/"):
        result = fetch(url)
        require(result.status == 200, f"{url} returned {result.status}", errors)
        require(result.final_url.startswith(f"{SITE_URL}/"), f"{url} did not redirect to HTTPS www domain: {result.final_url}", errors)

    not_found = fetch(f"{SITE_URL}/not-a-real-page-production-check")
    require(not_found.status == 404, f"unknown route returned {not_found.status}, expected 404", errors)
    require("页面未找到" in not_found.body, "custom 404 body did not contain expected title text", errors)
    require('name="robots" content="noindex, follow"' in not_found.body, "custom 404 page missing noindex meta", errors)


def check_static_content(errors: list[str]) -> None:
    tools = fetch(f"{SITE_URL}/tools.html")
    for marker in ["dataset.vercelAnalytics", "SoftwareApplication", "data-logistics-calculator"]:
        require(marker in tools.body, f"tools.html missing marker {marker}", errors)

    sample_article = fetch(f"{SITE_URL}/articles/volumetric-weight-formula-dhl-ems-sf.html")
    require('property="og:type" content="article"' in sample_article.body, "sample article should use article Open Graph type", errors)
    require('property="og:image:alt"' in sample_article.body, "sample article missing Open Graph image alt text", errors)
    require('name="twitter:image"' in sample_article.body, "sample article missing Twitter image meta", errors)
    sample_article_types = parse_json_ld_types(sample_article.body, "sample article", errors)
    require({"Article", "BreadcrumbList"}.issubset(sample_article_types), "sample article missing Article or BreadcrumbList JSON-LD", errors)

    js = fetch(f"{SITE_URL}/assets/site.js")
    for marker in ["ShippingCalculatorLogic", "saveClearedState", "computeCalculatorData", "JSPDF_SRC"]:
        require(marker in js.body, f"assets/site.js missing marker {marker}", errors)
    require(JSPDF_PATH in js.body, "assets/site.js does not load the self-hosted jsPDF file", errors)
    require("cdn.jsdelivr.net/npm/jspdf" not in js.body, "assets/site.js still points PDF export at jsDelivr", errors)
    require("saveStateNow('saveCleared')" not in js.body, "assets/site.js still has old clear-state save pattern", errors)

    ads = fetch(f"{SITE_URL}/ads.txt")
    require(ADS_TXT_LINE in ads.body, "ads.txt missing expected AdSense publisher line", errors)

    verification = fetch(f"{SITE_URL}/{GSC_VERIFICATION_FILE}")
    require(verification.body.strip() == GSC_VERIFICATION_BODY, f"{GSC_VERIFICATION_FILE} has unexpected verification body", errors)

    robots = fetch(f"{SITE_URL}/robots.txt")
    require(f"Sitemap: {SITE_URL}/sitemap.xml" in robots.body, "robots.txt missing canonical sitemap URL", errors)


def check_production_calculator_logic(errors: list[str]) -> None:
    js = fetch(f"{SITE_URL}/assets/site.js").body
    script = f"""
const noop = () => {{}};
global.window = {{
  localStorage: {{ getItem() {{ return null; }}, setItem() {{}}, removeItem() {{}} }},
  location: {{ pathname: '/tools.html', hostname: 'www.bevoorra.business' }},
  clearTimeout,
  setTimeout
}};
global.location = window.location;
global.document = {{
  documentElement: {{ lang: '', classList: {{ add: noop, remove: noop, toggle() {{ return false; }} }} }},
  body: {{ dataset: {{}} }},
  head: {{ appendChild: noop }},
  createElement() {{ return {{ dataset: {{}}, addEventListener: noop, remove: noop }}; }},
  querySelectorAll() {{ return []; }},
  querySelector() {{ return null; }},
  addEventListener: noop,
  dispatchEvent: noop
}};
global.CustomEvent = function CustomEvent(type, init) {{ return {{ type, detail: init && init.detail }}; }};

{js}

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
close(channel(mixed, 'dhlChannel').chargeable, 32, 'production DHL mixed chargeable weight');
close(channel(mixed, 'airChannel').chargeable, 32, 'production air mixed chargeable weight');
close(channel(mixed, 'emsChannel').chargeable, 55, 'production EMS piece chargeable weight');

const exact40 = logic.compute([{{ name: 'edge', qty: 1, l: 40, w: 20, h: 20, kg: 1 }}], 6000);
close(channel(exact40, 'emsChannel').chargeable, 1, 'production EMS exact 40cm boundary');

const custom = logic.compute([{{ name: 'custom', qty: 1, l: 50, w: 50, h: 50, kg: 10 }}], 4000);
close(channel(custom, 'customChannel').chargeable, 31.25, 'production custom divisor chargeable weight');
"""
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as handle:
        handle.write(script)
        script_path = handle.name
    try:
        completed = subprocess.run(
            ["node", script_path],
            text=True,
            capture_output=True,
            timeout=25,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        errors.append(f"production calculator runtime check could not run: {exc}")
        return
    finally:
        try:
            Path(script_path).unlink(missing_ok=True)
        except OSError:
            pass
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        errors.append(f"production calculator runtime check failed: {detail}")


def check_external_dependencies(errors: list[str]) -> None:
    jspdf = fetch(f"{SITE_URL}/{JSPDF_PATH}")
    require(jspdf.status == 200, f"self-hosted jsPDF returned {jspdf.status}", errors)
    require("jsPDF" in jspdf.body, "self-hosted jsPDF response did not contain expected jsPDF marker", errors)
    license_file = fetch(f"{SITE_URL}/assets/vendor/jspdf.LICENSE.txt")
    require(license_file.status == 200, f"jsPDF license file returned {license_file.status}", errors)
    for marker in ["Permission is hereby granted", "THE SOFTWARE IS PROVIDED"]:
        require(marker in license_file.body, f"jsPDF license file missing expected license marker: {marker}", errors)


def check_sitemap(errors: list[str]) -> None:
    sitemap = fetch(f"{SITE_URL}/sitemap.xml")
    try:
        root = ET.fromstring(sitemap.body)
    except ET.ParseError as exc:
        errors.append(f"sitemap.xml is not parseable XML: {exc}")
        return
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = [node.text or "" for node in root.findall("sm:url/sm:loc", namespace)]
    require(len(locs) == len(set(locs)), "sitemap contains duplicate URLs", errors)
    article_locs = [loc for loc in locs if "/articles/" in loc]
    require(len(article_locs) == MIN_ARTICLES, f"sitemap has {len(article_locs)} article URLs, expected {MIN_ARTICLES}", errors)
    expected_total = len(REQUIRED_SITEMAP_URLS) + MIN_ARTICLES
    require(len(locs) == expected_total, f"sitemap has {len(locs)} URLs, expected {expected_total}", errors)
    for expected in REQUIRED_SITEMAP_URLS:
        require(expected in locs, f"sitemap missing {expected}", errors)
    for loc in locs:
        if not loc.startswith(SITE_URL):
            errors.append(f"sitemap URL is outside production domain: {loc}")
            continue
        result = fetch(loc)
        require(result.status == 200, f"sitemap URL returned {result.status}: {loc}", errors)
        if "<html" in result.body[:300].lower():
            expected_canonical = f'<link rel="canonical" href="{loc}">'
            require(expected_canonical in result.body, f"sitemap URL canonical mismatch: {loc}", errors)
            require('name="robots" content="index, follow"' in result.body, f"sitemap URL is not indexable: {loc}", errors)
            require("dataset.vercelAnalytics" in result.body, f"sitemap URL missing Vercel Analytics marker: {loc}", errors)
            require("/_vercel/insights/script.js" in result.body, f"sitemap URL missing Vercel Analytics script path: {loc}", errors)
            schema_types_for_page = parse_json_ld_types(result.body, loc, errors)
            require(bool(schema_types_for_page), f"sitemap URL has no parseable JSON-LD: {loc}", errors)


def check_assets_from_pages(errors: list[str]) -> None:
    sitemap = fetch(f"{SITE_URL}/sitemap.xml")
    try:
        root = ET.fromstring(sitemap.body)
    except ET.ParseError as exc:
        errors.append(f"could not parse sitemap for asset checks: {exc}")
        return
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    pages = [node.text or "" for node in root.findall("sm:url/sm:loc", namespace)]
    checked: set[str] = set()
    for page in pages:
        if not page.startswith(SITE_URL):
            continue
        result = fetch(page)
        parser = AssetParser()
        parser.feed(result.body)
        for asset in parser.assets:
            absolute = urljoin(page, asset)
            if absolute in checked:
                continue
            checked.add(absolute)
            asset_result = fetch(absolute)
            require(asset_result.status == 200, f"asset link returned {asset_result.status}: {absolute}", errors)


def main() -> int:
    errors: list[str] = []
    checks = [
        check_dns,
        check_core_pages,
        check_static_content,
        check_production_calculator_logic,
        check_external_dependencies,
        check_sitemap,
        check_assets_from_pages,
    ]
    for check in checks:
        try:
            check(errors)
        except RuntimeError as exc:
            errors.append(str(exc))
    if errors:
        print(f"FAILED: {len(errors)} production issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: production verification completed")
    print(f"- domain: {SITE_URL}")
    print(f"- sitemap articles: {MIN_ARTICLES}")
    print("- checked DNS, HTTP to HTTPS redirects, core pages, all sitemap URLs, canonical tags, indexable sitemap pages, sitemap page analytics, sitemap page JSON-LD, sitemap page assets, production calculator logic, self-hosted jsPDF, analytics script, ads.txt, Google verification, robots.txt, sitemap, and custom 404")
    return 0


if __name__ == "__main__":
    sys.exit(main())
