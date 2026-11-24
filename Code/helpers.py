"""Beginner-friendly shared colors and small display helpers."""
from manim import *

# Editorial palette inspired by the user's references. Keep math roles consistent.
BG = "#F4F1EA"        # warm paper
INK = "#171719"       # near-black type and level curves
GRADIENT = "#EF3F35"  # vermilion: gradient / steepest ascent
DIRECTION = "#2389B8"  # restrained bright blue: test direction u
CONTOUR = "#25262A"   # charcoal: level curves
ACCENT = "#EF3F35"    # vermilion: editorial rules and callouts
MUTED = "#5C5C60"

# Manim defaults to white lettering. Set dark ink for this light paper canvas;
# objects with a specific math-role color still override these defaults.
Text.set_default(color=INK, font="Avenir Next")

def title(text):
    """Create a consistent heading with a bright coral underline."""
    heading = Text(text, font_size=35, weight=BOLD, color=INK, font="Avenir Next")
    underline = Line(LEFT*2.2, RIGHT*2.2, color=ACCENT, stroke_width=4)
    block = VGroup(heading, underline).arrange(DOWN, buff=.12)
    return block.to_edge(UP, buff=.22)

def formula(text, color=WHITE, size=34):
    """Display a Unicode math formula without a separate TeX installation."""
    return Text(text, color=color, font_size=size)
