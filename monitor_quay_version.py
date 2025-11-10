#!/usr/bin/env python3
"""
Monitor Quay.io repository for version updates.
When a new version is detected, update f-bootc-ws_version.txt and commit to git.
"""

import json
import subprocess
import sys
import urllib.request
import urllib.error
from pathlib import Path


QUAY_REPO_OWNER = "umeyatakuma"
QUAY_REPO_NAME = "f-bootc-ws"
QUAY_API_URL = f"https://quay.io/api/v1/repository/{QUAY_REPO_OWNER}/{QUAY_REPO_NAME}/tag/"

# Automatically detect the repository directory from the script's location
REPO_DIR = Path(__file__).resolve().parent
# Store version file in cache directory
CACHE_DIR = Path.home() / ".cache" / "f-bootc-ws"
VERSION_FILE = CACHE_DIR / "f-bootc-quay-img_version.txt"


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
    """Get the latest SHA256 digest from Quay.io repository using the API."""
    print(f"Querying Quay.io API: {QUAY_API_URL}")

    try:
        with urllib.request.urlopen(QUAY_API_URL) as response:
            data = json.loads(response.read().decode())

        tags = data.get("tags", [])
        if not tags:
            raise ValueError("No tags found in repository")

        # Filter to get only current tags (those without an end_ts)
        # and exclude 'latest' tag to get the main branch
        current_tags = [
            tag for tag in tags
            if tag.get("name") != "latest" and "end_ts" not in tag
        ]

        if not current_tags:
            raise ValueError("No current versioned tags found in repository")

        # Sort by last_modified (most recent first) and get the latest
        latest_tag = max(current_tags, key=lambda x: x.get("last_modified", ""))
        manifest_digest = latest_tag.get("manifest_digest")

        if not manifest_digest:
            raise ValueError("Could not determine manifest_digest from tag data")

        # Extract SHA256 hash and get first 12 characters
        # Format: "sha256:308249b9f13614a1cb3eb83a33d9884d9525f0135f0b83596b176db1f1db2dad"
        if manifest_digest.startswith("sha256:"):
            sha256_hash = manifest_digest[7:]  # Remove "sha256:" prefix
            version = sha256_hash[:12]  # Get first 12 characters
        else:
            raise ValueError(f"Unexpected manifest_digest format: {manifest_digest}")

        return version

    except urllib.error.HTTPError as e:
        raise ValueError(f"HTTP error accessing Quay.io API: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        raise ValueError(f"URL error accessing Quay.io API: {e.reason}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON response from Quay.io API: {e}")


def get_local_version():
    """Read the currently stored version from the local file."""
    if not VERSION_FILE.exists():
        return None
    return VERSION_FILE.read_text().strip()


def update_version_file(version):
    """Write the new version to the version file."""
    # Create cache directory if it doesn't exist
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    VERSION_FILE.write_text(f"{version}\n")
    print(f"Updated {VERSION_FILE} with version: {version}")


def main():
    """Main function to check for updates."""
    try:
        # Get remote version
        remote_version = get_remote_version()
        print(f"Remote version: {remote_version}")

        # Get local version
        local_version = get_local_version()

        # Compare versions
        if remote_version == local_version:
            return 0

        # Update version file
        update_version_file(remote_version)

        print("Successfully updated f-bootc-ws version")
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
