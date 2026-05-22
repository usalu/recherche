import re, ssl
from urllib.request import Request, urlopen
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
def grab(u):
    try:
        r=Request(u, headers={"User-Agent":"Mozilla/5.0 (recherche-ceg/1.0)"})
        t=urlopen(r,timeout=25,context=ctx).read(400000).decode("utf-8","replace")
        t=re.sub(r"<[^>]+>"," ",t); t=re.sub(r"\s+"," ",t)
        return t
    except Exception as e:
        return f"ERR {e}"
for u, needles in [
    ("https://www.la-ressourcerie.ch/les-mat%C3%A9riaux", ["fenêtre","fenetre","window","matériaux","bois","porte"]),
    ("https://www.lendager.com/projects/upcycle-studios", ["window","beton","concrete","dinesen","offcut","brick"]),
    ("https://circularhub.ch/magazin/details/sumami-wiederverwendung", ["sumami","wiederverwend","circular"]),
]:
    t=grab(u)
    print("URL:", u)
    print("  len:", len(t))
    low=t.lower()
    for n in needles:
        print(f"   {'YES' if n in low else 'no ':3} {n}")
    print()
