"""List names or export standalone, explicitly coloured SVG assets."""
import argparse
from importlib.resources import files
from pathlib import Path
import re

from .core import IconRegistry, get_css


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--icon-dir", type=Path, help="Trusted local SVG directory")
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list", help="List icon names")
    listing.add_argument("query", nargs="?", default="")
    export = commands.add_parser("export", help="Export SVG files and a stylesheet")
    export.add_argument("names", nargs="*", help="Icon names; omit to export all")
    export.add_argument("--output", type=Path, required=True)
    export.add_argument("--color", default="#5e5e5e", help="Hex colour for standalone SVGs")
    quarto = commands.add_parser("quarto", help="Export a self-contained Quarto shortcode extension")
    quarto.add_argument("--output", type=Path, default=Path("_extensions/blender-icons"),
                        help="Extension directory (default: _extensions/blender-icons)")
    args = parser.parse_args()
    try:
        registry = IconRegistry(args.icon_dir)
        if args.command == "quarto":
            from .quarto import export_quarto
            destination = export_quarto(args.output, registry)
            print(f"Exported Quarto extension to {destination}")
            return
        if args.command == "list":
            print("\n".join(name for name in registry.list_icons() if args.query.lower() in name))
            return
        if not re.fullmatch(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})", args.color):
            parser.error("--color must be a three- or six-digit hex colour, e.g. '#5e5e5e'")
        # Resolve every requested icon before writing anything.
        icons = {name.lower(): registry.get_svg(name) for name in (args.names or registry.list_icons())}
        args.output.mkdir(parents=True, exist_ok=True)
        for name, svg in icons.items():
            (args.output / f"{name}.svg").write_text(svg.replace("currentColor", args.color), encoding="utf-8")
        (args.output / "icons.css").write_text(get_css(), encoding="utf-8")
        notice = files("blender_doc_icons").joinpath("assets", "NOTICE.md").read_text(encoding="utf-8")
        (args.output / "NOTICE.md").write_text(notice.replace("LICENSES/CC-BY-SA-4.0.txt", "CC-BY-SA-4.0.txt"), encoding="utf-8")
        license_text = files("blender_doc_icons").joinpath("assets", "CC-BY-SA-4.0.txt").read_text(encoding="utf-8")
        (args.output / "CC-BY-SA-4.0.txt").write_text(license_text, encoding="utf-8")
        print(f"Exported {len(icons)} icons to {args.output}")
    except (ValueError, OSError) as error:
        parser.error(str(error))
