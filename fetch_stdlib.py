"""
fetch_stdlib.py -- refresh the vendored stdlib bundles from the project site.

The extension ships the self-contained stdlib bundles (see STDLIB_BUNDLES)
and the engine's support scripts (see SUPPORT_SCRIPTS) as byte-for-byte copies
of the published files at https://plantuml.github.io/plantuml/js-plantuml/.
They go stale whenever the site republishes (a library version bump upstream),
so refreshing them is part of preparing a release: run this script, review the
reported changes, and commit.

Every bundle is written to extension/ at the directory root: the engine
resolves `<lib>.min.js` relative to renderer.html, so the files cannot live
under vendor/.

The bundle list appears in three places that must stay in sync: this script,
build_zip.py (STDLIB_BUNDLES and SUPPORT_SCRIPTS) and the
web_accessible_resources list in extension/manifest.json.
"""

import sys
import urllib.request
from pathlib import Path

BASE_URL = "https://plantuml.github.io/plantuml/js-plantuml/"

# `awslib`, `material` and `material2` are tiny alias stubs that point at
# awslib14 / material2.1.19, so they travel with their targets.
STDLIB_BUNDLES = [
    "adaml", "archimate", "azure", "c4", "classy", "classy-c4",
    "cloudinsight", "cloudogu", "domainstory", "edgy", "eip",
    "elastic", "gcp", "k8s", "kubernetes", "osa2",
    "awslib10", "bootstrap", "bootstrap1.13.1", "office", "osa",
    # Heavy sprite collections (~80 MB).
    "awslib", "awslib14", "awslib20", "ibm", "logos",
    "material", "material2", "material2.1.19", "tupadr3",
]

# Support scripts the engine lazy-loads the same way, from the same place:
# emoji.js for <:emoji:> sprites, themes.js for `!theme`, openiconic.js for
# <&icon> sprites. Without them, a diagram using one of these features
# fails to render (the load of the missing file never completes).
SUPPORT_SCRIPTS = ["emoji.js", "themes.js", "openiconic.js"]

ROOT = Path(__file__).resolve().parent
TARGET_DIR = ROOT / "extension"


def main() -> int:
    changed = 0
    names = [f"{lib}.min.js" for lib in STDLIB_BUNDLES] + SUPPORT_SCRIPTS
    for name in names:
        url = BASE_URL + name
        try:
            with urllib.request.urlopen(url) as resp:
                fresh = resp.read()
        except Exception as e:
            print(f"ERROR  {name}: {e}")
            return 1

        current = TARGET_DIR / name
        if current.exists() and current.read_bytes() == fresh:
            print(f"same     {name}  ({len(fresh) / 1024:.0f} KB)")
            continue

        status = "updated" if current.exists() else "NEW"
        current.write_bytes(fresh)
        print(f"{status:8s} {name}  ({len(fresh) / 1024:.0f} KB)")
        changed += 1

    print(f"\n{changed} bundle(s) changed." if changed else "\nAll bundles already current.")
    if changed:
        print("Review with `git diff --stat`, then commit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
