#!/usr/bin/env bash
# Render all seven audio-timed scenes and combine them with natural-speed narration.
set -euo pipefail
cd "$(dirname "$0")"
if [[ -x ".venv/bin/manim" ]]; then
  PATH="$PWD/.venv/bin:/opt/homebrew/bin:$PATH"
fi
export PATH

scenes=(Scene0Opening Scene1Hook Scene2Concept Scene3Intuition Scene4Example Scene5Meaning Scene6Credits)
mkdir -p audio
if [[ ! -f audio/narration.wav ]]; then
  python voiceover.py
fi

videos=()
for scene in "${scenes[@]}"; do
  manim -qh --disable_caching scenes.py "$scene"
  video="media/videos/scenes/1080p60/${scene}.mp4"
  [[ -n "$video" ]] || { echo "Could not find render for $scene" >&2; exit 1; }
  videos+=("$video")
done

list=$(mktemp)
trap 'rm -f "$list"' EXIT
for video in "${videos[@]}"; do
  absolute=$(cd "$(dirname "$video")" && pwd)/$(basename "$video")
  printf "file '%s'\n" "$absolute" >> "$list"
done

ffmpeg -y -f concat -safe 0 -i "$list" -i audio/narration.wav \
  -map 0:v:0 -map 1:a:0 -c:v libx264 -preset medium -crf 18 \
  -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart \
  ../E25B070877_Video.mp4
echo "Created ../E25B070877_Video.mp4"
