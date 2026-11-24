# Gradient — M3 Animation Video

**Student:** Kaustubh Kashyap (E25B070877)  
**Format:** 16:9, 1920x1080, 60 fps, approximately five minutes  
**Software:** Manim Community Edition 0.19.0

This explainer introduces the gradient, directional derivatives, and level curves. Its editorial visual style uses warm paper, near-black typography, vermilion gradient arrows, blue direction arrows, and charcoal contours. A warm, confident adult female system voice narrates the lesson. Voice-over is synthesized locally; the narration is not uploaded. No background music is used.

## Project layout

```text
M3_AnimationVideo_Gradient_E25B070877/
├── E25B070877_Video.mp4       # rendered video, created by Code/render_all.sh
├── Code/
│   ├── scenes.py              # one Scene class for each storyboard scene
│   ├── helpers.py             # shared colors and layout helpers
│   ├── manim.cfg              # 1920x1080 render settings
│   ├── requirements.txt       # Manim CE and neural TTS dependencies
│   ├── voiceover.py           # creates and times female voice-over
│   └── render_all.sh          # renders and assembles the final MP4
├── Storyboard.pdf
├── Storyboard.md
├── Narration.md
└── README.md
```

## macOS setup and render

Install Python 3.9 or newer, Homebrew, and the native libraries Manim needs:

```bash
brew install ffmpeg cairo pango pkg-config
cd Code
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
bash render_all.sh
```

The script uses macOS Samantha, fits each narration passage to its scene duration, renders each scene at high quality, and combines the animation and voice into `E25B070877_Video.mp4` in the project root. You can replace the voice in `Code/voiceover.py`.

## Fast preview

From the `Code` folder with the virtual environment active:

```bash
manim -pql scenes.py Scene4Example
```

This renders only the worked example in low quality. For a preview with narration, run `python voiceover.py` first, then render the selected scene and combine its video with the matching file in `Code/audio/` using FFmpeg.

## Windows

Install Python 3.9+, FFmpeg, MiKTeX, and a Manim-compatible Cairo/Pango setup (MSYS2 is one option). In PowerShell, create and activate `.venv`, then run `python -m pip install -r requirements.txt`. The script uses a locally installed female SAPI voice. Use Git Bash or WSL for `bash render_all.sh`. For a quick check, run `manim -pql scenes.py Scene4Example` from `Code`.

## Linux

Install FFmpeg, Cairo/Pango development packages, and `espeak-ng` with your distribution's package manager. The equations use Unicode text, so no TeX installation is needed. Create a virtual environment, activate it, install `requirements.txt`, and run `bash render_all.sh` from `Code`.

## Google Colab

```python
!apt-get update -qq
!apt-get install -y ffmpeg libcairo2-dev libpango1.0-dev pkg-config espeak-ng
!apt-get install -y espeak-ng
!pip install manim==0.19.0
```

Upload or clone this project, change to its `Code` directory, and run `!manim -pql scenes.py Scene4Example` for a preview or `!bash render_all.sh` for the full render. Linux uses local `espeak-ng` voice `en-us+f3`. Download the finished MP4 from the project root.

## Voice-over and timing

`Narration.md` contains approximately 685 spoken words and action cues. The seven scenes are held to the storyboard timings of 8, 32, 45, 60, 85, 35, and 35 seconds (300 seconds total). `voiceover.py` synthesizes each passage separately with the operating system's local female voice and adjusts pacing slightly to fit the corresponding scene. For a personal recording, replace the generated audio files with your recordings, then use FFmpeg to fit each clip to the same scene durations. Keep any music low and add its track and artist credit to the final frame.

## Before submission

The closing frame cites OpenStax, *Calculus Volume 3*, Section 4.6, “Directional Derivatives and the Gradient.” Review the generated narration pronunciation and timing before submission.

## Mathematical verification checklist

- For `f=x²+2y²`, the partial derivatives are `f_x=2x` and `f_y=4y`.
- At `(1,1)`, `∇f=(2,4)`.
- `|∇f|=√(2²+4²)=√20=2√5≈4.47`.
- For unit direction `(1,0)`, the rate is `(2,4)·(1,0)=2`.
- For `(0,1)`, the rate is `4`.
- For `(1,1)/√2`, it is `(2+4)/√2=3√2≈4.24`.
- For `(1,2)/√5`, it is `(2+8)/√5=10/√5=2√5≈4.47`, the largest listed rate.
- Since `f(1,1)=3`, the level curve is `x²+2y²=3`.
- Implicit differentiation gives `2x+4y y'=0`, so `y'=-x/(2y)=-1/2` at `(1,1)`.
- Tangent direction `(2,-1)` is perpendicular because `(2,4)·(2,-1)=4-4=0`.

## Viva preparation

1. **What is the gradient?** The vector of first partial derivatives, `(f_x,f_y)`.
2. **What do its components mean?** Local rates of change in the coordinate directions.
3. **Why choose a unit vector for a directional derivative?** It compares change per unit distance.
4. **What does the dot product measure here?** Alignment between the gradient and chosen direction.
5. **Why is the gradient steepest increase?** `∇f·u=|∇f|cosθ` is largest when `θ=0`.
6. **What is the maximum directional rate?** `|∇f|`, when the gradient is nonzero.
7. **Why is the gradient perpendicular to a level curve?** The function is constant along it, so its tangent directional derivative is zero.
8. **What does the negative gradient do?** It points toward steepest local decrease.
9. **What if f is not differentiable at the point?** A gradient may not exist, and the directional-rate formula may fail.
10. **What if the gradient is zero?** First-order change is zero in every direction; the point can still be a saddle or another stationary point.
