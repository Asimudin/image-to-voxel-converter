#!/bin/bash
# Git commands to initialize and push your repository

echo "=== INITIALIZING GIT REPOSITORY ==="
git init

echo "=== ADDING FILES ==="
git add .

echo "=== FIRST COMMIT ==="
git commit -m "Initial commit: Image to Voxel Converter

- Added three conversion methods (height, color, structure)
- Implemented 3D visualization
- Added proper documentation and examples
- Processed sample image with 34,354 voxels (height method)"

echo "=== INSTRUCTIONS FOR GITHUB ==="
echo "1. Create a new repository on GitHub named 'image-to-voxel-converter'"
echo "2. Run these commands:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/image-to-voxel-converter.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Replace 'YOUR_USERNAME' with your actual GitHub username"

echo "=== REPOSITORY READY! ==="
