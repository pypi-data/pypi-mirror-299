#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status.

# Function to update version in a file
update_version() {
    sed -i "s/version = \".*\"/version = \"$1\"/" "$2"
    echo "Updated version in $2 to $1"
}

# Set the new version
NEW_VERSION="1.0.0"

# Update version in files
update_version $NEW_VERSION "pyproject.toml"
update_version $NEW_VERSION "setup.py"
update_version $NEW_VERSION "atomic-agents/atomic_agents/__init__.py"
update_version $NEW_VERSION "atomic-assembler/atomic_assembler/__init__.py"

# Build the consolidated package
echo "Building consolidated atomic-agents package..."
python -m build

# Upload to PyPI
echo "Uploading atomic-agents to PyPI..."
python -m twine upload dist/*

echo "Build and deploy process completed successfully!"
