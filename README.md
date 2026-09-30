# Blender documentation icons

Inline Blender SVG icons for **MkDocs**, **Python-Markdown**, and **Sphinx**,
with a dependency-free Python API and static SVG export for other platforms.
No Blender installation, JavaScript, Material theme, or network access is needed
when building documentation.

## MkDocs

```sh
pip install 'blender-doc-icons[mkdocs]'
```

```yaml
# mkdocs.yml
plugins:
  - search
  - blender-icons
```

```markdown
Open :blender-scene_data: **Scene Properties**.

An icon with an accessible label: :blender-camera_data|Camera:.
```

The plugin enables the Markdown extension and supplies its stylesheet. Do not
also enable the Markdown extension separately. Unknown icon names fail the build.
Use lowercase Blender icon names, without a `blender_icon_` prefix or `.svg` suffix.
Inline and fenced code examples retain their literal syntax.

### Custom icons and styling

```yaml
plugins:
  - blender-icons:
      icon_dir: docs/custom_icons
```

`icon_dir` is relative to `mkdocs.yml`. A file `microscopy_nodes.svg` becomes
`:blender-microscopy_nodes:`. Custom icons override bundled icons with the same
name and must have an SVG namespace and `viewBox`. These are trusted local assets,
not user uploads; the SVG normalizer is not a security sanitizer.

Icons inherit text colour and use a height of `1em`. Optional CSS:

```css
.blender-icon {
  --blender-icon-size: 1.1em;
  --blender-icon-color: #9d60bd;
}
```

Unlabelled icons are decorative (`aria-hidden`). Use a label after `|` when the
icon conveys information that is not already present in adjacent text. Labels
cannot contain colons or line breaks in Markdown syntax.

## Sphinx, including MyST

```sh
pip install 'blender-doc-icons[sphinx]'
```

```python
# conf.py
extensions = ['blender_doc_icons.sphinx']
# Optional, relative to the Sphinx source directory:
# blender_icons_dir = 'custom_icons'
```

reStructuredText:

```rst
Open :blender-icon:`scene_data` Scene Properties.
Labelled icon: :blender-icon:`camera_data|Camera`.
```

MyST Markdown (install and enable `myst_parser` separately):

```markdown
Open {blender-icon}`scene_data` Scene Properties.
```

HTML builds receive inline SVGs and CSS. Other builders receive the label or a
readable icon name, rather than an image; PDF icon rendering is not implemented.

## Python-Markdown without MkDocs

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

This integration supports Python-Markdown, not every Markdown engine. Platforms
such as markdown-it or MDX need their own adapter or exported images.

## Python API and static export

```sh
pip install blender-doc-icons
blender-icons list camera
blender-icons export scene_data camera_data --output icons --color '#5e5e5e'
# Omit names to export the entire catalogue.
```

```python
from blender_doc_icons import get_svg, list_icons, render_html, get_css

svg = get_svg('scene_data')
html = render_html('camera_data', label='Camera')
```

For a local collection, use `IconRegistry(icon_dir='my-icons')` and its
`list_icons()`, `get_svg()`, and `render_html()` methods.

The export command writes SVGs, CSS, attribution notes, and the artwork licence; files with matching
names in the output directory are replaced. Exported SVGs have an explicit colour
because `<img>` content does not inherit page text colour. For a GitHub README:

```html
<img src="icons/scene_data.svg" width="16" alt="Scene Properties">
```

## Developing and publishing

From this repository:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python -m unittest discover -s tests
mkdocs build --strict -f examples/mkdocs/mkdocs.yml
sphinx-build -W -b html examples/sphinx examples/sphinx/_build/html
python -m build
python -m twine check dist/*
```

Before the first public release, confirm the distribution name is available
on PyPI and update package metadata
with your repository URL. The Python code is MIT licensed; third-party artwork
has separate terms. The original Blender revision is currently unknown and is
recorded as such in the bundled manifest. No Blender-version compatibility claim
is made for this snapshot.

Upload to TestPyPI first, then PyPI:

```sh
python -m twine upload --repository testpypi dist/*
python -m twine upload dist/*
```

To refresh the trusted artwork after installing this package in editable mode:

```sh
python tools/prepare_icons.py /path/to/icons \
  --source-description 'Exact source URL and release' \
  --upstream-revision 'Exact upstream tag or commit'
```

The importer removes editor metadata, normalizes solid fills/strokes to
`currentColor`, preserves `none` and paint-server references, and records hashes.
It excludes the project-specific `microscopy_nodes` icon. Two legacy source files
without a viewBox receive an explicitly recorded 1600-unit canvas repair.
Review upstream changes and licensing before publishing a refreshed collection.

## Migrating Microscopy Nodes

Replace `{{ svg("scene_data") }}` with `:blender-scene_data:` and configure the
plugin. Keep `microscopy_nodes.svg` in a custom icon directory. Leave YouTube
macros in your project; the icon plugin does not depend on mkdocs-macros.
Replace `.icon` / `.small-icon` styling with `.blender-icon` styling as needed.
The source project is not automatically modified by this package.

## Updating directly from Blender

On GitHub, run **Actions → Refresh Blender icons → Run workflow** and enter a
Blender tag or commit (for example `v4.5.0`). The workflow sparsely checks out
`blender/blender`, reads `release/datafiles/icons_svg`, cleans the icons, and
uploads the generated assets, manifest, wheel, and source distribution as a
reviewable artifact. It does not commit, open a PR, or publish to PyPI.

Download the artifact, review the icon changes, replace the package's generated
`assets/icons` directory and `assets/manifest.json`, and commit the update.
Replace the directory as a whole so deleted upstream icons do not linger.
The manifest records the actual Git commit even if the workflow input was a tag.
Review upstream licence/attribution changes when adding new artwork.

For an existing local Blender checkout:

```sh
PYTHONPATH=src python tools/import_blender.py /path/to/blender
```

The importer accepts current icon names and strips `blender_icon_` from filenames
when present; dots in source names become underscores (for example
`light.inline.svg` becomes `light_inline`). It validates the new collection before writing and removes obsolete
generated icons. A missing source directory or unsupported SVG fails explicitly;
there is no silent fallback to stale assets. No Blender binary is needed.

## Attribution in publications

The Blender icons are **CC-BY-SA 4.0**; the package code is **MIT**. Include this
credit in documentation or publications using the icons:

> Blender icons designed by [@jenzdrich](https://blenderartists.org/t/new-icons-for-blender-2-8/1112701), used under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). SVGs adapted for documentation by blender-doc-icons.

See [NOTICE.md](NOTICE.md) for the original provenance, modification details, and
an alternative credit for publications that also use the Microscopy Nodes icon.
