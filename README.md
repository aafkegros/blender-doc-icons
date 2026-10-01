# Blender documentation icons

Bring Blender’s familiar interface icons into your tutorials and documentation.
Use inline SVGs alongside text to help readers find the right editor, property,
modifier, or tool.

![Microscopy Nodes documentation in MkDocs, with inline Blender icons identifying the Outliner and viewport shading modes.](https://raw.githubusercontent.com/aafkegros/blender-doc-icons/main/usage_example.png)

*In use in the [Microscopy Nodes](https://github.com/aafkegros/MicroscopyNodes)
documentation, built with MkDocs.*

Putting the actual icons beside your instructions makes it clear which interface
regions and buttons you mean. SVG icons stay crisp at any text size, without
cropping screenshots or building your own icon integration.

**MkDocs · Sphinx & Furo · Quarto · Python-Markdown · Python**

Icons scale with your text and inherit its colour, including in dark themes.
No Blender installation or JavaScript is needed, and the bundled icons work
without network access when building your documentation.

## Choose your setup

| Writing with | Get started |
| --- | --- |
| MkDocs | [Enable the plugin](#mkdocs) |
| Sphinx, Furo, or MyST | [Add the Sphinx extension](#sphinx-and-furo) |
| Quarto | [Export the shortcode extension](#quarto) |
| Python-Markdown | [Enable the Markdown extension](#python-markdown) |
| Other tools or a GitHub README | [Export SVG files](#export-svg-files) |
| Your own Python application | [Use the Python API](#python-api) |

Package installation requires **Python 3.10 or later**.

## MkDocs

Install the plugin:

```sh
pip install 'blender-doc-icons[mkdocs]'
```

Add it to your existing plugins in `mkdocs.yml`:

```yaml
plugins:
  - search
  - blender-icons
```

Then use icons in your Markdown:

```markdown
Open :blender-scene_data: **Scene Properties**.

:blender-camera_data|Camera: Add a camera to the scene.
```

The plugin includes the stylesheet and enables the Markdown syntax automatically.
There is no need to register a separate Markdown extension. Inline code and fenced
code blocks keep the icon syntax as literal text.

[View the MkDocs example](examples/mkdocs/docs/index.md).

## Sphinx and Furo

Install the extension:

```sh
pip install 'blender-doc-icons[sphinx]'
```

Add `blender_doc_icons.sphinx` to your existing extensions in `conf.py`:

```python
extensions = ['blender_doc_icons.sphinx']
```

Use the role in reStructuredText:

```rst
Open :blender-icon:`scene_data` Scene Properties.
Labelled icon: :blender-icon:`camera_data|Camera`.
```

For **MyST Markdown**, install and enable `myst_parser` as well:

```markdown
Open {blender-icon}`scene_data` Scene Properties.
Labelled icon: {blender-icon}`camera_data|Camera`.
```

**Furo works with the same extension.** Install `furo` and set
`html_theme = 'furo'` in `conf.py`. Icons follow the surrounding text colour in
both light and dark themes.

HTML builds include inline SVGs and the stylesheet automatically. Other output
formats use the label or a readable icon name as text; they do not render icons.

[View the Sphinx example](examples/sphinx/index.rst).

## Quarto

Install the package, then run `blender-icons quarto` from your Quarto project
folder or the folder containing your `.qmd` file:

```sh
pip install blender-doc-icons
blender-icons quarto
```

This creates `_extensions/blender-icons`. Quarto discovers the extension
automatically, so you can start using its shortcode:

```markdown
Open {{< blender scene_data >}} **Scene Properties**.
Labelled icon: {{< blender camera_data label="Camera Properties" >}}.
```

Keep the generated extension with your documentation. Rendering requires
**Quarto 1.4 or later**, but no Python installation or network connection.
HTML output includes inline SVGs and CSS; other formats, including PDF and Word,
use the label or a readable name such as `[scene data]`.

To choose another destination:

```sh
blender-icons quarto --output my-docs/_extensions/blender-icons
```

Run the export command again after updating the package or your custom icons.
It replaces matching generated files. To show literal shortcodes in fenced code
examples, add the Quarto code-block attribute `shortcodes=false`.

[View the Quarto example](examples/quarto/index.qmd).

## Find an icon

Search the installed collection by name:

```sh
blender-icons list camera
blender-icons list modifier
# List every available icon:
blender-icons list
```

You can also browse the [Blender icon browser](https://ui.blender.org/icons) for
visual reference. The installed collection may differ from the browser’s Blender
version; `blender-icons list` shows the names available in your package.

Names are case-insensitive: `SCENE_DATA` and `scene_data` refer to the same icon.
Use the name without a `blender_icon_` prefix or `.svg` suffix. Unknown names
produce an error so missing icons do not silently disappear from your docs.

## Styling and accessible labels

Inline icons default to **1em high** and inherit the surrounding text colour.
Add this to your documentation’s custom CSS to adjust them:

```css
.blender-icon {
  --blender-icon-size: 1.1em;
  --blender-icon-color: #9d60bd;
}
```

Omit `--blender-icon-color` to keep automatic colour inheritance in light and dark
themes.

Icons without labels are decorative and hidden from screen readers. Add a label
when an icon communicates something that the adjacent text does not explain:

| Integration | Label syntax |
| --- | --- |
| MkDocs / Python-Markdown | `:blender-camera_data\|Camera:` |
| Sphinx | `` :blender-icon:`camera_data\|Camera` `` |
| MyST | `` {blender-icon}`camera_data\|Camera` `` |
| Quarto | `{{< blender camera_data label="Camera" >}}` |

In the MkDocs and Python-Markdown syntax, labels cannot contain colons or line
breaks.

## Custom icons

Add your own SVGs or override a bundled icon by using the same filename. Use
lowercase filenames, such as `my_icon.svg`, containing letters, digits, and
underscores. Each SVG must have an SVG namespace and a `viewBox`.

**MkDocs** — set a directory relative to `mkdocs.yml`:

```yaml
plugins:
  - blender-icons:
      icon_dir: docs/custom_icons
```

**Sphinx / Furo** — set a directory relative to your Sphinx source folder:

```python
# conf.py
blender_icons_dir = 'custom_icons'
```

**Quarto** — include your custom icons when exporting the extension:

```sh
blender-icons --icon-dir custom_icons quarto
```

The file `my_icon.svg` is then available as `my_icon` using your platform’s normal
icon syntax. Quarto captures a copy at export time; re-export after making changes.
Use trusted SVG files: normalization is not a sanitizer for untrusted uploads.

## Python-Markdown

For Python-Markdown without MkDocs:

```sh
pip install 'blender-doc-icons[markdown]'
```

```python
import markdown
from blender_doc_icons import get_css

html = markdown.markdown(
    'Open :blender-scene_data: Scene Properties.',
    extensions=['blender_doc_icons.markdown'],
)
css = get_css()  # Include once in your page stylesheet.
```

This extension is for Python-Markdown. For other Markdown engines, such as
markdown-it or MDX, use exported SVG files or integrate the Python API.

## Export SVG files

Use standalone images in a GitHub README or other documentation tool:

```sh
pip install blender-doc-icons
blender-icons export scene_data camera_data --output icons --color '#5e5e5e'
```

Then reference a file:

```html
<img src="icons/scene_data.svg" width="16" alt="Scene Properties">
```

Omit icon names to export the whole collection. The command also writes CSS,
attribution notes, and the artwork licence. Matching files in the output folder
are replaced.

Exported images use an explicit colour because SVGs displayed through `<img>`
do not inherit the page’s text colour. Use an inline integration for automatic
light/dark theme colours.

## Python API

The core API has no third-party Python dependencies:

```python
from blender_doc_icons import get_css, get_svg, list_icons, render_html

names = list_icons()
svg = get_svg('scene_data')
html = render_html('camera_data', label='Camera')
css = get_css()
```

`get_svg()` returns SVG artwork. `render_html()` adds the inline wrapper,
accessibility attributes, and unique SVG IDs. Include `get_css()` once in your
page stylesheet when using the HTML output.

For custom icons:

```python
from blender_doc_icons import IconRegistry

icons = IconRegistry(icon_dir='custom_icons')
html = icons.render_html('my_icon', label='My tool')
```

## Credits and licence

Originally developed for [Microscopy Nodes](https://github.com/aafkegros/MicroscopyNodes)
to make Blender tutorials easier to follow.

The package code is **MIT licensed**. The Blender icon artwork is
**CC-BY-SA 4.0**. Include this credit in documentation or publications using the
icons:

> Blender icons designed by [@jenzdrich](https://blenderartists.org/t/new-icons-for-blender-2-8/1112701), used under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). SVGs adapted for documentation by blender-doc-icons.

See [NOTICE.md](NOTICE.md) for artwork sources and modifications,
[LICENSE](LICENSE) for the code licence, and
[CC-BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt) for the artwork licence.
