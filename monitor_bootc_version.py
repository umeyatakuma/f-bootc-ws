#!/usr/bin/env python3
"""
Monitor Fedora bootc container image for version updates.
When a new version is detected, update bootc_version.txt and commit to git.
"""

import json
import subprocess
import sys
from pathlib import Path


CONTAINER_IMAGE = "docker://registry.fedoraproject.org/fedora-bootc:latest"
REPO_DIR = Path.home() / "git" / "f-bootc-ws"
VERSION_FILE = REPO_DIR / "bootc_version.txt"


def run_command(cmd, capture_output=True, check=True, cwd=None):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture_output,
            text=True,
            check=check,
            cwd=cwd
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(cmd)}: {e}", file=sys.stderr)
        if e.stderr:
            print(f"stderr: {e.stderr}", file=sys.stderr)
        raise


def get_remote_version():
    """Get the current version of the remote container image using skopeo."""
    print(f"Inspecting remote image: {CONTAINER_IMAGE}")
    result = run_command(["skopeo", "inspect", CONTAINER_IMAGE])

    metadata = json.loads(result.stdout)
    version = metadata.get("Labels", {}).get("org.opencontainers.image.version")

    if not version:
        raise ValueError("Could not find org.opencontainers.image.version in image metadata")

    return version


def get_local_version():
    """Read the currently stored version from the local file."""
    if not VERSION_FILE.exists():
        return None

    return VERSION_FILE.read_text().strip()


def update_version_file(version):
    """Write the new version to the version file."""
    VERSION_FILE.write_text(f"{version}\n")
    print(f"Updated {VERSION_FILE} with version: {version}")


def git_commit_and_push(version):
    """Commit and push the version file update."""
    # Add the version file
    run_command(["git", "add", "bootc_version.txt"], cwd=REPO_DIR)

    # Commit with a descriptive message
    commit_message = f"Update bootc version to {version}"
    run_command(["git", "commit", "-m", commit_message], cwd=REPO_DIR)
    print(f"Committed: {commit_message}")

    # Push to remote
    run_command(["git", "push"], cwd=REPO_DIR)
    print("Pushed to remote repository")


def main():
    """Main function to check for updates and commit if necessary."""
    try:
        # Get remote version
        remote_version = get_remote_version()
        print(f"Remote version: {remote_version}")

        # Get local version
        local_version = get_local_version()
        if local_version:
            print(f"Local version: {local_version}")
        else:
            print("No local version found (first run)")

        # Check if update is needed
        if remote_version == local_version:
            print("Version unchanged. No action needed.")
            return 0

        print(f"Version changed: {local_version} -> {remote_version}")

        # Update version file
        update_version_file(remote_version)

        # Commit and push
        git_commit_and_push(remote_version)

        print("Successfully updated and pushed bootc version")
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
