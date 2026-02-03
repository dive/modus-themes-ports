#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.common import io


def render_all(palettes_dir: Path, mapping_file: Path, out_dir: Path, spec_file: Path):
    if not palettes_dir.is_dir():
        raise FileNotFoundError(f"Palettes directory missing: {palettes_dir}")
    mapping = io.load_mapping(str(mapping_file))
    spec = io.load_spec(str(spec_file))

    palette_files = sorted(palettes_dir.glob("*.json"))
    if not palette_files:
        raise FileNotFoundError("No palettes found. Run extract-palettes first.")

    outputs = []
    for palette_path in palette_files:
        theme_name, palette = io.load_palette(str(palette_path))
        content = spec.render(theme_name, palette, mapping)
        output_path = out_dir / theme_name
        io.write_output(str(output_path), content)
        outputs.append(output_path)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--palettes-dir", required=True)
    parser.add_argument("--mapping", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--spec", required=True)
    args = parser.parse_args()

    outputs = render_all(
        Path(args.palettes_dir),
        Path(args.mapping),
        Path(args.out_dir),
        Path(args.spec),
    )

    for output in outputs:
        print(f"Wrote {output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
