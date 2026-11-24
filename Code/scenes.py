"""Six independently renderable Manim scenes for the gradient lesson.
Run one scene with: manim -pql scenes.py Scene1Hook
"""
from manim import *
from helpers import *

class Scene0Opening(Scene):
    def construct(self):
        self.camera.background_color = "#101827"
        title=Text("THE GRADIENT", font_size=64, color=GRADIENT, weight=BOLD)
        sub=Text("The direction of steepest increase", font_size=32)
        who=Text("Kaustubh Kashyap  |  E25B070877", font_size=26, color=BLUE_B)
        group=VGroup(title,sub,who).arrange(DOWN, buff=.35)
        rings=VGroup(*[Circle(radius=r, color=CONTOUR, stroke_opacity=.25) for r in (1.2,1.8,2.4)]).shift(LEFT*4)
        self.play(Create(rings), FadeIn(group, shift=UP)); self.wait(4)

class Scene1Hook(Scene):
    def construct(self):
        self.add(title("Which way is uphill?"))
        axes=Axes(x_range=[-3,3], y_range=[-3,3], x_length=6, y_length=5, tips=False).shift(LEFT*2)
        contours=VGroup(*[Ellipse(width=w,height=h,color=CONTOUR) for w,h in [(1.2,.8),(2.4,1.6),(3.6,2.4),(4.8,3.2)]]).move_to(axes.c2p(0,0))
        p=Dot(axes.c2p(.5,.3),color=WHITE); label=Text("P",font_size=24).next_to(p,UR)
        arrow=Arrow(p.get_center(), p.get_center()+RIGHT*.6+UP*.9,color=GRADIENT,buff=0)
        copy=Text("Contour lines = equal height",font_size=26).to_edge(RIGHT).shift(UP*.4)
        self.play(Create(axes),Create(contours),FadeIn(p,label),Write(copy)); self.play(GrowArrow(arrow)); self.wait(8)

class Scene2Concept(Scene):
    def construct(self):
        self.add(title("From partial derivatives to a vector"))
        lines=VGroup(Text("f(x, y): height at horizontal position (x, y)",font_size=27),MathTex(r"f_x=\frac{\partial f}{\partial x}\quad (y\text{ fixed})",font_size=36),MathTex(r"f_y=\frac{\partial f}{\partial y}\quad (x\text{ fixed})",font_size=36),MathTex(r"\nabla f=(f_x,f_y)=\left(\frac{\partial f}{\partial x},\frac{\partial f}{\partial y}\right)",font_size=38,color=GRADIENT)).arrange(DOWN,buff=.35).move_to(UP*.4)
        for item in lines: self.play(Write(item)); self.wait(.5)
        objective=Text("Goal: compute the gradient and explain steepest increase.",font_size=24,color=BLUE_B).to_edge(DOWN)
        self.play(FadeIn(objective)); self.wait(6)

class Scene3Intuition(Scene):
    def construct(self):
        self.add(title("A direction samples the slope"))
        center=LEFT*3.6+DOWN*.6; p=Dot(center,color=WHITE); lab=Text("P",font_size=22).next_to(p,UR)
        circles=VGroup(*[Circle(radius=r,color=CONTOUR,stroke_opacity=.8) for r in (.7,1.3,1.9)]).move_to(center)
        grad=Arrow(center,center+RIGHT*1.5+UP*.8,color=GRADIENT,buff=0); u=Arrow(center,center+RIGHT*1.1,color=DIRECTION,buff=0)
        eq=MathTex(r"D_{\mathbf u}f=\nabla f\cdot\mathbf u=|\nabla f|\cos\theta",font_size=36).to_edge(RIGHT).shift(UP*.6)
        note=Text("u is a unit vector (length 1)",font_size=24).next_to(eq,DOWN)
        rates=VGroup(Text("Along gradient: maximum increase",font_size=23,color=GRADIENT),Text("Along contour: zero change",font_size=23,color=CONTOUR)).arrange(DOWN,aligned_edge=LEFT).next_to(note,DOWN,buff=.7)
        self.play(Create(circles),FadeIn(p,lab)); self.play(GrowArrow(grad),GrowArrow(u)); self.play(Write(eq),FadeIn(note)); self.play(FadeIn(rates)); self.play(Rotate(u,angle=PI/3,about_point=center)); self.wait(10)

class Scene4Example(Scene):
    def construct(self):
        self.add(title("Worked example at P = (1, 1)"))
        steps=[(r"f(x,y)=x^2+2y^2",WHITE),(r"f_x=2x,\qquad f_y=4y",WHITE),(r"\nabla f(1,1)=(2,4)",GRADIENT),(r"|\nabla f|=\sqrt{2^2+4^2}=\sqrt{20}=2\sqrt5\approx4.47",GRADIENT),(r"(2,4)\cdot(1,0)=2;\quad (2,4)\cdot(0,1)=4",BLUE_B),(r"(2,4)\cdot\frac{(1,1)}{\sqrt2}=3\sqrt2\approx4.24",BLUE_B),(r"(2,4)\cdot\frac{(1,2)}{\sqrt5}=\frac{10}{\sqrt5}=2\sqrt5\approx4.47",BLUE_B),(r"x^2+2y^2=3;\quad y'=-\frac{x}{2y}=-\frac12",CONTOUR),(r"(2,4)\cdot(2,-1)=0",CONTOUR)]
        y=2.75
        for tex,color in steps:
            m=MathTex(tex,font_size=31,color=color).move_to(UP*y)
            self.play(Write(m)); self.wait(.55); y-=.67
        self.wait(7)

class Scene5Meaning(Scene):
    def construct(self):
        self.add(title("Why steepest? The cosine does the work."))
        lines=VGroup(MathTex(r"D_{\mathbf u}f=|\nabla f|\cos\theta",font_size=42),Text("θ = 0: maximum rate along ∇f",font_size=27,color=GRADIENT),Text("Opposite direction: steepest decrease −∇f",font_size=27,color=BLUE_B),Text("Tangent to a level curve: rate 0",font_size=27,color=CONTOUR),Text("Assumption: f is differentiable at P",font_size=24)).arrange(DOWN,buff=.42)
        self.play(FadeIn(lines)); self.wait(10)

class Scene6Credits(Scene):
    def construct(self):
        self.add(title("Three ideas to take with you"))
        items=VGroup(Text("1. The gradient collects the partial derivatives.",font_size=27),Text("2. Its direction is steepest increase; its length is the rate.",font_size=27),Text("3. It is perpendicular to level curves.",font_size=27)).arrange(DOWN,aligned_edge=LEFT,buff=.3).to_edge(LEFT).shift(UP*.5)
        credits=VGroup(Text("References: add course notes and textbook details.",font_size=19),Text("Music: no background music.",font_size=19),Text("AI assistance (Claude by Anthropic): scripting, code drafting, storyboard. Mathematics verified by student.",font_size=18)).arrange(DOWN,aligned_edge=LEFT,buff=.18).to_edge(DOWN)
        self.play(FadeIn(items)); self.play(FadeIn(credits)); self.wait(10)
