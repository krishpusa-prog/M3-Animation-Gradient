"""Generate a local female voice-over and fit it to the five-minute storyboard.

All speech synthesis runs on the user's computer; narration is not uploaded.
macOS: Samantha (say). Windows: installed female SAPI voice. Linux: espeak-ng.
Usage: python voiceover.py
"""
from __future__ import annotations

import base64
import platform
import re
import subprocess
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "Narration.md"
OUT = HERE / "audio"
SCENES = [
    "Opening", "Scene1Hook", "Scene2Concept", "Scene3Intuition",
    "Scene4Example", "Scene5Meaning", "Scene6Credits",
]
HEADINGS = ["OPENING FRAME", "SCENE 1", "SCENE 2", "SCENE 3", "SCENE 4", "SCENE 5", "SCENE 6"]


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


def speak_locally(text: str, destination: Path) -> None:
    """Ask the operating system's built-in speech service to make a WAV file."""
    system = platform.system()
    if system == "Darwin":
        # Samantha is the built-in adult female English voice on macOS.
        subprocess.run(["say", "-v", "Samantha", "-r", "165", "-o", str(destination), text], check=True)
    elif system == "Linux":
        subprocess.run(["espeak-ng", "-v", "en-us+f3", "-s", "165", "-w", str(destination), text], check=True)
    elif system == "Windows":
        # PowerShell's local SAPI engine selects an installed female voice.
        script = (
            "$s=New-Object System.Speech.Synthesis.SpeechSynthesizer;"
            "$s.SelectVoiceByHints([System.Speech.Synthesis.VoiceGender]::Female);"
            f"$s.SetOutputToWaveFile('{str(destination).replace(chr(39), chr(39)*2)}');"
            f"$s.Speak(@'\n{text}\n'@);$s.Dispose()"
        )
        encoded = base64.b64encode(script.encode("utf-16le")).decode("ascii")
        subprocess.run(["powershell", "-NoProfile", "-EncodedCommand", encoded], check=True)
    else:
        raise RuntimeError(f"Unsupported operating system: {system}")


def run(*args: str) -> str:
    return subprocess.check_output(args, text=True).strip()


def main() -> None:
    OUT.mkdir(exist_ok=True)
    passages = read_narration()
    wavs = []
    durations = {}
    for scene, text in zip(SCENES, passages):
        source_suffix = ".aiff" if platform.system() == "Darwin" else ".wav"
        source = OUT / f"{scene}-source{source_suffix}"
        wav = OUT / f"{scene}.wav"
        print(f"Creating offline narration: {scene}")
        speak_locally(text, source)
        seconds = float(run("ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "default=noprint_wrappers=1:nokey=1", str(source)))
        # Keep the operating system voice at its natural generated speed. Add only
        # a short breath at the end of each passage; never time-stretch speech.
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
    print(f"Narration ready: {OUT / 'narration.wav'} ({sum(durations.values()):.1f} seconds; natural speed)")


if __name__ == "__main__":
    main()
