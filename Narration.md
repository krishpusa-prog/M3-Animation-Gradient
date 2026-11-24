# Narration script

Read in a warm, confident, playful adult female voice at natural speed. Target: about five minutes. Bracketed directions are not spoken.

## OPENING FRAME (0:00-0:15)
[Title and student details appear; brief pause.]
Gradient: the direction of steepest increase. A visual guide for Linear Algebra and Calculus M3. I’m Kaustubh Kashyap, student ID E25B070877.

## SCENE 1 — HOOK / CONTEXT (0:15-0:45)
[Reveal contour map and point P.]
Imagine you’re on a hillside in thick fog. You can feel the ground but can’t see the landscape. You want to climb quickly. Which way should you go? We represent height with a function of horizontal position. Each contour line connects places at the same height, and P marks your position. We want one arrow showing the fastest uphill direction and its rate.
If equal-height contours bunch together, the slope is steeper; wide gaps mean gentler ground.

## SCENE 2 — CONCEPT INTRODUCTION (0:45-1:27)
[Reveal each symbol as it is named; show the learning objective.]
Let x and y be horizontal coordinates, and let f be a differentiable function assigning a height to each location. So f of x comma y is height at that point. The partial derivative f sub x measures how height changes with x while y stays fixed. Similarly, f sub y measures change with y while x stays fixed. The symbol nabla, an upside-down triangle, collects these partial derivatives into the gradient. Its components are f sub x and f sub y. It points toward fastest local increase, and its length is that rate.
Each component is a signed slope. Positive components mean east and north rise; a zero gradient means no first-order change.
[Learning objective on screen: explain the gradient, compute it from partial derivatives, and justify why it points in the direction of steepest increase.]

## SCENE 3 — VISUAL INTUITION (1:27-2:19)
[Show contour map; rotate the blue unit vector u around P.]
A level curve joins points where f has one constant value: on a hill, it is a line of constant elevation. Choose a direction u at P. It is a unit vector, with length one, so we compare rates per equal distance. The directional derivative, D sub u f, is the instantaneous rate of change as we move from P in direction u.
[Display the dot product formula and compare the arrows.]
This rate equals the dot product of the gradient at P with u. If theta is the angle between them, it equals the gradient’s length times cosine theta. Cosine is greatest, one, when theta is zero. So the rate is greatest when u points along the gradient. Along a level curve, height stays constant and the rate is zero. The gradient is therefore perpendicular to the curve.
Turn u away: at sixty degrees the rate is half maximum, at ninety it is zero, and opposite the gradient it is negative maximum.

## SCENE 4 — WORKED EXAMPLE (2:19-3:58)
[Show each calculation in sequence.]
Take f of x comma y equal to x squared plus two y squared, at P equal to (1,1). The partial derivatives are two x and four y. At P, the gradient is (2,4). Its magnitude is square root of two squared plus four squared: square root of twenty, or two square root five, approximately 4.47.
[Show the four unit directions beside their dot products.]
Compare four unit directions. For (1,0), the dot product is 2; for (0,1), it is 4. For (1,1) divided by square root two, the rate is six over square root two, or 3 square root two, about 4.24. For (1,2) divided by square root five, it is ten over square root five, or 2 square root five, about 4.47. This is the gradient scaled to unit length, giving the largest rate.
A directional rate is change per unit distance, so normalize each test vector. The raw (1,2) has length square root five: its dot product 10 is not a per-unit rate. Dividing by square root five gives 4.47. That matches the gradient’s unit direction and largest climb; east or north alone captures less.
[Highlight the contour and its tangent.]
The height at P is 3, so the level curve is x squared plus two y squared equals 3. Implicit differentiation gives two x plus four y times y-prime equals zero. Thus y-prime is negative x over two y; at P, the slope is negative one-half. A tangent direction is (2, negative 1). Its dot product with the gradient is two times two plus four times negative one, which equals zero. The gradient is perpendicular to the level curve.

## SCENE 5 — INTERPRETATION (3:58-4:33)
[Return to the hillside; label increase, decrease, and level directions.]
At a differentiable point, the rate is gradient length times cosine theta. Its maximum occurs at theta zero, along the gradient. The opposite direction, negative gradient, gives steepest decrease. Along a level curve the rate is zero. These ideas appear in terrain analysis, heat flow, and gradient descent, where we move against the gradient to reduce a function. If f is not differentiable, a gradient may not exist and this formula may fail.
Gradient descent takes short steps against the gradient; steps that are too large can overshoot.

## SCENE 6 — SUMMARY & CREDITS (4:33-5:07)
[Three takeaways, then credits. Hold final frame.]
Three takeaways. First, collect the partial derivatives to compute the gradient. Second, its direction gives steepest increase, and its length gives the maximum rate. Third, it is perpendicular to a level curve because the function value stays constant along that curve.
Reference: OpenStax, Calculus Volume 3, Section 4.6, “Directional Derivatives and the Gradient.” Music: no background music. AI assistance from Claude by Anthropic was used for scripting, code drafting, and storyboard; I verified the mathematics and can explain the code.
