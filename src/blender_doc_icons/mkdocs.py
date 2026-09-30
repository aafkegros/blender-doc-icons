"""MkDocs integration: syntax, bundled CSS, and custom icon watching."""
from pathlib import Path

from mkdocs.config import base, config_options
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File

from .core import get_css
from .markdown import BlenderIconsExtension

CSS_PATH = "assets/blender-icons/icons.css"


class BlenderIconsConfig(base.Config):
    icon_dir = config_options.Optional(config_options.Type(str))


class BlenderIconsPlugin(BasePlugin[BlenderIconsConfig]):
    def on_config(self, config):
        self.icon_dir = None
        if self.config.icon_dir:
            self.icon_dir = (Path(config.config_file_path).parent / self.config.icon_dir).resolve()
            if not self.icon_dir.is_dir():
                raise PluginError(f"Icon directory does not exist: {self.icon_dir}")
        config.markdown_extensions.append(BlenderIconsExtension(icon_dir=str(self.icon_dir) if self.icon_dir else ""))
        if CSS_PATH not in config.extra_css:
            config.extra_css.append(CSS_PATH)
        return config

    def on_files(self, files, config):
        if files.get_file_from_path(CSS_PATH) is not None:
            raise PluginError(f"Generated icon stylesheet conflicts with {CSS_PATH}")
        files.append(File.generated(config, CSS_PATH, content=get_css()))
        return files

    def on_serve(self, server, config, builder):
        if self.icon_dir:
            server.watch(str(self.icon_dir), builder)
        return server
