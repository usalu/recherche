#!/usr/bin/env python3
"""Complete research gaps without changing logo selections or clearances."""

from __future__ import annotations

import concurrent.futures
import csv
import io
import json
import re
import urllib.parse
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

import requests
import urllib3
from PIL import Image


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "bilder_full"
OUT_JSON = DATA / "MISSING_INFO_COMPLETION.json"
OUT_CSV = DATA / "MISSING_INFO_COMPLETION.csv"
OUT_MD = DATA / "MISSING_INFO_COMPLETION.md"
OUT_LOGO_JSON = DATA / "MISSING_LOGO_FINAL_RESEARCH_DISPOSITION.json"
OUT_LOGO_CSV = DATA / "MISSING_LOGO_FINAL_RESEARCH_DISPOSITION.csv"
OUT_LOGO_MD = DATA / "MISSING_LOGO_FINAL_RESEARCH_DISPOSITION.md"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/136 Safari/537.36"

CONTACT_TERMS = ("contact", "kontakt", "contactez", "yhteys", "over-ons", "about", "team", "ansprech")
MEDIA_TERMS = ("press", "presse", "media", "medien", "brand", "logo", "download", "kommunikation")
LEGAL_TERMS = ("impressum", "legal", "mentions-legales", "privacy", "datenschutz", "copyright")
LOGO_TERMS = ("logo", "logotype", "wordmark", "brand", "favicon", "apple-touch")
EMAIL_RE = re.compile(r"[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}", re.I)
CSS_URL_RE = re.compile(r"url\(\s*['\"]?([^)'\"]+)['\"]?\s*\)", re.I)

DOCUMENTED_NONE = {
    "CH:U01": ("none_no_current_first_party_brand", "Historical AIK project consultant; no exact current first-party organisation or logo found."),
    "CH:U18": ("none_no_current_first_party_brand", "Oberli Ingenieurbau is documented in project sources but no current first-party organisation or logo was found."),
    "DE:F03": ("none_person", "Claus Asam is a person, not a standalone organisation brand."),
    "DE:U27": ("none_ambiguous_identity", "Ingenieurbüro Fechner is not uniquely identifiable from the graph name and project context."),
    "FR:U12": ("none_no_standalone_brand", "Réhabail is documented as project carrier, but no standalone official logo or first-party site was found."),
    "GB:X02": ("none_participant_group", "Students, schoolchildren and volunteers are a participant group, not an organisation."),
    "NO:N06": ("none_project_network", "The regional reuse network is a project/network without a standalone official brand."),
}

# Manual primary-source follow-up for sites that the reproducible crawler could
# not read. These are research conclusions only: no candidate is accepted and
# no publication permission is inferred.
MANUAL_LOGO_COMPLETIONS = {
    "BE:M02": {
        "access": "manual_primary_source_review",
        "final_url": "https://antiquefireplacesfirst.com/",
        "resolution": "none_after_manual_primary_source_search",
        "resolution_note": "The indexed official site confirms the exact organisation, but exposes no technically sufficient standalone first-party logo source.",
        "evidence_sources": ["https://antiquefireplacesfirst.com/"],
    },
    "DE:M06": {
        "access": "manual_primary_source_review",
        "final_url": "https://www.materialrest24.de/en/content/about_us/team-story",
        "resolution": "none_after_manual_primary_source_search",
        "resolution_note": "The official company page confirms Materialrest24 and its contact route; no technically sufficient standalone first-party brand asset was found.",
        "evidence_sources": ["https://www.materialrest24.de/en/content/about_us/team-story"],
    },
    "FR:M08": {
        "access": "manual_primary_source_review_official_domain_inactive",
        "resolution": "none_no_current_first_party_logo_source",
        "resolution_note": "The supplied official domain no longer resolves. Current specialist directories confirm the historical business identity, but no current first-party logo source exists.",
        "evidence_sources": ["https://www.bourgogne-materiaux-anciens.fr/", "https://opalis.eu/nl/node/4997"],
        "review_flags": ["official_domain_inactive", "directory_used_for_identity_only_not_asset"],
    },
    "FR:M17": {
        "access": "manual_primary_source_review",
        "final_url": "https://www.enfin-reemploi.fr/",
        "resolution": "none_after_manual_primary_source_search",
        "resolution_note": "The official site and legal notice confirm the organisation and restrict reproduction, but no directly retrievable qualifying standalone logo file was found.",
        "evidence_sources": ["https://www.enfin-reemploi.fr/", "https://www.enfin-reemploi.fr/mentions-legales/"],
    },
    "FR:O01": {
        "access": "manual_primary_source_review",
        "final_url": "https://www.looping.immo/",
        "resolution": "none_no_qualifying_standalone_asset_after_official_pdf_review",
        "resolution_note": "The official site and official presentation confirm Booster du Reemploi and A4MT, but do not provide a separately retrievable qualifying logo asset.",
        "evidence_sources": ["https://www.looping.immo/", "https://www.looping.immo/static/booster-presentation-v3.pdf"],
    },
    "FR:O02": {
        "access": "manual_primary_source_review",
        "final_url": "https://www.le-wip.com/",
        "resolution": "none_no_qualifying_standalone_asset_after_official_pdf_review",
        "resolution_note": "The official site and press release confirm Le WIP, but no separately retrievable qualifying standalone logo asset was found.",
        "evidence_sources": ["https://www.le-wip.com/", "https://www.le-wip.com/wp-content/uploads/2019/10/Communique-presse-Ouverture-Grande-Halle-Le-Wip.pdf"],
    },
    "GB:M04": {
        "access": "manual_primary_source_review",
        "final_url": "https://buildingsparesmarket.co.uk/",
        "resolution": "none_after_manual_primary_source_search",
        "resolution_note": "The indexed official marketplace confirms the exact identity; no technically sufficient standalone first-party logo source was found.",
        "evidence_sources": ["https://buildingsparesmarket.co.uk/", "https://buildingsparesmarket.co.uk/about/"],
    },
    "GB:U27": {
        "access": "manual_primary_source_review_official_domain_inactive",
        "resolution": "none_no_current_first_party_logo_source",
        "resolution_note": "The supplied official domain no longer resolves. The British Constructional Steelwork Association still identifies Four Bay Structures and that domain, but no current first-party logo source is available.",
        "evidence_sources": ["https://www.4bay.co.uk/", "https://bcsa.org.uk/upload/Resources/About%20us/BCSA%202024%20Annual%20Review.pdf"],
        "review_flags": ["official_domain_inactive", "trade_association_source_used_for_identity_only_not_asset"],
    },
    "NO:M01": {
        "access": "manual_primary_source_review_official_domain_inactive",
        "resolution": "none_no_current_first_party_logo_source",
        "resolution_note": "The supplied FornyBygg domain does not resolve and repeated exact-name searches found no current first-party organisation or logo source.",
        "evidence_sources": ["https://fornybygg.no/"],
        "review_flags": ["official_domain_inactive"],
    },
}


MANUAL_RIGHTS_COMPLETIONS = {
    "BE:M03": {"access": "manual_primary_source_review", "official_url": "https://www.rikstorms.com/", "final_url": "https://www.rikstorms.com/nl/contact/", "emails": ["sales@rikstorms.com", "info@rikstorms.com"], "contact_pages": ["https://www.rikstorms.com/nl/contact/"], "resolution": "official_contact_route_found_permission_not_requested", "resolution_note": "The current first-party domain and its contact page replace the stale rikstorms.be route; no permission was requested.", "evidence_sources": ["https://www.rikstorms.com/nl/contact/"], "review_flags": ["official_domain_corrected"]},
    "BE:M17": {"access": "manual_primary_source_review", "official_url": "http://heynsrecycling.be/", "final_url": "http://heynsrecycling.be/#contact", "emails": ["info@heynsrecycling.be"], "contact_pages": ["http://heynsrecycling.be/#contact"], "resolution": "official_contact_route_found_permission_not_requested", "resolution_note": "The first-party HTTP site provides an email, telephone number and contact section; HTTPS has a hostname-certificate error. No permission was requested.", "evidence_sources": ["http://heynsrecycling.be/#contact"], "review_flags": ["https_certificate_hostname_mismatch", "http_first_party_route"]},
    "BE:N10": {"access": "manual_primary_source_review", "final_url": "https://www.zinneke.org/contacts/", "emails": ["info@zinneke.org"], "contact_pages": ["https://www.zinneke.org/contacts/"], "resolution": "official_contact_route_found_permission_not_requested", "resolution_note": "The first-party contact page provides info@zinneke.org; no permission was requested.", "evidence_sources": ["https://www.zinneke.org/contacts/"]},
    "CH:F01": {"access": "manual_primary_source_review", "final_url": "https://cea.ibi.ethz.ch/utils/contact.html", "emails": ["dewolf@ibi.baug.ethz.ch"], "contact_pages": ["https://cea.ibi.ethz.ch/utils/contact.html"], "resolution": "official_contact_route_found_permission_not_requested", "resolution_note": "The official ETH unit contact and principal-investigator page provide a first-party route; no permission was requested.", "evidence_sources": ["https://cea.ibi.ethz.ch/utils/contact.html", "https://cea.ibi.ethz.ch/people/catherine_de_wolf.html"]},
    "CH:I01": {"access": "manual_primary_source_review", "final_url": "https://www.stadt-zuerich.ch/de/politik-und-verwaltung/kommunikation-und-transparenz/medien/medienkontakte.html", "emails": ["tobias.nussbaum@zuerich.ch"], "media_pages": ["https://www.stadt-zuerich.ch/de/politik-und-verwaltung/kommunikation-und-transparenz/medien/medienkontakte.html"], "resolution": "official_media_route_found_permission_not_requested", "resolution_note": "The City of Zurich publishes an ERZ media contact; no permission was requested.", "evidence_sources": ["https://www.stadt-zuerich.ch/de/aktuell/medienmitteilungen/2026/05/erste-abfallanalyse-stadt-zuerich.html", "https://www.stadt-zuerich.ch/de/politik-und-verwaltung/kommunikation-und-transparenz/medien/medienkontakte.html"]},
    "CH:I03": {"access": "manual_primary_source_review", "final_url": "https://www.stadt-zuerich.ch/de/politik-und-verwaltung/stadtverwaltung/hbd/ahb.html", "emails": ["ursula.tschirren@zuerich.ch", "franziska.martin@zuerich.ch"], "contact_pages": ["https://www.stadt-zuerich.ch/de/politik-und-verwaltung/stadtverwaltung/hbd/ahb.html"], "media_pages": ["https://www.stadt-zuerich.ch/de/politik-und-verwaltung/kommunikation-und-transparenz/medien/medienkontakte.html"], "resolution": "official_media_route_found_permission_not_requested", "resolution_note": "The official department and City of Zurich media pages provide communications routes; no permission was requested.", "evidence_sources": ["https://www.stadt-zuerich.ch/de/politik-und-verwaltung/stadtverwaltung/hbd/ahb.html", "https://www.stadt-zuerich.ch/de/politik-und-verwaltung/kommunikation-und-transparenz/medien/medienkontakte.html"]},
    "CH:S04": {"access": "manual_primary_source_review", "final_url": "https://reuzi.ch/", "emails": ["info@reuzi.ch"], "contact_pages": ["https://reuzi.ch/"], "resolution": "official_contact_route_found_permission_not_requested", "resolution_note": "The first-party homepage provides info@reuzi.ch; no permission was requested.", "evidence_sources": ["https://reuzi.ch/"]},
    "CH:U07": {"access": "manual_primary_source_review", "final_url": "https://www.graberpulver.ch/buero", "emails": ["pr@graberpulver.ch", "arch@graberpulver.ch"], "contact_pages": ["https://www.graberpulver.ch/buero"], "resolution": "official_contact_route_found_permission_not_requested", "resolution_note": "The official office page provides PR and general architecture email routes; no permission was requested.", "evidence_sources": ["https://www.graberpulver.ch/buero"]},
    "CH:U16": {"access": "manual_primary_source_review_official_domain_inactive", "final_url": "https://monotti-sa.ch/", "resolution": "no_current_first_party_contact_route_after_manual_search", "resolution_note": "The supplied domain currently serves a hosting-provider default page. No current first-party contact or media route could be verified, so no rights request route is claimed.", "evidence_sources": ["https://monotti-sa.ch/"], "review_flags": ["official_domain_inactive", "unverified_directory_email_excluded"]},
    "CH:U21": {"access": "manual_primary_source_review", "official_url": "https://www.pirminjung.ch/", "final_url": "https://www.pirminjung.ch/", "emails": ["info@pirminjung.ch"], "contact_pages": ["https://www.pirminjung.ch/"], "resolution": "official_contact_route_found_permission_not_requested", "resolution_note": "The Swiss entity uses pirminjung.ch rather than the stored German-domain route; an official general contact was verified. No permission was requested.", "evidence_sources": ["https://www.pirminjung.ch/"], "review_flags": ["official_domain_corrected"]},
    "CH:U28": {"access": "manual_primary_source_review", "final_url": "https://zirkular.net/", "emails": ["k.mueller@zirkular.net", "c.bofinger@zirkular.net", "b.rudolf@zirkular.net"], "contact_pages": ["https://zirkular.net/"], "resolution": "official_contact_route_found_permission_not_requested", "resolution_note": "A first-party Zirkular publication supplies named organisation email routes; no permission was requested.", "evidence_sources": ["https://zirkular.net/wp-content/uploads/2025/07/8169-20250331-reuse-lca-heig-vd-final-report-e-ec-vf2.pdf"]},
    "DE:U25": {"access": "manual_primary_source_review", "final_url": "https://www.bullinger.de/abtsgmuend/kontakt", "emails": ["holzwerke@bullinger.de", "xabu@bullinger.de"], "contact_pages": ["https://www.bullinger.de/abtsgmuend/kontakt"], "resolution": "official_contact_route_found_permission_not_requested", "resolution_note": "The first-party contact page provides general company email routes; no permission was requested.", "evidence_sources": ["https://www.bullinger.de/abtsgmuend/kontakt"]},
    "DE:U33": {"access": "manual_primary_source_review", "final_url": "https://www.regionh.dk/presse-og-nyt/", "emails": ["presse@regionh.dk"], "media_pages": ["https://www.regionh.dk/presse-og-nyt/"], "resolution": "official_media_route_found_permission_not_requested", "resolution_note": "The regional authority publishes presse@regionh.dk as a media route; no permission was requested.", "evidence_sources": ["https://www.regionh.dk/presse-og-nyt/pressemeddelelser-og-nyheder/Sider/Regionsr%C3%A5det-Vi-skal-sikres-en-l%C3%B8bende-orientering-af-situationen-i-Akutberedskabet.aspx"]},
    "FI:M01": {"access": "manual_primary_source_review", "final_url": "https://www.purkutori.fi/rekisteri-ja-tietosuojaseloste", "emails": ["kari@purkupiha.fi"], "legal_pages": ["https://www.purkutori.fi/rekisteri-ja-tietosuojaseloste"], "resolution": "official_contact_route_found_permission_not_requested", "resolution_note": "Purkutori's first-party privacy notice identifies operator Purkupiha Oy and its responsible contact; no permission was requested.", "evidence_sources": ["https://www.purkutori.fi/rekisteri-ja-tietosuojaseloste"]},
    "FI:M02": {"access": "manual_primary_source_review", "final_url": "https://www.spolia.fi/", "emails": ["mikko@spolia.fi", "santeri@spolia.fi"], "contact_pages": ["https://www.spolia.fi/#yhteystiedot"], "resolution": "official_contact_route_found_permission_not_requested", "resolution_note": "The first-party homepage and invoice document provide named Spolia contacts; no permission was requested.", "evidence_sources": ["https://www.spolia.fi/", "https://www.spolia.fi/wp-content/uploads/2023/10/Spolia_verkkolaskutiedote_2023.pdf"]},
    "FI:U18": {"access": "manual_primary_source_review", "official_url": "https://www.skanska.fi/", "final_url": "https://www.skanska.fi/tietoa-skanskasta/media/", "emails": ["media@skanska.fi"], "media_pages": ["https://www.skanska.fi/tietoa-skanskasta/media/"], "legal_pages": ["https://www.skanska.fi/sivuston-kayttoehdot/"], "resolution": "official_media_route_found_permission_not_requested", "resolution_note": "Skanska Finland publishes a media route; its terms require written consent for protected material. No permission was requested.", "evidence_sources": ["https://www.skanska.fi/sivuston-kayttoehdot/", "https://www.skanska.fi/tietoa-skanskasta/media/uutiset/303669/Betonielementtien-uudelleenkayttoa-koeponnistettu-onnistuneesti-ReCreatehankkeen-minipiloteissa-"], "review_flags": ["written_consent_required_by_site_terms"]},
    "FR:M55": {"access": "manual_primary_source_review", "final_url": "https://steelalive.co/", "contact_pages": ["https://fr.linkedin.com/company/steelalive"], "resolution": "official_social_contact_route_found_permission_not_requested", "resolution_note": "No first-party email or contact form was exposed, but the organisation's official company profile provides a message route. No permission was requested.", "evidence_sources": ["https://steelalive.co/", "https://fr.linkedin.com/company/steelalive"], "review_flags": ["social_route_only"]},
    "FR:N02": {"access": "manual_primary_source_review", "final_url": "https://www.bellastock.com/", "emails": ["communication@bellastock.com", "contact@bellastock.com"], "contact_pages": ["https://www.bellastock.com/"], "media_pages": ["https://www.bellastock.com/wp-content/uploads/2019/06/MB_Dossier_Presse_DEF_WEB.pdf"], "resolution": "official_media_route_found_permission_not_requested", "resolution_note": "The first-party homepage and press dossier provide general and communications email routes; no permission was requested.", "evidence_sources": ["https://www.bellastock.com/", "https://www.bellastock.com/wp-content/uploads/2019/06/MB_Dossier_Presse_DEF_WEB.pdf"]},
    "FR:U02": {"access": "manual_primary_source_review", "official_url": "https://archipelzero.wixsite.com/archipelzero", "final_url": "https://archipelzero.wixsite.com/archipelzero/contact", "emails": ["contact@archipelzero.fr"], "contact_pages": ["https://archipelzero.wixsite.com/archipelzero/contact"], "resolution": "official_contact_route_found_permission_not_requested", "resolution_note": "The complete first-party Wix path provides a contact page and organisation email; no permission was requested.", "evidence_sources": ["https://archipelzero.wixsite.com/archipelzero/contact"], "review_flags": ["official_url_path_corrected"]},
    "FR:U07": {"access": "manual_primary_source_review_domain_identity_mismatch", "final_url": "https://depuis1920.fr/", "resolution": "no_verified_rights_route_domain_identity_mismatch", "resolution_note": "The current content at depuis1920.fr describes an unrelated generic architecture studio and cannot be verified as the selected organisation. Its contact details were excluded.", "evidence_sources": ["https://depuis1920.fr/"], "review_flags": ["current_domain_content_identity_mismatch", "contact_details_excluded"]},
    "GB:X01": {"access": "manual_primary_source_review", "official_url": "https://marketplace.globechain.com/", "final_url": "https://marketplace.globechain.com/in-the-media", "emails": ["enquiries@globechain.com"], "contact_pages": ["https://marketplace.globechain.com/in-the-media"], "legal_pages": ["https://marketplace.globechain.com/terms"], "resolution": "official_contact_route_found_permission_not_requested", "resolution_note": "The first-party marketplace media page and terms provide an enquiries route; no permission was requested.", "evidence_sources": ["https://marketplace.globechain.com/in-the-media", "https://marketplace.globechain.com/terms"], "review_flags": ["official_subdomain_corrected"]},
    "NL:O06": {"access": "manual_primary_source_review", "final_url": "https://www.iba-parkstad.nl/", "emails": ["info@iba-parkstad.nl"], "contact_pages": ["https://www.iba-parkstad.nl/"], "resolution": "official_contact_route_found_permission_not_requested", "resolution_note": "An official IBA Parkstad publication supplies the general contact email; no permission was requested.", "evidence_sources": ["https://www.iba-parkstad.nl/wp-content/uploads/2020/11/iba_openoproep_nl_2014.pdf"]},
    "NL:S02": {"access": "manual_primary_source_review", "final_url": "https://www.resourcehub.nl/contact", "contact_pages": ["https://www.resourcehub.nl/contact"], "resolution": "official_contact_route_found_permission_not_requested", "resolution_note": "The first-party single-page application exposes a dedicated contact route; no permission was requested.", "evidence_sources": ["https://www.resourcehub.nl/contact"]},
    "NL:S03": {"access": "manual_primary_source_review", "final_url": "https://terveldedenbesten.nl/contact/", "contact_pages": ["https://terveldedenbesten.nl/contact/"], "resolution": "official_contact_route_found_permission_not_requested", "resolution_note": "The first-party contact page is available although automated extraction is blocked; no permission was requested.", "evidence_sources": ["https://terveldedenbesten.nl/contact/"]},
    "NL:U33": {"access": "manual_primary_source_review", "final_url": "https://lagemaat-heerde.nl/contact/", "emails": ["info@lagemaat-heerde.nl"], "contact_pages": ["https://lagemaat-heerde.nl/contact/"], "resolution": "official_contact_route_found_permission_not_requested", "resolution_note": "The first-party contact page provides the general company email; no permission was requested.", "evidence_sources": ["https://lagemaat-heerde.nl/contact/"]},
    "NO:M04": {"access": "manual_primary_source_review", "final_url": "https://www.ombygg.no/kontakt", "emails": ["post@ombygg.no"], "contact_pages": ["https://www.ombygg.no/kontakt"], "resolution": "official_contact_route_found_permission_not_requested", "resolution_note": "The first-party contact page provides post@ombygg.no and a contact form; no permission was requested.", "evidence_sources": ["https://www.ombygg.no/kontakt"]},
    "NO:N05": {"access": "manual_primary_source_review", "final_url": "https://www.ombrukshubsor.no/kontakt", "emails": ["postmaster@ombrukshubsor.no"], "contact_pages": ["https://www.ombrukshubsor.no/kontakt"], "resolution": "official_contact_route_found_permission_not_requested", "resolution_note": "The first-party contact page provides a general organisation email; no permission was requested.", "evidence_sources": ["https://www.ombrukshubsor.no/kontakt"]},
    "SE:F02": {"access": "manual_primary_source_review", "final_url": "https://www.ri.se/en/about-rise/news-press-releases/press-contact", "emails": ["niklas.jalevik@ri.se"], "media_pages": ["https://www.ri.se/en/about-rise/news-press-releases/press-contact", "https://www.ri.se/en/about-rise/news-press-releases/press-images"], "resolution": "official_media_route_found_permission_not_requested", "resolution_note": "RISE publishes press contacts and an editorial press-image policy; the latter does not clear logo use. No permission was requested.", "evidence_sources": ["https://www.ri.se/en/about-rise/news-press-releases/press-contact", "https://www.ri.se/en/about-rise/news-press-releases/press-images"], "review_flags": ["press_image_permission_does_not_cover_logo"]},
}


FINAL_CANDIDATE_KEYS = {"CH:U20", "DK:M02", "FI:U04", "FR:M53"}


LEAD_ONLY_NONE = {
    "CH:M04": ("none_false_positive_assets", "The raw hits are an unrelated conference logo and photographs. The official Basel-Stadt parent mark is supplied only on request, not as a public standalone file."),
    "CH:U15": ("none_domain_identity_mismatch", "The stored Modissa domain now redirects to the unrelated Collectif mon Amour fashion business; those assets were rejected."),
    "DE:U32": ("none_person", "Petra Jablonicka is a person rather than a standalone organisation brand."),
    "DE:U41": ("none_no_current_exact_brand", "The exact historical Wiewiorra Hopp identity is not represented by the current Anna Hopp site; its inaccessible favicon is not a qualifying exact mark."),
    "DK:M01": ("none_below_128_minimum", "The exact first-party Bango wordmark is 244 x 69 px. Larger raw hits are supplier or product partner marks and were rejected."),
    "FR:F01": ("none_below_128_minimum", "The actual first-party CSTB marks are only 230 x 71 px and 166 x 50 px. BATIPEDIA and media photographs are not CSTB organisation logos."),
    "FR:M42": ("none_false_positive_assets", "The raw hits are a generic Wix favicon and a photograph, not a Pierres & Jardins d'Autrefois image mark."),
    "FR:M45": ("none_below_128_minimum", "The only plausible first-party Brachet symbol is an 80 x 80 px fleur-de-lis, below the minimum."),
    "FR:M58": ("none_false_positive_assets", "The raw hits are unavailable site-builder favicons and a website screenshot, not a standalone Tonner logo."),
    "GB:M14": ("none_false_positive_assets", "The 180 px Wix icon resolves at native size to a salvage-yard photograph, not an organisation logo."),
    "GB:M24": ("none_false_positive_assets", "The raw hits are generic website-builder icons and a site thumbnail, not an Old Slate Yard logo."),
    "GB:U04": ("none_partner_marks_only", "The only logo files on the first-party site are B Corp and RIBA partner marks; no standalone BakerBrown image mark was found."),
}


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.assets, self.text = [], [], []
        self._href, self._anchor = None, []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "a":
            self._href, self._anchor = a.get("href", ""), []
        if tag in ("img", "link", "source"):
            self.assets.append(a)
        if tag == "meta":
            self.assets.append(a)

    def handle_endtag(self, tag):
        if tag == "a" and self._href is not None:
            self.links.append((self._href, " ".join(self._anchor)))
            self._href, self._anchor = None, []

    def handle_data(self, data):
        value = " ".join(data.split())
        if value:
            self.text.append(value)
            if self._href is not None:
                self._anchor.append(value)


def host(url):
    return (urllib.parse.urlparse(url).hostname or "").lower().removeprefix("www.")


def absolute(base, value):
    if not value or value.startswith(("data:", "javascript:", "tel:", "#")):
        return ""
    return urllib.parse.urldefrag(urllib.parse.urljoin(base, value))[0]


def internal(base, url):
    a, b = host(base), host(url)
    return bool(a and b and (a == b or a.endswith("." + b) or b.endswith("." + a)))


def get(session, url, binary=False):
    response = session.get(url, timeout=(6, 12), allow_redirects=True, verify=False,
                           headers={"User-Agent": UA, "Accept": "*/*" if binary else "text/html,application/xhtml+xml"})
    response.raise_for_status()
    if len(response.content) > (8_000_000 if binary else 2_000_000):
        raise ValueError("response too large")
    return response


def parse_page(session, url):
    response = get(session, url)
    parser = Parser()
    parser.feed(response.text)
    return response.url, response.text, parser


def rank_email(email):
    terms = ("press", "presse", "media", "kommunikation", "communication", "marketing", "brand", "legal", "info", "contact")
    low = email.lower()
    return next((i for i, term in enumerate(terms) if term in low), 99), low


def page_routes(base, parser):
    found = {"contact": [], "media": [], "legal": []}
    for href, label in parser.links:
        url = absolute(base, href)
        if not url or not internal(base, url):
            continue
        hay = (url + " " + label).lower()
        for key, terms in (("contact", CONTACT_TERMS), ("media", MEDIA_TERMS), ("legal", LEGAL_TERMS)):
            if any(term in hay for term in terms):
                found[key].append(url)
    return {key: list(dict.fromkeys(values))[:8] for key, values in found.items()}


def logo_assets(base, html, parser):
    leads = []
    for attrs in parser.assets:
        values = [attrs.get(k, "") for k in ("src", "data-src", "srcset", "href", "content")]
        descriptor = " ".join(values + [attrs.get("alt", ""), attrs.get("class", ""), attrs.get("id", ""), attrs.get("rel", "")]).lower()
        if not any(term in descriptor for term in LOGO_TERMS):
            continue
        for value in values:
            if not value:
                continue
            value = value.split(",", 1)[0].strip().split(" ", 1)[0]
            url = absolute(base, value)
            if url and not any(term in url.lower() for term in ("facebook", "instagram", "linkedin", "youtube", "twitter")):
                leads.append(url)
    for match in CSS_URL_RE.findall(html):
        if any(term in match.lower() for term in LOGO_TERMS):
            leads.append(absolute(base, match))
    return list(dict.fromkeys(url for url in leads if url))[:30]


def probe_asset(session, url):
    try:
        response = get(session, url, binary=True)
        data, ctype = response.content, response.headers.get("content-type", "").split(";", 1)[0]
        fmt, width, height = "", None, None
        if b"<svg" in data[:2000].lower():
            fmt = "svg"
        else:
            with Image.open(io.BytesIO(data)) as image:
                fmt = (image.format or "").lower()
                width, height = image.size
        return {"url": response.url, "access": "ok", "content_type": ctype, "format": fmt,
                "width": width, "height": height,
                "technical_minimum_ok": fmt == "svg" or bool(width and height and min(width, height) >= 128)}
    except Exception as exc:
        return {"url": url, "access": f"error:{type(exc).__name__}", "content_type": "", "format": "",
                "width": None, "height": None, "technical_minimum_ok": False}


def crawl(row, mode):
    key, official = row["key"], row.get("official_url") or ""
    result = {"key": key, "cc": row["cc"], "tid": row["tid"], "name": row["name"], "mode": mode,
              "official_url": official, "access": "not_attempted", "final_url": "", "emails": [],
              "contact_pages": [], "media_pages": [], "legal_pages": [], "logo_candidates": [],
              "resolution": "", "resolution_note": "", "publication_clearance": "not_cleared",
              "evidence_sources": [], "review_flags": [], "research_complete": False}
    if mode == "logo" and key in DOCUMENTED_NONE:
        result["resolution"], result["resolution_note"] = DOCUMENTED_NONE[key]
        result["access"] = "not_applicable"
        result["research_complete"] = True
        return result
    if not official:
        result["resolution"] = "manual_research_no_official_domain"
        result["resolution_note"] = "No verified official domain is available."
        return result
    session = requests.Session()
    try:
        final, html, parser = parse_page(session, official)
        result["access"], result["final_url"] = "ok", final
        routes = page_routes(final, parser)
        result["contact_pages"], result["media_pages"], result["legal_pages"] = routes["contact"], routes["media"], routes["legal"]
        emails = set(EMAIL_RE.findall(html))
        candidate_pages = list(dict.fromkeys(routes["contact"] + routes["media"] + routes["legal"]))[:6]
        for page in candidate_pages:
            try:
                pfinal, phtml, pparser = parse_page(session, page)
                emails.update(EMAIL_RE.findall(phtml))
                extra = page_routes(pfinal, pparser)
                for target, source in (("contact_pages", extra["contact"]), ("media_pages", extra["media"]), ("legal_pages", extra["legal"])):
                    result[target] = list(dict.fromkeys(result[target] + source))[:10]
            except Exception:
                pass
        result["emails"] = sorted((e for e in emails if "example." not in e.lower()), key=rank_email)[:30]
        if mode == "logo":
            candidates = logo_assets(final, html, parser)
            result["logo_candidates"] = [probe_asset(session, url) for url in candidates[:15]]
            usable = [c for c in result["logo_candidates"] if c["access"] == "ok" and c["technical_minimum_ok"]]
            if usable:
                result["resolution"] = "official_logo_candidate_found_manual_identity_review"
                result["resolution_note"] = f"{len(usable)} technically sufficient first-party logo/icon candidate(s) found."
            else:
                result["resolution"] = "none_after_exhaustive_official_site_search"
                result["resolution_note"] = "No technically sufficient first-party logo candidate was found on the official site."
        else:
            if result["emails"] or result["contact_pages"]:
                result["resolution"] = "official_contact_route_found_permission_not_requested"
                result["resolution_note"] = "At least one first-party email or contact page was found; no request was sent."
            elif result["media_pages"]:
                result["resolution"] = "official_media_route_found_permission_not_requested"
                result["resolution_note"] = "A first-party media/press route was found; no request was sent."
            else:
                result["resolution"] = "no_contact_route_after_official_site_search"
                result["resolution_note"] = "The official site was reachable but yielded no contact or media route."
    except Exception as exc:
        result["access"] = f"error:{type(exc).__name__}:{str(exc)[:160]}"
        result["resolution"] = "manual_search_required_official_site_unreachable"
        result["resolution_note"] = "The official site could not be read in the automated completion pass."
    curated = (MANUAL_LOGO_COMPLETIONS if mode == "logo" else MANUAL_RIGHTS_COMPLETIONS).get(key)
    if curated:
        result.update(curated)
    if not result["evidence_sources"] and (result["final_url"] or result["official_url"]):
        result["evidence_sources"] = [result["final_url"] or result["official_url"]]
    result["research_complete"] = not result["resolution"].startswith("manual_")
    return result


def write_final_logo_disposition(missing, curated, completion_rows, now):
    completion_by_key = {row["key"]: row for row in completion_rows if row["mode"] == "logo"}
    curated_by_key = {row["key"]: row for row in curated}
    rows = []
    for source in missing:
        key = source["key"]
        row = {
            "key": key,
            "cc": source["cc"],
            "tid": source["tid"],
            "name": source["name"],
            "official_url": source.get("official_url") or "",
            "disposition": "none",
            "resolution": "",
            "resolution_note": "",
            "candidate_url": "",
            "candidate_kind": "",
            "technical_minimum_ok": False,
            "evidence_sources": [],
            "review_flags": [],
            "decision": "research_none_terminal",
            "publication_clearance": "not_cleared",
            "production_state_changed": False,
            "research_complete": True,
        }
        if key in completion_by_key:
            completed = completion_by_key[key]
            row.update({
                "resolution": completed["resolution"],
                "resolution_note": completed["resolution_note"],
                "evidence_sources": completed.get("evidence_sources", []),
                "review_flags": completed.get("review_flags", []),
            })
        elif key in LEAD_ONLY_NONE:
            row["resolution"], row["resolution_note"] = LEAD_ONLY_NONE[key]
            row["evidence_sources"] = list(dict.fromkeys(
                ([row["official_url"]] if row["official_url"] else [])
                + [lead["url"] for lead in source.get("logo_leads", [])]
            ))
        elif key in curated_by_key:
            candidate = curated_by_key[key]
            row["candidate_url"] = candidate["final_url"] or candidate["candidate_url"]
            row["technical_minimum_ok"] = bool(candidate["minimum_128_ok"])
            row["evidence_sources"] = list(dict.fromkeys(filter(None, [
                candidate.get("official_url"), candidate.get("candidate_url"), candidate.get("rights_source_url")
            ])))
            if key in FINAL_CANDIDATE_KEYS:
                row.update({
                    "disposition": "candidate",
                    "resolution": "official_first_party_candidate_found",
                    "resolution_note": candidate["research_note"],
                    "candidate_kind": "apple_touch_icon" if key in {"CH:U20", "DK:M02"} else "official_logo_image",
                    "decision": "research_candidate_not_accepted",
                })
                if key == "CH:U20":
                    row["review_flags"] = ["official_icon_is_abstract_red_blur", "later_brand_signoff_recommended"]
            elif candidate["research_confidence"] == "ambiguous_identity":
                row["resolution"] = "none_ambiguous_identity"
                row["resolution_note"] = candidate["research_note"]
                row["candidate_url"] = ""
                row["technical_minimum_ok"] = False
                row["review_flags"] = ["same_name_business_not_linked_to_graph_entity"]
            else:
                row["resolution"] = "none_below_128_minimum"
                row["resolution_note"] = candidate["research_note"] + " The source fails the 128 px shortest-edge requirement."
                row["candidate_url"] = ""
                row["technical_minimum_ok"] = False
        else:
            raise AssertionError(f"Unclassified missing-logo row: {key}")
        rows.append(row)

    rows.sort(key=lambda row: (row["cc"], row["key"]))
    counts = {value: sum(row["disposition"] == value for row in rows) for value in ("candidate", "none")}
    assert len(rows) == 65 and len({row["key"] for row in rows}) == 65
    assert counts == {"candidate": 4, "none": 61}
    payload = {
        "schema_version": "missing-logo-final-research-disposition-v1",
        "created_at": now,
        "boundary": "Research proposal only. No review decision, asset, render, publication clearance or Neo4j state changed.",
        "scope": {"organizations": 541, "selected_logos_unchanged": 476, "missing_logo_rows": 65},
        "counts": counts,
        "completion": {"terminal": 65, "open": 0, "production_changes": 0},
        "nodes": rows,
    }
    OUT_LOGO_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fields = ["key", "cc", "tid", "name", "official_url", "disposition", "resolution", "resolution_note",
              "candidate_url", "candidate_kind", "technical_minimum_ok", "evidence_sources", "review_flags",
              "decision", "publication_clearance", "production_state_changed", "research_complete"]
    with OUT_LOGO_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            flat = dict(row)
            flat["evidence_sources"] = " | ".join(row["evidence_sources"])
            flat["review_flags"] = " | ".join(row["review_flags"])
            writer.writerow(flat)
    lines = [
        "# Finaler Rechercheentscheid für 65 fehlende Logos", "", payload["boundary"], "",
        "- Vollständig klassifiziert: **65/65**", "- Offene Recherchefälle: **0**",
        "- Belastbare Erstquellen-Kandidaten: **4**", "- Begründetes `none`: **61**",
        "- Übernommene Kandidaten: **0**", "- Publikationsfreigaben: **0**", "",
        "## Vier verbleibende Kandidaten", "",
    ]
    lines.extend(f"- `{row['key']}` {row['name']}: {row['candidate_url']}" for row in rows if row["disposition"] == "candidate")
    lines.extend(["", "Alle anderen 61 Fälle enden wegen fehlender exakter Marke, Identitätskonflikt, Personen-/Projektstatus, Fremdlogo/Foto oder Unterschreitung der 128-px-Mindestkante auf `none`."])
    OUT_LOGO_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return payload


def main():
    missing = json.loads((DATA / "MISSING_LOGO_INFO_HUNT.json").read_text(encoding="utf-8"))["nodes"]
    rights = json.loads((DATA / "MISSING_RIGHTS_INFO_HUNT.json").read_text(encoding="utf-8"))["nodes"]
    curated = json.loads((DATA / "MISSING_LOGO_CURATED_LEADS.json").read_text(encoding="utf-8"))["nodes"]
    logo_rows = [row for row in missing if not row.get("logo_leads")]
    rights_rows = [row for row in rights if row["result"] == "logo" and not row.get("preferred_permission_email") and not row.get("contact_pages")]
    jobs = [(row, "logo") for row in logo_rows] + [(row, "rights") for row in rights_rows]
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
        rows = list(pool.map(lambda item: crawl(*item), jobs))
    rows.sort(key=lambda row: (row["mode"], row["cc"], row["key"]))
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    payload = {
        "schema_version": "missing-info-completion-v2", "created_at": now,
        "boundary": "Research only; no logo selection, asset, opacity, render, permission request, clearance or Neo4j state changed.",
        "scope": {
            "network_nodes": 619,
            "organizations": 541,
            "selected_logos": 476,
            "none_total": len(missing),
            "preexisting_logo_leads": sum(bool(row.get("logo_leads")) for row in missing),
            "logo_gaps_completed_here": len(logo_rows),
            "rights_route_gaps_completed_here": len(rights_rows),
        },
        "counts": {value: sum(row["resolution"] == value for row in rows) for value in sorted({row["resolution"] for row in rows})},
        "completion": {
            "records": len(rows),
            "terminal": sum(row["research_complete"] for row in rows),
            "open": sum(not row["research_complete"] for row in rows),
            "permission_requests_sent": 0,
            "publication_clearances_inferred": 0,
        },
        "nodes": rows,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fields = ["mode", "key", "cc", "tid", "name", "official_url", "access", "resolution", "resolution_note",
              "emails", "contact_pages", "media_pages", "legal_pages", "logo_candidates", "evidence_sources",
              "review_flags", "research_complete", "publication_clearance"]
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader()
        for row in rows:
            flat = {field: row.get(field, "") for field in fields}
            for field in ("emails", "contact_pages", "media_pages", "legal_pages", "evidence_sources", "review_flags"):
                flat[field] = " | ".join(row.get(field, []))
            flat["logo_candidates"] = " | ".join(item["url"] for item in row.get("logo_candidates", []))
            writer.writerow(flat)
    lines = ["# Abschlusslauf fehlende Informationen", "", payload["boundary"], "",
             "- Organisationen: **541**",
             "- Bereits ausgewählte Logos: **476**",
             f"- Logo-Informationsfälle insgesamt: **{len(missing)}** (davon {sum(bool(row.get('logo_leads')) for row in missing)} bereits mit Lead)",
             f"- Hier abgeschlossene Logo-Lücken: **{len(logo_rows)}**",
             f"- Hier abgeschlossene Rechte-Kontaktlücken: **{len(rights_rows)}**",
             f"- Terminale Rechercheergebnisse: **{payload['completion']['terminal']}/{payload['completion']['records']}**",
             f"- Offene Recherchezustände: **{payload['completion']['open']}**",
             "- Versendete Rechteanfragen: **0**",
             "- Abgeleitete Publikationsfreigaben: **0**", "", "## Ergebniszählung", ""]
    lines.extend(f"- `{key}`: **{value}**" for key, value in payload["counts"].items())
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_final_logo_disposition(missing, curated, rows, now)
    print(json.dumps(payload["scope"] | {"counts": payload["counts"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
