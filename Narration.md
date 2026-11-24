OPENING FRAME (0:00–0:08)
[Soft, assured delivery. Title appears.]
Gradient: the direction of steepest increase. A visual guide for Linear Algebra and Calculus M3. I’m Kaustubh Kashyap, student ID E25B070877.

SCENE 1 — HOOK / CONTEXT (0:08–0:40)
[Show a contour map and mark P.]
Imagine you’re standing on a hillside in thick fog. You can feel the ground under your feet, but you can’t see the landscape. You want to climb as quickly as possible. Which direction should you take? Around you, the ground rises and falls differently depending on the direction you walk. We can model its height by a function of position. In this picture, each contour line connects places at the same height. The point P marks where you are standing. Our goal is to turn the local shape of the ground into one vector: an arrow that tells us which way height increases fastest, and how quickly it increases.

SCENE 2 — CONCEPT INTRODUCTION (0:40–1:25)
[Reveal symbols one at a time.]
Let x and y be the two horizontal coordinates, and let f be a differentiable function that assigns a height to each location. So f of x comma y is the height at that point. The partial derivative f sub x measures how height changes as x changes while y stays fixed. Similarly, f sub y measures the change as y changes while x stays fixed. The symbol nabla, an upside-down triangle, tells us to collect these partial derivatives into the gradient. The gradient of f is the vector whose components are f sub x and f sub y. It points in the horizontal direction of fastest local increase; its length gives the rate of that increase.
[Learning objective appears.]
By the end of this video, you’ll be able to explain the gradient, compute it from partial derivatives, and justify why it points in the direction of steepest increase.

SCENE 3 — VISUAL INTUITION (1:25–2:25)
[Show surface, then its contour map. Keep P fixed.]
A level curve is a curve along which f has one constant value. On a hill, it is like a line of constant elevation. At P, choose a direction u of length one. The unit length means we compare rates per unit of distance, fairly across directions. The directional derivative, written D sub u f, is the instantaneous rate of change of height as we move from P in direction u.
[Rotate u; update rate indicator.]
Here is the key connection: this rate equals the dot product of the gradient at P with u. The dot product measures alignment. If theta is the angle between the gradient and u, the dot product is the gradient’s length times cosine theta. Cosine is largest, equal to one, when theta is zero. So the rate is largest when u points along the gradient. If u runs along a level curve, height does not change; the rate is zero. That means the gradient is perpendicular to the level curve.

SCENE 4 — WORKED EXAMPLE (2:25–3:50)
[Show each line only as it is narrated.]
Take f of x comma y equal to x squared plus two y squared, and evaluate at P equal to (1,1). First compute partial derivatives: f sub x is two x, and f sub y is four y. Substituting x equals one and y equals one gives gradient (2,4). Its magnitude is square root of two squared plus four squared, which is square root of twenty, or two square root five, approximately 4.47.
[Show the four unit directions and dot products.]
Now compare four unit directions. For u equal to (1,0), the rate is (2,4) dot (1,0), which is 2. For (0,1), it is 4. For (1,1) divided by square root two, it is 2 plus 4 over square root two, or 3 square root two, about 4.24. Finally, for (1,2) divided by square root five, it is (2 plus 8) divided by square root five: 10 over square root five, equal to 2 square root five, about 4.47. This last direction is exactly the gradient normalized to length one, so it achieves the largest rate.
[Draw the level curve and tangent.]
The level curve through P has height f(1,1), which is 3, so its equation is x squared plus two y squared equals 3. Implicitly differentiating gives 2x plus 4y times dy by dx equals zero. Therefore dy by dx equals negative x over 2y. At (1,1), the slope is negative one-half, so one tangent direction is (2, negative 1). Check the dot product: (2,4) dot (2, negative 1) equals 4 minus 4, or zero. The tangent is perpendicular to the gradient, just as the contour picture suggested.

SCENE 5 — INTERPRETATION (3:50–4:25)
[Return to hillside visualization.]
At a differentiable point, the directional rate is the gradient’s magnitude times cosine theta. Its maximum occurs at theta zero, directly along the gradient. The opposite direction gives the most rapid decrease, and is the negative gradient. Any direction tangent to the level curve is perpendicular to the gradient, so its rate is zero. These ideas guide terrain analysis, heat-flow models, and gradient descent, where we move against the gradient to reduce a function. Differentiability matters: without it, a single local gradient may not exist, so this directional description can fail or need a more careful replacement.

SCENE 6 — SUMMARY & CREDITS (4:25–5:00)
[Show three takeaways, then credits.]
Three takeaways. First, compute the gradient by collecting the partial derivatives. Second, its direction gives steepest increase, and its length gives that maximum rate. Third, it is perpendicular to a level curve because moving along the curve changes no function value.
References: [Add your course notes and textbook, with author, title, edition, and page.] Background music: none. AI disclosure: AI assistance (Claude by Anthropic) was used for scripting, code drafting, and storyboard; I verified all mathematics and can explain the code.
[Hold final frame for readability.]