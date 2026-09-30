"""Prepare trusted SVG assets and record source hashes and upstream revision."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from blender_doc_icons.core import normalize_svg

ASSETS = Path(__file__).resolve().parents[1] / "src/blender_doc_icons/assets"


def prepare_icons(source_dir, *, source_description, upstream_revision="unknown", exclude=("microscopy_nodes",), assets_dir=ASSETS):
    source_dir = Path(source_dir)
    paths = sorted(source_dir.glob("*.svg"))
    if not paths:
        raise ValueError(f"No SVG icons found in {source_dir}")
    entries, prepared = {}, {}
    for path in paths:
        name = path.stem.removeprefix("blender_icon_").replace(".", "_")
        if name in exclude:
            continue
        if not re.fullmatch(r"[a-z0-9_]+", name):
            raise ValueError(f"Unsupported icon filename: {path.name}")
        if name in prepared:
            raise ValueError(f"Duplicate normalized icon name: {name}")
        data = path.read_bytes()
        source = data.decode("utf-8")
        repair = None
        if name in {"char_replacement", "outliner_data_gp_layer"}:
            root = ET.fromstring(source)
            if "viewBox" not in root.attrib:
                repair = "Added viewBox 0 0 1600 1600 to legacy source"
                root.set("viewBox", "0 0 1600 1600")
                source = ET.tostring(root, encoding="unicode")
        try:
            svg = normalize_svg(source)
        except (ValueError, ET.ParseError) as error:
            raise ValueError(f"Cannot prepare {path.name}: {error}") from error
        prepared[name] = svg
        entries[name] = {
            "source_filename": path.name,
            "source_sha256": hashlib.sha256(data).hexdigest(),
            "sha256": hashlib.sha256(svg.encode()).hexdigest(),
            "repair": repair,
        }
    if not prepared:
        raise ValueError("No icons remain after exclusions")
    # Validate everything before replacing the generated collection. Remove obsolete
    # generated files so an upstream deletion cannot silently survive a refresh.
    destination = Path(assets_dir) / "icons"
    destination.mkdir(parents=True, exist_ok=True)
    for path in destination.glob("*.svg"):
        if path.stem not in prepared:
            path.unlink()
    for name, svg in prepared.items():
        (destination / f"{name}.svg").write_text(svg, encoding="utf-8")
    manifest = {
        "source": source_description,
        "upstream_revision": upstream_revision,
        "license": "CC-BY-SA-4.0",
        "attribution": "Blender UI icons designed by @jenzdrich; see NOTICE.md",
        "excluded": list(exclude),
        "icons": entries,
    }
    (Path(assets_dir) / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {len(entries)} icons from {upstream_revision}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--source-description", required=True)
    parser.add_argument("--upstream-revision", default="unknown")
    parser.add_argument("--exclude", action="append", default=["microscopy_nodes"])
    args = parser.parse_args()
    prepare_icons(args.source, source_description=args.source_description, upstream_revision=args.upstream_revision, exclude=args.exclude)


if __name__ == '__main__':
    main()
