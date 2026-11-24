# Gradient — M3 Animation Video

**Student:** Kaustubh Kashyap (E25B070877)

A Manim Community Edition explainer on the gradient vector, directional derivatives, and level curves. The source targets Manim CE 0.19.0. Narration is supplied separately for recording or TTS; timing cues are in `Narration.md`. `Code/voiceover.py` demonstrates a swappable neural female TTS voice.

## Repository layout

```
M3_AnimationVideo_Gradient_E25B070877/
├── E25B070877_Video.mp4   # created by render script
├── Code/                  # scenes, helpers, config, dependencies, scripts
├── Storyboard.pdf
├── Storyboard.md
├── Narration.md
└── README.md
```

## Install and render

Install Python 3.10+ and FFmpeg, then create a virtual environment. In `Code/`, run `python -m pip install -r requirements.txt`, then `bash render_all.sh`. This renders each scene at Manim `-qh` quality (1080p) and joins them. The resulting silent video is placed at the project root. Record narration using the supplied script, then synchronize it in an editor; the supplied scenes are concise visual scaffolds and can be extended to match a full five-minute narration.

### Fast preview

`manim -pql scenes.py Scene4Example` (low quality, one scene).

### Windows

Install Python and FFmpeg, then in PowerShell: `py -m venv .venv`, activate with `.venv\Scripts\Activate.ps1`, `py -m pip install -r requirements.txt`. Use Git Bash or WSL to run `bash render_all.sh`; alternatively invoke each `manim -qh scenes.py SceneName` command and concatenate with FFmpeg.

### macOS / Linux

Install Python and FFmpeg with your package manager, create/activate a virtual environment (`python3 -m venv .venv`; `source .venv/bin/activate`), install dependencies, and run `bash render_all.sh`.

### Google Colab

Run `!apt-get update -qq && apt-get install -y ffmpeg libcairo2-dev libpango1.0-dev`, then `!pip install manim==0.19.0 edge-tts`. Upload this folder or clone its repository, `%cd` into `Code`, and use `!manim -pql scenes.py Scene4Example` for a preview. For the full render, run `!bash render_all.sh`. Download the resulting MP4 from the project folder.

## Voice-over

Record a human narration from `Narration.md`, or adapt `Code/voiceover.py` to synthesize each scene. The included sample uses `en-US-JennyNeural`, a warm, clear adult female voice, with slightly slower pacing. The scenes intentionally do not embed audio, so voice can be replaced without rerendering animation. If adding music, keep it low and credit the track and artist on the final frame.

## References to complete before submission

Replace the reference placeholder in Storyboard and the closing frame with the exact textbook/course notes actually used.

## Mathematical verification checklist

- `f=x²+2y²`; therefore `f_x=2x`, `f_y=4y`.
- At `(1,1)`, `∇f=(2,4)`.
- `|∇f|=√(2²+4²)=√20=2√5≈4.47`.
- For `(1,0)`, rate `2`; for `(0,1)`, rate `4`.
- For `(1,1)/√2`, rate `(2+4)/√2=3√2≈4.24`.
- For `(1,2)/√5`, rate `(2+8)/√5=10/√5=2√5≈4.47`, the maximum.
- `f(1,1)=3`, so the level curve is `x²+2y²=3`.
- Differentiating: `2x+4y y'=0`; hence `y'=-x/(2y)=-1/2` at `(1,1)`.
- Tangent direction `(2,-1)` satisfies `(2,4)·(2,-1)=4-4=0`.

## Viva preparation

1. **What is the gradient?** The vector of first partial derivatives, `(f_x,f_y)`.
2. **What do its components mean?** Local rates of change along the coordinate axes.
3. **Why use a unit direction in a directional derivative?** To compare change per unit distance.
4. **What does the dot product encode?** Alignment of the gradient with the chosen direction.
5. **Why is the gradient steepest increase?** `∇f·u=|∇f|cosθ` is largest when `θ=0`.
6. **What is the maximum rate?** `|∇f|`, attained in the gradient direction when nonzero.
7. **Why is the gradient perpendicular to a level curve?** Along the curve `f` is constant, so its tangent directional derivative is zero; the gradient is orthogonal to that tangent.
8. **What does the negative gradient do?** It points in the direction of steepest local decrease.
9. **What if f is not differentiable at the point?** A gradient may not exist, and the directional-rate formula may fail; analyze directions or use suitable generalized notions.
10. **When is the gradient zero?** At a stationary point; first-order change vanishes in every direction, but the point need not be a maximum or minimum.
