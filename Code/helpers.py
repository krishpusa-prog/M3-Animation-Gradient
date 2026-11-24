"""Beginner-friendly shared colors and small display helpers."""
from manim import *

# Keep these colors fixed throughout the video.
GRADIENT = GOLD
DIRECTION = BLUE
CONTOUR = TEAL

def title(text):
    """Create a consistent scene heading."""
    return Text(text, font_size=34, weight=BOLD).to_edge(UP)

def formula(text, color=WHITE, size=34):
    """Typeset a short formula using LaTeX."""
    return MathTex(text, color=color, font_size=size)
