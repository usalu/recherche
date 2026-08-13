# -*- coding: utf-8 -*-
"""
Assemble the final classification prompt for one batch:

    KANTEN_TAXONOMIE.md   (the whole prompt, {{KANTENDATEN}} at the end)
  + kanten_batches/kanten_<CC>_b<N>.md

The result is ONE self-contained file per batch: the agent opens it, does the
work, returns the table. Nothing else to read, nothing to combine.

`validate_kanten.py` extracts the legal relationship names from the same
taxonomy file, so prompt and validator cannot drift apart.

Usage:
    python assemble_kanten_prompt.py kanten_BE_b1.md > prompt.md
    python assemble_kanten_prompt.py --all        # writes kanten_prompts/*.md
"""
import os, sys, glob

BASE = os.path.dirname(os.path.abspath(__file__))
TAXONOMIE = os.path.join(BASE, "KANTEN_TAXONOMIE.md")
BATCHDIR = os.path.join(BASE, "kanten_batches")
PROMPTDIR = os.path.join(BASE, "kanten_prompts")

PLACEHOLDER = "{{KANTENDATEN}}"


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def build(batch_name):
    taxo = read(TAXONOMIE)
    daten = read(os.path.join(BATCHDIR, batch_name)).rstrip() + "\n"

    if PLACEHOLDER not in taxo:
        sys.exit(f"{TAXONOMIE} enthaelt keinen {PLACEHOLDER}-Platzhalter.")
    return taxo.replace(PLACEHOLDER, daten)


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    if args[0] in ("-h", "--help"):
        print(__doc__)
        return

    if args[0] == "--all":
        os.makedirs(PROMPTDIR, exist_ok=True)
        for old in glob.glob(os.path.join(PROMPTDIR, "prompt_*.md")):
            os.remove(old)
        n = 0
        for p in sorted(glob.glob(os.path.join(BATCHDIR, "kanten_*.md"))):
            name = os.path.basename(p)
            out = os.path.join(PROMPTDIR, name.replace("kanten_", "prompt_"))
            with open(out, "w", encoding="utf-8", newline="\n") as f:
                f.write(build(name))
            n += 1
        print(f"{n} Prompts geschrieben nach {PROMPTDIR}")
    else:
        sys.stdout.write(build(args[0]))


if __name__ == "__main__":
    main()
