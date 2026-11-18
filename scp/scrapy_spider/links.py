# -*- coding: utf-8 -*-
"""URL helpers shared by spiders and the pipeline."""
import re

SITE_HOST = "scp-wiki-cn.wikidot.com"
SITE_PREFIXES = (
    "https://scp-wiki-cn.wikidot.com",
    "http://scp-wiki-cn.wikidot.com",
)

SERIES_LINK = re.compile(r"^/scp-(\d+)$")
LOST_SERIES_LINK = re.compile(r"^/scp-l(\d+)$")
CN_SERIES_LINK = re.compile(r"^/scp-cn-(\d+)$")
PAGE_SUFFIX = re.compile(r"/p/\d+$")
PAGER_TOTAL = re.compile(
    r'class="pager-no"[^>]*>\s*page\s+\d+\s+of\s+(\d+)',
    re.I,
)
HREF_RE = re.compile(r"""href=["']([^"'#]+)["']""", re.I)

# Safety cap so a broken pager cannot enqueue the whole wiki.
MAX_EXTRA_PAGES = 100


def normalize_link(link):
    """Return a site path (``/scp-173``) or an empty string when it is not ours."""
    if not link:
        return ""
    link = link.strip()
    for prefix in SITE_PREFIXES:
        if link.startswith(prefix):
            link = link[len(prefix):]
            break
    else:
        if link.startswith("http://") or link.startswith("https://"):
            return ""
    link = link.split("?")[0].split("#")[0]
    if not link.startswith("/"):
        return ""
    if len(link) <= 1:
        return ""
    return link


def page_number(url):
    match = re.search(r"/p/(\d+)$", url.split("?")[0].rstrip("/"))
    if not match:
        return 1
    return int(match.group(1))


def strip_page_suffix(url):
    return PAGE_SUFFIX.sub("", url.split("?")[0].rstrip("/"))


def extra_page_urls(url, html):
    """Other ``/p/N`` URLs for a list page. Only the first page fans out."""
    if PAGE_SUFFIX.search(url.split("?")[0].rstrip("/")):
        return []
    totals = [int(value) for value in PAGER_TOTAL.findall(html or "")]
    if not totals:
        return []
    last = min(max(totals), MAX_EXTRA_PAGES)
    if last <= 1:
        return []
    base = strip_page_suffix(url)
    return ["%s/p/%s" % (base, number) for number in range(2, last + 1)]


def parent_slug(link):
    path = normalize_link(link) or (link or "")
    path = path.split("/offset/")[0]
    return path.strip("/")


def child_links(parent_link, html):
    """Offset and fragment URLs that belong to this article, in document order."""
    slug = parent_slug(parent_link)
    if not slug or not html:
        return []
    found = []
    seen = set()
    prefix = "/" + slug + "/offset/"
    for raw in HREF_RE.findall(html):
        path = normalize_link(raw)
        if not path or path in seen:
            continue
        if path.startswith(prefix):
            seen.add(path)
            found.append(path)
            continue
        if path.startswith("/fragment:"):
            name = path.split(":", 1)[-1]
            if name == slug or name.startswith(slug + "-"):
                seen.add(path)
                found.append(path)
    return found
