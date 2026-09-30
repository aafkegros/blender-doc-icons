"""Export a self-contained Quarto shortcode extension."""
from importlib.resources import files
import json
from pathlib import Path

from .core import IconRegistry, get_css


def export_quarto(output: str | Path, registry: IconRegistry | None = None) -> Path:
    """Write an extension directory; custom artwork is captured at export time."""
    registry = registry if registry is not None else IconRegistry()
    # Validate all artwork before touching the destination.
    icons = {name: registry.render_html(name) for name in registry.list_icons()}
    assets = files("blender_doc_icons").joinpath("assets")
    contents = {
        "icons.json": json.dumps(icons, ensure_ascii=False) + "\n",
        "icons.css": get_css(),
        "NOTICE.md": assets.joinpath("NOTICE.md").read_text(encoding="utf-8").replace(
            "LICENSES/CC-BY-SA-4.0.txt", "CC-BY-SA-4.0.txt"
        ),
        "CC-BY-SA-4.0.txt": assets.joinpath("CC-BY-SA-4.0.txt").read_text(encoding="utf-8"),
    }
    for name in ("_extension.yml", "blender-icons.lua"):
        contents[name] = assets.joinpath("quarto", name).read_text(encoding="utf-8")
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    for name, content in contents.items():
        (output / name).write_text(content, encoding="utf-8")
    return output
