# Quarto example

From the repository root, after installing the package:

```sh
blender-icons quarto --output examples/quarto/_extensions/blender-icons
quarto render examples/quarto/index.qmd
# Exercise the text fallback without a TeX installation:
quarto render examples/quarto/index.qmd --to gfm
```

The exported extension includes the icon snapshot and stylesheet; Python is not
needed when rendering. Re-export after changing the package or custom icons.
