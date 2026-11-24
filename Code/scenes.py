"""Seven Manim scenes for the five-minute gradient explainer.

Render with: manim -qh scenes.py Scene0Opening
The shell script renders all scenes in order and builds the final MP4.
Each scene holds its closing frame until its storyboard time has elapsed.
"""
import json
from pathlib import Path

from manim import *
from helpers import *

BG = "#F4F1EA"


def scene_seconds(scene, fallback):
    """Read the matching natural voice duration written by voiceover.py."""
    names = {"Scene0Opening": "Opening"}
    audio_name = names.get(scene.__class__.__name__, scene.__class__.__name__)
    path = Path(__file__).parent / "audio" / "scene_durations.json"
    try:
        return json.loads(path.read_text())[audio_name]
    except (OSError, KeyError, ValueError):
        return fallback


def finish_scene(scene, fallback):
    """End at the audio's natural duration; never stretch narration to a template."""
    remaining = scene_seconds(scene, fallback) - scene.time
    if remaining > 0.08:
        scene.wait(remaining)


def reveal_equation_beats(scene, entries, duration):
    """Replace one bold equation card at a time, paced to the spoken example."""
    weights = [entry[2] for entry in entries]
    total_weight = sum(weights)
    old = None
    used = scene.time
    for text, color, weight in entries:
        beat = duration * weight / total_weight
        card = Text(text, font_size=36, weight=MEDIUM, color=color, line_spacing=.9)
        card.move_to(RIGHT * 2.15 + DOWN * .2)
        if old is None:
            scene.play(FadeIn(card, shift=RIGHT*.45), run_time=.55)
        else:
            scene.play(ReplacementTransform(old, card), run_time=.55)
        hold = max(.12, beat - .55)
        scene.wait(hold)
        used += beat
        old = card


class Scene0Opening(Scene):
    def construct(self):
        self.camera.background_color = BG
        title_text = Text("THE", font_size=35, weight=BOLD).move_to(RIGHT*1.55+UP*.75)
        title_gradient = Text("GRADIENT", font_size=82, color=INK, weight=BOLD).next_to(title_text, DOWN, aligned_edge=LEFT, buff=.05)
        subtitle = Text("THE DIRECTION OF STEEPEST INCREASE", font_size=20, color=GRADIENT, weight=BOLD).next_to(title_gradient, DOWN, aligned_edge=LEFT, buff=.2)
        student = Text("KAUSTUBH KASHYAP   /   E25B070877", font_size=18, color=MUTED).next_to(subtitle, DOWN, aligned_edge=LEFT, buff=.48)
        VGroup(title_text, title_gradient, subtitle, student).shift(LEFT*.5)
        title_block = VGroup(title_text, title_gradient, subtitle, student)
        rings = VGroup(*[Circle(radius=r, color=CONTOUR, stroke_opacity=.55, stroke_width=2.5)
                         for r in (0.8, 1.28, 1.76, 2.24)]).shift(LEFT*4.2)
        arrow = Arrow(LEFT*4.2, LEFT*3.35+UP*1.5, color=GRADIENT, buff=0, stroke_width=7)
        index = Text("01", font_size=21, color=GRADIENT, weight=BOLD).to_corner(UL, buff=.4)
        self.add(index)
        self.play(Create(rings), run_time=.8)
        self.play(GrowArrow(arrow), FadeIn(title_text, shift=RIGHT*.4), run_time=.7)
        self.play(FadeIn(title_gradient, shift=RIGHT*.65), run_time=.9)
        self.play(FadeIn(subtitle, shift=UP*.12), run_time=.45)
        self.play(FadeIn(student, shift=UP*.12), run_time=.45)
        self.play(rings.animate.scale(1.16), arrow.animate.shift(UP*.12), run_time=1.2, rate_func=there_and_back)
        finish_scene(self, 12)


class Scene1Hook(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(title("Which way is uphill?"))
        axes = Axes(x_range=[-3, 3], y_range=[-2.5, 2.5], x_length=6.3, y_length=4.7,
                    tips=False, axis_config={"color": "#B8B5AF"}).shift(LEFT*2.8+DOWN*.2)
        contours = VGroup(*[Ellipse(width=w, height=h, color=CONTOUR, stroke_width=3)
                            for w, h in ((1.0,.65),(1.8,1.15),(2.7,1.75),(3.7,2.4))])
        contours.move_to(axes.c2p(0, 0))
        point = Dot(axes.c2p(.45,.3), color=INK, radius=.09)
        label = Text("P", font_size=23).next_to(point, UR, buff=.08)
        uphill_halo = Arrow(point.get_center(), point.get_center()+RIGHT*.7+UP*1.0,
                            color=GRADIENT, buff=.05, stroke_width=18, stroke_opacity=.16)
        uphill = Arrow(point.get_center(), point.get_center()+RIGHT*.7+UP*1.0,
                       color=GRADIENT, buff=.05, stroke_width=5)
        caption = VGroup(Text("Contour lines", font_size=27, color=CONTOUR),
                         Text("= equal height", font_size=24)).arrange(DOWN, aligned_edge=LEFT)
        caption.to_edge(RIGHT).shift(LEFT*.3+UP*.6)
        prompt = Text("Find the fastest local climb.", font_size=22, color=MUTED)
        prompt.next_to(caption, DOWN, buff=.45).align_to(caption, RIGHT)
        spacing_note = Text("CLOSE CONTOURS  /  STEEPER GROUND", font_size=16, color=GRADIENT, weight=BOLD)
        spacing_note.next_to(prompt, DOWN, buff=.32).align_to(prompt, RIGHT)
        self.play(Create(axes), run_time=1)
        self.play(LaggedStart(*[Create(c) for c in contours], lag_ratio=.15), run_time=1.5)
        self.play(FadeIn(point, label), FadeIn(caption), Write(prompt), FadeIn(spacing_note), run_time=1)
        self.play(GrowArrow(uphill_halo), GrowArrow(uphill), run_time=1)
        self.play(Indicate(point, color=ACCENT, scale_factor=1.7), run_time=.45)
        # Let the eye travel uphill as the question is asked; a dotted trail
        # makes the direction legible even on a small phone screen.
        traveler = Dot(point.get_center(), radius=.075, color=DIRECTION)
        trail = TracedPath(traveler.get_center, stroke_color=DIRECTION, stroke_width=3, dissipating_time=1.5)
        self.add(trail, traveler)
        for destination in (point.get_center()+RIGHT*.25+UP*.3,
                            point.get_center()+RIGHT*.48+UP*.66,
                            point.get_center()+RIGHT*.7+UP*1.0):
            self.play(traveler.animate.move_to(destination), run_time=.75, rate_func=smooth)
        stamp = Text("UPHILL?", font_size=53, color=GRADIENT, weight=BOLD).rotate(-PI/2).to_edge(RIGHT, buff=.08)
        self.play(FadeIn(stamp, scale=1.3), run_time=.45)
        finish_scene(self, 20)


class Scene2Concept(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(title("From partial derivatives to a vector"))
        intro = Text("Let x and y describe horizontal position; f gives height.", font_size=25).move_to(UP*1.45)
        fx = Text("fₓ = ∂f/∂x   (y held fixed)", font_size=29).move_to(UP*.62)
        fy = Text("fᵧ = ∂f/∂y   (x held fixed)", font_size=29).move_to(DOWN*.08)
        component_note = Text("Each component is a signed slope along one axis.", font_size=21, color=DIRECTION).move_to(LEFT*3.65+DOWN*.5)
        nabla = Text("∇  NABLA", font_size=20, weight=BOLD, color=GRADIENT).move_to(LEFT*3.65+DOWN*1.15)
        vector = Text("∇f = (fₓ, fᵧ)", font_size=45, weight=BOLD, color=GRADIENT).move_to(RIGHT*.55+DOWN*1.18)
        expansion = Text("= (∂f/∂x, ∂f/∂y)", font_size=27, color=GRADIENT).next_to(vector, DOWN, buff=.2)
        self.play(FadeIn(intro, shift=UP*.12), run_time=.45)
        self.wait(2)
        self.play(FadeIn(fx, shift=RIGHT*.2), run_time=.45)
        self.play(Indicate(fx, color=DIRECTION, scale_factor=1.045), run_time=.45)
        self.wait(2.4)
        self.play(FadeIn(fy, shift=RIGHT*.2), run_time=.45)
        self.play(Indicate(fy, color=DIRECTION, scale_factor=1.045), run_time=.45)
        self.play(FadeIn(component_note, shift=UP*.08), run_time=.45)
        self.wait(2.8)
        self.play(FadeIn(nabla, shift=LEFT*.2), run_time=.45)
        self.wait(1)
        self.play(FadeIn(vector, shift=RIGHT*.25), run_time=.55)
        self.play(Indicate(vector, color=ACCENT, scale_factor=1.055), run_time=.55)
        self.wait(2.8)
        self.play(FadeIn(expansion, shift=DOWN*.12), run_time=.45)
        self.wait(1.2)
        zero_note = Text("∇f = 0  /  0 FIRST-ORDER RATE", font_size=18, color=DIRECTION, weight=BOLD)
        zero_note.move_to(LEFT*3.25+DOWN*2.18)
        self.play(FadeIn(zero_note, shift=RIGHT*.18), run_time=.45)
        objective = Text(
            "By the end of this video, the viewer will be able to explain what the gradient vector\n"
            "of a two-variable function is, compute it from partial derivatives, and justify why it\n"
            "points in the direction of steepest increase.",
            font_size=18, color=DIRECTION, line_spacing=.85,
        ).to_edge(DOWN, buff=.2)
        self.play(FadeIn(objective), run_time=.7)
        self.wait(2.5)
        self.play(FadeOut(objective, shift=DOWN*.15), run_time=.4)
        box = SurroundingRectangle(vector, color=ACCENT, buff=.16, stroke_width=2)
        self.play(Create(box), run_time=.6)
        self.play(vector.animate.scale(1.08), box.animate.scale(1.08), run_time=.75, rate_func=there_and_back)
        finish_scene(self, 32)


class Scene3Intuition(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(title("A direction samples the slope"))
        center = LEFT*3.7+DOWN*.45
        point = Dot(center, color=INK, radius=.09)
        p_label = Text("P", font_size=22).next_to(point, UR, buff=.08)
        contours = VGroup(*[Circle(radius=r, color=CONTOUR, stroke_width=2.5)
                            for r in (.65, 1.2, 1.75)]).move_to(center)
        gradient_halo = Arrow(center, center+RIGHT*1.65+UP*.85, color=GRADIENT,
                              buff=.04, stroke_width=20, stroke_opacity=.16)
        gradient = Arrow(center, center+RIGHT*1.65+UP*.85, color=GRADIENT, buff=.04, stroke_width=6)
        gradient_angle = np.arctan2(.85, 1.65)
        theta_tracker = ValueTracker(1.15)
        direction = always_redraw(lambda: Arrow(
            center,
            center + 1.25*np.array([np.cos(gradient_angle-theta_tracker.get_value()),
                                    np.sin(gradient_angle-theta_tracker.get_value()), 0]),
            color=DIRECTION, buff=.04, stroke_width=5,
        ))
        grad_label = Text("∇f", color=GRADIENT, font_size=28).next_to(gradient.get_end(), UR, buff=.08)
        u_label = always_redraw(lambda: Text("u", color=DIRECTION, font_size=25)
                                .next_to(direction.get_end(), DOWN, buff=.08))
        equation = Text("Dᵤf = ∇f · u = |∇f| cos θ",
                        font_size=29).to_edge(RIGHT).shift(UP*1.0)
        relative_rate = Text(f"{np.cos(1.15):.2f}", font_size=23, color=DIRECTION)
        def update_relative_rate(mob):
            # Rebuild only this small numeric label from the current vector angle.
            center_of_label = mob.get_center()
            value = np.cos(theta_tracker.get_value())
            mob.become(Text(f"{value:.2f}", font_size=23, color=DIRECTION).move_to(center_of_label))
        relative_rate.add_updater(update_relative_rate)
        explanation = VGroup(
            Text("u is a unit vector: |u| = 1", font_size=23, color=DIRECTION),
            Text("Dot product = rate of change in direction u", font_size=21),
            VGroup(Text("Relative rate cos θ =", font_size=21), relative_rate).arrange(RIGHT, buff=.12),
            Text("Along a level curve, the rate is zero.", font_size=22, color=CONTOUR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.27).next_to(equation, DOWN, buff=.55).to_edge(RIGHT, buff=.28)
        self.play(Create(contours), FadeIn(point, p_label), run_time=1.2)
        self.play(GrowArrow(gradient_halo), GrowArrow(gradient), FadeIn(grad_label),
                  GrowArrow(direction), FadeIn(u_label), run_time=1.2)
        self.play(Write(equation), run_time=1)
        self.play(LaggedStart(*[FadeIn(x, shift=UP*.12) for x in explanation], lag_ratio=.2), run_time=1.2)
        self.play(theta_tracker.animate.set_value(0), run_time=2.0)
        self.play(theta_tracker.animate.set_value(PI/2), run_time=2.0)
        self.play(theta_tracker.animate.set_value(0), run_time=2.0)
        self.play(Indicate(gradient, color=ACCENT), run_time=.8)
        # Keep exploring angles as the explanation compares alignment and rate.
        for angle in (PI/3, PI/6, 0, PI/2, PI, 0):
            self.play(theta_tracker.animate.set_value(angle), run_time=2.1)
            self.wait(1.1)
        finish_scene(self, 41)


class Scene4Example(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(title("Worked example at P = (1, 1)"))
        # A live contour diagram stays on screen while the calculation unfolds.
        axes = Axes(x_range=[-1.8, 1.8, 1], y_range=[-1.55, 1.55, 1],
                    x_length=4.35, y_length=3.75,
                    axis_config={"color": MUTED, "stroke_width": 2},
                    tips=True).shift(LEFT*3.55+DOWN*.35)
        contour = Ellipse(width=4.18, height=2.95, color=CONTOUR, stroke_width=3)
        contour.move_to(axes.c2p(0, 0))
        point = Dot(axes.c2p(1, 1), color=INK, radius=.09)
        p_label = Text("P", font_size=21, weight=BOLD).next_to(point, UR, buff=.08)
        grad_arrow = Arrow(axes.c2p(1,1), axes.c2p(1.35,1.7), buff=0, color=GRADIENT, stroke_width=7)
        tangent = Arrow(axes.c2p(.66,1.17), axes.c2p(1.34,.83), buff=0, color=DIRECTION, stroke_width=5)
        contour_label = Text("f = 3", color=CONTOUR, font_size=19).next_to(contour, DOWN, buff=.1)
        self.play(Create(axes), run_time=.65)
        self.play(Create(contour), FadeIn(point, p_label), run_time=.8)
        self.play(GrowArrow(grad_arrow), run_time=.55)

        duration = max(8, scene_seconds(self, 78) - self.time - .8)
        entries = [
            ("f(x,y) = x² + 2y²", INK, 1.0),
            ("fₓ = 2x\nfᵧ = 4y", INK, 1.0),
            ("∇f(1,1)\n= (2,4)", GRADIENT, .9),
            ("|∇f| = √20\n= 2√5 ≈ 4.47", GRADIENT, 1.0),
            ("East  →  rate 2\nNorth → rate 4", DIRECTION, .7),
            ("NE  →  3√2 ≈ 4.24", DIRECTION, .85),
            ("(1,2) is √5 units long.\nNormalize before comparing.", DIRECTION, .95),
            ("Along ∇f  →  2√5 ≈ 4.47", GRADIENT, .9),
            ("Level curve: x² + 2y² = 3", CONTOUR, 1.0),
            ("Tangent slope: y′ = −1/2", CONTOUR, .85),
            ("(2,4) · (2,−1) = 0", DIRECTION, .9),
        ]
        # The card changes with each narrated step; the diagram builds toward
        # the result instead of leaving a wall of equations parked on screen.
        weights = [entry[2] for entry in entries]
        old = None
        for text, color, weight in entries:
            beat = duration * weight / sum(weights)
            card = Text(text, font_size=36, weight=MEDIUM, color=color, line_spacing=.95)
            card.move_to(RIGHT*2.25+DOWN*.15)
            if old is None:
                self.play(FadeIn(card, shift=RIGHT*.35), run_time=.48)
            else:
                self.play(ReplacementTransform(old, card), run_time=.48)
            self.wait(max(.12, beat-.48))
            old = card
        self.play(GrowArrow(tangent), FadeIn(contour_label), run_time=.55)
        finish_scene(self, 79)


class Scene5Meaning(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(title("Why steepest? The cosine does the work."))
        main = Text("Dᵤf = |∇f| cos θ", font_size=48, weight=BOLD).shift(UP*1.55)
        points = VGroup(
            Text("θ = 0: maximum increase along ∇f", font_size=26, color=GRADIENT),
            Text("−∇f points toward steepest decrease", font_size=25, color=DIRECTION),
            Text("Tangent to a level curve: rate = 0", font_size=25, color=CONTOUR),
            Text("Assume f is differentiable at P.", font_size=23, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.4).next_to(main, DOWN, buff=.55)
        real_world = VGroup(
            Text("Terrain and heat flow.  Gradient descent:", font_size=19, color=MUTED),
            Text("short steps opposite ∇f reduce a function.", font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.12).to_edge(DOWN, buff=.28)
        self.play(Write(main), run_time=.8)
        self.wait(2)
        # A sweeping angle marker makes the cosine argument visible, not just stated.
        center = DOWN*2.65+LEFT*4.2
        radius = .75
        base = Arrow(center, center+RIGHT*radius, buff=0, color=DIRECTION, stroke_width=5)
        theta = ValueTracker(PI/2)
        rotating = always_redraw(lambda: Arrow(
            center, center+radius*np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]),
            buff=0, color=GRADIENT, stroke_width=6))
        arc = Arc(radius=.48, start_angle=0, angle=PI/2, arc_center=center, color=INK, stroke_width=2)
        theta_label = Text("θ", font_size=22).move_to(center+RIGHT*.54+UP*.34)
        readout = Text("ALONG ∇f  /  MAX", font_size=17, color=GRADIENT, weight=BOLD)
        readout.move_to(center+LEFT*.25+DOWN*.48)
        self.play(GrowArrow(base), Create(arc), FadeIn(theta_label), GrowArrow(rotating), FadeIn(readout), run_time=.6)
        self.play(FadeIn(points[0], shift=RIGHT*.32), theta.animate.set_value(0), run_time=1.0, rate_func=smooth)
        self.wait(3.1)
        self.play(Transform(readout, Text("−∇f  /  STEEPEST DOWN", font_size=17, color=DIRECTION, weight=BOLD).move_to(readout)),
                  FadeIn(points[1], shift=RIGHT*.32), theta.animate.set_value(PI), run_time=1.1, rate_func=smooth)
        self.wait(3.1)
        self.play(Transform(readout, Text("TANGENT  /  ZERO RATE", font_size=17, color=CONTOUR, weight=BOLD).move_to(readout)),
                  FadeIn(points[2], shift=RIGHT*.32), theta.animate.set_value(PI/2), run_time=.9, rate_func=smooth)
        self.wait(2.8)
        self.play(FadeIn(points[3], shift=RIGHT*.32), run_time=.45)
        self.wait(.7)
        self.play(FadeIn(real_world), run_time=.45)
        finish_scene(self, 28)


class Scene6Credits(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(title("Three ideas to take with you"))
        takeaways = [
            Text("THE VECTOR", font_size=23, color=MUTED, weight=BOLD),
            Text("Collect the partial derivatives.", font_size=34, weight=BOLD),
            Text("THE CLIMB", font_size=23, color=MUTED, weight=BOLD),
            Text("Direction = steepest increase.\nLength = maximum rate.", font_size=32, weight=BOLD, line_spacing=.9),
            Text("THE CONTOUR", font_size=23, color=MUTED, weight=BOLD),
            Text("Gradient ⟂ level curve.", font_size=34, weight=BOLD),
        ]
        credits = VGroup(
            Text("Reference: OpenStax, Calculus Volume 3, Section 4.6: Directional Derivatives and the Gradient.",
                 font_size=15, color=MUTED),
            Text("Music: none.", font_size=17, color=MUTED),
            Text("AI assistance (Claude by Anthropic): scripting, code drafting, storyboard. Mathematics verified by student.",
                 font_size=16, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.2).to_edge(DOWN, buff=.22)
        index = Text("06", font_size=21, color=GRADIENT, weight=BOLD).to_corner(UL, buff=.4)
        self.add(index)
        start_time = self.time
        for j in range(0, len(takeaways), 2):
            kicker, message = takeaways[j:j+2]
            kicker.move_to(LEFT*2.25+UP*.72)
            message.next_to(kicker, DOWN, aligned_edge=LEFT, buff=.16)
            self.play(FadeIn(kicker, shift=LEFT*.25), FadeIn(message, shift=RIGHT*.4), run_time=.7)
            self.play(message.animate.scale(1.025), run_time=.35, rate_func=there_and_back)
            self.wait(4.25)
            if j < 4:
                self.play(FadeOut(kicker, shift=LEFT*.25), FadeOut(message, shift=LEFT*.25), run_time=.35)
        # Keep the citations and disclosure on screen long enough to read.
        self.wait(.7)
        self.play(FadeIn(credits, shift=UP*.18), run_time=.55)
        finish_scene(self, 35)
