"""Synthesize the narration with Microsoft's online neural voice and fit scenes to it.

The narration text is sent to Microsoft Edge's online TTS service.
Usage: python voiceover.py
"""
from __future__ import annotations

import asyncio
import json
import re
import subprocess
from pathlib import Path

import edge_tts

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "Narration.md"
OUT = HERE / "audio"
SCENES = [
    "Opening", "Scene1Hook", "Scene2Concept", "Scene3Intuition",
    "Scene4Example", "Scene5Meaning", "Scene6Credits",
]
HEADINGS = ["OPENING FRAME", "SCENE 1", "SCENE 2", "SCENE 3", "SCENE 4", "SCENE 5", "SCENE 6"]
VOICE = "en-US-AriaNeural"
RATE = "+15%"


def read_narration() -> list[str]:
    """Split the Markdown script into its seven spoken passages."""
    raw = SCRIPT.read_text(encoding="utf-8")
    positions = [raw.find(h) for h in HEADINGS]
    if any(p < 0 for p in positions):
        raise ValueError("Narration.md must contain the seven expected scene headings.")
    sections = []
    for i, start in enumerate(positions):
        end = positions[i + 1] if i + 1 < len(positions) else len(raw)
        body = raw[start:end]
        body = re.sub(r"^.*\n", "", body, count=1)
        body = re.sub(r"\[[^]]*\]", " ", body)
        body = re.sub(r"\s+", " ", body).strip()
        sections.append(body)
    return sections


async def synthesize(text: str, destination: Path) -> None:
    """Use Microsoft's Aria neural voice at a lightly lively speaking rate."""
    communicate = edge_tts.Communicate(text, voice=VOICE, rate=RATE, pitch="+0Hz", volume="+0%")
    await communicate.save(str(destination))


def run(*args: str) -> str:
    return subprocess.check_output(args, text=True).strip()


def main() -> None:
    OUT.mkdir(exist_ok=True)
    passages = read_narration()
    wavs = []
    durations = {}
    for scene, text in zip(SCENES, passages):
        source = OUT / f"{scene}-source.mp3"
        wav = OUT / f"{scene}.wav"
        print(f"Requesting Microsoft {VOICE} narration: {scene}")
        asyncio.run(synthesize(text, source))
        seconds = float(run("ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "default=noprint_wrappers=1:nokey=1", str(source)))
        # Preserve the generated speech. Add a short breath only; never time-stretch.
        tail = 0.35
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(source),
                        "-af", f"apad=pad_dur={tail},asetpts=PTS-STARTPTS",
                        "-ar", "48000", "-ac", "2", str(wav)], check=True)
        wavs.append(wav)
        durations[scene] = round(seconds + tail, 3)

    concat = OUT / "concat.txt"
    concat.write_text("".join(f"file '{p.name}'\n" for p in wavs), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(concat), "-c:a", "pcm_s16le", str(OUT / "narration.wav")], check=True)
    (OUT / "scene_durations.json").write_text(json.dumps(durations, indent=2) + "\n", encoding="utf-8")
    print(f"Narration ready: {OUT / 'narration.wav'} ({sum(durations.values()):.1f} seconds; {VOICE} {RATE})")


if __name__ == "__main__":
    main()
