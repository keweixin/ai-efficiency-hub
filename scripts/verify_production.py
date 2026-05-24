from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen
import socket
import ssl
import sys
import xml.etree.ElementTree as ET


SITE_URL = "https://www.bevoorra.business"
ROOT_DOMAIN_URL = "https://bevoorra.business"
HTTP_ROOT_DOMAIN_URL = "http://bevoorra.business"
HTTP_WWW_URL = "http://www.bevoorra.business"
ADS_TXT_LINE = "google.com, pub-7663008606677915, DIRECT, f08c47fec0942fa0"
MIN_ARTICLES = 30


@dataclass
class FetchResult:
    url: str
    status: int
    final_url: str
    body: str


class AssetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.assets: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        for key in ("href", "src", "srcset"):
            value = values.get(key)
            if not value:
                continue
            first = value.split()[0]
            if first.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if any(marker in first for marker in ("assets/", "articles/", ".html", ".css", ".js", ".png", ".webp")):
                self.assets.add(first)


def fetch(url: str, timeout: int = 25) -> FetchResult:
    request = Request(url, headers={"User-Agent": "ai-efficiency-hub-production-check/1.0"})
    try:
        with urlopen(request, timeout=timeout, context=ssl.create_default_context()) as response:
            raw = response.read()
            charset = response.headers.get_content_charset() or "utf-8"
            return FetchResult(url, response.status, response.geturl(), raw.decode(charset, errors="replace"))
    except HTTPError as error:
        raw = error.read()
        charset = error.headers.get_content_charset() or "utf-8"
        return FetchResult(url, error.code, error.geturl(), raw.decode(charset, errors="replace"))
    except URLError as error:
        raise RuntimeError(f"{url} failed: {error}") from error


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


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

    js = fetch(f"{SITE_URL}/assets/site.js")
    for marker in ["ShippingCalculatorLogic", "saveClearedState", "computeCalculatorData", "JSPDF_SRC"]:
        require(marker in js.body, f"assets/site.js missing marker {marker}", errors)
    require("saveStateNow('saveCleared')" not in js.body, "assets/site.js still has old clear-state save pattern", errors)

    ads = fetch(f"{SITE_URL}/ads.txt")
    require(ADS_TXT_LINE in ads.body, "ads.txt missing expected AdSense publisher line", errors)

    robots = fetch(f"{SITE_URL}/robots.txt")
    require(f"Sitemap: {SITE_URL}/sitemap.xml" in robots.body, "robots.txt missing canonical sitemap URL", errors)


def check_sitemap(errors: list[str]) -> None:
    sitemap = fetch(f"{SITE_URL}/sitemap.xml")
    try:
        root = ET.fromstring(sitemap.body)
    except ET.ParseError as exc:
        errors.append(f"sitemap.xml is not parseable XML: {exc}")
        return
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = [node.text or "" for node in root.findall("sm:url/sm:loc", namespace)]
    article_locs = [loc for loc in locs if "/articles/" in loc]
    require(len(article_locs) == MIN_ARTICLES, f"sitemap has {len(article_locs)} article URLs, expected {MIN_ARTICLES}", errors)
    for expected in [SITE_URL, f"{SITE_URL}/tools.html", f"{SITE_URL}/smoke-test.html"]:
        require(expected in locs, f"sitemap missing {expected}", errors)


def check_assets_from_pages(errors: list[str]) -> None:
    pages = [
        f"{SITE_URL}/",
        f"{SITE_URL}/tools.html",
        f"{SITE_URL}/articles/volumetric-weight-formula-dhl-ems-sf.html",
    ]
    checked: set[str] = set()
    for page in pages:
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
    check_dns(errors)
    check_core_pages(errors)
    check_static_content(errors)
    check_sitemap(errors)
    check_assets_from_pages(errors)
    if errors:
        print(f"FAILED: {len(errors)} production issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: production verification completed")
    print(f"- domain: {SITE_URL}")
    print(f"- sitemap articles: {MIN_ARTICLES}")
    print("- checked DNS, HTTP to HTTPS redirects, core pages, assets, analytics script, ads.txt, robots.txt, sitemap, and custom 404")
    return 0


if __name__ == "__main__":
    sys.exit(main())
