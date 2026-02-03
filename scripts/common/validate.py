#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.common import io


from typing import Optional


def validate_all(themes_dir: Path, spec_file: Path, theme: Optional[str] = None):
    if not themes_dir.is_dir():
        raise FileNotFoundError(f"Themes directory missing: {themes_dir}")

    spec = io.load_spec(str(spec_file))
    files = sorted(themes_dir.iterdir())
    if not files:
        raise FileNotFoundError("No theme files found to validate.")

    errors = []
    validated = 0

    for path in files:
        if path.name.startswith(".") or path.is_dir():
            continue
        if theme and path.name != theme:
            continue
        text = path.read_text(encoding="utf-8")
        issues = spec.validate(text)
        if not isinstance(issues, list):
            raise TypeError(f"validate() must return list, got {type(issues)} for {path}")
        if issues:
            errors.append((path, issues))
        else:
            validated += 1

    return validated, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--themes-dir", required=True)
    parser.add_argument("--spec", required=True)
    args = parser.parse_args()

    validated, errors = validate_all(Path(args.themes_dir), Path(args.spec))

    for path, issues in errors:
        print(f"Invalid theme: {path}")
        for issue in issues:
            print(f"  {issue}")

    if errors:
        print(f"Validation failed for {len(errors)} theme(s).", file=sys.stderr)
        return 1

    print(f"Validated {validated} theme(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
