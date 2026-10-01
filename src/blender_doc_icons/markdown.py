"""Python-Markdown syntax: :blender-scene_data: or :blender-scene_data|Scene:."""
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor

from .core import IconRegistry


class IconInlineProcessor(InlineProcessor):
    def __init__(self, registry, md):
        super().__init__(r":blender-([a-zA-Z0-9_]+)(?:\|([^:\n]+))?:", md)
        self.registry = registry

    def handleMatch(self, match, data):
        html = self.registry.render_html(match[1], label=match[2])
        return self.md.htmlStash.store(html), match.start(0), match.end(0)


class BlenderIconsExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {"icon_dir": ["", "Directory of trusted custom SVG icons"]}
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        registry = IconRegistry(self.getConfig("icon_dir") or None)
        md.registerExtension(self)
        # Run before pymdownx.emoji (75), while keeping code, links, and HTML protected.
        md.inlinePatterns.register(IconInlineProcessor(registry, md), "blender-icons", 76)


def makeExtension(**kwargs):
    return BlenderIconsExtension(**kwargs)
