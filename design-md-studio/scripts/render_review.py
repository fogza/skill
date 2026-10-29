#!/usr/bin/env python3
"""Render a review fragment or verify source fingerprints. Never saves DESIGN.md."""

import argparse
import hashlib
import json
import math
from pathlib import Path

GROUPS = {"colors", "typography", "rounded", "spacing", "components", "prose"}
ORIGINS = {"observed", "framework", "preset", "proposed", "confirmed"}
ROLES = {"background", "foreground", "primary", "primaryForeground", "muted", "mutedForeground", "body", "radius", "spacing"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":"))


def source_path(root, relative):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError("Sources must be nonempty paths relative to project_root")
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError("Source escapes project_root: " + relative)
    return path


def prepare(data):
    data = json.loads(canonical(data))
    data.pop("base_revision", None)
    data.pop("source_fingerprints", None)
    if not isinstance(data.get("project_root"), str) or not Path(data["project_root"]).is_absolute():
        raise ValueError("project_root must be an absolute directory")
    root = Path(data["project_root"]).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("project_root must be a directory")
    data["project_root"] = str(root)
    tokens = data["tokens"]
    if not isinstance(tokens, list):
        raise ValueError("tokens must be a list")
    ids = set()
    for item in tokens:
        for key in ("id", "path", "group", "origin"):
            if not isinstance(item.get(key), str) or not item[key]:
                raise ValueError("Missing entry field: " + key)
        if item["id"] in ids:
            raise ValueError("Duplicate entry ID: " + item["id"])
        ids.add(item["id"])
        if item["group"] not in GROUPS or item["origin"] not in ORIGINS:
            raise ValueError("Unknown group or origin")
        value = item["value"]
        item.setdefault("original_value", value)
        item.setdefault("original_path", item["path"])
        if isinstance(value, bool) or not isinstance(value, (str, int, float, dict)):
            raise ValueError("Entry value must be a string, finite number or object")
        if isinstance(value, (int, float)) and not math.isfinite(value):
            raise ValueError("Non-finite value")
        for key in ("theme", "source", "usage"):
            if key in item and not isinstance(item[key], str):
                raise ValueError(key + " must be a string")
    if not isinstance(data.get("bindings", {}), dict):
        raise ValueError("bindings must be an object")
    for theme, bindings in data.get("bindings", {}).items():
        if not isinstance(theme, str) or not isinstance(bindings, dict):
            raise ValueError("Invalid theme bindings")
        for role, token_id in bindings.items():
            if role not in ROLES or token_id not in ids:
                raise ValueError("Unknown preview role or ID: " + str(role))
    if not isinstance(data.get("labels", {}), dict) or any(not isinstance(v, str) for v in data.get("labels", {}).values()):
        raise ValueError("labels must map names to strings")
    sources = data.get("sources", [])
    if not isinstance(sources, list):
        raise ValueError("sources must be a list")
    data["source_fingerprints"] = [{"path": p, "sha256": digest(source_path(root, p))} for p in sources]
    data["base_revision"] = hashlib.sha256(canonical(data).encode()).hexdigest()[:16]
    return data


def render(data, output):
    prepared = prepare(data)
    output = Path(output)
    if output.suffix.lower() != ".html":
        raise ValueError("Review output must be an HTML fragment")
    if output.resolve().is_relative_to(Path(prepared["project_root"])):
        raise ValueError("Review artifacts must be outside project source")
    template = (Path(__file__).resolve().parent.parent / "assets" / "review.html").read_text(encoding="utf-8")
    if template.count("/*STUDIO_DATA*/ {}") != 1:
        raise ValueError("Review template must contain one data marker")
    payload = canonical(prepared).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    html = template.replace("/*STUDIO_DATA*/ {}", payload)
    with output.open("x", encoding="utf-8") as stream:
        stream.write(html)
    return prepared


def check_sources(state):
    root = Path(state["project_root"]).resolve(strict=True)
    if "source_fingerprints" not in state:
        raise ValueError("Prepared/submitted state with fingerprints is required")
    for item in state["source_fingerprints"]:
        path = source_path(root, item["path"])
        if not path.is_file() or digest(path) != item["sha256"]:
            raise ValueError("Source changed: " + item["path"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    review = sub.add_parser("render")
    review.add_argument("input", type=Path)
    review.add_argument("output", type=Path)
    check = sub.add_parser("check-sources")
    check.add_argument("state", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "render":
            state = render(json.loads(args.input.read_text(encoding="utf-8")), args.output)
            print(json.dumps({"path": str(args.output.resolve()), "base_revision": state["base_revision"], "source_fingerprints": state["source_fingerprints"]}))
        else:
            check_sources(json.loads(args.state.read_text(encoding="utf-8")))
            print("Source fingerprints match; destination must be checked separately.")
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(1, str(exc) + "\n")


if __name__ == "__main__":
    main()
