"""Import icons from an existing Blender Git checkout; no Blender build required."""
import argparse
from pathlib import Path
import subprocess

from prepare_icons import prepare_icons


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('checkout', type=Path, help='Root of a Blender Git checkout')
    args = parser.parse_args()
    revision = subprocess.check_output(
        ['git', '-C', str(args.checkout), 'rev-parse', 'HEAD'], text=True
    ).strip()
    source = args.checkout / 'release/datafiles/icons_svg'
    prepare_icons(
        source,
        source_description=f'https://github.com/blender/blender/tree/{revision}/release/datafiles/icons_svg',
        upstream_revision=revision,
    )


if __name__ == '__main__':
    main()
