"""Display vocabulary: German names/labels shown to a human reader. Distinct
from netz.data._identity (which holds the SAME-shaped tables but for
interpreting data, e.g. resolving an overlay's cc="BE" to the country the
raw export calls it by) -- this module is presentation only.
"""
from ...data._identity import ISO, ROLE_DE
from ._rolegroups import ROLE_GROUP, GROUP_LABEL, ROLE_GROUPS  # noqa: F401

CC_NAME = {v: k for k, v in ISO.items()}   # ISO2 -> German country name

ROLE_SHORT = {k: v.split("/")[0][:14] for k, v in ROLE_DE.items()}

TYP_ORDER = ["Unternehmen", "Materialhub_Bauteilboerse", "Forschung_Lehre",
             "NGO_Verband_Netzwerk", "Oeffentliche_Institution", "Software_Tool_Anbieter",
             "Organisation", "Foerdergeber_Programmtraeger", "Unbekannt"]
TYP_NAME_DE = {
    "Unternehmen": "Unternehmen", "Materialhub_Bauteilboerse": "Materialhub / Bauteilbörse",
    "Forschung_Lehre": "Forschung / Lehre", "NGO_Verband_Netzwerk": "NGO / Verband / Netzwerk",
    "Oeffentliche_Institution": "Öffentliche Institution", "Software_Tool_Anbieter": "Software / Tool-Anbieter",
    "Organisation": "Organisation", "Foerdergeber_Programmtraeger": "Förderträger", "Unbekannt": "Unbekannt"}
