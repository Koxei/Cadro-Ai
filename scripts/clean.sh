#!/bin/bash

# Navigate to the script's directory
cd "$(dirname "$0")"/..

# Find and remove node_modules directories and pnpm-lock.yaml file
find . -type d -name "node_modules" -exec rm -rf {} + \
    -o -type f -name "pnpm-lock.yaml" -exec rm -f {} +

echo "Cleanup finished."