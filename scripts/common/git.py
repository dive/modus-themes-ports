#!/usr/bin/env python3
"""Git utilities for Modus theme ports."""

from __future__ import annotations

import os
import subprocess


def default_branch(remote_url: str) -> str:
    """Get the default branch name for a remote repository.

    Args:
        remote_url: URL of the remote repository.

    Returns:
        The default branch name (e.g., "main" or "master").
    """
    result = subprocess.run(
        ["git", "ls-remote", "--symref", remote_url, "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    for line in result.stdout.splitlines():
        if line.startswith("ref:"):
            ref = line.split()[1]
            return ref.replace("refs/heads/", "")
    return "master"


def subtree_update(repo_root: str, remote_url: str, prefix: str) -> None:
    """Add or update a git subtree.

    Args:
        repo_root: Path to the repository root.
        remote_url: URL of the remote repository.
        prefix: Subtree prefix path (relative to repo root).
    """
    branch = default_branch(remote_url)
    prefix_path = os.path.join(repo_root, prefix)
    if not os.path.isdir(prefix_path):
        subprocess.run(
            ["git", "subtree", "add", "--prefix", prefix, remote_url, branch, "--squash"],
            check=True,
            cwd=repo_root,
        )
    else:
        subprocess.run(
            ["git", "subtree", "pull", "--prefix", prefix, remote_url, branch, "--squash"],
            check=True,
            cwd=repo_root,
        )
