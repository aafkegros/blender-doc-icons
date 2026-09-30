# Blender icon attribution

All bundled icons were designed for Blender by
[@jenzdrich](https://blenderartists.org/t/new-icons-for-blender-2-8/1112701)
under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
The project-specific Microscopy Nodes icon is not included in this package.
The Python code is separately licensed under MIT; it does not relicense artwork.

## Recommended publication credit

Include this credit in documentation, publications, or other projects using the
icons (for example on the credits page):

> Blender icons designed by [@jenzdrich](https://blenderartists.org/t/new-icons-for-blender-2-8/1112701), used under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). SVGs adapted for documentation by blender-doc-icons (colour normalization and metadata cleanup).

If your publication also uses the separate Microscopy Nodes icon, use:

> All icons used except the Microscopy Nodes icon were designed for Blender by [@jenzdrich](https://blenderartists.org/t/new-icons-for-blender-2-8/1112701) under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Blender SVGs adapted for documentation by blender-doc-icons.

Retain attribution, the licence link, and an indication of modifications.
See `LICENSES/CC-BY-SA-4.0.txt` for the full licence terms. Custom icon directories
may have separate authors and licences. No endorsement by Blender is implied.

## Provenance

The initial 750-icon snapshot was imported on 2026-09-30 from MicroscopyNodes
`docs/html_blender_icons`. The maintainer confirmed that these SVGs originally
came from a clone of Blender itself and supplied the attribution above.
The exact original Blender revision is unknown; `assets/manifest.json` records
that explicitly, along with source and prepared SVG SHA-256 hashes.

Future imports use Blender's `release/datafiles/icons_svg` directory and record
an exact Git commit and source URL in the manifest. The refresh workflow does
not build Blender. Review added artwork and any changed upstream notices when
refreshing the catalogue.

## Modifications

Preparation removes editor metadata and fixed dimensions and normalizes solid
fill/stroke colours to currentColor, preserving `none`, transparency, and paint
references. Two legacy files without a viewBox (`char_replacement` and
`outliner_data_gp_layer`) receive `0 0 1600 1600`, consistent with their path
coordinates and the collection's standard canvas. Inline HTML gives SVG IDs
unique prefixes. Static export substitutes an explicit colour for currentColor.
