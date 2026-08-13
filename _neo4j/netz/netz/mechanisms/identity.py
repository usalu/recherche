"""Identity assignment: the unified `tid` (Typ-letter + per-country per-type
running number) that is BOTH the label burned into every graph circle and the
table's primary key. Verbatim port of netplate.Model's stage 4 (NUMBER).

Also assigns the internal-only `num` (plain per-country running int, used
solely for deterministic layout tie-breaking -- never shown to the reader).
"""
import collections
from ..data._identity import TYPE_LETTER


def assign_num(raw, panels: dict) -> dict:
    """Internal tie-break numbers only -- not the public id."""
    num = {}
    for c, pan in panels.items():
        for i, e in enumerate(sorted(pan.actors, key=lambda x: raw.name(x).lower()), start=1):
            num[e] = i
        for i, e in enumerate(sorted(pan.projects, key=lambda x: raw.name(x).lower()), start=1):
            num[e] = i
    return num


def assign_ids(raw, panels: dict, cc: dict, is_person) -> dict:
    """The public id: `tid[eid] -> "M07" | "U46" | "P3" | "E12"`. Actors sorted
    by name within (country, typ); projects "P%d"; persons (excluded from
    every panel's actors, but still resolved to a country in `cc`) get their
    own per-country sequence under the Person letter."""
    tid = {}
    for c, pan in panels.items():
        by_typ = collections.defaultdict(list)
        for e in pan.actors:
            by_typ[raw.types.get(e, "Unbekannt")].append(e)
        for typ, es in by_typ.items():
            letter = TYPE_LETTER.get(typ, "X")
            for i, e in enumerate(sorted(es, key=lambda x: raw.name(x).lower()), start=1):
                tid[e] = "%s%02d" % (letter, i)
        for i, e in enumerate(sorted(pan.projects, key=lambda x: raw.name(x).lower()), start=1):
            tid[e] = "P%d" % i

    by_cc_person = collections.defaultdict(list)
    for a in raw.actors:
        e = a["eid"]
        if is_person(raw, e) and cc.get(e) in panels:
            by_cc_person[cc[e]].append(e)
    letter = TYPE_LETTER["Person"]
    for c, es in by_cc_person.items():
        for i, e in enumerate(sorted(es, key=lambda x: raw.name(x).lower()), start=1):
            tid[e] = "%s%02d" % (letter, i)
    return tid
