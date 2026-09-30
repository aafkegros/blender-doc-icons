"""Read packaged SVGs and render inline HTML without a documentation framework."""
from __future__ import annotations

from functools import lru_cache
from html import escape
from importlib.resources import files
from pathlib import Path
import re
from uuid import uuid4
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
_NAME = re.compile(r"[a-z0-9_]+\Z")


class UnknownIconError(ValueError):
    """An icon name does not exist in this registry."""


def normalize_svg(source: str) -> str:
    """Prepare trusted SVG artwork; this is not an untrusted-SVG sanitizer."""
    root = ET.fromstring(source)
    if root.tag != f"{{{SVG_NS}}}svg" or "viewBox" not in root.attrib:
        raise ValueError("Icons must be SVG documents with a viewBox")
    for parent in root.iter():
        for child in list(parent):
            if not child.tag.startswith(f"{{{SVG_NS}}}") or child.tag == f"{{{SVG_NS}}}metadata":
                parent.remove(child)
    root.attrib.pop("width", None)
    root.attrib.pop("height", None)
    root.attrib.setdefault("fill", "currentColor")
    for element in root.iter():
        for attr in ("fill", "stroke"):
            value = element.get(attr)
            if value and value not in ("none", "inherit", "currentColor", "transparent") and not value.startswith("url("):
                element.set(attr, "currentColor")
        # Preserve non-colour style declarations and explicit unpainted areas.
        if "style" in element.attrib:
            declarations = []
            for declaration in element.attrib["style"].split(";"):
                key, sep, value = declaration.partition(":")
                if not sep:
                    continue
                if key.strip() in ("fill", "stroke") and value.strip() not in ("none", "inherit", "currentColor", "transparent") and not value.strip().startswith("url("):
                    value = "currentColor"
                declarations.append(f"{key.strip()}:{value.strip()}")
            element.set("style", ";".join(declarations))
    return ET.tostring(root, encoding="unicode")


@lru_cache(maxsize=1024)
def _bundled_svg(name: str) -> str:
    return files("blender_doc_icons").joinpath("assets", "icons", f"{name}.svg").read_text(encoding="utf-8")


class IconRegistry:
    """Bundled icons with optional trusted local overrides, read fresh per render."""

    def __init__(self, icon_dir: str | Path | None = None):
        self.icon_dir = Path(icon_dir).resolve() if icon_dir is not None else None
        if self.icon_dir is not None and not self.icon_dir.is_dir():
            raise ValueError(f"Icon directory does not exist: {self.icon_dir}")
        self._bundled = frozenset(
            p.name[:-4] for p in files("blender_doc_icons").joinpath("assets", "icons").iterdir()
            if p.name.endswith(".svg")
        )

    def list_icons(self) -> list[str]:
        local = {p.stem for p in self.icon_dir.glob("*.svg") if _NAME.fullmatch(p.stem)} if self.icon_dir else set()
        return sorted(self._bundled | local)

    def get_svg(self, name: str) -> str:
        if not _NAME.fullmatch(name):
            raise UnknownIconError(f"Invalid icon name: {name!r}; use lowercase letters, digits, and underscores")
        if self.icon_dir is not None:
            path = self.icon_dir / f"{name}.svg"
            if path.is_file():
                return normalize_svg(path.read_text(encoding="utf-8"))
        if name not in self._bundled:
            raise UnknownIconError(f"Unknown Blender icon {name!r}. Use 'blender-icons list' to see available names.")
        return _bundled_svg(name)

    def render_html(self, name: str, *, label: str | None = None) -> str:
        root = ET.fromstring(self.get_svg(name))
        # Repeated inline SVGs must not share gradient/clip IDs.
        prefix = f"bi-{uuid4().hex}-"
        ids = {e.attrib["id"]: prefix + e.attrib["id"] for e in root.iter() if "id" in e.attrib}
        for element in root.iter():
            for key, value in list(element.attrib.items()):
                if key == "id":
                    value = ids[value]
                else:
                    value = re.sub(r"url\(#([^)]*)\)", lambda m: f"url(#{ids.get(m[1], m[1])})", value)
                    if key.split("}")[-1] == "href" and value.startswith("#"):
                        value = "#" + ids.get(value[1:], value[1:])
                element.set(key, value)
        root.set("aria-hidden", "true")
        root.set("focusable", "false")
        accessibility = f'role="img" aria-label="{escape(label, quote=True)}"' if label else 'aria-hidden="true"'
        return f'<span class="blender-icon" {accessibility}>{ET.tostring(root, encoding="unicode")}</span>'


@lru_cache(maxsize=1)
def _default_registry() -> IconRegistry:
    return IconRegistry()


def list_icons() -> list[str]:
    return _default_registry().list_icons()


def get_svg(name: str) -> str:
    return _default_registry().get_svg(name)


def render_html(name: str, *, label: str | None = None) -> str:
    return _default_registry().render_html(name, label=label)


def get_css() -> str:
    return files("blender_doc_icons").joinpath("assets", "icons.css").read_text(encoding="utf-8")
