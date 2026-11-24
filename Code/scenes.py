"""Seven Manim scenes for the five-minute gradient explainer.

Render with: manim -qh scenes.py Scene0Opening
The shell script renders all scenes in order and builds the final MP4.
Each scene holds its closing frame until its storyboard time has elapsed.
"""
from manim import *
from helpers import *

BG = "#F4F1EA"


def finish_scene(scene, seconds, focus=None):
    """Use small, repeated emphasis beats until the scene's target duration."""
    while seconds - scene.time > 0.2:
        remaining = seconds - scene.time
        if focus is not None and remaining > 3.2:
            # A restrained pulse keeps a narrated point alive without adding noise.
            scene.play(Indicate(focus, color=focus.get_color(), scale_factor=1.035), run_time=1.6)
            remaining = seconds - scene.time
            if remaining > 1.5:
                scene.wait(min(1.7, remaining - .2))
        else:
            scene.wait(remaining)


class Scene0Opening(Scene):
    def construct(self):
        self.camera.background_color = BG
        title_text = Text("THE GRADIENT", font_size=66, color=GRADIENT, weight=BOLD)
        subtitle = Text("The direction of steepest increase", font_size=31)
        student = Text("Kaustubh Kashyap  |  E25B070877", font_size=25, color=DIRECTION)
        title_block = VGroup(title_text, subtitle, student).arrange(DOWN, buff=0.36).shift(RIGHT*1.2)
        rings = VGroup(*[Circle(radius=r, color=CONTOUR, stroke_opacity=.42, stroke_width=2)
                         for r in (0.9, 1.4, 1.9, 2.4)]).shift(LEFT*4.2)
        arrow_halo = Arrow(LEFT*4.2, LEFT*3.3+UP*1.5, color=GRADIENT,
                           buff=0, stroke_width=18, stroke_opacity=.16)
        arrow = Arrow(LEFT*4.2, LEFT*3.3+UP*1.5, color=GRADIENT, buff=0, stroke_width=5)
        self.play(Create(rings), run_time=1.2)
        self.play(GrowArrow(arrow_halo), GrowArrow(arrow), FadeIn(title_block, shift=UP*.2), run_time=1.4)
        self.play(rings.animate.scale(1.08), run_time=1.1, rate_func=there_and_back)
        finish_scene(self, 8, rings)


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
        self.play(Create(axes), run_time=1)
        self.play(LaggedStart(*[Create(c) for c in contours], lag_ratio=.15), run_time=1.5)
        self.play(FadeIn(point, label), FadeIn(caption), Write(prompt), run_time=1)
        self.play(GrowArrow(uphill_halo), GrowArrow(uphill), run_time=1)
        self.play(Indicate(point, color=ACCENT, scale_factor=1.7), run_time=.6)
        finish_scene(self, 32, uphill)


class Scene2Concept(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(title("From partial derivatives to a vector"))
        lines = [
            Text("Let x and y describe horizontal position; f gives height.", font_size=25),
            Text("fₓ = ∂f/∂x     (y held fixed)", font_size=29),
            Text("fᵧ = ∂f/∂y     (x held fixed)", font_size=29),
            Text("∇ (nabla)     ∇f = (fₓ, fᵧ)", font_size=32, color=GRADIENT),
            Text("= (∂f/∂x, ∂f/∂y)", font_size=29, color=GRADIENT),
        ]
        group = VGroup(*lines).arrange(DOWN, buff=.32).move_to(UP*.35)
        for line in group:
            self.play(Write(line), run_time=.85)
            self.wait(2.6)
            self.play(Indicate(line, color=ACCENT, scale_factor=1.025), run_time=.7)
        objective = Text(
            "By the end of this video, the viewer will be able to explain what the gradient vector\n"
            "of a two-variable function is, compute it from partial derivatives, and justify why it\n"
            "points in the direction of steepest increase.",
            font_size=18, color=DIRECTION, line_spacing=.85,
        ).to_edge(DOWN, buff=.2)
        self.play(FadeIn(objective), run_time=.7)
        finish_scene(self, 45, group[3])


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
        for angle in (PI/3, PI/6, 0, PI/2, 0):
            self.play(theta_tracker.animate.set_value(angle), run_time=2.1)
            self.wait(1.1)
        finish_scene(self, 60, gradient)


class Scene4Example(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(title("Worked example at P = (1, 1)"))
        # Reveal one verified algebra step at a time. Color ties each result to the visual key.
        derivation = [
            ("f(x, y) = x² + 2y²", INK),
            ("fₓ = 2x       fᵧ = 4y", INK),
            ("∇f(1, 1) = (2, 4)", GRADIENT),
            ("|∇f| = √(2² + 4²)\n= √20 = 2√5 ≈ 4.47", GRADIENT),
            ("(2,4) · (1,0) = 2\n(2,4) · (0,1) = 4", DIRECTION),
            ("(2,4) · (1,1)/√2\n= 3√2 ≈ 4.24", DIRECTION),
            ("(2,4) · (1,2)/√5\n= 10/√5 = 2√5 ≈ 4.47", DIRECTION),
            ("f(1,1) = 3   →   x² + 2y² = 3", CONTOUR),
            ("2x + 4y y′ = 0   →   y′ = −x/(2y) = −1/2", CONTOUR),
            ("Tangent (2,−1):   (2,4) · (2,−1) = 0", CONTOUR),
        ]
        # Fit ten compact equations in two columns for legibility at 1080p.
        left = VGroup(*[Text(tex, color=color, font_size=25) for tex, color in derivation[:5]])
        right = VGroup(*[Text(tex, color=color, font_size=22) for tex, color in derivation[5:]])
        left.arrange(DOWN, aligned_edge=LEFT, buff=.42).scale(.92).to_edge(LEFT, buff=.48).shift(DOWN*.1)
        right.arrange(DOWN, aligned_edge=LEFT, buff=.44).scale(.92).to_edge(RIGHT, buff=.38).shift(DOWN*.1)
        for obj in left:
            self.play(Write(obj), run_time=.9)
            self.wait(2.5)
        for obj in right:
            self.play(Write(obj), run_time=.9)
            self.wait(2.5)
        # A small graphic reinforces orthogonality without obscuring the calculations.
        key = VGroup(Dot(radius=.045,color=INK), Text("Gradient: red   Direction: blue   Contour: charcoal", font_size=17))
        key.arrange(RIGHT, buff=.16).to_edge(DOWN, buff=.18)
        self.play(FadeIn(key), run_time=.5)
        self.play(Indicate(right[1], color=ACCENT, scale_factor=1.04), run_time=1.2)
        self.play(Indicate(right[4], color=ACCENT, scale_factor=1.04), run_time=1.2)
        finish_scene(self, 85, right[1])


class Scene5Meaning(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(title("Why steepest? The cosine does the work."))
        main = Text("Dᵤf = |∇f| cos θ", font_size=43).shift(UP*1.35)
        points = VGroup(
            Text("θ = 0: maximum increase along ∇f", font_size=26, color=GRADIENT),
            Text("−∇f points toward steepest decrease", font_size=25, color=BLUE_B),
            Text("Tangent to a level curve: rate = 0", font_size=25, color=CONTOUR),
            Text("Assume f is differentiable at P.", font_size=23, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.4).next_to(main, DOWN, buff=.55)
        real_world = Text("Used in terrain, heat flow, and gradient descent.",
                          font_size=22).to_edge(DOWN, buff=.4)
        self.play(Write(main), run_time=1)
        for item in points:
            self.play(FadeIn(item, shift=RIGHT*.12), run_time=.65)
            self.wait(1.8)
        self.play(FadeIn(real_world), run_time=.6)
        finish_scene(self, 35, main)


class Scene6Credits(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(title("Three ideas to take with you"))
        takeaways = VGroup(
            Text("1. The gradient collects the partial derivatives.", font_size=27),
            Text("2. It points to steepest increase; its length is the rate.", font_size=26),
            Text("3. It is perpendicular to level curves.", font_size=27),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.38).to_edge(LEFT, buff=.75).shift(UP*.55)
        credits = VGroup(
            Text("Reference: OpenStax, Calculus Volume 3, Section 4.6: Directional Derivatives and the Gradient.",
                 font_size=15, color=MUTED),
            Text("Music: none.", font_size=17, color=MUTED),
            Text("AI assistance (Claude by Anthropic): scripting, code drafting, storyboard. Mathematics verified by student.",
                 font_size=16, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.2).to_edge(DOWN, buff=.22)
        self.play(LaggedStart(*[FadeIn(line, shift=UP*.1) for line in takeaways], lag_ratio=.2), run_time=1.4)
        self.play(FadeIn(credits), run_time=.8)
        finish_scene(self, 35, takeaways)
