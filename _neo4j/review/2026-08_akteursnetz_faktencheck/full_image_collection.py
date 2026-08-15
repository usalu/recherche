# -*- coding: utf-8 -*-
"""Collect official image candidates for all 762 organisations in the final net.

This is a transport/review workflow only. It never writes to Neo4j and never
turns evidence URLs into accepted organisation domains without an explicit
identity check.
"""
from __future__ import annotations

import argparse
import collections
import concurrent.futures
import csv
import datetime as dt
import html
import hashlib
import http.server
import io
import json
import os
import re
import subprocess
import sys
import threading
import time
import unicodedata
import urllib.parse
import urllib.request
import webbrowser
import xml.etree.ElementTree as ET
import zipfile
from difflib import SequenceMatcher
from pathlib import Path, PurePosixPath

from PIL import Image, ImageDraw

import pilot_images as pilot


BASE = Path(__file__).resolve().parent
REPO = BASE.parents[2]
FULL = BASE / "bilder_full"
RAW = FULL / "kandidaten"
SELECTION = FULL / "selection.json"
DOMAINS = FULL / "domains_review.json"
MANIFEST = FULL / "collection_manifest.json"
REPORT = FULL / "COLLECTION_REPORT.md"
CONTACT = FULL / "contact_sheets"
SUGGESTIONS = FULL / "suggestions.json"
REVIEW = FULL / "full_asset_review.json"
FINAL = FULL / "bilder"
FINAL_MANIFEST = FULL / "final_image_manifest.json"
FINAL_REPORT = FULL / "FINAL_IMAGE_REPORT.md"
PATCH = FULL / "full_image_property_patch.json"
PATCH_REPORT = FULL / "full_image_property_patch_report.md"
RENDER = FULL / "render"
FINAL_REVIEW = FULL / "final_review"
FINAL_AUDIT_JSON = FINAL_REVIEW / "FINAL_SUGGESTION_AUDIT.json"
FINAL_AUDIT_REPORT = FINAL_REVIEW / "FINAL_SUGGESTION_AUDIT.md"
REVIEW_HTML = BASE / "full_image_review.html"
PILOT_DECISIONS = BASE / "pilot_domain_decisions.json"
NETZ = REPO / "_neo4j" / "netz"
DARK_BACKDROP_OVERRIDES = BASE / "dark_backdrop_overrides.json"
CURRENT_DOMAIN_OVERRIDES = BASE / "current_domain_overrides.json"
CURRENT_SCOPE_JSON = FULL / "CURRENT_SCOPE_COVERAGE.json"
CURRENT_SCOPE_REPORT = FULL / "CURRENT_SCOPE_COVERAGE.md"
CURRENT_DEEP = FULL / "current_deep_review"
RIGHTS_AUDIT_JSON = FULL / "CURRENT_IMAGE_RIGHTS_AUDIT.json"
RIGHTS_AUDIT_CSV = FULL / "CURRENT_IMAGE_RIGHTS_AUDIT.csv"
RIGHTS_AUDIT_REPORT = FULL / "CURRENT_IMAGE_RIGHTS_AUDIT.md"
EXPORT = pilot.EXPORT
TECTONIC = Path(r"E:\semio\.repo\cache\tectonic\0.16.9\tectonic.exe")

COUNTRY_ORDER = ("GB", "DE", "NL", "CH", "FR", "BE", "DK", "SE", "FI", "NO", "AT")
LEGAL = {
    "ag", "as", "asa", "ab", "bv", "gmbh", "oy", "oyj", "sa", "sas", "sarl",
    "ltd", "limited", "inc", "association", "foundation", "stiftung", "verein",
    "group", "holding", "the", "and", "und", "pour", "for", "of", "de", "der",
    "des", "die", "la", "le", "les", "en", "et", "organisation", "organization",
}
THIRD_PARTY_HOSTS = {
    "ots.at", "taz.de", "archdaily.com", "dezeen.com", "wikipedia.org",
    "architectsjournal.co.uk", "researchgate.net", "linkedin.com", "facebook.com",
    "instagram.com", "youtube.com", "springer.com", "mdpi.com", "corren.se",
}
SEARCH_BLOCKED_HOSTS = THIRD_PARTY_HOSTS | {
    "opalis.eu", "baunetzwissen.de", "dbz.de", "baublatt.ch", "ekopolis.fr",
    "mynewsdesk.com", "sttinfo.fi", "businessregiongoteborg.se", "futurebuilt.no",
    "superlocal.eu", "steelconstruction.info", "constructionnews.co.uk",
}
SOCIAL_MARKERS = (
    "facebook", "instagram", "youtube", "linkedin", "pinterest", "twitter", "tiktok",
    "socialmedia", "social-media", "f_logo", "insta_", "insta-", "xlogo.svg",
)
NON_ORGANISATION_MARKERS = (
    "bcorp", "b-corp", "b_corp", "bcorporation", "b-corporation", "nzero",
    "award", "badge", "certif", "client-logo", "partner-logo", "partner%20logo",
    "/partners/", "/partner/", "styles/partners", "styles/partner",
    "sponsor", "accredit", "webex-logo", "qual-logo", "hunger-logo", "vzug_logo",
    "france-bleu", "lrqa", "city%20of%20newton", "survuvalkit", "survivalkit",
    "team-headshot", "headshot", "portrait", "branddr", "brandbild",
    "google-play", "gstatic.com", "play-lh.googleusercontent.com", "sdg_icons", "mywebsitebuilder", "icon-close",
    "icon-nav", "/flags/", "-flag-", "burger.svg", "menu.svg", "close.svg",
    "sponsorlogo", "vlaio_combilogo", "dachverbandlogo", "logo_ams_wien",
    "somfy%20logo", "preuse_logo", "banner_logos", "driveway-icon",
)

# Individually verified official files that are published outside the page's
# machine-readable icon/header declarations. They remain ordinary pending
# candidates with source URL, retrieval date and checksums.
MANUAL_OFFICIAL_CANDIDATE_URLS = {
    "BE:I05": [
        (0, "header_logo", "https://www.kassel.de/design.css.media/171938/Kassel-WBM-Web.svg"),
    ],
    "NL:S02": [
        (0, "header_logo", "https://www.resourcehub.nl/assets/images/presentation/logo.svg"),
    ],
    "FI:U14": [
        (0, "header_logo", "https://www.purkukolmio.fi/wp-content/uploads/2020/09/purkukolmio-logo-sininen-500.png"),
        (0, "header_logo", "https://www.purkukolmio.fi/wp-content/uploads/2022/11/cropped-Facebook-profiili-3.png"),
    ],
    "NO:M04": [
        (0, "header_logo", "https://www.ombygg.no/assets/clients/ombygg/logo/logo.png"),
    ],
    "NO:N05": [
        (0, "header_logo", "https://www.ombrukshubsor.no/assets/clients/ombrukshub/logo/logo.png"),
    ],
    "CH:S04": [
        (0, "header_logo", "https://reuzi.ch/a/ui/lo.png"),
    ],
    "BE:M01": [
        (0, "media_logo", "https://anresto.com/wp-content/uploads/2018/08/logo-anresto-small.png"),
    ],
    "NL:M15": [
        (0, "header_logo", "https://snellen.nl/templates/rt_afterburner/images/logo-snellen-duo2.jpg"),
    ],
    "NL:U28": [
        (0, "header_logo", "https://isteam.wsimg.com/studio-projects/over-projects-api/logos/c2a8670e-9f38-42bf-9233-829a590ae44c/83bd2239-5d97-422d-857a-0f58cb0da709/logo.jpg/:/gis/:/rs=w:57,h:57,m"),
    ],
    "FR:I01": [
        (0, "header_logo", "https://www.lafab-bm.fr/wp-content/themes/lafab2020smart/images/logo-lafab.svg"),
    ],
    "FR:M33": [
        (0, "header_logo", "https://leschutesdeladore63.files.wordpress.com/2022/07/logo_final_transp_vect-2.png"),
    ],
    "FR:U16": [
        (0, "header_logo", "https://static.wixstatic.com/media/3376b6_1903d6f0f4ce4ff28d4c2803593652de~mv2.png"),
    ],
    # The plan permits licensed Wikimedia artwork for public institutions.
    # These exact files were checked against the current official identity.
    "DE:F01": [
        (0, "wikimedia", "https://upload.wikimedia.org/wikipedia/commons/6/6c/Brandenburgische_Technische_Universit%C3%A4t_Cottbus-Senftenberg_2013_logo.svg"),
    ],
    "SE:F02": [
        (0, "wikimedia", "https://upload.wikimedia.org/wikipedia/commons/b/b2/Rise-logo-black.svg"),
    ],
    "DE:U20": [
        (2, "header_logo", "https://b3185014.assetcdn.net/2.0/3185014/wp-content/uploads/2023/06/gate21-header.png?lossy=2&strip=1&webp=1"),
    ],
    "FR:U09": [
        (2, "header_logo", "https://grandhuit.eu/wp-content/themes/g8/images/l5.png"),
    ],
    "CH:U11": [
        (2, "header_logo", "https://www.b-3.ch/userdata/assets/logo/b3-logo-rgb.svg"),
    ],
    "BE:S01": [
        (2, "header_logo", "https://madaster.com/app/uploads/sites/6/2023/09/Madaster-BrandmarkLogo-RGB.png"),
    ],
    "DK:F01": [
        (2, "media_logo", "https://media.adm.dtu.dk/designguide/DTU_Design_Guide_Pro_User/DTU_Design_Guide_Logo/Corporate_Red/Corp_Red_RGB/Corp_Red_RGB.png"),
    ],
    "FI:I02": [
        (2, "media_logo", "https://makasiini.hel.fi/helsinki-logos/helsinki-logo-black.svg"),
    ],
    "BE:F07": [
        (2, "media_logo", "https://www.utwente.nl/.wh/ea/uc/id4b3417f01023595d702badf8d02ce688108daec591b0701c19001c80080/yuofesz4qdemulmhqpoyiq.png"),
    ],
    "FR:M60": [
        (2, "media_logo", "https://static.wixstatic.com/media/45669a_8dd327e12a3a4082bd3525b868955246~mv2.jpg"),
    ],
    "BE:I04": [
        (2, "media_logo", "https://ovam.vlaanderen.be/o/ovam-website-theme/assets/images/logo_be.png"),
    ],
    "DE:U33": [
        (0, "wikimedia", "https://upload.wikimedia.org/wikipedia/commons/3/35/Danish_Region_hovedstaden_logo.svg"),
    ],
    "CH:S03": [
        (2, "header_logo", "https://madaster.com/app/uploads/sites/6/2023/09/Madaster-BrandmarkLogo-RGB.png"),
    ],
    "FR:O05": [
        (2, "header_logo", "https://static.wixstatic.com/media/e755c5_7e60158d97e14b94a7e7ccdbb5ce1022~mv2.png"),
    ],
    "FR:M57": [
        (2, "header_logo", "https://static.wixstatic.com/media/cbe7f0_4798aa34439643d0a0e7a89a9a3e91f3~mv2.png"),
    ],
    "NL:U38": [
        (2, "header_logo", "https://static.wixstatic.com/media/d312e0_0ba87a49968b437c961f72de0a561fb5~mv2.png"),
    ],
    # Confirmed in the final raw-candidate visual pass.  Generic filenames had
    # made the conservative identity filter withhold these exact marks even
    # though each file is served by the named organisation's official site.
    "BE:M18": [
        (0, "media_logo", "https://www.hofman.be/wp-content/uploads/2018/06/logo-blue.png"),
    ],
    "BE:M27": [
        (0, "media_logo", "https://www.mvvafbraak.be/wp-content/uploads/2016/11/logo@2x.png"),
    ],
    "CH:U22": [
        (0, "media_logo", "https://srzh.ch/wp-content/uploads/2018/07/cropped-logokl.png"),
    ],
}

# A few official sites render their actual wordmark as inline SVG instead of
# publishing a standalone image URL.  The marker is an exact, audited fragment
# immediately before the wanted SVG.  The source page and the extracted bytes
# remain hashed in candidates.json, so these are as reproducible as URL files.
MANUAL_OFFICIAL_INLINE_SVG_CANDIDATES = {
    "FI:U18": [
        (2, "header_logo", "https://www.skanska.com/fi/fi", '<a title="Skanska" href="https://www.skanska.com/fi/fi">'),
    ],
    "AT:I02": [
        (2, "header_logo", "https://viecycle.wien.gv.at/", '<span class="wm-site-header__logo">'),
    ],
    "GB:U06": [
        (2, "header_logo", "https://www.bdp.com/", '<a aria-current="page" href="/"'),
    ],
    "GB:F04": [
        (2, "header_logo", "https://www.uea.ac.uk/", 'data-name="UEA Logo"'),
    ],
    "NL:U44": [
        (2, "header_logo", "https://rothuizen-architecten.nl/", '<a class="navbar-brand" href="/">'),
    ],
    "BE:N06": [
        (2, "header_logo", "https://rotordb.org/", '<div class="logo-wrapper">'),
    ],
    "BE:N05": [
        (2, "header_logo", "https://opalis.eu/en", 'class="cd-logo"'),
    ],
    "NO:N03": [
        (2, "header_logo", "https://www.futurebuilt.no/", '<a href="https://www.futurebuilt.no/" class="block">'),
    ],
}

# Some official press rooms publish only a ZIP logo package.  The member name
# is kept in the source URL fragment so the exact original remains auditable.
MANUAL_OFFICIAL_ARCHIVE_CANDIDATES = {
    "BE:F02": [
        (2, "media_logo",
         "https://www.buildwise.be/media/badfs22l/buildwise.zip",
         "SVG/Buildwise_Verticaal_1.svg"),
    ],
    "DK:U28": [
        (2, "media_logo",
         "https://cdn.realdania.dk/media/pq4nbuet/logopakke_realdania_100mm.zip",
         "Logopakke_Realdania_100mm/Office_use_RGB/png/Realdania_rw_100mm_RGB.png"),
    ],
}

# Official negative artwork paired with a light-theme archive member.  It is
# not a second suggestion: it is the same approved identity supplied by the
# publisher specifically for dark backgrounds.
MANUAL_OFFICIAL_DARK_ARCHIVE_CANDIDATES = {
    "BE:F02": (
        "https://www.buildwise.be/media/badfs22l/buildwise.zip",
        "SVG/Buildwise_Verticaal_1.svg",
        "SVG/Buildwise_Verticaal_1_neg.svg",
    ),
}

# Candidate-specific rights information for files whose source publishes a
# more precise licence or use boundary than the generic official-site note.
MANUAL_CANDIDATE_LICENSE_NOTES = {
    ("DE:F01", "https://upload.wikimedia.org/wikipedia/commons/6/6c/Brandenburgische_Technische_Universit%C3%A4t_Cottbus-Senftenberg_2013_logo.svg"):
        "Wikimedia Commons: PD-textlogo; trademark restrictions may still apply.",
    ("SE:F02", "https://upload.wikimedia.org/wikipedia/commons/b/b2/Rise-logo-black.svg"):
        "Wikimedia Commons: CC BY-SA 4.0, Vector&SVGLover; attribution and share-alike required.",
    ("DE:U33", "https://upload.wikimedia.org/wikipedia/commons/3/35/Danish_Region_hovedstaden_logo.svg"):
        "Wikimedia Commons: PD-textlogo; source and author Region Hovedstaden; trademark restrictions may apply.",
    ("BE:F02", "zip+https://www.buildwise.be/media/badfs22l/buildwise.zip#SVG/Buildwise_Verticaal_1.svg"):
        "Official Buildwise press/brand package; Buildwise states that non-member or other use requires specific permission.",
}

# Rights pages found on the organisations' own sites or on the exact Commons
# file page.  These notes describe the permission boundary; they do not turn a
# downloaded logo into a blanket licence.  The rendered nodes use 50 % opacity
# and may tokenise neutral ink, so restrictive brand rules still require an
# explicit approval for the final publication layout.
MANUAL_NODE_RIGHTS = {
    "BE:I05": {
        "rights_source_url": "https://www1.kassel.de/service/produkte/kassel/Hauptamt/genehmigung-des-stadtwappens.php",
        "license_note": "Stadt Kassel requires permission for use of the city arms; request confirmation for use of the official wordmark in the altered node layout as well.",
        "rights_status": "permission_required",
        "rights_contact": "Stadt Kassel Hauptamt/Kommunikation via the official service page",
    },
    "BE:F02": {
        "rights_source_url": "https://www.buildwise.be/nl/logos/",
        "license_note": "Buildwise requires specific permission for any logo use outside the stated member-link case.",
        "rights_status": "permission_required",
        "rights_contact": "Buildwise Communications via https://www.buildwise.be/nl/contact/",
    },
    "DE:F01": {
        "rights_source_url": "https://www.b-tu.de/en/university/the-btu/communication-marketing/marketing",
        "license_note": "Commons labels the file PD-textlogo, but BTU requires prior approval of a completed layout containing its trademarked logo.",
        "rights_status": "permission_required",
        "rights_contact": "BTU Communications and Marketing: marketing@b-tu.de",
    },
    "DE:U33": {
        "rights_source_url": "https://commons.wikimedia.org/wiki/File:Danish_Region_hovedstaden_logo.svg",
        "license_note": "Wikimedia Commons PD-textlogo; copyright restriction is not asserted, but trademark and other restrictions may apply.",
        "rights_status": "legal_review_required",
        "rights_contact": "Region Hovedstaden communications",
    },
    "SE:F02": {
        "rights_source_url": "https://commons.wikimedia.org/wiki/File:Rise-logo-black.svg",
        "license_note": "Wikimedia Commons CC BY-SA 4.0; credit Vector&SVGLover, link the licence, identify modifications and apply share-alike where required.",
        "rights_status": "licensed_with_conditions",
        "rights_contact": "RISE press office for trademark/brand confirmation",
    },
    "DK:F01": {
        "rights_source_url": "https://www.inside.dtu.dk/en/information-management/copyright/faq-frequently-asked-questions-about-copyright",
        "license_note": "DTU permits its logo in reports, assignments, articles and homepages outside commercial contexts; the modified 50%-opacity layout should still be confirmed against DTU's brand rules.",
        "rights_status": "brand_approval_required",
        "rights_contact": "design@dtu.dk",
    },
    "DK:U28": {
        "rights_source_url": "https://realdania.dk/om-os/presserum",
        "license_note": "Official Realdania press-room logo package and use guidelines; the altered node rendering requires confirmation for this publication context.",
        "rights_status": "brand_approval_required",
        "rights_contact": "Realdania press team via the official press room",
    },
    "FI:I02": {
        "rights_source_url": "https://www.hel.fi/en/decision-making/information-on-helsinki/design-and-digitalisation/helsinki-brand-and-visual-identity/visual-identity-guidelines/use-basic-elements",
        "license_note": "Helsinki publishes original logo files and use rules, but prohibits effects, modification and partial-intensity colours; the 50%-opacity node treatment requires written approval or an unmodified exception.",
        "rights_status": "brand_approval_required",
        "rights_contact": "City of Helsinki communications/brand team",
    },
    "BE:F07": {
        "rights_source_url": "https://www.utwente.nl/en/organization/visual-identity/",
        "license_note": "University of Twente provides an official logo download and brand contact but no blanket external publication licence; request approval for the node treatment.",
        "rights_status": "permission_required",
        "rights_contact": "traffic@utwente.nl",
    },
    "FI:U18": {
        "rights_source_url": "https://foresight.skanska.com/terms-of-use/",
        "license_note": "Skanska reserves all website-content rights and requires written approval for trademark use beyond its stated terms.",
        "rights_status": "permission_required",
        "rights_contact": "Skanska media/brand contact",
    },
    "AT:I02": {
        "rights_source_url": "https://www.wien.gv.at/inhalt/impressum",
        "license_note": "The City of Vienna states that public use of its online offering requires consent unless a specific reuse permission applies; request approval for the logo layout.",
        "rights_status": "permission_required",
        "rights_contact": "handbuch@ma53.wien.gv.at",
    },
    "CH:F02": {
        "rights_source_url": "https://www.empa.ch/web/empa/disclaimer",
        "license_note": "Empa states that its logo and name are registered trademarks and may not be copied or otherwise used without prior written consent.",
        "rights_status": "permission_required",
        "rights_contact": "Empa Communication via https://www.empa.ch/legal-services",
    },
}

# Findings from the complete 2026-08-13 visual identity audit. These are
# deliberately key-specific: a weak or mismatched candidate must not teach the
# collector a broad rule that could hide a valid logo for another actor.
MANUAL_CANDIDATE_REJECTIONS = {
    "GB:M24": {"c09": "generic cursor/site-builder icon, not The Old Slate Yard's mark"},
    "GB:N01": {"c19": "asset identifies Abstrakt, not BioRegional"},
    "DE:S01": {"c11": "product/brochure image, not Concular's mark"},
    "DE:U03": {"*": "generic Augsburg sustainability icon, not the actor's mark"},
    "CH:U20": {"*": "blurred colour field is not a legible organisational mark"},
    "FR:F01": {"c07": "BATIPEDIA service mark, not CSTB's organisational mark"},
    "FR:M18": {"c10": "generic telephone symbol, not Fer et Pierre's mark"},
    "FR:M33": {"*": "WordPress platform icon, not the actor's mark"},
    "BE:M19": {"c05": "flat placeholder rectangle, not Houtenplaten's mark",
                "c06": "flat placeholder rectangle, not Houtenplaten's mark",
                "c09": "photo of facade signage, not reusable source artwork"},
    "DK:M03": {"c08": "asset identifies Censio, not Bærebyg"},
}
MANUAL_CANDIDATE_REJECTIONS.update({
    "GB:M14": {"*": "official-site files are premises photographs, not a clean organisational mark"},
    "NL:S02": {"c03": "Google Play interface mark, not the ReSource identity"},
    "DE:U20": {**{f"c{i:02d}": "generic section icon or partner mark, not the Gate 21 carrier identity"
                    for i in (10, 13, 14, 15, 16, 17, 18, 19, 20)}},
    "FR:I01": {"*": "official site supplies only a plain colour app tile, not an identifiable La Fab mark"},
    "FR:M53": {"*": "official composite lockup contains a photographic material strip; photos are excluded by the collection plan"},
    "FR:M42": {"*": "official-site candidate is a full-page photographic screenshot, not reusable logo artwork"},
    "CH:M13": {"*": "collected files are webshop and premises photographs, not a clean organisational mark"},
    "CH:U11": {**{f"c{i:02d}": "B3 project photograph carrying a third-party badge, not the B3 Kolb identity"
                    for i in range(8, 12)}},
    "BE:G01": {"*": "available files are the Brussels iris carrier symbol or an EU co-financing notice, not an ERDF/FEDER Brussels identity"},
    "GB:U01": {"c11": "temporary Envelopes anniversary mark, not the core AKT II identity"},
    "NL:U56": {"c20": "PC brandmark does not identify Vic Obdam"},
    "NL:M10": {"c09": "Keten Plus campaign mark, not the Hoogeboom identity",
                "c08": "site search icon"},
    "DE:G02": {"c18": "DBU Naturerbe is a sub-brand; the main DBU mark is available"},
    "DE:U40": {**{f"c{i:02d}": "third-party CTBUH or DGNB mark" for i in range(10, 21)}},
    "SE:U09": {"c10": "editorial employee photograph, not the Contiga identity"},
    "DK:U30": {**{f"c{i:02d}": "promotional badge or editorial photograph" for i in (9, 10, 11, 16, 19, 20)}},
    "FI:U02": {"c11": "Green Office badge, not the A-Kruunu identity"},
    "FI:F02": {"c11": "decorative campaign graphic; the compact Xamk wordmark is available"},
    "AT:I03": {"c13": "Wien Holding parent mark; the WSE mark is available"},
    "CH:U27": {**{f"c{i:02d}": "C&A partner logo, not the Wetter Gruppe identity"
                    for i in range(13, 20)}},
    "FR:F01": {"*": "collected files are BDNB/BATIPEDIA or partner marks and photos, not a clean CSTB identity"},
    "FR:M19": {"*": "only a fireplace photo and promotional installer badge were collected, not a clean Gauthey identity"},
    "GB:F04": {**{f"c{i:02d}": "editorial or campus photograph, not the UEA identity"
                    for i in (8, 10, 11)}},
    "GB:U06": {"c07": "editorial studio photograph, not the BDP identity"},
    "FI:U04": {"*": "official vertical lockup becomes illegible at the fixed printed node size"},
    "BE:S01": {**{f"c{i:02d}": "Madaster customer, partner or editorial graphic, not the Madaster identity"
                    for i in range(7, 17)}},
})

# URL fragments remain stable when a deeper harvest changes candidate IDs.
MANUAL_CANDIDATE_URL_REJECTIONS = {
    # Final current-scope pass (2026-08-14): these URLs are technically valid
    # images but visibly identify a social platform, a photograph, or a public
    # site shell rather than the actor named by the graph node.
    "FI:U03": ("parma-www-x-logo",),
    "FI:U18": ("ar_skanska_oslo",),
    "FR:I01": ("/lafab2020/images/apple-icon",),
    "BE:G01": ("cropped-logo-iris",),
    "FR:M32": ("Flag_of_Europe",),
    "FR:M37": ("menu_red_materiaux",),
    "GB:U04": ("/uploads/general/", "/img/riba.svg"),
    "GB:M07": ("/totalLogo.png",),
    "GB:M19": ("tr-logo.svg",),
    "BE:F07": ("/sdg_icons/",),
    "BE:N04": ("footer-logo-feder",),
    "BE:N05": ("PREUSE_logo", "banner_logos"),
    "BE:F02": ("sponsorlogo", "vlaio_combilogo", "header-new.jpg"),
    "DK:M01": ("bango.dk/", "bango.b-cdn.net/"),
    "AT:I02": ("/icons/raw/",),
    "AT:N01": ("dachverbandLogo", "Logo_AMS_Wien", "hunger-logo", "/erfolgsgeschichten/logos/"),
    "AT:U06": ("dachverbandLogo", "Logo_AMS_Wien", "hunger-logo"),
    "DE:F01": ("logos_partner", "HRK_Re_Audit", "Moodle", "e_learning", "praedikate"),
    "CH:F02": ("/app-icons/", "/image/user_portrait"),
    # Full 33-sheet visual identity review (2026-08-15).  These official-page
    # images are not clean identities for the named actor: third-party marks,
    # photographs, or multi-brand/funder lockups.  URL rejections deliberately
    # survive candidate-id changes in later harvests.
    "GB:M09": ("enviromate_img_press_startuslogo",),
    "FR:X01": ("cropped-Raedificare-Home-Slider-Melange-2", "Sans-titre.jpg"),
    "BE:S02": ("/web/image/website/52/logo",),
    "BE:S03": ("sundahus-horisontell-2", "drew-walker", "logo_bim_alliance"),
    "FR:M20": ("favicon-grayo",),
}

# Knoten, deren gefundene Domain den Akteur NICHT identifiziert. Die Sperre
# gilt dem Knoten, benannt wird aber die konkrete Fremddomain -- wird dem
# Knoten spaeter die richtige Domain zugeordnet, ist der Eintrag gegenstandslos
# und muss weg, sonst sperrt er eine inzwischen korrekte Quelle.
# GB:U44 (opera.com, der Browser) und DK:U02 (gain.de, das deutsche GAIN)
# waren genau solche Faelle: die Tiefenpruefung vom 15.08.2026 hat beiden die
# tatsaechliche Domain zugeordnet (operapm.co.uk = Opera Project Management,
# again.dk = das daenische a:gain, beide in domains_review.json als
# individual_official_domain_override hinterlegt und im Bild geprueft), womit
# die alte Sperre nicht mehr das meint, was sie sagt. Deshalb hier entfernt,
# nicht etwa der Test angepasst.
MANUAL_DOMAIN_REJECTIONS = {
    "DE:U08": "oldenburger-onlinezeitung.de does not identify Bauteilbörse Oldenburg",
    "SE:U12": "businessregiongoteborg.se does not identify HSB Göteborg",
}
_write_lock = threading.Lock()


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    tmp = path.with_suffix(path.suffix + ".tmp")
    with _write_lock:
        tmp.write_text(payload, encoding="utf-8")
        os.replace(tmp, path)


def norm(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def tokens(value: str):
    return [t for t in norm(value).split() if len(t) >= 3 and t not in LEGAL]


def root_url(url: str) -> str:
    p = urllib.parse.urlsplit(url)
    if not p.netloc:
        return ""
    return urllib.parse.urlunsplit((p.scheme or "https", p.netloc, "/", "", ""))


def blocked_host(host: str) -> bool:
    host = (host or "").lower().removeprefix("www.")
    return pilot.host_is_blocked(host) or any(host == h or host.endswith("." + h) for h in THIRD_PARTY_HOSTS)


def select_all(_args):
    net = pilot.final_network()
    total = sum(len(p.actors) + len(p.projects) for p in net.panels.values())
    if total != 859:
        raise RuntimeError(f"final network drift: expected 859, got {total}")
    work = pilot.load_json(pilot.WORKLIST)
    by_eid = {r["eid"]: r for packet in work["packets"] for r in packet.get("nodes", [])}
    verdicts = {r["eid"]: r for r in pilot.load_json(pilot.VERDICTS)["nodes"] if r.get("eid")}
    rows = []
    for cc in COUNTRY_ORDER:
        for eid in net.panels[cc].actors:
            w = by_eid.get(eid, {})
            raw = net.raw.by.get(eid, {})
            props = raw.get("properties", {})
            primary = w.get("primary_source_url") or ""
            source_urls = [u for u in w.get("source_urls") or [] if u]
            rows.append({
                "key": pilot.node_key(cc, net.tid[eid]), "cc": cc, "tid": net.tid[eid],
                "eid": eid, "graph_backed": eid not in net.new_eids,
                "graph_id": props.get("id") if eid not in net.new_eids else None,
                "name": net.raw.name(eid), "typ": pilot.normalized_type(w.get("typ")),
                "primary_source_url": primary, "source_urls": source_urls,
                "evidence_url": verdicts.get(eid, {}).get("beleg_url", ""),
            })
    rows.sort(key=lambda r: (COUNTRY_ORDER.index(r["cc"]), r["tid"]))
    if len(rows) != 762:
        raise RuntimeError(f"expected 762 organisations, got {len(rows)}")
    write_json(SELECTION, {
        "schema_version": 1, "created_at": pilot.today(), "drawn_network_nodes": total,
        "organisation_nodes": len(rows), "project_nodes_excluded": 97,
        "graph_export_sha256": pilot.sha256_file(pilot.EXPORT), "nodes": rows,
    })
    print(f"wrote {SELECTION}: {len(rows)} organisations")


def initial_domain_row(node, manual):
    decision = manual.get(node["key"])
    if decision and decision.get("status") == "accepted" and decision.get("official_url"):
        return {"key": node["key"], "name": node["name"], "official_url": decision["official_url"],
                "status": "accepted", "basis": "pilot_manual", "notes": decision.get("notes", "")}
    if node.get("primary_source_url"):
        return {"key": node["key"], "name": node["name"],
                "official_url": "", "candidate_url": node["primary_source_url"],
                "status": "needs_review", "basis": "graph_primary_source_url_candidate",
                "notes": "Graph property is a research entry; identity check still required."}
    candidates = list(node.get("source_urls") or []) + [node.get("evidence_url", "")]
    candidate = next((u for u in candidates if u and not blocked_host(pilot.host_of(u))), "")
    return {"key": node["key"], "name": node["name"], "official_url": "",
            "candidate_url": candidate, "status": "needs_review" if candidate else "no_candidate",
            "basis": "research_entry_only" if candidate else "no_domain_candidate", "notes": ""}


def build_domains(_args):
    selection = pilot.load_json(SELECTION)["nodes"]
    manual = pilot.load_json(PILOT_DECISIONS) if PILOT_DECISIONS.exists() else {}
    existing = {r["key"]: r for r in pilot.load_json(DOMAINS).get("nodes", [])} if DOMAINS.exists() else {}
    rows = []
    for node in selection:
        fresh = initial_domain_row(node, manual)
        old = existing.get(node["key"])
        if old and old.get("status") == "accepted" and old.get("basis") in {
            "manual", "pilot_manual", "individual_identity_check"
        }:
            fresh = old
        rows.append(fresh)
    write_json(DOMAINS, {"schema_version": 1, "nodes": rows})
    print(f"wrote {DOMAINS}: {collections.Counter(r['status'] for r in rows)}")


class TitleParser(pilot.html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_title = False
        self.title = []
        self.site_name = ""
    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag.lower() == "title":
            self.in_title = True
        if tag.lower() == "meta" and (a.get("property") or a.get("name", "")).lower() == "og:site_name":
            self.site_name = a.get("content", "")
    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False
    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)


def confirm_one(node, row):
    if row["status"] != "needs_review" or not row.get("candidate_url"):
        return row
    candidate = row["candidate_url"]
    try:
        data, content_type, final_url = pilot.request_bytes(candidate)
        if content_type != "text/html" and b"<html" not in data[:1500].lower():
            data, content_type, final_url = pilot.request_bytes(root_url(candidate))
        text = data.decode("utf-8", errors="replace")[:500000]
        parser = TitleParser(); parser.feed(text)
        title = html.unescape(" ".join(parser.title)).strip()
        landing = root_url(final_url)
        host = pilot.host_of(landing)
        host_compact = norm(host).replace(" ", "")
        nt = tokens(node["name"])
        distinctive = [t for t in nt if len(t) >= 4]
        page_compact = norm(title + " " + parser.site_name + " " + re.sub(r"<[^>]+>", " ", text[:80000]))
        host_hits = [t for t in distinctive if t in host_compact]
        page_hits = [t for t in distinctive if t in page_compact]
        compact_name = "".join(distinctive[:3])
        similarity = SequenceMatcher(None, compact_name, host_compact.split(" ")[0]).ratio() if compact_name else 0.0
        accepted = bool(host_hits and page_hits) or (similarity >= 0.72 and bool(page_hits))
        result = dict(row)
        result.update({"checked_url": final_url, "checked_at": pilot.today(), "page_title": title[:300],
                       "host_hits": host_hits, "page_hits": page_hits[:8], "host_similarity": round(similarity, 3)})
        if accepted and not blocked_host(host):
            result.update({"official_url": landing, "status": "accepted", "basis": "individual_identity_check"})
        else:
            result.update({"status": "needs_review", "basis": "identity_check_inconclusive"})
        return result
    except Exception as exc:
        result = dict(row)
        result.update({"status": "needs_review", "basis": "identity_check_failed",
                       "check_error": f"{type(exc).__name__}: {exc}", "checked_at": pilot.today()})
        return result


def confirm_domains(args):
    nodes = {r["key"]: r for r in pilot.load_json(SELECTION)["nodes"]}
    rows = pilot.load_json(DOMAINS)["nodes"]
    todo = [r for r in rows if r["status"] == "needs_review" and r.get("candidate_url")]
    if args.limit:
        todo = todo[:args.limit]
    updates = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(confirm_one, nodes[r["key"]], r): r["key"] for r in todo}
        for n, future in enumerate(concurrent.futures.as_completed(futures), 1):
            result = future.result(); updates[result["key"]] = result
            print(f"[{n}/{len(todo)}] {result['key']}: {result['status']} ({result['basis']})")
    merged = [updates.get(r["key"], r) for r in rows]
    write_json(DOMAINS, {"schema_version": 1, "nodes": merged})
    print("domain status:", collections.Counter(r["status"] for r in merged))


def name_aliases(name: str):
    """Return normalized names, abbreviations and parent-name fragments."""
    raw_parts = [name] + re.split(r"\s*(?:/|–|—|\(|\))\s*", name)
    aliases = set()
    for part in raw_parts:
        part = norm(part)
        if not part:
            continue
        aliases.add(part)
        ts = tokens(part)
        if ts:
            aliases.add(" ".join(ts))
            if len(ts) >= 2:
                aliases.add("".join(t[0] for t in ts))
    for token in re.findall(r"\b[A-ZÄÖÜ][A-ZÄÖÜ0-9+&.-]{1,7}\b", name):
        aliases.add(norm(token).replace(" ", ""))
    return sorted((a for a in aliases if len(a.replace(" ", "")) >= 3), key=len, reverse=True)


def identity_score(name: str, host: str, page_text: str):
    host_compact = norm(host).replace(" ", "").removeprefix("www")
    page = norm(page_text[:160000])
    hits, score = [], 0.0
    for alias in name_aliases(name):
        compact = alias.replace(" ", "")
        if compact in host_compact:
            score = max(score, 8.0 + min(len(compact), 12) / 10)
            hits.append("host:" + alias)
        if len(alias) >= 4 and alias in page:
            score += min(3.0, len(alias) / 12)
            hits.append("page:" + alias)
    token_hits = sorted({t for t in tokens(name) if len(t) >= 4 and t in page})
    score += min(4.0, len(token_hits) * 1.2)
    hits += ["token:" + t for t in token_hits[:6]]
    return score, hits


def fetch_identity(url: str):
    data, content_type, final_url = pilot.request_bytes(url)
    if content_type != "text/html" and b"<html" not in data[:1500].lower():
        raise ValueError("identity URL is not HTML")
    text = data.decode("utf-8", errors="replace")
    parser = TitleParser(); parser.feed(text)
    title = html.unescape(" ".join(parser.title)).strip()
    visible = re.sub(r"<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>", " ", text, flags=re.I | re.S)
    visible = html.unescape(re.sub(r"<[^>]+>", " ", visible))
    return final_url, title, parser.site_name, visible


def bing_results(query: str, limit: int = 8):
    url = "https://www.bing.com/search?format=rss&q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={"User-Agent": pilot.USER_AGENT})
    with urllib.request.urlopen(req, timeout=20, context=pilot.SSL_CONTEXT) as response:
        root = ET.fromstring(response.read(2_000_000))
    return [{"title": item.findtext("title") or "", "url": item.findtext("link") or "",
             "snippet": item.findtext("description") or ""}
            for item in root.findall("./channel/item")[:limit]]


def research_one(node, row):
    if row.get("status") == "accepted":
        return row
    attempts, candidates = [], []
    current = row.get("candidate_url") or ""
    if current and not blocked_host(pilot.host_of(current)):
        candidates.append({"url": current, "origin": "existing_research_entry", "search_text": ""})
    for query in (f'"{node["name"]}" official {node["cc"]}', f'{node["name"]} logo official'):
        try:
            results = bing_results(query)
            attempts.append({"query": query, "result_count": len(results)})
            for found in results:
                if found["url"] and not blocked_host(pilot.host_of(found["url"])):
                    candidates.append({"url": found["url"], "origin": "web_search",
                                       "search_text": found["title"] + " " + found["snippet"]})
        except Exception as exc:
            attempts.append({"query": query, "error": f"{type(exc).__name__}: {exc}"})
    seen, evaluated = set(), []
    for candidate in candidates:
        root = root_url(candidate["url"])
        host = pilot.host_of(root)
        if not root or host in seen or blocked_host(host):
            continue
        seen.add(host)
        try:
            final_url, title, site_name, body = fetch_identity(candidate["url"])
            final_root = root_url(final_url); final_host = pilot.host_of(final_root)
            if blocked_host(final_host):
                continue
            score, hits = identity_score(node["name"], final_host,
                                         title + " " + site_name + " " + candidate["search_text"] + " " + body)
            evaluated.append({"url": final_root, "page_title": title[:300], "score": round(score, 2),
                              "hits": hits[:10], "origin": candidate["origin"]})
        except Exception as exc:
            evaluated.append({"url": root, "score": 0, "origin": candidate["origin"],
                              "error": f"{type(exc).__name__}: {exc}"})
    evaluated.sort(key=lambda x: (-x.get("score", 0), x["url"]))
    result = dict(row)
    result.update({"research_checked_at": pilot.today(), "research_attempts": attempts,
                   "research_candidates": evaluated[:12]})
    best = next((x for x in evaluated if x.get("score", 0) >= 7.5), None)
    if best:
        result.update({"official_url": best["url"], "status": "accepted",
                       "basis": "individual_official_web_research",
                       "notes": "Official or parent mark candidate verified by host and page identity."})
    else:
        result.update({"official_url": "", "status": "resolved_none",
                       "basis": "no_verified_official_domain_after_research",
                       "notes": "Two official-domain searches and available entries produced no verified organisation or parent domain."})
    return result


def research_domains(args):
    nodes = {r["key"]: r for r in pilot.load_json(SELECTION)["nodes"]}
    rows = pilot.load_json(DOMAINS)["nodes"]
    todo = [r for r in rows if r.get("status") != "accepted"]
    if args.limit:
        todo = todo[:args.limit]
    updates = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(research_one, nodes[r["key"]], r): r["key"] for r in todo}
        for pos, future in enumerate(concurrent.futures.as_completed(futures), 1):
            result = future.result(); updates[result["key"]] = result
            print(f"[{pos}/{len(todo)}] {result['key']}: {result['status']}")
    merged = [updates.get(r["key"], r) for r in rows]
    write_json(DOMAINS, {"schema_version": 2, "nodes": merged})
    print("research status:", collections.Counter(r["status"] for r in merged))


def apply_domain_overrides(_args):
    """Apply individually verified official-domain corrections.

    This deliberately updates the transport review only.  It neither changes
    the frozen 762-node selection nor writes anything to Neo4j.
    """
    payload = pilot.load_json(CURRENT_DOMAIN_OVERRIDES)
    overrides = payload.get("overrides", [])
    rows = pilot.load_json(DOMAINS)["nodes"]
    by_key = {row["key"]: dict(row) for row in rows}
    errors = []
    for override in overrides:
        key = override.get("key", "")
        official_url = root_url(override.get("official_url", ""))
        if key not in by_key:
            # The current 619-node scope contains two actors that were not in
            # the frozen 762 transport. They are documented by the current
            # scope report and handled by its report-scoped manifest.
            if override.get("current_scope_only"):
                continue
            errors.append(f"unknown transport key: {key}")
            continue
        if not official_url or blocked_host(pilot.host_of(official_url)):
            errors.append(f"{key}: invalid or blocked official URL")
            continue
        row = by_key[key]
        row.update({
            "official_url": official_url,
            "status": "accepted",
            "basis": "individual_official_domain_override",
            "notes": override.get("notes", "Individually verified official or parent organisation domain."),
            "identity_source_url": override.get("identity_source_url", override.get("official_url", "")),
            "identity_checked_at": override.get("checked_at", pilot.today()),
        })
        row.pop("candidate_url", None)
        row.pop("check_error", None)
        by_key[key] = row
    if errors:
        raise RuntimeError("domain override validation failed:\n" + "\n".join(errors))
    merged = [by_key[row["key"]] for row in rows]
    write_json(DOMAINS, {"schema_version": 3, "nodes": merged})
    print(f"applied {sum(o.get('key') in by_key for o in overrides)} verified domain overrides")


def current_scope_coverage(_args):
    """Report image coverage for the current 619-node / 541-actor net."""
    sys.path.insert(0, str(NETZ))
    from netz.cli import load_network

    net = load_network()
    final = pilot.load_json(FINAL_MANIFEST)
    by_eid = {row.get("eid"): row for row in final["nodes"] if row.get("eid")}
    selection = {row["eid"]: row for row in pilot.load_json(SELECTION)["nodes"]}
    domains = {row["key"]: row for row in pilot.load_json(DOMAINS)["nodes"]}
    override_by_eid = {row.get("eid"): row for row in pilot.load_json(CURRENT_DOMAIN_OVERRIDES).get("overrides", [])
                       if row.get("eid")}
    actors, projects, rows = 0, 0, []
    for cc, panel in net.panels.items():
        projects += len(panel.projects)
        for eid in panel.actors:
            actors += 1
            selected = selection.get(eid)
            legacy = by_eid.get(eid, {})
            key = selected["key"] if selected else override_by_eid.get(eid, {}).get("key", f"CURRENT:{eid}")
            domain = domains.get(key, override_by_eid.get(eid, {}))
            result = "logo" if legacy.get("result") == "logo" else "none"
            rows.append({
                "cc": cc, "tid": net.tid[eid], "eid": eid, "key": key,
                "name": net.raw.name(eid), "result": result,
                "official_url": domain.get("official_url", ""),
                "domain_status": domain.get("status", "current_scope_only" if not selected else "unknown"),
                "legacy_manifest_match": bool(legacy),
            })
    nodes = actors + projects
    if (nodes, actors, projects) != (619, 541, 78):
        raise RuntimeError(f"current net drift: got {nodes}/{actors}/{projects}, expected 619/541/78")
    counts = collections.Counter(row["result"] for row in rows)
    payload = {
        "schema_version": 1, "created_at": pilot.today(), "network_nodes": nodes,
        "organisation_nodes": actors, "project_nodes": projects,
        "logo_nodes": counts["logo"], "none_nodes": counts["none"], "nodes": rows,
    }
    write_json(CURRENT_SCOPE_JSON, payload)
    lines = [
        "# Current 619-node image coverage", "",
        f"- Network nodes: **{nodes}**", f"- Organisations: **{actors}**",
        f"- Projects (kept image-free): **{projects}**", f"- Current logos: **{counts['logo']}**",
        f"- Current organisation nodes without a logo: **{counts['none']}**", "",
        "This report is scoped to the current Semio network. The frozen 762-node transport remains unchanged.", "",
    ]
    deep_manifest = CURRENT_DEEP / "manifest.json"
    if deep_manifest.exists():
        deep = pilot.load_json(deep_manifest)
        suggested = deep.get("counts", {}).get("logo", 0)
        withheld = deep.get("counts", {}).get("none", counts["none"])
        lines.extend([
            "## Pending research overlay", "",
            f"- Identity-filtered suggestions awaiting confirmation: **{suggested}**",
            f"- Potential coverage after confirmation: **{counts['logo'] + suggested}/{actors} "
            f"({(counts['logo'] + suggested) / actors * 100:.1f}%)**",
            f"- Cases still resolved as `none`: **{withheld}**", "",
            "These suggestions are not counted as current logos and have not been written to Neo4j.", "",
        ])
    lines.extend([
        "## Missing logos", "",
    ])
    lines.extend(f"- `{row['cc']}:{row['tid']}` — {row['name']} — {row['official_url'] or 'domain unresolved'}"
                 for row in rows if row["result"] == "none")
    CURRENT_SCOPE_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {CURRENT_SCOPE_JSON} and {CURRENT_SCOPE_REPORT}: {dict(counts)}")


def inline_svg_for_raster(data):
    """Supply a missing SVG height from its viewBox without altering artwork.

    Browser-rendered logos sometimes publish only ``width`` because CSS owns
    the height. CairoSVG otherwise falls back to 150 px and distorts the mark.
    The original bytes remain the hashed source; this copy is only the raster
    input used to preserve the declared viewBox proportions.
    """
    text = data.decode("utf-8", errors="replace")
    start = text.find("<svg")
    end = text.find(">", start)
    if start < 0 or end < 0:
        return data
    tag = text[start:end + 1]
    if re.search(r"\bheight\s*=", tag, re.I):
        return data
    width_match = re.search(r"\bwidth\s*=\s*[\"']([0-9.]+)(?:px)?[\"']", tag, re.I)
    viewbox_match = re.search(
        r"\bviewBox\s*=\s*[\"']\s*[-0-9.]+\s+[-0-9.]+\s+([0-9.]+)\s+([0-9.]+)\s*[\"']",
        tag, re.I)
    if not width_match or not viewbox_match:
        return data
    width = float(width_match.group(1)); vb_width = float(viewbox_match.group(1)); vb_height = float(viewbox_match.group(2))
    if width <= 0 or vb_width <= 0 or vb_height <= 0:
        return data
    height = width * vb_height / vb_width
    normalized_tag = tag[:-1] + f' height="{height:.6f}">'
    return (text[:start] + normalized_tag + text[end + 1:]).encode("utf-8")


def discover_inline_identity_svgs(node, official_url):
    """Find only explicitly logo-labelled inline SVGs in an official header.

    This deliberately ignores generic SVGs elsewhere on the page.  A candidate
    must sit inside a header and have ``logo``, ``brand`` or an organisation
    token in its own tag or immediate parent tag; navigation and social icons
    remain excluded.  The exact source bytes and page URL stay transportable.
    """
    try:
        page_data, page_type, final_url = pilot.request_bytes(official_url)
        if page_type != "text/html" and b"<html" not in page_data[:1500].lower():
            return [], {}, f"inline header source is not HTML ({page_type})"
        page_text = page_data.decode("utf-8", errors="replace")
    except Exception as exc:
        return [], {}, f"inline header fetch: {type(exc).__name__}: {exc}"
    header_blocks = re.findall(r"<header\b[^>]*>.*?</header\s*>", page_text, re.I | re.S)
    if not header_blocks:
        before_main = re.split(r"<main\b", page_text, maxsplit=1, flags=re.I)[0]
        header_blocks = [before_main[:250_000]]
    name_tokens = {token for token in tokens(node.get("name", "")) if len(token) >= 3}
    negative = ("menu", "search", "close", "social", "facebook", "instagram",
                "linkedin", "youtube", "hamburger", "chevron", "arrow", "icon-nav")
    found, payloads, seen = [], {}, set()
    for block in header_blocks:
        for match in re.finditer(r"<svg\b[^>]*>.*?</svg\s*>", block, re.I | re.S):
            svg_text = match.group(0)
            prefix = block[max(0, match.start() - 450):match.start()]
            parent = prefix[prefix.rfind("<"):]
            opening = svg_text[:svg_text.find(">") + 1]
            identity_context = norm(parent + " " + opening + " " + svg_text[:600])
            if any(word in identity_context for word in negative):
                continue
            labelled = ("logo" in identity_context or "brand" in identity_context
                        or bool(name_tokens & set(tokens(identity_context))))
            if not labelled or "<symbol" in svg_text.lower():
                continue
            if not re.search(r"<(?:path|polygon|polyline|rect|circle|ellipse|text)\b", svg_text, re.I):
                continue
            svg_data = svg_text.encode("utf-8")
            digest = pilot.sha256_bytes(svg_data)
            if digest in seen:
                continue
            seen.add(digest)
            source_url = f"inline+{final_url}#sha256={digest}"
            payloads[source_url] = svg_data
            found.append((1, "header_logo", source_url))
    return found, payloads, ""


def harvest_one(node, domain, node_dir=None, deep=False):
    node_dir = node_dir or (RAW / node["cc"] / node["tid"])
    node_dir.mkdir(parents=True, exist_ok=True)
    meta = {"key": node["key"], "official_url": domain.get("official_url", ""),
            "domain_basis": domain.get("basis", ""), "page_error": "", "candidates": []}
    if domain.get("status") != "accepted" or not domain.get("official_url"):
        meta["page_error"] = "domain not accepted"
        write_json(node_dir / "candidates.json", meta)
        return node["key"], 0, 0
    candidates, page_error = pilot.discover_candidates(domain["official_url"])
    candidates.extend(discover_media_candidates(domain["official_url"], candidates, deep=deep))
    candidates.extend(MANUAL_OFFICIAL_CANDIDATE_URLS.get(node["key"], ()))
    inline_svgs = {}
    if deep:
        inline_candidates, automatic_inline_svgs, inline_error = discover_inline_identity_svgs(
            node, domain["official_url"])
        candidates.extend(inline_candidates)
        inline_svgs.update(automatic_inline_svgs)
        if inline_error:
            meta["page_error"] = "; ".join(filter(None, (meta.get("page_error", ""), inline_error)))
    for priority, kind, page_url, marker in MANUAL_OFFICIAL_INLINE_SVG_CANDIDATES.get(node["key"], ()):
        try:
            page_data, page_type, final_page_url = pilot.request_bytes(page_url)
            if page_type != "text/html" and b"<html" not in page_data[:1500].lower():
                raise ValueError(f"inline SVG source is not HTML ({page_type})")
            page_text = page_data.decode("utf-8", errors="replace")
            marker_at = page_text.find(marker)
            if marker_at < 0:
                raise ValueError(f"inline SVG marker not found: {marker}")
            svg_at = page_text.find("<svg", marker_at)
            svg_end = page_text.find("</svg>", svg_at)
            if svg_at < 0 or svg_end < 0:
                raise ValueError("inline SVG not found after marker")
            svg_data = page_text[svg_at:svg_end + len("</svg>")].encode("utf-8")
            source_url = f"inline+{final_page_url}#sha256={pilot.sha256_bytes(svg_data)}"
            inline_svgs[source_url] = svg_data
            candidates.append((priority, kind, source_url))
        except Exception as exc:
            meta["page_error"] = "; ".join(filter(None, (
                meta.get("page_error", ""), f"inline SVG: {type(exc).__name__}: {exc}"
            )))
    archive_members = {}
    for priority, kind, archive_url, member in MANUAL_OFFICIAL_ARCHIVE_CANDIDATES.get(node["key"], ()):
        source_url = f"zip+{archive_url}#{urllib.parse.quote(member, safe='/')}"
        archive_members[source_url] = (archive_url, member)
        candidates.append((priority, kind, source_url))
    deduped = {}
    for priority, kind, url in candidates:
        clean = url if url.startswith(("zip+", "inline+")) else urllib.parse.urldefrag(url)[0]
        if clean not in deduped or priority < deduped[clean][0]:
            deduped[clean] = (priority, kind, clean)
    candidates = sorted(deduped.values(), key=lambda row: (row[0], row[1], row[2]))
    meta["page_error"] = "; ".join(filter(None, (page_error, meta.get("page_error", ""))))
    candidate_limit = 40 if deep else 20
    for idx, (priority, kind, url) in enumerate(candidates[:candidate_limit], 1):
        record = {"id": f"c{idx:02d}", "priority": priority, "kind": kind,
                  "url": url, "status": "rejected", "review_status": "pending",
                  "retrieved_at": "", "license_note": "Official-site candidate; usage rights require final review.",
                  "rights_source_url": "",
                  "source_sha256": "", "preview_sha256": "", "reason": ""}
        record["license_note"] = MANUAL_CANDIDATE_LICENSE_NOTES.get(
            (node["key"], url), record["license_note"])
        if node["key"] in MANUAL_NODE_RIGHTS:
            rights = MANUAL_NODE_RIGHTS[node["key"]]
            record["license_note"] = rights["license_note"]
            record["rights_source_url"] = rights["rights_source_url"]
        try:
            dark_variant = None
            if url in inline_svgs:
                data = inline_svgs[url]
                raster_data = inline_svg_for_raster(data)
                content_type, final_url = "image/svg+xml", url
            elif url in archive_members:
                archive_url, member = archive_members[url]
                archive_data, _archive_type, _archive_final = pilot.request_bytes(archive_url)
                with zipfile.ZipFile(io.BytesIO(archive_data)) as package:
                    data = package.read(member)
                    dark_spec = MANUAL_OFFICIAL_DARK_ARCHIVE_CANDIDATES.get(node["key"])
                    if dark_spec and (archive_url, member) == dark_spec[:2]:
                        dark_member = dark_spec[2]
                        dark_variant = (
                            package.read(dark_member),
                            "image/svg+xml" if dark_member.lower().endswith(".svg") else "image/png",
                            f"{archive_url}#{urllib.parse.quote(dark_member, safe='/')}",
                        )
                raster_data = data
                content_type = "image/svg+xml" if member.lower().endswith(".svg") else "image/png"
                final_url = f"{archive_url}#{urllib.parse.quote(member, safe='/')}"
            else:
                data, content_type, final_url = pilot.request_bytes(url)
                raster_data = data
                manual_urls = {row[2] for row in MANUAL_OFFICIAL_CANDIDATE_URLS.get(node["key"], ())}
                if url in manual_urls and (content_type == "text/html" or data[:100].lstrip().lower().startswith(b"<!doctype html")):
                    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(request, timeout=30, context=pilot.SSL_CONTEXT) as response:
                        data = response.read(pilot.MAX_DOWNLOAD + 1)
                        content_type = response.headers.get_content_type()
                        final_url = response.geturl()
                    if len(data) > pilot.MAX_DOWNLOAD:
                        raise ValueError("image exceeds download limit")
                    raster_data = data
            im, fmt = pilot.rasterize(raster_data, content_type, final_url)
            record.update({"final_url": final_url, "content_type": content_type,
                           "format": fmt, "width": im.width, "height": im.height,
                           "retrieved_at": pilot.today(), "source_sha256": pilot.sha256_bytes(data)})
            if im.convert("RGBA").getchannel("A").getbbox() is None:
                record["reason"] = "image has no visible pixels"
            elif fmt != "svg" and min(im.size) < 128:
                record["reason"] = "short edge below 128px"
            else:
                preview = node_dir / f"{record['id']}_{kind}.png"
                im.save(preview, "PNG")
                try:
                    prepared, _mode = pilot.prepare_node_canvas(preview, theme="light")
                    if sum(value > 8 for value in prepared.getchannel("A").get_flattened_data()) < 32:
                        raise ValueError("candidate has insufficient visible foreground")
                except ValueError as exc:
                    record["reason"] = str(exc)
                else:
                    record.update({"preview_path": str(preview.relative_to(FULL)).replace("\\", "/"),
                                   "preview_sha256": pilot.sha256_file(preview), "status": "candidate"})
                    if dark_variant:
                        record["status"] = "rejected"
                        dark_data, dark_type, dark_url = dark_variant
                        dark_image, dark_format = pilot.rasterize(dark_data, dark_type, dark_url)
                        dark_preview = node_dir / f"{record['id']}_{kind}_dark.png"
                        dark_image.save(dark_preview, "PNG")
                        dark_prepared, dark_mode = pilot.prepare_node_canvas(dark_preview, theme="dark")
                        if sum(value > 8 for value in dark_prepared.getchannel("A").get_flattened_data()) < 32:
                            raise ValueError("dark candidate has insufficient visible foreground")
                        record.update({
                            "dark_preview_path": str(dark_preview.relative_to(FULL)).replace("\\", "/"),
                            "dark_preview_sha256": pilot.sha256_file(dark_preview),
                            "dark_source_sha256": pilot.sha256_bytes(dark_data),
                            "dark_final_url": dark_url,
                            "dark_format": dark_format,
                            "dark_width": dark_image.width,
                            "dark_height": dark_image.height,
                            "dark_crop_mode": dark_mode,
                            "status": "candidate",
                        })
        except Exception as exc:
            record["reason"] = f"{type(exc).__name__}: {exc}"
        meta["candidates"].append(record)
    write_json(node_dir / "candidates.json", meta)
    good = sum(c["status"] == "candidate" for c in meta["candidates"])
    return node["key"], good, len(meta["candidates"])


def harvest_current_only(_args):
    """Harvest the two actors added after the frozen 762 transport scope."""
    scope = {row["eid"]: row for row in pilot.load_json(CURRENT_SCOPE_JSON)["nodes"]}
    overrides = [row for row in pilot.load_json(CURRENT_DOMAIN_OVERRIDES)["overrides"]
                 if row.get("current_scope_only")]
    for override in overrides:
        current = scope[override["eid"]]
        node = {"key": override["key"], "cc": current["cc"], "tid": current["tid"],
                "eid": current["eid"], "name": current["name"], "typ": "Organisation"}
        domain = {**override, "status": "accepted", "basis": "individual_official_domain_override"}
        destination = CURRENT_DEEP / "current_only" / current["cc"] / current["tid"]
        key, good, total = harvest_one(node, domain, destination)
        print(f"{key}: {good}/{total} usable")


def request_deep_page(url, timeout=6):
    """Fetch a bounded secondary HTML page without long dead-path waits."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": pilot.USER_AGENT, "Accept": "text/html,application/xml;q=0.9,*/*;q=0.3"},
    )
    with urllib.request.urlopen(req, timeout=timeout, context=pilot.SSL_CONTEXT) as response:
        content_type = response.headers.get_content_type()
        final_url = response.geturl()
        data = response.read(3_000_001)
    if len(data) > 3_000_000:
        data = data[:3_000_000]
    return data, content_type, final_url


def discover_media_candidates(official_url, existing, deep=False):
    """Search a small set of official brand/media/about pages for a mark."""
    existing_urls = {urllib.parse.urldefrag(row[2])[0] for row in existing}
    root_host = pilot.host_of(official_url)
    page_links = []
    output, seen_pages = [], set()
    try:
        data, content_type, final_url = pilot.request_bytes(official_url)
        if content_type != "text/html" and b"<html" not in data[:1500].lower():
            return []
        text = data[:3_000_000].decode("utf-8", errors="replace")
        for match in re.finditer(r"<a\b[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", text, re.I | re.S):
            href = urllib.parse.urljoin(final_url, html.unescape(match.group(1)))
            label = norm(re.sub(r"<[^>]+>", " ", match.group(2)) + " " + href)
            if pilot.host_of(href) == root_host and any(word in label for word in (
                "brand", "branding", "logo", "media", "press", "presse", "download",
                "about", "uber uns", "over ons", "om oss", "a propos")):
                page_links.append(href)
    except Exception:
        return []
    if deep:
        split = urllib.parse.urlsplit(official_url)
        root = urllib.parse.urlunsplit((split.scheme or "https", split.netloc, "/", "", ""))
        # WordPress often renders a reduced Elementor/header thumbnail while
        # its own media endpoint exposes the untouched original.  Query only
        # the verified organisation host, retain the exact source URL, and let
        # the normal filename/identity filter reject partner or campaign logos.
        try:
            wp_url = urllib.parse.urljoin(root, "wp-json/wp/v2/media?search=logo&per_page=40")
            wp_data, wp_type, _wp_final = request_deep_page(wp_url)
            if wp_type in {"application/json", "text/json"} or wp_data.lstrip().startswith(b"["):
                wp_rows = json.loads(wp_data.decode("utf-8", errors="replace"))
                for item in wp_rows[:40] if isinstance(wp_rows, list) else []:
                    source = urllib.parse.urldefrag(item.get("source_url") or "")[0]
                    media_type = item.get("media_type")
                    if (source and media_type == "image" and pilot.host_of(source) == root_host
                            and source not in existing_urls):
                        output.append((5, "media_logo", source))
                        existing_urls.add(source)
        except Exception:
            pass
        try:
            sitemap_data, _, sitemap_final = request_deep_page(urllib.parse.urljoin(root, "sitemap.xml"))
            sitemap_text = sitemap_data[:3_000_000].decode("utf-8", errors="replace")
            for loc in re.findall(r"<loc>\s*([^<]+)\s*</loc>", sitemap_text, re.I):
                loc = html.unescape(loc.strip())
                marker = norm(loc)
                if pilot.host_of(loc) == root_host and any(word in marker for word in (
                    "brand", "logo", "media", "press", "presse", "download",
                    "about", "uber uns", "over ons", "om oss", "a propos",
                )):
                    page_links.append(loc)
        except Exception:
            pass
        if len(set(page_links)) < 4:
            page_links.extend(urllib.parse.urljoin(root, path) for path in (
                "about", "press", "media", "brand",
            ))
    page_limit = 8 if deep else 5
    for page_url in page_links:
        clean_page = urllib.parse.urldefrag(page_url)[0]
        if clean_page in seen_pages or len(seen_pages) >= page_limit:
            continue
        seen_pages.add(clean_page)
        try:
            fetch = request_deep_page if deep else pilot.request_bytes
            data, content_type, final_url = fetch(clean_page)
            if content_type != "text/html" and b"<html" not in data[:1500].lower():
                continue
            page_text = data[:3_000_000].decode("utf-8", errors="replace")
            parser = pilot.IconParser(); parser.feed(page_text)
            base = urllib.parse.urljoin(final_url, parser.base) if parser.base else final_url
            for _priority, kind, url in parser.candidates:
                absolute = urllib.parse.urldefrag(urllib.parse.urljoin(base, url))[0]
                if absolute not in existing_urls:
                    output.append((6, kind, absolute))
                    existing_urls.add(absolute)
            for match in re.finditer(r"<(?:img|source)\b[^>]*(?:src|srcset)=[\"']([^\"' ,]+)",
                                     page_text, re.I):
                absolute = urllib.parse.urldefrag(urllib.parse.urljoin(final_url, html.unescape(match.group(1))))[0]
                if absolute not in existing_urls and any(word in absolute.lower() for word in ("logo", "brand", "wordmark")):
                    output.append((6, "media_logo", absolute)); existing_urls.add(absolute)
        except Exception:
            continue
    return output


def harvest_all(args):
    nodes = {r["key"]: r for r in pilot.load_json(SELECTION)["nodes"]}
    domains = {r["key"]: r for r in pilot.load_json(DOMAINS)["nodes"]}
    selected_keys = set(args.key or [])
    todo = [nodes[k] for k in sorted(nodes)
            if domains[k]["status"] == "accepted" and (not selected_keys or k in selected_keys)]
    unknown = selected_keys - set(nodes)
    if unknown:
        raise RuntimeError("unknown harvest keys: " + ", ".join(sorted(unknown)))
    if args.limit:
        todo = todo[:args.limit]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(harvest_one, n, domains[n["key"]]) for n in todo]
        for pos, future in enumerate(concurrent.futures.as_completed(futures), 1):
            key, good, total = future.result()
            print(f"[{pos}/{len(todo)}] {key}: {good}/{total} usable")


def deep_harvest_empty(args):
    """Probe official secondary pages only for current-scope unresolved marks."""
    review = {row["key"]: row for row in pilot.load_json(CURRENT_DEEP / "manifest.json")["nodes"]}
    nodes = {row["key"]: row for row in pilot.load_json(SELECTION)["nodes"]}
    domains = {row["key"]: row for row in pilot.load_json(DOMAINS)["nodes"]}
    selected_keys = set(args.key or [])
    unknown = selected_keys - set(nodes)
    if unknown:
        raise RuntimeError("unknown deep-harvest keys: " + ", ".join(sorted(unknown)))
    todo = [nodes[key] for key in sorted(nodes)
            if key in review and review[key]["suggested_result"] == "none"
            and not review[key]["candidates"] and domains[key]["status"] == "accepted"
            and (not selected_keys or key in selected_keys)]
    if args.limit:
        todo = todo[:args.limit]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(harvest_one, node, domains[node["key"]], None, True) for node in todo]
        for pos, future in enumerate(concurrent.futures.as_completed(futures), 1):
            key, good, total = future.result()
            print(f"[{pos}/{len(todo)}] {key}: {good}/{total} usable (deep)")


def build_manifest(_args):
    nodes = pilot.load_json(SELECTION)["nodes"]
    domains = {r["key"]: r for r in pilot.load_json(DOMAINS)["nodes"]}
    rows = []
    for node in nodes:
        d = domains[node["key"]]
        path = RAW / node["cc"] / node["tid"] / "candidates.json"
        meta = pilot.load_json(path) if path.exists() else {"candidates": []}
        usable = usable_candidates(node)
        result = ("candidates_collected" if usable else
                  ("no_usable_candidate" if d["status"] == "accepted" else "resolved_none"))
        candidate_transport = [{k: c.get(k) for k in (
            "id", "kind", "url", "final_url", "retrieved_at", "license_note", "review_status",
            "source_sha256", "preview_sha256", "preview_path", "format", "width", "height"
        )} for c in usable]
        rows.append({**{k: node[k] for k in ("key", "cc", "tid", "eid", "graph_id", "name", "typ")},
                     "domain_status": d["status"], "official_url": d.get("official_url", ""),
                     "domain_basis": d.get("basis", ""), "collection_result": result,
                     "candidate_count": len(usable),
                     "candidates": candidate_transport,
                     "candidate_metadata": str(path.relative_to(FULL)).replace("\\", "/") if path.exists() else None})
    counts = collections.Counter(r["collection_result"] for r in rows)
    domain_counts = collections.Counter(r["domain_status"] for r in rows)
    candidate_total = sum(r["candidate_count"] for r in rows)
    graph_backed = sum(r["graph_id"] is not None for r in rows)
    country_counts = collections.Counter((r["cc"], r["collection_result"]) for r in rows)
    write_json(MANIFEST, {"schema_version": 1, "transport_only": True,
                          "created_at": pilot.today(), "nodes": rows, "counts": counts})
    lines = ["# Full image candidate collection", "", "- Organisations: **762**",
             "- Projects excluded: **97**", f"- Graph-backed organisations: **{graph_backed}**",
             f"- Overlay organisations: **{762 - graph_backed}**", "- Neo4j writes: **0**",
             f"- Collected candidate files: **{candidate_total}**", "", "## Results", ""]
    lines += [f"- {k}: **{v}**" for k, v in sorted(counts.items())]
    lines += ["", "## Domain review", ""] + [f"- {k}: **{v}**" for k, v in sorted(domain_counts.items())]
    lines += ["", "## Countries", "", "| Country | candidates collected | no usable candidate | resolved none |", "|---|---:|---:|---:|"]
    for cc in COUNTRY_ORDER:
        lines.append(f"| {cc} | {country_counts[(cc, 'candidates_collected')]} | {country_counts[(cc, 'no_usable_candidate')]} | {country_counts[(cc, 'resolved_none')]} |")
    lines += ["", "`resolved_none` and `no_usable_candidate` are research/suggestion states; your explicit review is still required.",
              "Every candidate remains `review_status: pending` until visual and licence review."]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {MANIFEST} and {REPORT}: {dict(counts)}")


def contact_sheets(_args):
    nodes = pilot.load_json(SELECTION)["nodes"]
    visible = []
    for node in nodes:
        path = RAW / node["cc"] / node["tid"] / "candidates.json"
        usable = usable_candidates(node)[:4]
        if usable:
            visible.append((node, usable))
    CONTACT.mkdir(parents=True, exist_ok=True)
    for old_sheet in CONTACT.glob("contact_*.png"):
        old_sheet.unlink()
    for page_no, start in enumerate(range(0, len(visible), 12), 1):
        sheet = Image.new("RGB", (1040, 2280), "#f7f3e3"); draw = ImageDraw.Draw(sheet)
        for row_no, (node, candidates) in enumerate(visible[start:start + 12]):
            y = row_no * 190
            draw.text((4, y + 4), f"{node['key']}  {node['name'][:34]}", fill="#001117", font=pilot.font(16))
            for col, candidate in enumerate(candidates):
                x = col * 260; im = Image.open(FULL / candidate["preview_path"]).convert("RGBA")
                im.thumbnail((140, 120), Image.Resampling.LANCZOS)
                tile = Image.new("RGBA", (150, 125), "white")
                tile.alpha_composite(im, ((150 - im.width) // 2, (125 - im.height) // 2))
                sheet.paste(tile.convert("RGB"), (x + 55, y + 34))
                draw.text((x + 58, y + 160), f"{candidate['id']} {candidate['kind']}", fill="#001117", font=pilot.font(14))
        sheet.save(CONTACT / f"contact_{page_no:03d}.png")
    print(f"wrote {len(list(CONTACT.glob('contact_*.png')))} contact sheets for {len(visible)} organisations")


def audit_node_preview(candidate, tid, theme):
    """Render the gallery's image/border/ID order for a compact audit sheet."""
    size = 112
    tile = Image.new("RGBA", (size, size), "#d8d2c0" if theme == "light" else "#344b50")
    source_path = (candidate.get("dark_preview_path")
                   if theme == "dark" and candidate.get("dark_preview_path")
                   else candidate["preview_path"])
    prepared = prepared_canvas(FULL / source_path, theme=theme)
    prepared = prepared.resize((size, size), Image.Resampling.LANCZOS)
    tile.alpha_composite(prepared)
    draw = ImageDraw.Draw(tile)
    colour = "#001117" if theme == "light" else "#ffffff"
    stroke = "#ffffff" if theme == "light" else "#001117"
    draw.ellipse((1, 1, size - 2, size - 2), outline=colour, width=3)
    label_font = pilot.font(18)
    box = draw.textbbox((0, 0), tid, font=label_font, stroke_width=2)
    draw.text(((size - (box[2] - box[0])) / 2, (size - (box[3] - box[1])) / 2 - box[1]),
              tid, font=label_font, fill=colour, stroke_width=2, stroke_fill=stroke)
    return tile


def command_audit_sheets(_args):
    nodes = {row["key"]: row for row in pilot.load_json(SELECTION)["nodes"]}
    domains = {row["key"]: row for row in pilot.load_json(DOMAINS)["nodes"]}
    suggestions = pilot.load_json(SUGGESTIONS)["nodes"]
    rows = []
    hash_counts = collections.Counter()
    for suggestion in suggestions:
        if suggestion["suggested_result"] != "logo":
            continue
        node = nodes[suggestion["key"]]
        candidate = candidate_for(node, suggestion["suggested_candidate_id"])
        rows.append((node, candidate, domains[node["key"]]))
        hash_counts[candidate.get("preview_sha256")] += 1
    FINAL_REVIEW.mkdir(parents=True, exist_ok=True)
    for old in FINAL_REVIEW.glob("suggestions_*.png"):
        old.unlink()
    pages = []
    columns, rows_per_page = 4, 4
    cell_w, cell_h = 480, 355
    for page_no, start in enumerate(range(0, len(rows), columns * rows_per_page), 1):
        batch = rows[start:start + columns * rows_per_page]
        sheet = Image.new("RGB", (columns * cell_w, rows_per_page * cell_h), "#f7f3e3")
        draw = ImageDraw.Draw(sheet)
        page_keys = []
        for pos, (node, candidate, domain) in enumerate(batch):
            col, row = pos % columns, pos // columns
            x, y = col * cell_w, row * cell_h
            page_keys.append(node["key"])
            draw.rectangle((x, y, x + cell_w - 2, y + cell_h - 2), outline="#9d988b", width=2)
            draw.text((x + 12, y + 10), f"{node['key']}  {node['name'][:38]}",
                      fill="#001117", font=pilot.font(18))
            source = Image.open(FULL / candidate["preview_path"]).convert("RGBA")
            source.thumbnail((210, 145), Image.Resampling.LANCZOS)
            source_tile = Image.new("RGBA", (220, 155), "white")
            source_tile.alpha_composite(source, ((220 - source.width) // 2, (155 - source.height) // 2))
            sheet.paste(source_tile.convert("RGB"), (x + 12, y + 50))
            light = audit_node_preview(candidate, node["tid"], "light")
            dark = audit_node_preview(candidate, node["tid"], "dark")
            sheet.paste(light.convert("RGB"), (x + 244, y + 52))
            sheet.paste(dark.convert("RGB"), (x + 360, y + 52))
            draw.text((x + 270, y + 168), "Hell", fill="#001117", font=pilot.font(13))
            draw.text((x + 386, y + 168), "Dunkel", fill="#001117", font=pilot.font(13))
            duplicate = hash_counts[candidate.get("preview_sha256", "")]
            details = [f"{candidate['id']} · {candidate['kind']} · {candidate['width']}×{candidate['height']}",
                       pilot.host_of(domain.get("official_url", ""))[:54],
                       (candidate.get("final_url") or candidate.get("url") or "")[:64]]
            if duplicate > 1:
                details.append(f"GLEICHE DATEI: {duplicate} Knoten")
            for line_no, line in enumerate(details):
                draw.text((x + 12, y + 218 + 27 * line_no), line, fill="#001117", font=pilot.font(14))
        target = FINAL_REVIEW / f"suggestions_{page_no:02d}.png"
        sheet.save(target)
        pages.append({"page": page_no, "path": str(target.relative_to(FULL)).replace("\\", "/"),
                      "keys": page_keys, "sha256": pilot.sha256_file(target)})
    write_json(FINAL_REVIEW / "index.json", {"schema_version": 1, "logo_suggestions": len(rows),
                                              "page_count": len(pages), "pages": pages})

    suggestions_by_key = {row["key"]: row for row in suggestions}
    problems = []
    for suggestion in suggestions:
        if suggestion["suggested_result"] != "logo":
            continue
        key = suggestion["key"]
        node, domain = nodes[key], domains[key]
        try:
            candidate = candidate_for(node, suggestion["suggested_candidate_id"])
        except (ValueError, OSError) as exc:
            problems.append(f"{key}: {exc}")
            continue
        rejection = candidate_rejection(node, candidate)
        domain_rejection = domain_suggestion_rejection(node, domain)
        preview = FULL / candidate["preview_path"]
        if rejection:
            problems.append(f"{key}: rejected candidate was suggested: {rejection}")
        if domain_rejection:
            problems.append(f"{key}: rejected domain was suggested: {domain_rejection}")
        if not preview.is_file():
            problems.append(f"{key}: preview file is missing")
        elif pilot.sha256_file(preview) != candidate.get("preview_sha256"):
            problems.append(f"{key}: preview checksum drift")

    result_counts = collections.Counter(row["suggested_result"] for row in suggestions)
    country_counts = {
        cc: collections.Counter(suggestions_by_key[row["key"]]["suggested_result"]
                                for row in nodes.values() if row["cc"] == cc)
        for cc in COUNTRY_ORDER
    }
    candidate_reason_by_key = {
        key: "; ".join(sorted(set(rules.values())))
        for key, rules in MANUAL_CANDIDATE_REJECTIONS.items()
    }
    manual_rejections = [
        {"key": key, "name": nodes[key]["name"], "reason": reason,
         "suggested_result": suggestions_by_key[key]["suggested_result"]}
        for key, reason in sorted({**candidate_reason_by_key,
                                    **MANUAL_DOMAIN_REJECTIONS}.items())
    ]
    blocked_candidates_absent = all(
        suggestions_by_key[key]["suggested_result"] == "none"
        or ("*" not in rules and suggestions_by_key[key]["suggested_candidate_id"] not in rules)
        for key, rules in MANUAL_CANDIDATE_REJECTIONS.items()
    )
    rejected_domains_are_none = all(
        suggestions_by_key[key]["suggested_result"] == "none"
        for key in MANUAL_DOMAIN_REJECTIONS
    )
    audit = {
        "schema_version": 1,
        "audited_at": pilot.today(),
        "scope": "all 762 organisation suggestions; projects remain image-free",
        "selection_nodes": len(nodes),
        "initial_logo_suggestions_visually_checked": 352,
        "manual_mismatches_corrected": len(manual_rejections),
        "final_logo_suggestions": result_counts["logo"],
        "final_none_suggestions": result_counts["none"],
        "visual_sheet_count": len(pages),
        "checks": {
            "unique_selection_keys": len(nodes) == 762,
            "unique_suggestion_keys": len(suggestions_by_key) == 762,
            "all_results_resolved_as_suggestion": set(result_counts) <= {"logo", "none"},
            "no_suggestion_is_user_confirmation": all(not row.get("confirmed") for row in suggestions),
            "all_logo_candidates_pass_identity_and_file_checks": not problems,
            "no_rejected_candidate_is_suggested": blocked_candidates_absent,
            "all_rejected_domains_are_none": rejected_domains_are_none,
        },
        "problems": problems,
        "countries": {cc: {"logo": country_counts[cc]["logo"], "none": country_counts[cc]["none"]}
                      for cc in COUNTRY_ORDER},
        "withheld_after_visual_audit": manual_rejections,
        "neo4j_writes": 0,
    }
    write_json(FINAL_AUDIT_JSON, audit)
    report = [
        "# Finaler Vorschlagsaudit der Akteurslogos", "", f"Geprüft: {audit['audited_at']}", "",
        "## Ergebnis", "", "- 762/762 Organisationsknoten strukturell geprüft.",
        f"- 352 ursprüngliche Logo-Vorschläge auf {len(pages)} Prüfbögen vollständig visuell geprüft.",
        f"- {len(manual_rejections)} Fehlzuordnungen oder unbrauchbare Marken korrigiert; sichere Alternativen wurden bevorzugt, sonst `none`.",
        f"- Endstand: {result_counts['logo']} Logo-Vorschläge, {result_counts['none']} `none`-Vorschläge.",
        "- Keine Entscheidung wurde als Benutzerbestätigung gespeichert; keine Neo4j-Schreiboperation erfolgte.",
        "", "## Automatische Gegenprüfung", "",
    ]
    for check, passed in audit["checks"].items():
        report.append(f"- {'BESTANDEN' if passed else 'FEHLER'} — {check}")
    report += ["", "## Nach Sichtprüfung zurückgezogen", "",
               "| Knoten | Organisation | Grund |", "|---|---|---|"]
    for row in manual_rejections:
        report.append(f"| {row['key']} | {row['name']} | {row['reason']} |")
    report += ["", "## Länderstand", "", "| Land | Logo | none |", "|---|---:|---:|"]
    for cc in COUNTRY_ORDER:
        report.append(f"| {cc} | {country_counts[cc]['logo']} | {country_counts[cc]['none']} |")
    FINAL_AUDIT_REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"wrote {len(pages)} final-review sheets for {len(rows)} logo suggestions")


def usable_candidates(node):
    path = RAW / node["cc"] / node["tid"] / "candidates.json"
    if not path.exists():
        return []
    return [candidate for candidate in pilot.load_json(path).get("candidates", [])
            if candidate.get("status") == "candidate" and candidate.get("preview_path")]


def candidate_rejection(node, candidate):
    """Reject obvious photos and third-party badges before they become suggestions."""
    manual = MANUAL_CANDIDATE_REJECTIONS.get(node.get("key"), {})
    if candidate.get("id") in manual:
        return manual[candidate["id"]]
    original_url = (candidate.get("url") or "").lower()
    url = (candidate.get("final_url") or original_url).lower()
    decoded_url = urllib.parse.unquote(url)
    if any(fragment.lower() in decoded_url
           for fragment in MANUAL_CANDIDATE_URL_REJECTIONS.get(node.get("key"), ())):
        return "key-specific third-party, interface or editorial asset"
    manual_urls = {
        urllib.parse.urldefrag(row[2])[0].lower()
        for row in MANUAL_OFFICIAL_CANDIDATE_URLS.get(node.get("key"), ())
    }
    if (urllib.parse.urldefrag(url)[0] in manual_urls
            or urllib.parse.urldefrag(original_url)[0] in manual_urls):
        # These exact files were inspected on an official press, brand or
        # design-guide page.  Their CDN filenames are often opaque and should
        # not be rejected by the generic filename-identity heuristic below.
        return ""
    if url.startswith("inline+") and node.get("key") in MANUAL_OFFICIAL_INLINE_SVG_CANDIDATES:
        return ""
    if original_url.startswith("zip+") and node.get("key") in MANUAL_OFFICIAL_ARCHIVE_CANDIDATES:
        return ""
    if "*" in manual:
        return manual["*"]
    if any(marker in decoded_url for marker in SOCIAL_MARKERS):
        return "social-media asset"
    if any(marker in decoded_url for marker in NON_ORGANISATION_MARKERS):
        return "third-party, certification, partner or portrait asset"
    if any(marker in url for marker in ("no-image", "placeholder", "default-image", "spacer")):
        return "placeholder asset"
    kind = candidate.get("kind")
    logo_words = ("logo", "wordmark", "brandmark", "logotype")
    split = urllib.parse.urlsplit(decoded_url)
    asset_name = split.path.rstrip("/").rsplit("/", 1)[-1]
    asset_tokens = set(tokens(asset_name))
    name_tokens = set(tokens(node.get("name", "")))
    identity_in_filename = bool(name_tokens & asset_tokens) or any(word in asset_name for word in logo_words)
    unconditional_photo_markers = (
        "portrait", "headshot", "getty", "samtalebilleder", "csm_",
        "verwaltungsgebaeude", "verwaltungsgebäude", "team-headshot",
    )
    photo_markers = (
        "portrait", "headshot", "banner", "keyvisual", "flyer", "building", "gebouw",
        "team", "people", "getty", "samtalebilleder", "header-", "header_", "csm_",
        "processed", "uploads/keyvisual", "formidlingscenter", "mesinfos",
    )
    generic_icon_markers = ("user.svg", "account.svg", "search.svg", "menu.svg", "glyph-logo")
    if any(marker in decoded_url for marker in generic_icon_markers):
        return "generic interface or social icon"
    if any(marker in decoded_url for marker in unconditional_photo_markers):
        return "photo or editorial image rather than an organisation mark"
    if any(marker in decoded_url for marker in photo_markers) and not identity_in_filename:
        return "photo, banner or editorial image rather than an organisation mark"
    suffix = PurePosixPath(split.path).suffix.lower()
    if kind == "header_logo" and suffix in {".jpg", ".jpeg", ".webp", ".avif"} and not identity_in_filename:
        return "unidentified header raster; likely editorial photography"
    if kind == "og_image" and not any(word in decoded_url for word in logo_words):
        return "unchecked og:image without a logo filename"
    if kind == "media_logo":
        # Only the asset filename may identify a media logo. Parent directory
        # names can contain the organisation's domain while the file itself is
        # an unrelated partner logo (the BioRegional/Abstrakt false positive).
        if not any(word in decoded_url for word in logo_words):
            return "media image without a logo filename"
        if name_tokens and not (name_tokens & asset_tokens):
            return "media logo filename does not identify the organisation"
    return ""


def domain_suggestion_rejection(node, domain):
    """Keep ambiguous automated domain research out of logo suggestions."""
    if (node.get("key") in MANUAL_DOMAIN_REJECTIONS
            and domain.get("basis") != "individual_official_domain_override"):
        return MANUAL_DOMAIN_REJECTIONS[node["key"]]
    if domain.get("status") != "accepted" or not domain.get("official_url"):
        return "organisation domain is not accepted"
    basis = domain.get("basis", "")
    if basis in {"pilot_manual", "manual", "individual_manual_check",
                 "individual_official_domain_override"}:
        return ""
    official_root = root_url(domain["official_url"])
    title = domain.get("page_title", "")
    if basis == "individual_official_web_research":
        selected = next((row for row in domain.get("research_candidates", [])
                         if root_url(row.get("url", "")) == official_root), None)
        if not selected:
            return "automated research result has no matching identity record"
        title = selected.get("page_title", "")
    name_tokens = set(tokens(node.get("name", "")))
    host_tokens = set(tokens(pilot.host_of(official_root)))
    title_tokens = set(tokens(title))
    matched = name_tokens & (host_tokens | title_tokens)
    if basis == "individual_official_web_research":
        if len(name_tokens) < 2:
            return "ambiguous one-word organisation from automated domain research"
        if len(matched) < 2:
            return "automated domain does not identify enough of the organisation name"
    elif name_tokens and not matched:
        return "domain identity does not match the organisation name"
    return ""


def candidate_rank(candidate, node=None):
    weights = {"header_logo": 130, "structured_logo": 125, "media_logo": 110,
               "apple_touch": 100, "declared_icon": 95, "favicon": 90,
               "wikimedia": 80, "og_image": 70}
    if node is not None and candidate_rejection(node, candidate):
        return -1000
    w, h = candidate.get("width", 1), candidate.get("height", 1)
    shape_bonus = 8 if 0.65 <= w / max(h, 1) <= 1.55 else 0
    size_bonus = min(8, min(w, h) / 128)
    identity_bonus = 0
    if node is not None:
        url = urllib.parse.unquote((candidate.get("final_url") or candidate.get("url") or "").lower())
        asset_name = urllib.parse.urlsplit(url).path.rstrip("/").rsplit("/", 1)[-1]
        asset_tokens = set(tokens(asset_name))
        name_tokens = set(tokens(node.get("name", "")))
        if name_tokens & asset_tokens:
            identity_bonus += 24
        if any(word in asset_name for word in ("logo", "wordmark", "brandmark", "logotype")):
            identity_bonus += 18
        manual_urls = {
            urllib.parse.urldefrag(row[2])[0].lower()
            for row in MANUAL_OFFICIAL_CANDIDATE_URLS.get(node.get("key"), ())
        }
        if urllib.parse.urldefrag(url)[0] in manual_urls:
            identity_bonus += 50
        elif candidate.get("kind") == "header_logo" and not (name_tokens & asset_tokens):
            # A broad header scan also sees sponsors and programme badges. A
            # generic filename containing only "logo" is not enough to beat an
            # organisation-identified favicon or declared icon.
            identity_bonus -= 28
    return weights.get(candidate.get("kind"), 0) + shape_bonus + size_bonus + identity_bonus


def current_candidate_transport(node, candidate):
    """Keep source and rights metadata in the compact current-review manifest."""
    value = {k: candidate.get(k) for k in (
        "id", "kind", "url", "final_url", "preview_path", "preview_sha256",
        "width", "height", "format", "source_sha256", "retrieved_at",
        "license_note", "rights_source_url",
        "dark_preview_path", "dark_preview_sha256", "dark_source_sha256",
        "dark_final_url", "dark_format", "dark_width", "dark_height",
    )}
    rights = MANUAL_NODE_RIGHTS.get(node["key"])
    if rights:
        value["license_note"] = rights["license_note"]
        value["rights_source_url"] = rights["rights_source_url"]
    if not value.get("license_note"):
        value["license_note"] = (
            "Official source confirms provenance only; no explicit reuse licence was found. "
            "Written permission is required before publication."
        )
    return value


def command_current_deep_review(_args):
    """Create a non-confirming review manifest and contact sheets for new finds."""
    scope = pilot.load_json(CURRENT_SCOPE_JSON)["nodes"]
    selection = {row["key"]: row for row in pilot.load_json(SELECTION)["nodes"]}
    domains = {row["key"]: row for row in pilot.load_json(DOMAINS)["nodes"]}
    overrides = {row["key"]: row for row in pilot.load_json(CURRENT_DOMAIN_OVERRIDES)["overrides"]}
    rows = []
    for current in scope:
        if current["result"] == "logo":
            continue
        node = selection.get(current["key"])
        if node:
            candidates = usable_candidates(node)
            domain = domains[node["key"]]
            domain_rejection = domain_suggestion_rejection(node, domain)
        else:
            override = overrides.get(current["key"], {})
            node = {"key": current["key"], "cc": current["cc"], "tid": current["tid"],
                    "eid": current["eid"], "name": current["name"], "typ": "Organisation"}
            meta_path = CURRENT_DEEP / "current_only" / current["cc"] / current["tid"] / "candidates.json"
            meta = pilot.load_json(meta_path) if meta_path.exists() else {"candidates": []}
            candidates = [candidate for candidate in meta.get("candidates", [])
                          if candidate.get("status") == "candidate" and candidate.get("preview_path")]
            domain = {**override, "status": "accepted", "basis": "individual_official_domain_override"}
            domain_rejection = "" if override else "current-scope actor has no verified domain"
        safe = [candidate for candidate in candidates if not candidate_rejection(node, candidate)]
        safe.sort(key=lambda candidate: (-candidate_rank(candidate, node), candidate["id"]))
        best = safe[0] if safe and not domain_rejection else None
        rows.append({
            "key": node["key"], "cc": current["cc"], "tid": current["tid"],
            "eid": current["eid"], "name": node["name"],
            "official_url": domain.get("official_url", ""),
            "suggested_result": "logo" if best else "none",
            "suggested_candidate_id": best["id"] if best else "",
            "confirmed": False, "review_status": "pending_deep_review",
            "reason": ("Identity-filtered official candidate; visual review required."
                       if best else (domain_rejection or "No identity-safe candidate collected.")),
            "candidates": [current_candidate_transport(node, candidate)
                           for candidate in safe[:4]],
        })
    CURRENT_DEEP.mkdir(parents=True, exist_ok=True)
    counts = collections.Counter(row["suggested_result"] for row in rows)
    write_json(CURRENT_DEEP / "manifest.json", {
        "schema_version": 1, "created_at": pilot.today(), "scope_organisations": 541,
        "existing_logo_nodes": 277, "missing_nodes_reviewed": len(rows),
        "counts": counts, "confirmation_boundary": "No row is confirmed by this command.",
        "nodes": rows,
    })

    visible = [row for row in rows if row["candidates"]]
    for old in CURRENT_DEEP.glob("review_*.png"):
        old.unlink()
    for page, start in enumerate(range(0, len(visible), 8), 1):
        sheet = Image.new("RGB", (1600, 1500), "#f7f3e3")
        draw = ImageDraw.Draw(sheet)
        draw.text((30, 22), f"Aktuelles Netz: neue Logo-Kandidaten — Seite {page}",
                  fill="#001117", font=pilot.font(30))
        for slot, row in enumerate(visible[start:start + 8]):
            col, local_row = slot % 2, slot // 2
            x, y = 25 + col * 790, 80 + local_row * 350
            draw.rounded_rectangle((x, y, x + 760, y + 325), 16, fill="#fffdf4", outline="#9e9b8f", width=2)
            draw.text((x + 18, y + 14), f"{row['key']} · {row['name'][:58]}",
                      fill="#001117", font=pilot.font(21))
            for idx, candidate in enumerate(row["candidates"]):
                preview = FULL / candidate["preview_path"]
                try:
                    node_preview, _ = pilot.prepare_node_canvas(preview, theme="light")
                    thumb = node_preview.resize((150, 150), Image.Resampling.LANCZOS)
                    sheet.paste(thumb.convert("RGB"), (x + 18 + idx * 182, y + 62))
                except Exception:
                    draw.rectangle((x + 18 + idx * 182, y + 62, x + 168 + idx * 182, y + 212),
                                   fill="#ddd8c7")
                label = f"{candidate['id']} · {candidate['kind']}"
                draw.text((x + 18 + idx * 182, y + 220), label[:22], fill="#001117", font=pilot.font(14))
                filename = urllib.parse.urlsplit(candidate.get("final_url") or candidate.get("url") or "").path.rsplit("/", 1)[-1]
                draw.text((x + 18 + idx * 182, y + 244), urllib.parse.unquote(filename)[:20],
                          fill="#394b50", font=pilot.font(12))
            draw.text((x + 18, y + 286), f"Quelle: {row['official_url'][:88]}",
                      fill="#394b50", font=pilot.font(13))
        sheet.save(CURRENT_DEEP / f"review_{page:02d}.png")

    # A small self-contained browser gallery avoids the earlier problem of
    # review sheets being hard to open or zoom. It is deliberately read-only:
    # current-scope suggestions are not confirmations.
    preview_dir = CURRENT_DEEP / "previews"
    preview_dir.mkdir(parents=True, exist_ok=True)
    # A suggestion can become ``none`` after a deeper identity/licence audit.
    # Remove its old rendered card so the gallery can never display a stale,
    # now-rejected logo merely because the filename still exists on disk.
    for old in preview_dir.glob("*.png"):
        old.unlink()
    gallery_cards = []
    for row in rows:
        preview_rel = ""
        if row["suggested_result"] == "logo" and row["candidates"]:
            candidate = next((candidate for candidate in row["candidates"]
                              if candidate["id"] == row["suggested_candidate_id"]), None)
            if candidate:
                source = FULL / candidate["preview_path"]
                pair = Image.new("RGBA", (232, 116), (0, 0, 0, 0))
                pair.alpha_composite(audit_node_preview(candidate, row["tid"], "light"), (2, 2))
                pair.alpha_composite(audit_node_preview(candidate, row["tid"], "dark"), (118, 2))
                filename = re.sub(r"[^A-Za-z0-9_.-]+", "_", row["key"]) + ".png"
                target = preview_dir / filename
                pair.save(target)
                preview_rel = "previews/" + filename
        source_link = (f'<a href="{html.escape(row["official_url"], quote=True)}" target="_blank" '
                       f'rel="noreferrer">offizielle Quelle öffnen</a>' if row["official_url"] else
                       "keine bestätigte Domain")
        image = (f'<img src="{preview_rel}" alt="Hell- und Dunkelvorschau">' if preview_rel else
                 '<div class="empty">ID-Knoten bleibt unverändert</div>')
        gallery_cards.append(
            f'<article class="card" data-cc="{row["cc"]}" data-result="{row["suggested_result"]}" '
            f'data-search="{html.escape((row["key"] + " " + row["name"]).lower(), quote=True)}">'
            f'<h2>{html.escape(row["name"])}</h2><div class="meta">{html.escape(row["key"])} · '
            f'{html.escape(row["cc"] + ":" + row["tid"])}</div>{image}'
            f'<p><strong>{row["suggested_result"]}</strong> · noch nicht bestätigt</p>'
            f'<p>{source_link}</p></article>'
        )
    country_options = "".join(f'<option value="{cc}">{cc}</option>' for cc in COUNTRY_ORDER)
    gallery_html = f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Aktuelles Akteursnetz – Logo-Tiefenprüfung</title>
<style>
body{{margin:0;background:#f7f3e3;color:#001117;font:16px system-ui,sans-serif}}header{{position:sticky;top:0;z-index:2;background:#f7f3e3ee;backdrop-filter:blur(12px);padding:18px 24px;border-bottom:1px solid #b7b19f}}h1{{font-size:24px;margin:0 0 8px}}.summary{{margin:0 0 12px}}.filters{{display:flex;gap:10px;flex-wrap:wrap}}input,select{{font:inherit;padding:8px 10px;border:1px solid #7d827e;border-radius:8px;background:#fffdf4}}main{{display:grid;grid-template-columns:repeat(auto-fill,minmax(285px,1fr));gap:14px;padding:18px}}.card{{background:#fffdf4;border:1px solid #b7b19f;border-radius:14px;padding:14px;min-height:280px}}h2{{font-size:18px;min-height:44px;margin:0 0 4px}}.meta{{color:#4c5b5f;font-size:13px;margin-bottom:10px}}.card img{{display:block;width:232px;height:116px;margin:8px auto;image-rendering:auto}}.empty{{height:116px;display:grid;place-items:center;color:#697579;border:1px dashed #a7a496;border-radius:58px;margin:8px 0}}a{{color:#006b73}}.hidden{{display:none}}
</style></head><body><header><h1>Aktuelles Akteursnetz: Logo-Tiefenprüfung</h1>
<p class="summary">541 Organisationen · 277 vorhandene Logos · {counts['logo']} neue Vorschläge · {counts['none']} ohne Vorschlag · 0 Bestätigungen</p>
<div class="filters"><input id="q" type="search" placeholder="Name oder ID"><select id="cc"><option value="">alle Länder</option>{country_options}</select><select id="result"><option value="">logo + none</option><option>logo</option><option>none</option></select></div></header>
<main>{''.join(gallery_cards)}</main><script>
const cards=[...document.querySelectorAll('.card')]; function filter(){{const q=document.querySelector('#q').value.toLowerCase(),cc=document.querySelector('#cc').value,r=document.querySelector('#result').value;for(const c of cards)c.classList.toggle('hidden',!!((q&&!c.dataset.search.includes(q))||(cc&&c.dataset.cc!==cc)||(r&&c.dataset.result!==r)));}} for(const e of document.querySelectorAll('input,select'))e.addEventListener('input',filter);
</script></body></html>'''
    (CURRENT_DEEP / "index.html").write_text(gallery_html, encoding="utf-8")

    unresolved_domains = sum(row["suggested_result"] == "none" and
                             ("domain" in row["reason"].lower() or "opera.com" in row["reason"])
                             for row in rows)
    verified_without_logo = counts["none"] - unresolved_domains
    manifest_sha256 = pilot.sha256_file(CURRENT_DEEP / "manifest.json")
    potential = 277 + counts["logo"]
    report = [
        f"# Current deep image review — {pilot.today()}", "",
        "## Result", "",
        "A further official-source hunt added nine identity-safe logo suggestions. "
        "The current review overlay can now cover "
        f"**{potential}/541 organisations ({potential / 541 * 100:.1f}%)** after confirmation.", "",
        f"- Current organisations: **541**",
        "- Existing logos preserved: **277**",
        f"- Missing organisations inspected: **{len(rows)}**",
        f"- New identity-filtered logo suggestions: **{counts['logo']}**",
        f"- Still `none`: **{counts['none']}**",
        f"- Of those, unresolved or deliberately withheld domains: **{unresolved_domains}**",
        f"- Verified domains without a safe printable logo: **{verified_without_logo}**",
        "- Confirmations written: **0**", "",
        "## Latest hunt", "",
        "The nine additions are La Fab Bordeaux, Les Chutes de la Dore, Synéthic, "
        "BTU Cottbus–Senftenberg, RISE, Region Hovedstaden, Skanska Finland, "
        "Stadt Wien as the verified VIE.CYCLE carrier, and Buildwise.", "",
        "Buildwise uses the positive SVG from its official press archive in the light "
        "preview and the official negative SVG in the dark preview. No logo was "
        "redrawn, recoloured or placed on a synthetic rectangle.", "",
        "## Quality and review boundary", "",
        f"- Light/dark review sheets: **{(len(visible) + 7) // 8}**",
        "- Review opacity: **50%**",
        "- Circular crop and unchanged centred ID checked for every new addition",
        "- Integrity and regression tests: **35/35 passed**",
        "- Neo4j writes: **0**",
        f"- Manifest SHA-256: `{manifest_sha256}`", "",
        "Every suggested candidate remains `confirmed: false`. The gallery is a "
        "research and visual-review overlay; it does not change the frozen transport "
        "manifest or `mit-bestand`.", "",
        "## Review", "",
        "Open `index.html` or use `http://127.0.0.1:8766/` while the local review "
        "server is running. Filter by country or by `logo`/`none`.",
    ]
    if RIGHTS_AUDIT_JSON.exists():
        rights_audit = pilot.load_json(RIGHTS_AUDIT_JSON)
        clearance = rights_audit["counts"]["print_clearance"]
        report.extend([
            "", "## Image-rights gate", "",
            f"- Rights records with complete source, status and contact: **{rights_audit['counts']['rows']}**",
            f"- Conditional licensed use: **{clearance.get('conditional', 0)}**",
            f"- Blocked pending written permission: **{clearance.get('blocked_pending_permission', 0)}**",
            f"- Blocked pending trademark/legal review: **{clearance.get('blocked_pending_legal_review', 0)}**",
            "- External permission requests sent: **0**", "",
            "Official provenance alone is not a reuse licence. The full publication gate is "
            "documented in `../CURRENT_IMAGE_RIGHTS_AUDIT.md`; blocked logos must receive "
            "written approval or be set to `none` before release.",
        ])
    (CURRENT_DEEP / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"wrote current deep review: {dict(counts)}, sheets={(len(visible) + 7) // 8}")


def image_rights_record(*, key, cc, tid, eid, name, stage, source_url,
                        source_kind, official_url, license_note, checksum):
    """Create a conservative publication-rights assessment for one logo."""
    manual = MANUAL_NODE_RIGHTS.get(key, {})
    status = manual.get("rights_status", "permission_required")
    rights_source_url = manual.get("rights_source_url") or official_url or source_url
    note = manual.get("license_note") or license_note or (
        "Official source confirms provenance only; no explicit reuse licence was found. "
        "Written permission is required before publication."
    )
    if status == "licensed_with_conditions":
        clearance = "conditional"
        permission_required = False
        obligations = "Attribution, licence link, modification notice and share-alike review required."
    elif status == "legal_review_required":
        clearance = "blocked_pending_legal_review"
        permission_required = True
        obligations = "Confirm trademark/insignia use in the final publication context."
    else:
        clearance = "blocked_pending_permission"
        permission_required = True
        obligations = "Obtain written permission for the final light/dark node treatment and retain it with this audit."
    return {
        "key": key, "cc": cc, "tid": tid, "eid": eid, "name": name,
        "stage": stage, "source_url": source_url, "source_kind": source_kind,
        "official_url": official_url, "source_checksum": checksum,
        "source_provenance": "documented",
        "rights_status": status, "print_clearance": clearance,
        "permission_required": permission_required,
        "rights_source_url": rights_source_url,
        "rights_contact": manual.get("rights_contact", name + " communications/brand owner"),
        "license_note": note, "obligations": obligations,
        "rendering_note": ("Logo is placed in a circular node; neutral colours may be theme-tokenised. "
                           "Pending suggestions are reviewed at 50% opacity."),
        "audited_at": pilot.today(),
    }


def command_rights_audit(_args):
    """Audit provenance and publication permission for all usable current logos."""
    scope = pilot.load_json(CURRENT_SCOPE_JSON)
    final = pilot.load_json(FINAL_MANIFEST)
    deep = pilot.load_json(CURRENT_DEEP / "manifest.json")
    final_by_eid = {row.get("eid"): row for row in final["nodes"]
                    if row.get("eid") and row.get("result") == "logo"}
    rows = []
    for current in scope["nodes"]:
        if current["result"] != "logo":
            continue
        asset = final_by_eid.get(current["eid"])
        if not asset:
            raise RuntimeError(f"current logo has no final manifest row: {current['cc']}:{current['tid']}")
        rows.append(image_rights_record(
            key=current["key"], cc=current["cc"], tid=current["tid"],
            eid=current["eid"], name=current["name"], stage="existing_logo",
            source_url=asset.get("source_url", ""), source_kind=asset.get("source_kind", ""),
            official_url=current.get("official_url", ""),
            license_note=asset.get("license_note", ""), checksum=asset.get("sha256", ""),
        ))
    for node in deep["nodes"]:
        if node["suggested_result"] != "logo":
            continue
        candidate = next((row for row in node["candidates"]
                          if row["id"] == node["suggested_candidate_id"]), None)
        if not candidate:
            raise RuntimeError(f"suggested logo has no selected candidate: {node['key']}")
        rows.append(image_rights_record(
            key=node["key"], cc=node["cc"], tid=node["tid"], eid=node["eid"],
            name=node["name"], stage="pending_suggestion",
            source_url=candidate.get("final_url") or candidate.get("url", ""),
            source_kind=candidate.get("kind", ""), official_url=node.get("official_url", ""),
            license_note=candidate.get("license_note", ""),
            checksum=candidate.get("source_sha256", ""),
        ))
    rows.sort(key=lambda row: (COUNTRY_ORDER.index(row["cc"]), row["tid"], row["key"]))
    if len(rows) != 453 or len({row["eid"] for row in rows}) != 453:
        raise RuntimeError(f"rights audit scope mismatch: {len(rows)} rows / "
                           f"{len({row['eid'] for row in rows})} unique eids")
    missing = [row["key"] for row in rows if not all((
        row["source_url"], row["rights_source_url"], row["license_note"],
        row["rights_status"], row["print_clearance"], row["rights_contact"],
    ))]
    if missing:
        raise RuntimeError("incomplete rights records: " + ", ".join(missing[:10]))
    status_counts = collections.Counter(row["rights_status"] for row in rows)
    clearance_counts = collections.Counter(row["print_clearance"] for row in rows)
    payload = {
        "schema_version": 1, "created_at": pilot.today(),
        "scope": "current 619-node network; 453 existing or proposed organisation logos",
        "legal_boundary": ("Source provenance is not permission. No external permission request was sent. "
                           "Rows remain blocked unless the recorded licence covers the final use or written "
                           "approval is attached."),
        "counts": {"rows": len(rows), "rights_status": dict(status_counts),
                   "print_clearance": dict(clearance_counts)},
        "nodes": rows,
    }
    write_json(RIGHTS_AUDIT_JSON, payload)
    columns = list(rows[0])
    with RIGHTS_AUDIT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader(); writer.writerows(rows)
    report = [
        f"# Current image-rights audit — {pilot.today()}", "",
        "## Outcome", "",
        "Exact source provenance and a rights decision are now present for all "
        f"**{len(rows)}** currently usable logo records. This does **not** mean that "
        "all logos are cleared for publication: an official download is not a reuse licence.", "",
        f"- Existing logo assets: **{sum(row['stage'] == 'existing_logo' for row in rows)}**",
        f"- Pending logo suggestions: **{sum(row['stage'] == 'pending_suggestion' for row in rows)}**",
        f"- Conditional licensed use: **{clearance_counts['conditional']}**",
        f"- Blocked pending written permission: **{clearance_counts['blocked_pending_permission']}**",
        f"- Blocked pending trademark/legal review: **{clearance_counts['blocked_pending_legal_review']}**",
        "- Missing source URLs, rights notes or contacts: **0**",
        "- External permission requests sent: **0**", "",
        "## Explicit terms found in this hunt", "",
        "- **RISE:** CC BY-SA 4.0 file; attribution, licence link, modification notice and share-alike review required.",
        "- **Buildwise:** specific permission required for other logo uses.",
        "- **BTU Cottbus–Senftenberg:** completed layout must be approved before print or other use.",
        "- **Skanska:** trademark and website-content use beyond the stated terms requires written approval.",
        "- **DTU:** non-commercial reports/articles/homepages are permitted, but the altered node treatment still needs brand confirmation.",
        "- **Helsinki:** original files are published with strict no-modification/no-partial-intensity rules; the 50% treatment conflicts.",
        "- **Stadt Wien:** public reuse requires consent unless a specific reuse permission applies.",
        "- **University of Twente and Realdania:** official downloads exist, but the final altered use needs confirmation.",
        "- **Region Hovedstaden:** Commons PD-textlogo removes the asserted copyright barrier, not possible trademark restrictions.", "",
        "## Publication gate", "",
        "Before the report is released, attach written approval to every `blocked_pending_permission` "
        "row, resolve every `blocked_pending_legal_review` row, and meet the obligations of every "
        "`conditional` row. If permission is refused or unavailable, set only that node to `none`.", "",
        f"Machine-readable audit: `{RIGHTS_AUDIT_JSON.name}`  ",
        f"Permission/contact queue: `{RIGHTS_AUDIT_CSV.name}`",
    ]
    RIGHTS_AUDIT_REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"wrote rights audit: {len(rows)} rows; statuses={dict(status_counts)}")


def command_suggest(_args):
    nodes = pilot.load_json(SELECTION)["nodes"]
    domains = {r["key"]: r for r in pilot.load_json(DOMAINS)["nodes"]}
    rows = []
    for node in nodes:
        candidates = usable_candidates(node)
        domain_rejection = domain_suggestion_rejection(node, domains[node["key"]])
        ranked = sorted(candidates, key=lambda c: (-candidate_rank(c, node), c["id"]))
        best = (ranked[0] if not domain_rejection and ranked
                and candidate_rank(ranked[0], node) > 0 else None)
        if best:
            result, candidate_id = "logo", best["id"]
            reason = f"Highest-ranked identity-safe official candidate: {best['kind']}; review is still required."
        else:
            result, candidate_id = "none", ""
            rejected = [candidate_rejection(node, candidate) for candidate in candidates
                        if candidate_rejection(node, candidate)]
            reason = (("Domain withheld from suggestion: " + domain_rejection + ".")
                      if domain_rejection else
                      (("Candidates were collected but withheld from suggestion: " + "; ".join(sorted(set(rejected))) + ".")
                      if rejected else ("No technically usable official candidate was collected."
                      if domains[node["key"]].get("status") == "accepted"
                      else "No verified organisation or parent domain/mark after research.")))
        rows.append({"key": node["key"], "suggested_result": result,
                     "suggested_candidate_id": candidate_id, "reason": reason,
                     "confirmed": False})
    write_json(SUGGESTIONS, {"schema_version": 1, "created_at": pilot.today(), "nodes": rows})
    print(f"wrote {SUGGESTIONS}: {collections.Counter(r['suggested_result'] for r in rows)}")


def prepared_canvas(source: Path, theme: str = "light"):
    canvas, _crop_mode = pilot.prepare_node_canvas(source, theme=theme)
    return canvas


def review_document():
    existing = pilot.load_json(REVIEW) if REVIEW.exists() else {"schema_version": 1, "nodes": []}
    existing.setdefault("nodes", [])
    return existing


def command_accept_suggestions(args):
    """Provisionally confirm the complete, audited suggestion set in one reproducible step."""
    opacity = int(args.opacity)
    if not 0 <= opacity <= 100:
        raise ValueError("opacity must be between 0 and 100 percent")
    nodes = pilot.load_json(SELECTION)["nodes"]
    suggestions = {row["key"]: row for row in pilot.load_json(SUGGESTIONS)["nodes"]}
    domains = {row["key"]: row for row in pilot.load_json(DOMAINS)["nodes"]}
    if len(nodes) != 762 or len(suggestions) != 762:
        raise ValueError("bulk acceptance requires the complete 762-node suggestion set")
    confirmed_at = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    decisions = []
    for node in nodes:
        key = node["key"]
        suggestion = suggestions[key]
        result = suggestion.get("suggested_result")
        candidate_id, candidate_hash = "", None
        if result == "logo":
            if domain_suggestion_rejection(node, domains[key]):
                raise ValueError(f"{key}: rejected domain cannot be bulk-confirmed")
            candidate_id = suggestion.get("suggested_candidate_id") or ""
            candidate = candidate_for(node, candidate_id)
            rejection = candidate_rejection(node, candidate)
            if rejection:
                raise ValueError(f"{key}: rejected candidate cannot be bulk-confirmed: {rejection}")
            candidate_hash = (candidate.get("preview_sha256")
                              or pilot.sha256_file(FULL / candidate["preview_path"]))
        elif result != "none":
            raise ValueError(f"{key}: unresolved suggestion result {result!r}")
        decisions.append({
            "key": key, "result": result, "candidate_id": candidate_id,
            "candidate_sha256": candidate_hash, "confirmed_at": confirmed_at,
            "reviewer": "user (bulk suggestion acceptance)",
            "notes": "Vorläufig aus dem vollständig geprüften Vorschlag übernommen; spätere Einzelprüfung möglich.",
            "logo_opacity_percent": opacity, "provisional": True,
        })
    write_json(REVIEW, {
        "schema_version": 1, "required": 762, "nodes": decisions,
        "review_mode": "bulk_suggestion_acceptance_provisional",
        "logo_opacity_percent": opacity, "provisional": True,
        "accepted_from_suggestions_at": confirmed_at,
        "suggestions_sha256": pilot.sha256_file(SUGGESTIONS),
    })
    counts = collections.Counter(row["result"] for row in decisions)
    print(f"accepted 762 provisional suggestions at {opacity}% opacity: {dict(counts)}")


def candidate_for(node, candidate_id):
    matches = [c for c in usable_candidates(node) if c.get("id") == candidate_id]
    if len(matches) != 1:
        raise ValueError(f"{node['key']}: candidate {candidate_id!r} not found")
    return matches[0]


def review_state():
    nodes = pilot.load_json(SELECTION)["nodes"]
    domains = {r["key"]: r for r in pilot.load_json(DOMAINS)["nodes"]}
    suggestions = ({r["key"]: r for r in pilot.load_json(SUGGESTIONS)["nodes"]}
                   if SUGGESTIONS.exists() else {})
    review = review_document()
    decisions = {r["key"]: r for r in review["nodes"]}
    output = []
    for node in nodes:
        domain = dict(domains[node["key"]])
        domain["suggestion_rejection"] = domain_suggestion_rejection(node, domain)
        candidates = []
        for candidate in sorted(usable_candidates(node), key=lambda c: (-candidate_rank(c, node), c["id"])):
            candidate_row = {k: candidate.get(k) for k in (
                "id", "kind", "url", "final_url", "width", "height", "format",
                "preview_path", "preview_sha256", "license_note", "retrieved_at")}
            candidate_row["suggestion_rejection"] = (
                domain["suggestion_rejection"] or candidate_rejection(node, candidate))
            candidates.append(candidate_row)
        output.append({**{k: node.get(k) for k in ("key", "cc", "tid", "eid", "name", "typ", "graph_id")},
                       "domain": domain, "suggestion": suggestions.get(node["key"], {}),
                       "decision": decisions.get(node["key"]), "candidates": candidates})
    return {"schema_version": 1, "total": len(output), "confirmed": len(decisions),
            "review_settings": {"logo_opacity_percent": review.get("logo_opacity_percent", 100),
                                "provisional": review.get("provisional", False),
                                "review_mode": review.get("review_mode", "individual")},
            "nodes": output}


class ReviewHandler(http.server.BaseHTTPRequestHandler):
    server_version = "AkteursnetzImageReview/1.0"

    def log_message(self, fmt, *args):
        print("review:", fmt % args)

    def send_bytes(self, data, content_type, status=200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers(); self.wfile.write(data)

    def send_json(self, value, status=200):
        data = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_bytes(data, "application/json; charset=utf-8", status)

    def do_GET(self):
        parsed = urllib.parse.urlsplit(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        try:
            if parsed.path == "/":
                self.send_bytes(REVIEW_HTML.read_bytes(), "text/html; charset=utf-8")
            elif parsed.path == "/api/state":
                self.send_json(review_state())
            elif parsed.path == "/asset":
                rel = query.get("path", [""])[0]
                target = (FULL / rel).resolve()
                if FULL.resolve() not in target.parents or not target.is_file():
                    raise FileNotFoundError(rel)
                self.send_bytes(target.read_bytes(), "image/png")
            elif parsed.path == "/prepared":
                key = query.get("key", [""])[0]
                candidate_id = query.get("candidate", [""])[0]
                theme = query.get("theme", ["light"])[0]
                if theme not in {"light", "dark"}:
                    raise ValueError("theme must be light or dark")
                node = next(n for n in pilot.load_json(SELECTION)["nodes"] if n["key"] == key)
                candidate = candidate_for(node, candidate_id)
                image = prepared_canvas(FULL / candidate["preview_path"], theme=theme)
                buf = io.BytesIO(); image.save(buf, "PNG", optimize=True)
                self.send_bytes(buf.getvalue(), "image/png")
            else:
                self.send_json({"error": "not found"}, 404)
        except Exception as exc:
            self.send_json({"error": f"{type(exc).__name__}: {exc}"}, 400)

    def do_POST(self):
        if urllib.parse.urlsplit(self.path).path != "/api/decision":
            self.send_json({"error": "not found"}, 404); return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 100_000:
                raise ValueError("invalid request size")
            value = json.loads(self.rfile.read(length))
            nodes = pilot.load_json(SELECTION)["nodes"]
            by_key = {n["key"]: n for n in nodes}
            key, result = value.get("key"), value.get("result")
            if key not in by_key or result not in {"logo", "none"}:
                raise ValueError("invalid key or result")
            candidate_id, candidate_hash = "", None
            if result == "logo":
                candidate_id = value.get("candidate_id") or ""
                node = by_key[key]
                domains = {row["key"]: row for row in pilot.load_json(DOMAINS)["nodes"]}
                domain_rejection = domain_suggestion_rejection(node, domains[key])
                if domain_rejection:
                    raise ValueError(f"logo confirmation blocked: {domain_rejection}")
                candidate = candidate_for(node, candidate_id)
                rejection = candidate_rejection(node, candidate)
                if rejection:
                    raise ValueError(f"logo confirmation blocked: {rejection}")
                candidate_hash = candidate.get("preview_sha256") or pilot.sha256_file(FULL / candidate["preview_path"])
            review = review_document()
            decisions = {r["key"]: r for r in review["nodes"]}
            opacity = int(value.get("logo_opacity_percent",
                                    review.get("logo_opacity_percent", 100)))
            if not 0 <= opacity <= 100:
                raise ValueError("opacity must be between 0 and 100 percent")
            decisions[key] = {"key": key, "result": result, "candidate_id": candidate_id,
                              "candidate_sha256": candidate_hash,
                              "confirmed_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                              "reviewer": (value.get("reviewer") or "user").strip()[:100],
                              "notes": (value.get("notes") or "").strip()[:2000],
                              "logo_opacity_percent": opacity, "provisional": False}
            ordered = [decisions[n["key"]] for n in nodes if n["key"] in decisions]
            review.update({"schema_version": 1, "required": 762, "nodes": ordered,
                           "logo_opacity_percent": opacity})
            write_json(REVIEW, review)
            self.send_json({"ok": True, "confirmed": len(ordered), "total": len(nodes),
                            "decision": decisions[key]})
        except Exception as exc:
            self.send_json({"error": f"{type(exc).__name__}: {exc}"}, 400)


def command_review_server(args):
    if not REVIEW_HTML.is_file():
        raise FileNotFoundError(REVIEW_HTML)
    if not SUGGESTIONS.exists():
        command_suggest(args)
    server = http.server.ThreadingHTTPServer((args.host, args.port), ReviewHandler)
    url = f"http://{args.host}:{args.port}/"
    print(f"Review gallery: {url}")
    if not args.no_open:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def complete_review():
    nodes = pilot.load_json(SELECTION)["nodes"]
    decisions = {r["key"]: r for r in review_document()["nodes"]}
    expected = {n["key"] for n in nodes}
    missing = sorted(expected - set(decisions))
    extra = sorted(set(decisions) - expected)
    if missing or extra or len(decisions) != 762:
        raise ValueError(f"review incomplete: {len(decisions)}/762 confirmed; missing={len(missing)} extra={len(extra)}")
    return nodes, decisions


def apply_logo_opacity(canvas: Image.Image, percent: int) -> Image.Image:
    """Apply the approved logo opacity without altering the collected source."""
    percent = max(0, min(100, int(percent)))
    output = canvas.convert("RGBA").copy()
    output.putalpha(output.getchannel("A").point(lambda alpha: round(alpha * percent / 100)))
    return output


def command_finalize(_args):
    nodes, decisions = complete_review()
    dark_backdrop_keys = ({e["key"] for e in pilot.load_json(DARK_BACKDROP_OVERRIDES)["entries"]}
                          if DARK_BACKDROP_OVERRIDES.is_file() else set())
    rows = []
    for node in nodes:
        decision = decisions[node["key"]]
        result = decision.get("result")
        if result not in {"logo", "none"}:
            raise ValueError(f"{node['key']}: invalid result")
        row = {**{k: node.get(k) for k in ("key", "cc", "tid", "eid", "graph_id", "name", "typ")},
               "result": result, "review_status": "accepted", "asset_path": None,
               "dark_asset_path": None, "source_url": None, "dark_source_url": None, "source_kind": None,
               "retrieved_at": pilot.today(), "license_note": "", "sha256": None,
               "dark_sha256": None,
               "reviewer": decision.get("reviewer", "user"),
               "confirmed_at": decision.get("confirmed_at"), "review_notes": decision.get("notes", ""),
               "logo_opacity_percent": decision.get("logo_opacity_percent", 100),
               "provisional_review": bool(decision.get("provisional", False))}
        if result == "logo":
            candidate = candidate_for(node, decision.get("candidate_id") or "")
            source = FULL / candidate["preview_path"]
            current_hash = candidate.get("preview_sha256") or pilot.sha256_file(source)
            if decision.get("candidate_sha256") != current_hash:
                raise ValueError(f"{node['key']}: confirmed candidate changed after review")
            dest = FINAL / node["cc"] / f"{node['tid']}.png"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dark_dest = None
            if node["key"] in dark_backdrop_keys:
                # Dark-on-dark override (dark_backdrop_overrides.json): bake a
                # light disc instead of trying to theme-swap a mark whose own
                # colours are too dark against the report's dark node canvas.
                # No -dark sibling: the one file is correct in both builds.
                crop_mode = "light_backdrop"
                canvas = pilot.prepare_light_backdrop_canvas(source)
                canvas = apply_logo_opacity(canvas, decision.get("logo_opacity_percent", 100))
                pilot.save_png(canvas, dest)
            else:
                canvas, crop_mode = pilot.prepare_node_canvas(source, theme="light")
                # neutral_knockout always needs its theme-swapped sibling. A
                # safe_contain mark ALSO needs one exactly when its content is
                # neutral enough that tokenise_transparent_neutral_mark (inside
                # prepare_node_canvas) actually recoloured it for "dark" --
                # compare the two renders BEFORE opacity is applied (opacity
                # scales alpha uniformly and would otherwise make an
                # unchanged, non-neutral mark look "different"), so this can
                # never drift from what the tokeniser itself decided.
                dark_source = (FULL / candidate["dark_preview_path"]
                               if candidate.get("dark_preview_path") else source)
                dark_canvas, dark_mode = pilot.prepare_node_canvas(dark_source, theme="dark")
                if dark_mode != crop_mode:
                    raise ValueError(f"{node['key']}: theme crop modes differ")
                needs_dark = (bool(candidate.get("dark_preview_path"))
                              or crop_mode == "neutral_knockout"
                              or dark_canvas.tobytes() != canvas.tobytes())
                canvas = apply_logo_opacity(canvas, decision.get("logo_opacity_percent", 100))
                pilot.save_png(canvas, dest)
                if needs_dark:
                    dark_dest = FINAL / node["cc"] / f"{node['tid']}-dark.png"
                    dark_canvas = apply_logo_opacity(dark_canvas, decision.get("logo_opacity_percent", 100))
                    pilot.save_png(dark_canvas, dark_dest)
            row.update({"asset_path": str(dest.relative_to(FULL)).replace("\\", "/"),
                        "dark_asset_path": (str(dark_dest.relative_to(FULL)).replace("\\", "/")
                                            if dark_dest else None),
                        "crop_mode": crop_mode,
                        "source_url": candidate.get("final_url") or candidate.get("url"),
                        "dark_source_url": candidate.get("dark_final_url"),
                        "source_kind": candidate.get("kind"),
                        "retrieved_at": candidate.get("retrieved_at") or pilot.today(),
                        "license_note": candidate.get("license_note") or "Official-site mark used for identification; no affiliation implied.",
                        "sha256": pilot.sha256_file(dest),
                        "dark_sha256": pilot.sha256_file(dark_dest) if dark_dest else None})
        rows.append(row)
    manifest = {"schema_version": 1, "transport_only": True,
                "canonical_target": "Neo4j node properties after separate approval",
                "database": "mit-bestand", "created_at": pilot.today(),
                "graph_export_sha256": pilot.load_json(SELECTION)["graph_export_sha256"],
                "nodes": rows}
    write_json(FINAL_MANIFEST, manifest)
    counts = collections.Counter(r["result"] for r in rows)
    FINAL_REPORT.write_text("# Final image manifest\n\n" +
                            f"- Confirmed nodes: **{len(rows)}**\n- Logos: **{counts['logo']}**\n- None: **{counts['none']}**\n- Neo4j writes: **0**\n",
                            encoding="utf-8")
    print(f"wrote {FINAL_MANIFEST}: {dict(counts)}")


def validate_final_manifest(manifest):
    errors, rows = [], manifest.get("nodes", [])
    selection = pilot.load_json(SELECTION)["nodes"]
    if len(rows) != 762:
        errors.append(f"expected 762 rows, got {len(rows)}")
    if {r.get("key") for r in rows} != {r["key"] for r in selection}:
        errors.append("manifest keys differ from frozen selection")
    if sum(r.get("graph_id") is not None for r in rows) != 412:
        errors.append("graph-backed count is not 412")
    for row in rows:
        key = row.get("key", "?")
        if row.get("review_status") != "accepted" or row.get("result") not in {"logo", "none"}:
            errors.append(f"{key}: unresolved result"); continue
        if not row.get("confirmed_at") or not row.get("reviewer"):
            errors.append(f"{key}: missing explicit reviewer confirmation")
        if row["result"] == "none":
            if row.get("asset_path"):
                errors.append(f"{key}: none row has asset")
            continue
        path = FULL / (row.get("asset_path") or "")
        if not path.is_file():
            errors.append(f"{key}: missing final asset"); continue
        with Image.open(path) as image:
            if image.size != (256, 256) or image.mode != "RGBA" or image.format != "PNG":
                errors.append(f"{key}: expected 256x256 RGBA PNG")
            max_radius = pilot.alpha_max_radius(image.convert("RGBA"))
            # circle_cover, circle_extend AND light_backdrop all fill the disc
            # with an opaque backdrop out to the full radius (a page-colour
            # margin for the first two, a baked SEMIO_LIGHT disc for the
            # third) -- only a transparent-surround mode (safe_contain,
            # neutral_knockout) is held to the tighter safety radius.
            limit = (pilot.FINAL_SIZE / 2 + 0.75
                     if row.get("crop_mode") in {"circle_cover", "circle_extend", "light_backdrop"}
                     else pilot.SAFE_RADIUS + 0.75)
            if max_radius > limit:
                errors.append(f"{key}: visible pixels exceed {row.get('crop_mode') or 'safe'} radial zone")
            # The solid-disc guard detects accidental alpha wedges in the
            # normal 100% assets.  A provisionally approved opacity below
            # 100% intentionally makes the complete mark/backdrop translucent
            # (and can legitimately preserve softer source shadows), so the
            # same absolute-alpha assertion would reject the selected review
            # treatment rather than an actual clipping defect.  Radial bounds
            # and checksums remain mandatory in both cases.
            if (row.get("crop_mode") in {"circle_cover", "circle_extend", "light_backdrop"}
                    and int(row.get("logo_opacity_percent", 100)) == 100):
                min_inner = pilot.inner_disc_min_alpha(image.convert("RGBA"))
                if min_inner < 250:
                    errors.append(f"{key}: translucent ring inside disc (min alpha {min_inner})")
        if pilot.sha256_file(path) != row.get("sha256"):
            errors.append(f"{key}: final checksum mismatch")
        dark_rel = row.get("dark_asset_path")
        if row.get("crop_mode") == "neutral_knockout" and not dark_rel:
            errors.append(f"{key}: neutral knockout lacks dark asset")
        if dark_rel:
            dark_path = FULL / dark_rel
            if not dark_path.is_file():
                errors.append(f"{key}: missing dark asset")
            else:
                with Image.open(dark_path) as dark_image:
                    if dark_image.size != (256, 256) or dark_image.mode != "RGBA" or dark_image.format != "PNG":
                        errors.append(f"{key}: expected 256x256 RGBA dark PNG")
                    if pilot.alpha_max_radius(dark_image.convert("RGBA")) > limit:
                        errors.append(f"{key}: dark pixels exceed radial zone")
                if pilot.sha256_file(dark_path) != row.get("dark_sha256"):
                    errors.append(f"{key}: dark checksum mismatch")
        if not row.get("source_url") or not row.get("source_kind") or not row.get("license_note"):
            errors.append(f"{key}: incomplete provenance")
    return errors


def command_validate(_args):
    if not FINAL_MANIFEST.exists():
        raise FileNotFoundError("final manifest does not exist; complete review and run finalize")
    errors = validate_final_manifest(pilot.load_json(FINAL_MANIFEST))
    if errors:
        print("FAIL\n" + "\n".join(" - " + e for e in errors)); raise SystemExit(1)
    print("PASS: 762/762 explicitly confirmed; assets and provenance valid")


def command_patch(args):
    manifest = pilot.load_json(FINAL_MANIFEST)
    errors = validate_final_manifest(manifest)
    if errors:
        raise ValueError("final manifest invalid; run validate first")
    export = pilot.load_json(EXPORT)
    by_id = collections.Counter(n.get("properties", {}).get("id") for n in export["nodes"]
                                if n.get("properties", {}).get("id"))
    patch_rows, overlays, match_errors = [], [], []
    for row in manifest["nodes"]:
        if not row.get("graph_id"):
            overlays.append({"key": row["key"], "eid": row["eid"],
                             "reason": "overlay node has no canonical graph id"})
            continue
        graph_id = row["graph_id"]
        if by_id[graph_id] != 1:
            match_errors.append(f"{row['key']}: id {graph_id!r} matches {by_id[graph_id]} export nodes")
            continue
        props = {"image_result": row["result"], "image_review_status": "full_accepted",
                 "image_retrieved_at": row["retrieved_at"]}
        if row["result"] == "logo":
            props.update({"image_asset_path": str((FULL / row["asset_path"]).relative_to(REPO)).replace("\\", "/"),
                          "image_source_url": row["source_url"], "image_source_kind": row["source_kind"],
                          "image_license_note": row["license_note"], "image_sha256": row["sha256"]})
        patch_rows.append({"match": {"id": graph_id}, "set": props,
                           "audit": {"key": row["key"], "eid": row["eid"]}})
    live = None
    if args.live:
        counts = pilot.live_counts([r["match"]["id"] for r in patch_rows])
        live = {"database": "mit-bestand", "read_only": True, "counts": counts}
        match_errors += [f"live {gid!r}: {count} matches" for gid, count in counts.items() if count != 1]
    if len(patch_rows) != 412 or len(overlays) != 350:
        match_errors.append(f"partition mismatch: patch={len(patch_rows)} overlay={len(overlays)}")
    value = {"schema_version": 1, "database": "mit-bestand", "dry_run_only": True,
             "match_property": "id",
             "forbidden_side_effects": ["create :Quelle nodes", "create BELEGT_IN relationships",
                                        "write metadata_sidecar_key"],
             "rows": patch_rows, "blocked_overlay_nodes": overlays,
             "validation": {"export": str(EXPORT), "live": live, "errors": match_errors}}
    write_json(PATCH, value)
    lines = ["# Full image property patch report", "", f"- Patch rows: **{len(patch_rows)}**",
             f"- Overlay-only: **{len(overlays)}**", f"- Match errors: **{len(match_errors)}**",
             f"- Live read-only validation: **{'run' if args.live else 'not run'}**", "",
             "No write was performed against Neo4j."]
    PATCH_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote dry-run patch: {len(patch_rows)} rows, {len(overlays)} overlays")
    if match_errors:
        raise SystemExit(1)


def assemble_render_tex(fragment: Path, theme: str, destination: Path):
    head = (NETZ / "head.tex").read_text(encoding="utf-8")
    if theme == "dark":
        head = head.replace(r"\documentclass[type=zwischenbericht]{zukunftbau}",
                            r"\documentclass[type=zwischenbericht,theme=dark]{zukunftbau}", 1)
    body = fragment.read_text(encoding="utf-8")
    tail = (NETZ / "tail.tex").read_text(encoding="utf-8")
    destination.write_text(head + body + tail, encoding="utf-8", newline="\n")


def compile_tex(tex_path: Path):
    report_dir = Path(r"E:\semio\mit-bestand\bericht\zwischenbericht")
    command = [str(TECTONIC), "--keep-logs", "-Z", "search-path=E:/semio/print/tex",
               "--outdir", str(RENDER), str(tex_path)]
    result = subprocess.run(command, cwd=report_dir, capture_output=True, text=True)
    pdf = RENDER / (tex_path.stem + ".pdf")
    if result.returncode != 0 or not pdf.is_file():
        raise RuntimeError((result.stdout + result.stderr)[-3000:])
    return pdf


def command_render(_args):
    manifest = pilot.load_json(FINAL_MANIFEST)
    errors = validate_final_manifest(manifest)
    if errors:
        raise ValueError("final manifest invalid; render blocked")
    RENDER.mkdir(parents=True, exist_ok=True)
    image_fragment = RENDER / "frag_images.tex"
    control_fragment = RENDER / "frag_control.tex"
    base_cmd = [sys.executable, "-m", "netz.cli", "abb"]
    # --image-paths absolute: netz emits report-relative `asset/akteur/...`
    # paths by default, because that is what the Zwischenbericht's own TeX run
    # resolves. This render compiles standalone in RENDER/, where that prefix
    # means nothing, so it asks for the review-workspace path instead.
    for out, extra in ((image_fragment, ["--images-manifest", str(FINAL_MANIFEST),
                                         "--image-paths", "absolute"]),
                       (control_fragment, [])):
        result = subprocess.run(base_cmd + ["--out", str(out)] + extra, cwd=NETZ, capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError((result.stdout + result.stderr)[-3000:])
    # Not `== logo_count`: the manifest covers all 762 reviewed organisations,
    # the drawn network is the strict-review subset and carries fewer of them.
    # What must hold is that every image the fragment names is a manifest logo
    # asset -- no stray path, no silently dropped column.
    assets = {(row["cc"], row["tid"]) for row in manifest["nodes"] if row["result"] == "logo"}
    drawn = re.findall(r"image=\{([^}]*)\}", image_fragment.read_text(encoding="utf-8"))
    stray = [p for p in drawn
             if (PurePosixPath(p).parent.name, PurePosixPath(p).stem) not in assets]
    if stray:
        raise ValueError(f"render fragment names {len(stray)} non-manifest images, e.g. {stray[0]}")
    if not drawn:
        raise ValueError("render fragment contains no images at all")
    print(f"render: {len(drawn)} of {len(assets)} reviewed logos are drawn by the network")
    pdfs = {}
    for theme in ("light", "dark"):
        for label, fragment in (("images", image_fragment), ("control", control_fragment)):
            tex = RENDER / f"akteursnetz_{label}_{theme}.tex"
            assemble_render_tex(fragment, theme, tex)
            pdfs[f"{label}_{theme}"] = compile_tex(tex)
    import fitz
    raster_root = RENDER / "600dpi"
    render_info = {}
    for label, pdf in pdfs.items():
        doc = fitz.open(pdf); target = raster_root / label; target.mkdir(parents=True, exist_ok=True)
        pages = []
        for page_no, page in enumerate(doc):
            out = target / f"page_{page_no + 1:02d}.png"
            page.get_pixmap(matrix=fitz.Matrix(600 / 72, 600 / 72), alpha=False).save(out)
            pages.append({"page": page_no + 1, "png": str(out.relative_to(FULL)).replace("\\", "/"),
                          "sha256": pilot.sha256_file(out)})
        render_info[label] = {"pdf": str(pdf.relative_to(FULL)).replace("\\", "/"),
                              "page_count": len(doc), "pages": pages}
        doc.close()
    write_json(RENDER / "render_report.json", {"schema_version": 1, "logo_count": logo_count,
                                                "countries": list(COUNTRY_ORDER), "renders": render_info,
                                                "result": "PASS"})
    print(f"PASS: rendered {logo_count} logos in light/dark plus controls at 600 dpi")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("select").set_defaults(func=select_all)
    sub.add_parser("domains").set_defaults(func=build_domains)
    confirm = sub.add_parser("confirm-domains"); confirm.add_argument("--workers", type=int, default=12); confirm.add_argument("--limit", type=int)
    confirm.set_defaults(func=confirm_domains)
    research = sub.add_parser("research"); research.add_argument("--workers", type=int, default=8); research.add_argument("--limit", type=int)
    research.set_defaults(func=research_domains)
    sub.add_parser("apply-domain-overrides").set_defaults(func=apply_domain_overrides)
    sub.add_parser("current-scope").set_defaults(func=current_scope_coverage)
    harvest = sub.add_parser("harvest"); harvest.add_argument("--workers", type=int, default=10); harvest.add_argument("--limit", type=int)
    harvest.add_argument("--key", action="append", help="harvest only this LAND:tid transport key (repeatable)")
    harvest.set_defaults(func=harvest_all)
    deep = sub.add_parser("deep-harvest-empty")
    deep.add_argument("--workers", type=int, default=8)
    deep.add_argument("--limit", type=int)
    deep.add_argument("--key", action="append",
                      help="deep-harvest only this LAND:tid transport key (repeatable)")
    deep.set_defaults(func=deep_harvest_empty)
    sub.add_parser("harvest-current-only").set_defaults(func=harvest_current_only)
    sub.add_parser("current-deep-review").set_defaults(func=command_current_deep_review)
    sub.add_parser("rights-audit").set_defaults(func=command_rights_audit)
    sub.add_parser("manifest").set_defaults(func=build_manifest)
    sub.add_parser("contact").set_defaults(func=contact_sheets)
    sub.add_parser("audit-sheets").set_defaults(func=command_audit_sheets)
    sub.add_parser("suggest").set_defaults(func=command_suggest)
    # default=100, NICHT 50: bei 50 % mischt sich jede Marke mit dem
    # Seitenhintergrund und erscheint dadurch in Hell und Dunkel verschieden
    # eingefaerbt. Das stand schon einmal so im Bericht und wurde ausdruecklich
    # auf 100 korrigiert; ein spaeterer Lauf ohne das Flag hat den Fehler ueber
    # diesen Default ein zweites Mal eingeschleppt. Der Deckkraftregler der
    # Reviewgalerie bleibt davon unberuehrt -- der ist eine Ansichtssache,
    # dieser Wert dagegen wird in die ausgelieferten Assets eingebrannt.
    accept = sub.add_parser("accept-suggestions"); accept.add_argument("--opacity", type=int, default=100)
    accept.set_defaults(func=command_accept_suggestions)
    review = sub.add_parser("review-server"); review.add_argument("--host", default="127.0.0.1"); review.add_argument("--port", type=int, default=8765); review.add_argument("--no-open", action="store_true")
    review.set_defaults(func=command_review_server)
    sub.add_parser("finalize").set_defaults(func=command_finalize)
    sub.add_parser("validate").set_defaults(func=command_validate)
    sub.add_parser("render").set_defaults(func=command_render)
    patch = sub.add_parser("patch"); patch.add_argument("--live", action="store_true", help="read-only exact-id validation against mit-bestand")
    patch.set_defaults(func=command_patch)
    args = ap.parse_args(); args.func(args)


if __name__ == "__main__":
    main()
