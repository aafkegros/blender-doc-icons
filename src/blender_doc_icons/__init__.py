"""Framework-independent Blender icon access. No optional imports at package level."""
from .core import IconRegistry, UnknownIconError, get_css, get_svg, list_icons, render_html

__all__ = ["IconRegistry", "UnknownIconError", "get_css", "get_svg", "list_icons", "render_html"]
__version__ = "0.1.0"
