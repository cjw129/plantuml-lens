"""
Build the extension ZIP (plantuml-lens.zip) from extension/.

Why Python and not PowerShell's Compress-Archive:
  Compress-Archive on some Windows builds writes path separators as
  backslashes inside the archive, which violates the ZIP spec and can
  trip strict validators. Python's zipfile uses '/' consistently and
  lets us set arcname explicitly, so we're safe.

The ZIP is flat: manifest.json sits at the root of the archive, so it can be
extracted and loaded with "Load unpacked" as is.

The engine (extension/vendor/plantuml.js, a TeaVM-compiled PlantUML, about
4 MB) is a single file imported by renderer.js as an ES module. Graph layout
is done by Smetana, PlantUML's built-in port of Graphviz layout, compiled
into the same file, so there is no separate viz-global.js and no WebAssembly
module.
"""

import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXT_DIR = ROOT / "extension"
OUT = ROOT / "plantuml-lens.zip"

with open(EXT_DIR / "manifest.json", "r", encoding="utf-8") as f:
    version = json.load(f)["version"]

# Exact list of files to ship, as (arcname inside ZIP -> source path).
# Listing every file explicitly avoids accidentally bundling leftover
# artifacts from earlier experiments.
FILES = {
    "manifest.json":         EXT_DIR / "manifest.json",
    "content.js":            EXT_DIR / "content.js",
    "renderer.html":         EXT_DIR / "renderer.html",
    "renderer.js":           EXT_DIR / "renderer.js",
    "options.html":          EXT_DIR / "options.html",
    "options.js":            EXT_DIR / "options.js",
    "icons/icon16.png":      EXT_DIR / "icons" / "icon16.png",
    "icons/icon48.png":      EXT_DIR / "icons" / "icon48.png",
    "icons/icon128.png":     EXT_DIR / "icons" / "icon128.png",
    "vendor/plantuml.js":    EXT_DIR / "vendor" / "plantuml.js",
    "LICENSE":              ROOT / "LICENSE",
    "THIRD_PARTY_NOTICES.md": ROOT / "THIRD_PARTY_NOTICES.md",
}

# Standard-library bundles the engine lazy-loads for `!include <lib/...>`.
# TeaVmScriptLoader resolves `<lib>.min.js` relative to renderer.html, so
# these MUST live at the extension root (not under vendor/).
# `awslib`, `material` and `material2` are tiny alias stubs that point at
# awslib14 / material2.1.19.
STDLIB_BUNDLES = [
    "adaml", "archimate", "azure", "c4", "classy", "classy-c4",
    "cloudinsight", "cloudogu", "domainstory", "edgy", "eip",
    "elastic", "gcp", "k8s", "kubernetes", "osa2",
    "awslib10", "bootstrap", "bootstrap1.13.1", "office", "osa",
    "awslib", "awslib14", "awslib20", "ibm", "logos",
    "material", "material2", "material2.1.19", "tupadr3",
]
for lib in STDLIB_BUNDLES:
    FILES[f"{lib}.min.js"] = EXT_DIR / f"{lib}.min.js"

# Support scripts the engine lazy-loads the same way (same root-level
# location): emoji.js for <:emoji:> sprites, themes.js for `!theme`,
# openiconic.js for <&icon> sprites. Fetched by fetch_stdlib.py.
for name in ["emoji.js", "themes.js", "openiconic.js"]:
    FILES[name] = EXT_DIR / name

missing = [arcname for arcname, src in FILES.items() if not src.exists()]
if missing:
    raise SystemExit(
        "ERROR: missing files:\n"
        + "\n".join(f"  - {m}" for m in missing)
    )

if OUT.exists():
    OUT.unlink()

with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for arcname, src in FILES.items():
        zf.write(src, arcname=arcname)

print(f"Created: {OUT.name} (version {version}, {OUT.stat().st_size / 1024 / 1024:.2f} MB)")

# Sanity check: no backslashes in entry names, manifest.json at the root.
with zipfile.ZipFile(OUT, "r") as zf:
    names = zf.namelist()
    if any("\\" in n for n in names):
        raise SystemExit("ERROR: archive entries use backslashes")
    if "manifest.json" not in names:
        raise SystemExit("ERROR: manifest.json is not at the archive root")
print(f"OK - {len(names)} entries, flat layout.")
