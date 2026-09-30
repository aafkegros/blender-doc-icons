"""Small regression checks for the shared behaviour and Markdown integration."""
import tempfile
import importlib.util
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET

import markdown

from blender_doc_icons import IconRegistry, UnknownIconError, get_svg, render_html
from blender_doc_icons.core import normalize_svg


class IconTests(unittest.TestCase):
    def test_accessibility_and_unique_ids(self):
        markup = render_html('scene_data', label='Scene "Properties"')
        self.assertIn('aria-label="Scene &quot;Properties&quot;"', markup)
        self.assertIn('aria-hidden="true"', render_html('scene_data'))
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, 'custom.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><defs><linearGradient id="a" /></defs><path fill="url(#a)" /></svg>')
            registry = IconRegistry(directory)
            first, second = registry.render_html('custom'), registry.render_html('custom')
            self.assertNotEqual(first, second)
            root = ET.fromstring(first)
            identifier = next(e.get('id') for e in root.iter() if e.get('id'))
            self.assertIn(f'url(#{identifier})', first)

    def test_unknown_names_and_paths(self):
        for name in ('../scene_data', 'missing_icon_name', 'Scene_Data'):
            with self.assertRaises(UnknownIconError):
                get_svg(name)

    def test_local_override_and_no_stale_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, 'scene_data.svg')
            path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path fill="none" stroke="#fff" /></svg>')
            registry = IconRegistry(directory)
            self.assertIn('fill="none"', registry.get_svg('scene_data'))
            self.assertIn('stroke="currentColor"', registry.get_svg('scene_data'))
            path.write_text(path.read_text().replace('16 16', '24 24'))
            self.assertIn('24 24', registry.get_svg('scene_data'))

    def test_markdown_code_links_and_labels(self):
        source = ':blender-scene_data: :blender-camera_data|Camera: [link](https://example.com/:blender-scene_data:)\n\n`:blender-scene_data:`\n\n```\n:blender-scene_data:\n```'
        html = markdown.markdown(source, extensions=['blender_doc_icons.markdown', 'fenced_code'])
        self.assertEqual(html.count('class="blender-icon"'), 2)
        self.assertIn('<code>:blender-scene_data:</code>', html)
        self.assertIn('href="https://example.com/:blender-scene_data:"', html)
        self.assertIn('aria-label="Camera"', html)
        with self.assertRaises(UnknownIconError):
            markdown.markdown(':blender-does_not_exist:', extensions=['blender_doc_icons.markdown'])

    def test_import_normalizes_names_records_provenance_and_prunes(self):
        tool = Path(__file__).resolve().parents[1] / 'tools' / 'prepare_icons.py'
        spec = importlib.util.spec_from_file_location('prepare_icons', tool)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            source, assets = Path(directory) / 'source', Path(directory) / 'assets'
            source.mkdir()
            (assets / 'icons').mkdir(parents=True)
            (assets / 'icons' / 'obsolete.svg').write_text('old')
            (source / 'blender_icon_sample.inline.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path fill="#fff" /></svg>')
            module.prepare_icons(source, source_description='fixture', upstream_revision='abc123', assets_dir=assets)
            self.assertTrue((assets / 'icons' / 'sample_inline.svg').exists())
            self.assertFalse((assets / 'icons' / 'obsolete.svg').exists())
            self.assertIn('abc123', (assets / 'manifest.json').read_text())

    def test_normalizer_preserves_unpainted_shapes(self):
        svg = normalize_svg('<svg xmlns="http://www.w3.org/2000/svg" width="16" viewBox="0 0 16 16"><path style="fill:none;stroke:#fff;opacity:.5" /></svg>')
        self.assertIn('fill:none;stroke:currentColor;opacity:.5', svg)
        self.assertNotIn('width=', svg)


if __name__ == '__main__':
    unittest.main()
