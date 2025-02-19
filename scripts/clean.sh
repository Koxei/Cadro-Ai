#!/bin/bash

# Navigate to the script's directories
cd "$(dirname "$0")"/..

# Find and remove node_modules directories and pnpm-lock.yaml files
find . -type d -name "node_modules" -exec rm -rf {} + \
    -o -type f -name "pnpm-lock.yaml" -exec rm -f {} +

echo "Cleanup finished."