# -*- coding: utf-8 -*-
import db_constants

HEADERS = {
    "User-Agent": "SCP-Spider/1.0 (personal archive; low rate)",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.7",
}

CATE_DB_NAME = db_constants.CATE_DB_NAME
DETAIL_DB_NAME = db_constants.DETAIL_DB_NAME
TEST_DB_NAME = db_constants.TEST_DB_NAME

URL_BASE = "https://scp-wiki-cn.wikidot.com"

# Stop probing further series pages after this many, even if none 404.
SERIES_PROBE_MAX = 30
CN_SERIES_PROBE_MAX = 20

DATA_TYPE = {
    "scp-series": 1,
    "scp-series-cn": 2,
    "joke-scps": 3,
    "joke-scps-cn": 4,
    "scp-ex": 5,
    "scp-ex-cn": 6,
    "tales-by-page-name": 7,
    "tales-cn-by-page-name": 8,
    "canon-hub": 9,
    "canon-hub-cn": 10,
    "series-archive": 11,
    "series-archive-cn": 12,
    "reports-interviews-and-logs": 13,
    "log-of-anomalous-page-cn": 14,
    "short-story": 15,
    "library-single-page": 16,
    "goi": 17,
    "art": 18,
    "contest-archive": 19,
    "contest-archive-cn": 20,
    "wander": 21,
    "wander-cn": 22,
    "scp-international": 23,
    "info-single-page": 24,
    "offset": 100,
}

# Catalog seeds. Further /p/N pages are discovered from the pager.
# Series pages are requested as a chain until HTTP 404, not listed here.
LIST_SEED_URLS = [
    f"{URL_BASE}/joke-scps",
    f"{URL_BASE}/joke-scps-cn",
    f"{URL_BASE}/scp-ex",
    f"{URL_BASE}/scp-ex-cn",
    f"{URL_BASE}/tales-by-page-name",
    f"{URL_BASE}/tales-cn-by-page-name",
    f"{URL_BASE}/canon-hub",
    f"{URL_BASE}/canon-hub-cn",
    f"{URL_BASE}/series-archive",
    f"{URL_BASE}/series-archive-cn",
    f"{URL_BASE}/incident-reports-eye-witness-interviews-and-personal-logs",
    f"{URL_BASE}/scp-artwork-hub",
    f"{URL_BASE}/goi-formats",
    f"{URL_BASE}/contest-archive",
    f"{URL_BASE}/contest-archive-cn",
    f"{URL_BASE}/wanderers:the-index",
    f"{URL_BASE}/wanderers:the-index-cn",
    f"{URL_BASE}/wanderers:the-library-cn",
    f"{URL_BASE}/scp-international",
    f"{URL_BASE}/lost-scp-series",
]

LIBRARY_PAGE = [
    f"{URL_BASE}/user-curated-lists",
    f"{URL_BASE}/log-of-anomalous-items",
    f"{URL_BASE}/log-of-extranormal-events",
    f"{URL_BASE}/log-of-extranormal-events-cn",
    f"{URL_BASE}/log-of-unexplained-locations",
]

# First page only. ScpSinglePageSpider follows the pager.
PAGINATED_SINGLE_PAGES = [
    f"{URL_BASE}/log-of-anomalous-items-cn",
    f"{URL_BASE}/short-stories",
]

INFO_PAGE = [
    f"{URL_BASE}/about-the-scp-foundation",
    f"{URL_BASE}/groups-of-interest",
    f"{URL_BASE}/groups-of-interest-cn",
    f"{URL_BASE}/object-classes",
    f"{URL_BASE}/personnel-and-character-dossier",
    f"{URL_BASE}/security-clearance-levels",
    f"{URL_BASE}/secure-facilities-locations",
    f"{URL_BASE}/secure-facilities-locations-cn",
    f"{URL_BASE}/task-forces",
    f"{URL_BASE}/guide-hub",
    f"{URL_BASE}/faq",
    f"{URL_BASE}/guide-for-newbies",
    f"{URL_BASE}/how-to-write-an-scp",
    f"{URL_BASE}/image-use-policy",
    f"{URL_BASE}/licensing-guide",
    f"{URL_BASE}/tag-guide",
    f"{URL_BASE}/translation-movement-guide",
    f"{URL_BASE}/translation-rules",
    f"{URL_BASE}/site-rules",
    f"{URL_BASE}/deletions-guide",
    f"{URL_BASE}/criticism-policy",
]

REPORT_SUBTYPES = (
    "lab_record",
    "discovery_report",
    "event_report",
    "interview",
    "addon",
)
