"""Regression for MkDocs configurations that enable pymdownx.emoji."""
import unittest

import markdown
from blender_doc_icons.markdown import BlenderIconsExtension


class EmojiIntegrationTests(unittest.TestCase):
    def test_icons_and_emoji_in_either_extension_order(self):
        source = ':blender-SCENE_DATA: :blender-camera_data|Camera: :smile: `:blender-SCENE_DATA:`'
        for icons_first in (False, True):
            with self.subTest(icons_first=icons_first):
                extensions = [BlenderIconsExtension(), 'pymdownx.emoji']
                if not icons_first:
                    extensions.reverse()
                html = markdown.markdown(source, extensions=extensions)
                self.assertEqual(html.count('class="blender-icon"'), 2)
                self.assertIn('aria-label="Camera"', html)
                self.assertIn('<code>:blender-SCENE_DATA:</code>', html)
                self.assertIn('class="emojione"', html)


if __name__ == '__main__':
    unittest.main()
