"""Sphinx role for reStructuredText and MyST, with non-HTML text fallbacks."""
from pathlib import Path

from docutils import nodes
from sphinx.util.docutils import SphinxRole

from .core import IconRegistry, get_css


class BlenderIcon(nodes.Inline, nodes.Element):
    pass


def _registry(env):
    directory = env.config.blender_icons_dir
    return IconRegistry(Path(env.srcdir) / directory if directory else None)


class BlenderIconRole(SphinxRole):
    def run(self):
        name, separator, label = self.text.partition("|")
        name = name.strip().lower()
        label = label.strip() if separator else None
        try:
            registry = _registry(self.env)
            registry.get_svg(name)
        except ValueError as error:
            message = self.inliner.reporter.error(str(error), line=self.lineno)
            return [self.inliner.problematic(self.rawtext, self.rawtext, message)], [message]
        if registry.icon_dir and (registry.icon_dir / f"{name}.svg").is_file():
            self.env.note_dependency(str(registry.icon_dir / f"{name}.svg"))
        return [BlenderIcon(self.rawtext, name=name, label=label)], []


def _visit_html(translator, node):
    translator.body.append(_registry(translator.builder.env).render_html(node["name"], label=node["label"]))
    raise nodes.SkipNode


def _resolve_fallbacks(app, doctree, docname):
    if app.builder.format != "html":
        for node in list(doctree.findall(BlenderIcon)):
            node.replace_self(nodes.Text(node["label"] or f'[{node["name"].replace("_", " ")}]'))


def _write_css(app, exception):
    if exception is None and app.builder.format == "html":
        path = Path(app.outdir) / "_static" / "blender-icons.css"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(get_css(), encoding="utf-8")


def setup(app):
    app.add_config_value("blender_icons_dir", None, "env", types=[str, type(None)])
    app.add_role("blender-icon", BlenderIconRole())
    app.add_node(BlenderIcon, html=(_visit_html, None))
    app.add_css_file("blender-icons.css")
    app.connect("doctree-resolved", _resolve_fallbacks)
    app.connect("build-finished", _write_css)
    return {"version": "0.1.0", "parallel_read_safe": True, "parallel_write_safe": True}
