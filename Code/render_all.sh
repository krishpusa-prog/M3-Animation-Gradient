#!/usr/bin/env bash
# Render each scene, then concatenate in storyboard order.
set -euo pipefail
cd "$(dirname "$0")"
scenes=(Scene0Opening Scene1Hook Scene2Concept Scene3Intuition Scene4Example Scene5Meaning Scene6Credits)
files=()
for scene in "${scenes[@]}"; do
  manim -qh scenes.py "$scene"
  found=$(find media/videos/scenes/1080p60 -name "${scene}.mp4" -print -quit)
  [[ -n "$found" ]] || { echo "Missing render: $scene" >&2; exit 1; }
  files+=("$found")
done
list=$(mktemp)
for f in "${files[@]}"; do printf "file '%s'\n" "$(cd "$(dirname "$f")" && pwd)/$(basename "$f")" >> "$list"; done
ffmpeg -f concat -safe 0 -i "$list" -c:v libx264 -pix_fmt yuv420p -movflags +faststart ../E25B070877_Video.mp4
rm -f "$list"
