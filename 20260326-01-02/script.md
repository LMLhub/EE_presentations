# Speaker Script — Growth Rates in Ergodicity Economics: Beyond the Log Transform

**Format:** 12 slides (~9–10 min), seven interactive app slides
**Audience:** EE 2026 — researchers and practitioners familiar with economics, not necessarily EE specialists
**Delivery goal:** Conversational and confident. Lead with intuition. Let the figures do the heavy lifting. On interactive slides, speak *while* the audience is watching — do not wait for silence.

---

## Slide 1 — Title

*(pause, let the room settle)*

"This talk is about growth rates — specifically, about one persistent misconception about what ergodicity economics actually says. People often reduce EE to a single trick: take the log of your wealth. Today I want to show you why that framing, fundamentally misses the point."

---

## Slide 2 — The Misconception

"Here's what people think EE says: take the log, maximise its expected value. That's it. Which is basically just log utility in a different outfit.

What EE actually says is something more general: find the **time-average growth rate** of your wealth under its **actual dynamics**, and maximise that.

The log is one answer to the question 'what are the dynamics?' — but only one. Today I want to show you how far that question reaches."

---

## Slide 3 — Interactive: Additive Window

"Let's start with the simplest case. Additive dynamics: x grows by a fixed amount α every step. I've drawn the path, and this window represents one clock rotation — a fixed measurement interval.

*(move the slider slowly)*

Watch what happens as I slide the window along the time axis. The δx arrow — the wealth gained inside one clock tick — stays exactly the same everywhere. It doesn't matter whether we measure early or late: the same time, the same gain.

This is what a good clock looks like. The additive clock ticks steadily for additive dynamics."

---

## Slide 4 — Interactive: Multiplicative Window

"Now let's try the same thing for multiplicative dynamics: x gets scaled by a factor each step. Same fixed window, same clock rotation.

*(move slider from left to right)*

Look at δx. Early in the path, when wealth is small, the window captures very little growth. Move it to the right — the same time interval now captures an enormous jump. Same window. Same clock speed. Completely different reading.

The additive clock is broken for this process. It is not measuring a property of the dynamics — it is measuring where you happened to start looking."

---

## Slide 4b — Interactive: Clock Speed Solution

"So what can we do? One option: speed up the clock as wealth grows. If δx keeps changing, maybe we can shrink δt to compensate.

*(point to the three coloured windows)*

These three anchors show exactly how short the clock rotation would need to be to capture the same δx = 1 at each wealth level. Early on: δt is large. Higher up: δt shrinks dramatically. At higher wealth, you'd need to take measurements much more frequently just to see the same absolute gain.

That works — but it's impractical. Your clock speed would depend on your current wealth. There's a cleaner solution."

---

## Slide 4t — Interactive: Log Transform

"The cleaner solution: don't change the clock speed — change what you're measuring. Apply the ergodic transform. For multiplicative dynamics, that transform is the logarithm.

*(move the slider)*

Now I'm plotting ln(x) instead of x. And look: the window captures the same δ(ln x) no matter where I place it. The log clock ticks steadily.

This is why EE recommends the log — not because of utility theory, not as an assumption, but because ln(x) is the function that converts a multiplicative process into one with constant increments. The log clock is forced by the dynamics."

---

## Slide 5 — Power-Law Derivation

"Now let's push one step further. What if the dynamics aren't multiplicative — what if x is raised to a power each step? x goes to x to the α.

One line of algebra: let y = ln(x). Then under x → xᵅ, we get y → α·y. Still multiplicative. The log clock has the same problem the additive clock had one step back.

Take one more log. Let z = ln(ln(x)). Now the increment is ln(α) — a constant. The double-log clock ticks steadily for power-law dynamics.

The growth rate is g = ln(α). A clean, wealth-independent constant."

---

## Slide 5b — Interactive: Power-Law in Two Worlds

"Let me show you both worlds side by side for power-law dynamics.

*(move the slider)*

Left panel: x(t) itself — super-exponential growth. δx balloons as we move the window right. Right panel: ln(x(t)) — still exponential. δ(ln x) also changes with position.

Neither the additive clock nor the log clock works here. Both fail. We need to go one level deeper."

---

## Slide 5t — Interactive: Double-Log Window

"And here it is — ln(ln(x)).

*(move the slider)*

The δ(ln ln x) is constant everywhere. Every position of the window gives exactly the same reading. The double-log clock ticks steadily for power-law dynamics.

The pattern is clear: each new class of dynamics demands one more log."

---

## Slide 6 — Interactive: Three Clocks Summary

"Let's put everything together. Three dynamics, three clocks, nine combinations.

*(point to the diagonal — let the animation run)*

The diagonal cells tick steadily — evenly spaced hand positions. Those are the right clock-dynamic pairs. Everything off the diagonal is erratic: the hand lurches, bunches up, races ahead. Wrong clock.

Additive dynamics: the additive clock. Multiplicative dynamics: the log clock. Power-law dynamics: the double-log clock.

EE is not about picking the log. It is about asking: **what clock does your process demand?** The log is one answer. It is not the only one."

---

## Slide 7 — Absorbing Boundaries

"One honest limitation before we close.

Everything I've said assumes the clock runs forever. But real wealth processes have absorbing states — bankruptcy, ruin, zero. Once you hit the boundary, the clock stops permanently.

*(gesture to the two diverging trajectories)*

These two paths start identically. One survives and compounds. The other is absorbed and stays at zero. Near such a boundary, maximising the growth rate alone is not enough. The strategy must weigh g against the probability that the clock stops before the long run ever arrives. This is the frontier EE is now pushing into."

---

## Slide 8 — Summary

"Three lessons.

Additive dynamics: the natural clock is x itself — constant increments without transformation.

Multiplicative dynamics: the log clock. g = ln(α). This is where the familiar EE result lives.

Power-law dynamics: the double-log clock. g = ln(α) again — one level deeper.

And when there are absorbing boundaries: growth rate alone is not enough.

The log is the right clock for multiplicative dynamics. It is not magic. It is not the whole story.

The question EE actually asks is simple: **what is the right clock for your dynamics?**

Thank you."

---

# Open Issues

---

## Title slide has no author or affiliation

Slide 1 shows only the title, subtitle, and "EE 2026". Add your name and affiliation before presenting.

---

## Three-clocks animation (Slide 6) requires Pillow

The GIF is generated on first load using `pillow` as the matplotlib animation writer. Ensure `pillow` is installed (`pip install pillow`) before presenting. First render takes several seconds; after that it is cached for the session.

---

## Power-law figures start above x = 1

Power-law dynamics collapse for x < 1 (the opposite behaviour). The slides use x(0) = e (ln x₀ = 1). If an audience member asks, note that x₀ > 1 is assumed throughout — a small annotation on slide 5b could pre-empt the question.

---

## Citation style inconsistency

If references are added to the PDF slides, unify to one citation style throughout.
