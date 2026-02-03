#!/usr/bin/env python3
import argparse
import importlib.util
import os
import sys


def load_spec(path: str):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Spec not found: {path}")
    spec = importlib.util.spec_from_file_location("tool_spec", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load spec: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "validate"):
        raise AttributeError("Spec missing validate(text) -> list[str]")
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--themes-dir", required=True)
    parser.add_argument("--spec", required=True)
    args = parser.parse_args()

    if not os.path.isdir(args.themes_dir):
        print(f"Error: themes directory missing: {args.themes_dir}", file=sys.stderr)
        return 1

    spec = load_spec(args.spec)

    files = sorted(os.listdir(args.themes_dir))
    if not files:
        print("Error: no theme files found to validate.", file=sys.stderr)
        return 1

    errors = 0
    validated = 0

    for filename in files:
        if filename.startswith("."):
            continue
        path = os.path.join(args.themes_dir, filename)
        if os.path.isdir(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        issues = spec.validate(text)
        if not isinstance(issues, list):
            print(f"Error: validate() must return list, got {type(issues)} for {path}", file=sys.stderr)
            return 1
        if issues:
            errors += 1
            print(f"Invalid theme: {path}")
            for issue in issues:
                print(f"  {issue}")
            continue
        validated += 1

    if errors:
        print(f"Validation failed for {errors} theme(s).", file=sys.stderr)
        return 1

    print(f"Validated {validated} theme(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
