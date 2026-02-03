#!/usr/bin/env python3
import os
import subprocess


def default_branch(remote_url: str) -> str:
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


def subtree_update(repo_root: str, remote_url: str, prefix: str):
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
