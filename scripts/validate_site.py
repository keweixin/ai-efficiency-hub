from __future__ import annotations

from html import unescape
from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://ai-efficiency-hub.pages.dev"
MIN_ARTICLES = 50
MIN_CJK = 1200
FORBIDDEN_TERMS = [
    "价格",
    "购买",
    "付款",
    "资料包",
    "上架建议",
    "建议定价",
    "机场",
    "节点",
    "破解",
    "封号",
    "绕过",
    "代写",
    "作弊",
    "面包多",
    "顿顿",
    "data-payment-link",
]
OLD_SLUGS = [
    "activity-plan-template.html",
    "ai-account-safety.html",
    "assignment-prompt.html",
    "automation-test-interview.html",
    "cet-ai-study.html",
    "gpt-claude-beginner.html",
    "graduate-project-story.html",
    "prompt-library.html",
    "resume-ai-polish.html",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def cjk_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def strip_tags(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def html_files() -> list[Path]:
    return sorted(ROOT.glob("*.html")) + sorted((ROOT / "articles").glob("*.html"))


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
        if len(re.findall(r"<h2\b", text)) < 4:
            errors.append(f"{path.relative_to(ROOT)} has fewer than 4 h2 sections")
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
    article_urls = re.findall(rf"<loc>{re.escape(SITE_URL)}/articles/[^<]+</loc>", sitemap)
    if len(article_urls) != MIN_ARTICLES:
        errors.append(f"sitemap has {len(article_urls)} article urls")
    for page in ["articles.html", "campus.html", "career.html", "tools.html", "about.html", "privacy.html", "contact.html"]:
        if f"{SITE_URL}/{page}" not in sitemap:
            errors.append(f"sitemap missing {page}")
    if f"{SITE_URL}/404.html" in sitemap:
        errors.append("sitemap should not include 404.html")
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
    public_files += [ROOT / "assets" / "site.js", ROOT / "assets" / "search-index.json", ROOT / "sitemap.xml", ROOT / "robots.txt"]
    for path in public_files:
        if not path.exists():
            continue
        text = read(path)
        for term in FORBIDDEN_TERMS:
            if term in text:
                errors.append(f"{path.relative_to(ROOT)} contains forbidden term: {term}")


def main() -> int:
    errors: list[str] = []
    validate_articles(errors)
    validate_seo(errors)
    validate_links_and_images(errors)
    validate_sitemap_and_index(errors)
    validate_sensitive_terms(errors)
    if errors:
        print(f"FAILED: {len(errors)} issue(s)")
        for error in errors[:200]:
            print(f"- {error}")
        return 1
    print("PASS: site validation completed")
    print(f"- articles: {MIN_ARTICLES}")
    print(f"- minimum CJK chars per article: {MIN_CJK}")
    print("- SEO, links, images, sitemap, search index, and sensitive terms checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
