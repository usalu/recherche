"""Diff snapshot vs live for the 23 Materialdepot IDs (pass-2 verifier 4)."""
import json
from collections import defaultdict, Counter

IDS = [
    'bw_crclr_kindl_hall',
    'bw_chiro_itterbeek_reuse_supply_network',
    'bw_berlin_fitout_donor_sources',
    'bw_paris_regional_donor_sources_ferme_du_rail',
    'bw_paris_material_sources_circular_pavilion',
    'bw_p2_massenwohnungsbau_donor_unknown',
    'bw_unknown_demolition_wood_streams',
    'bw_holbein_grosvenor_donor_projects',
    'bw_maison_des_canaux_unspecified_donors',
    'bw_verbiest_lagerhaus_zu_haus_und_atelier',
    'bw_rotor_reuse_stock_charles_malis',
    'bw_messebau_lager_hannover',
    'bw_maison_dna_unknown_brick_donor',
    'bw_externe_stahl_donor_stockholder',
    'bw_unknown_brick_donor_sources_gjg',
    'bw_lo_reninge_reuse_brick_source',
    'bw_unbekanntes_transformationsgebaeude_kellerwaende',
    'bw_unbekannte_donor_buildings_zinneke_material_lots',
    'bw_cleveland_steel_and_tubes_stock',
    'bw_wbs70_donor_groeditz',
    'bw_bellastock_ville_des_terres_l_ile_saint_denis_lager',
    'bw_donor_gebaudegruppe_resource_rows_mauerwerk',
    'bw_elys_ehemaliges_getraenkelager_areal',
]

iid_to_bid, bid_to_iid, iid_to_labels = {}, {}, {}
NODES = r'E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\snapshot\nodes.jsonl'
RELS = r'E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\snapshot\relationships.jsonl'

with open(NODES, encoding='utf-8') as f:
    for line in f:
        n = json.loads(line)
        iid = n['neo4j_internal_id']
        bid = (n.get('properties') or {}).get('id')
        iid_to_bid[iid] = bid
        iid_to_labels[iid] = n.get('labels', [])
        if bid:
            bid_to_iid[bid] = iid

target_iids = {b: bid_to_iid[b] for b in IDS}
target_iid_to_bid = {v: k for k, v in target_iids.items()}

snap = defaultdict(Counter)
with open(RELS, encoding='utf-8') as f:
    for line in f:
        r = json.loads(line)
        s = r['start_node_internal_id']
        e = r['end_node_internal_id']
        t = r['type']
        if s in target_iid_to_bid:
            bid = target_iid_to_bid[s]
            ol = (iid_to_labels.get(e) or ['?'])[0]
            other_bid = iid_to_bid.get(e, '?')
            snap[bid][('out', t, ol, other_bid)] += 1
        if e in target_iid_to_bid:
            bid = target_iid_to_bid[e]
            ol = (iid_to_labels.get(s) or ['?'])[0]
            other_bid = iid_to_bid.get(s, '?')
            snap[bid][('in', t, ol, other_bid)] += 1

# Type aggregation per ID
snap_by_dir_type = defaultdict(Counter)
for bid, cnt in snap.items():
    for (d, t, ol, ob), c in cnt.items():
        snap_by_dir_type[bid][(d, t)] += c

# Live edge counts copied from Neo4j query output
live = {
    'bw_bellastock_ville_des_terres_l_ile_saint_denis_lager': {
        ('out','HAT_BAUOBJEKTKLASSE'):1, ('out','HAT_BAUOBJEKTROLLE'):1,
        ('out','HAT_STATUS'):1, ('out','BELEGT_IN'):1, ('out','BETRIEBEN_VON'):1,
        ('in','FROM_DONOR'):1,
    },
    'bw_berlin_fitout_donor_sources': {
        ('out','HAT_BAUOBJEKTKLASSE'):2, ('out','HAT_BAUOBJEKTROLLE'):1,
        ('out','HAT_STATUS'):1, ('out','HAT_NUTZUNG'):2,
        ('out','LIEGT_IN_STADT'):1, ('out','LIEGT_IN_LAND'):1, ('out','BELEGT_IN'):1,
        ('in','FROM_DONOR'):7, ('in','NUTZT_BAUWERK'):1,
    },
    'bw_chiro_itterbeek_reuse_supply_network': {
        ('out','HAT_BAUOBJEKTKLASSE'):1, ('out','HAT_BAUOBJEKTROLLE'):2,
        ('out','HAT_STATUS'):1, ('out','LIEGT_IN_STADT'):1, ('out','LIEGT_IN_LAND'):1, ('out','BELEGT_IN'):1,
        ('in','FROM_DONOR'):13, ('in','NUTZT_BAUWERK'):1,
    },
    'bw_cleveland_steel_and_tubes_stock': {
        ('out','HAT_BAUOBJEKTKLASSE'):1, ('out','HAT_BAUOBJEKTROLLE'):1, ('out','HAT_STATUS'):1,
        ('out','HAT_RESSOURCENQUELLE'):1, ('out','BELEGT_IN'):1,
        ('in','FROM_DONOR'):1,
    },
    'bw_crclr_kindl_hall': {
        ('out','HAT_BAUOBJEKTKLASSE'):1, ('out','HAT_BAUOBJEKTROLLE'):3, ('out','HAT_TRAGWERKSPRINZIP'):1,
        ('out','HAT_BAUWEISE'):3, ('out','HAT_BAUSYSTEM'):2, ('out','HAT_STATUS'):1, ('out','HAT_NUTZUNG'):3,
        ('out','LIEGT_IN_STADT'):1, ('out','LIEGT_IN_LAND'):1, ('out','BELEGT_IN'):1,
        ('in','FROM_DONOR'):2, ('in','INTO_RECEIVER'):6, ('in','NUTZT_BAUWERK'):1,
    },
    'bw_donor_gebaudegruppe_resource_rows_mauerwerk': {
        ('out','HAT_BAUOBJEKTKLASSE'):1, ('out','HAT_BAUOBJEKTROLLE'):1, ('out','HAT_STATUS'):1, ('out','BELEGT_IN'):1,
        ('in','FROM_DONOR'):1,
    },
    'bw_elys_ehemaliges_getraenkelager_areal': {
        ('out','HAT_BAUOBJEKTKLASSE'):1, ('out','HAT_BAUOBJEKTROLLE'):1, ('out','HAT_STATUS'):1, ('out','BELEGT_IN'):1,
    },
    'bw_externe_stahl_donor_stockholder': {
        ('out','HAT_BAUOBJEKTKLASSE'):1, ('out','HAT_BAUOBJEKTROLLE'):1, ('out','HAT_STATUS'):1,
        ('out','HAT_NUTZUNG'):1, ('out','LIEGT_IN_STADT'):1, ('out','LIEGT_IN_LAND'):1, ('out','BELEGT_IN'):1,
        ('in','FROM_DONOR'):1, ('in','NUTZT_BAUWERK'):1,
    },
    'bw_holbein_grosvenor_donor_projects': {
        ('out','HAT_BAUOBJEKTKLASSE'):1, ('out','HAT_BAUOBJEKTROLLE'):1, ('out','HAT_TRAGWERKSPRINZIP'):1,
        ('out','HAT_BAUWEISE'):1, ('out','HAT_BAUSYSTEM'):1, ('out','HAT_STATUS'):1, ('out','HAT_NUTZUNG'):1,
        ('out','LIEGT_IN_STADT'):1, ('out','LIEGT_IN_LAND'):1, ('out','BELEGT_IN'):1, ('out','BETRIEBEN_VON'):1,
        ('in','FROM_DONOR'):1, ('in','NUTZT_BAUWERK'):1,
    },
    'bw_lo_reninge_reuse_brick_source': {
        ('out','HAT_BAUOBJEKTKLASSE'):1, ('out','HAT_BAUOBJEKTROLLE'):1, ('out','HAT_STATUS'):1,
        ('out','LIEGT_IN_STADT'):1, ('out','LIEGT_IN_LAND'):1, ('out','BELEGT_IN'):1,
        ('in','FROM_DONOR'):1, ('in','NUTZT_BAUWERK'):1,
    },
    'bw_maison_des_canaux_unspecified_donors': {
        ('out','HAT_BAUOBJEKTKLASSE'):1, ('out','HAT_BAUOBJEKTROLLE'):1, ('out','HAT_STATUS'):1,
        ('out','LIEGT_IN_STADT'):1, ('out','LIEGT_IN_LAND'):1, ('out','BELEGT_IN'):1,
        ('in','FROM_DONOR'):4, ('in','NUTZT_BAUWERK'):1,
    },
    'bw_maison_dna_unknown_brick_donor': {
        ('out','HAT_BAUOBJEKTKLASSE'):1, ('out','HAT_BAUOBJEKTROLLE'):1, ('out','HAT_STATUS'):1,
        ('out','LIEGT_IN_STADT'):1, ('out','LIEGT_IN_LAND'):1, ('out','BELEGT_IN'):1,
        ('in','FROM_DONOR'):1, ('in','NUTZT_BAUWERK'):1,
    },
    'bw_messebau_lager_hannover': {
        ('out','HAT_BAUOBJEKTKLASSE'):1, ('out','HAT_BAUOBJEKTROLLE'):1, ('out','HAT_STATUS'):1,
        ('out','HAT_NUTZUNG'):1, ('out','LIEGT_IN_STADT'):1, ('out','LIEGT_IN_LAND'):1, ('out','BELEGT_IN'):1,
        ('in','FROM_DONOR'):1, ('in','NUTZT_BAUWERK'):1,
    },
    'bw_p2_massenwohnungsbau_donor_unknown': {
        ('out','HAT_BAUOBJEKTKLASSE'):1, ('out','HAT_BAUOBJEKTROLLE'):1, ('out','HAT_TRAGWERKSPRINZIP'):1,
        ('out','HAT_BAUWEISE'):2, ('out','HAT_BAUSYSTEM'):1, ('out','HAT_STATUS'):1,
        ('out','LIEGT_IN_STADT'):1, ('out','LIEGT_IN_LAND'):1, ('out','BELEGT_IN'):1,
        ('in','FROM_DONOR'):2, ('in','NUTZT_BAUWERK'):1,
    },
    'bw_paris_material_sources_circular_pavilion': {
        ('out','HAT_BAUOBJEKTKLASSE'):1, ('out','HAT_BAUOBJEKTROLLE'):2, ('out','HAT_STATUS'):1,
        ('out','LIEGT_IN_STADT'):1, ('out','LIEGT_IN_LAND'):1, ('out','BELEGT_IN'):1,
        ('in','FROM_DONOR'):6, ('in','NUTZT_BAUWERK'):1,
    },
    'bw_paris_regional_donor_sources_ferme_du_rail': {
        ('out','HAT_BAUOBJEKTKLASSE'):1, ('out','HAT_BAUOBJEKTROLLE'):1, ('out','HAT_STATUS'):1,
        ('out','LIEGT_IN_STADT'):1, ('out','LIEGT_IN_LAND'):1, ('out','BELEGT_IN'):1,
        ('in','FROM_DONOR'):8, ('in','NUTZT_BAUWERK'):1,
    },
    'bw_rotor_reuse_stock_charles_malis': {
        ('out','HAT_BAUOBJEKTKLASSE'):1, ('out','HAT_BAUOBJEKTROLLE'):2, ('out','HAT_STATUS'):1,
        ('out','LIEGT_IN_STADT'):1, ('out','LIEGT_IN_LAND'):1, ('out','BELEGT_IN'):1, ('out','BETRIEBEN_VON'):1,
        ('in','FROM_DONOR'):2, ('in','NUTZT_BAUWERK'):1,
    },
    'bw_unbekannte_donor_buildings_zinneke_material_lots': {
        ('out','HAT_BAUOBJEKTKLASSE'):1, ('out','HAT_BAUOBJEKTROLLE'):1, ('out','HAT_STATUS'):1, ('out','BELEGT_IN'):1,
        ('in','FROM_DONOR'):4,
    },
    'bw_unbekanntes_transformationsgebaeude_kellerwaende': {
        ('out','HAT_BAUOBJEKTKLASSE'):1, ('out','HAT_BAUOBJEKTROLLE'):1, ('out','HAT_STATUS'):1,
        ('out','LIEGT_IN_LAND'):1, ('out','BELEGT_IN'):1,
        ('in','FROM_DONOR'):1, ('in','NUTZT_BAUWERK'):1,
    },
    'bw_unknown_brick_donor_sources_gjg': {
        ('out','HAT_BAUOBJEKTKLASSE'):1, ('out','HAT_BAUOBJEKTROLLE'):1, ('out','HAT_STATUS'):1,
        ('out','LIEGT_IN_STADT'):1, ('out','LIEGT_IN_LAND'):1, ('out','BELEGT_IN'):1,
        ('in','FROM_DONOR'):1, ('in','NUTZT_BAUWERK'):1,
    },
    'bw_unknown_demolition_wood_streams': {
        ('out','HAT_BAUOBJEKTKLASSE'):1, ('out','HAT_BAUOBJEKTROLLE'):1, ('out','HAT_TRAGWERKSPRINZIP'):1,
        ('out','HAT_BAUWEISE'):1, ('out','HAT_STATUS'):1,
        ('out','LIEGT_IN_STADT'):1, ('out','LIEGT_IN_LAND'):1, ('out','BELEGT_IN'):1,
        ('in','FROM_DONOR'):3, ('in','NUTZT_BAUWERK'):1,
    },
    'bw_verbiest_lagerhaus_zu_haus_und_atelier': {
        ('out','HAT_BAUOBJEKTKLASSE'):1, ('out','HAT_BAUOBJEKTROLLE'):1, ('out','HAT_STATUS'):1,
        ('out','LIEGT_IN_STADT'):1, ('out','BELEGT_IN'):1,
        ('in','FROM_DONOR'):1, ('in','INTO_RECEIVER'):5, ('in','NUTZT_BAUWERK'):1,
    },
    'bw_wbs70_donor_groeditz': {
        ('out','HAT_BAUOBJEKTKLASSE'):1, ('out','HAT_BAUOBJEKTROLLE'):1, ('out','HAT_STATUS'):1,
        ('out','LIEGT_IN_STADT'):1, ('out','BELEGT_IN'):1,
        ('in','FROM_DONOR'):1,
    },
}

# Apply Phase 1.1 rename: in-AUS_BAUWERK from :Wiederverwendungskette --> in-FROM_DONOR
#                          in-EINGEBAUT_IN from :Wiederverwendungskette --> in-INTO_RECEIVER
# Plus outAUS_BAUWERK from :Bauwerk (self->bauwerk) - those AUS_BAUWERK out edges in snapshot WERE eliminated by Phase 1.1!
# Actually the Phase 1.1 chain demote only deleted the 98 Wiederverwendungskette nodes. Look at snapshot data:
# - bw_cleveland_steel_and_tubes_stock had out AUS_BAUWERK x1 to ?  -- end node was perhaps a Wiederverwendungskette?
# - bw_maison_des_canaux_unspecified_donors had out AUS_BAUWERK x1 to ?
# Let me check what the targets were
print("=== Snapshot AUS_BAUWERK/EINGEBAUT_IN edges and their other-end label ===")
for bid in IDS:
    for (d, t, ol, ob), c in snap[bid].items():
        if t in ('AUS_BAUWERK', 'EINGEBAUT_IN'):
            print(f"  {bid:<58} {d:3} {t:14} other_label={ol:<22} other_id={ob}")

# Now compute snap normalised: apply renames where source/target was Wiederverwendungskette
snap_norm = defaultdict(Counter)
for bid, cnt in snap.items():
    for (d, t, ol, ob), c in cnt.items():
        if t == 'AUS_BAUWERK' and d == 'in' and ol == 'Wiederverwendungskette':
            snap_norm[bid][('in','FROM_DONOR')] += c
        elif t == 'AUS_BAUWERK' and d == 'in' and ol == 'Bauteilgruppe':
            snap_norm[bid][('in','FROM_DONOR')] += c  # Phase 1.1 may have moved this too? Actually no, AUS_BAUWERK from Bauteilgruppe -> Bauwerk should remain unchanged
            snap_norm[bid][('in','AUS_BAUWERK')] += 0  # placeholder note
        elif t == 'EINGEBAUT_IN' and d == 'in' and ol == 'Wiederverwendungskette':
            snap_norm[bid][('in','INTO_RECEIVER')] += c
        elif t == 'AUS_BAUWERK' and d == 'out':
            # Out AUS_BAUWERK from Bauwerk -> X, target may be Wiederverwendungskette or Bauwerk
            # Phase 1.1 may delete it if target was Wiederverwendungskette
            if ol == 'Wiederverwendungskette':
                # Likely dropped (Wiederverwendungskette node deleted)
                pass
            else:
                snap_norm[bid][(d,t)] += c
        else:
            snap_norm[bid][(d,t)] += c

# Now do the proper compare
print("\n=== Per-ID degree comparison (Snapshot normalised + Phase 1.4 BETRIEBEN_VON addition vs Live) ===")
print(f"{'id':<60} {'snap_orig':>9} {'snap_norm':>9} {'+BV':>4} {'expected':>9} {'live':>5} {'Δ(live-expected)':>17}")
total_unexplained_drop = 0
for bid in IDS:
    s_orig = sum(snap[bid].values())
    s_norm = sum(snap_norm[bid].values())
    bv = 1 if bid in ('bw_bellastock_ville_des_terres_l_ile_saint_denis_lager',
                       'bw_holbein_grosvenor_donor_projects',
                       'bw_rotor_reuse_stock_charles_malis') else 0
    l = sum(live[bid].values())
    expected = s_norm + bv
    delta = l - expected
    print(f"{bid:<60} {s_orig:>9} {s_norm:>9} {bv:>4} {expected:>9} {l:>5} {delta:>17}")
    if delta < 0:
        total_unexplained_drop += -delta
print(f"\nTotal unexplained edge drop across 23 Materialdepots: {total_unexplained_drop}")
