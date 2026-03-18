"""Slide 6: Three dynamics × three clocks — animated ticking clocks.

Each cell shows an analogue clock.  The hand advances one tick per frame
at a constant Δt.  Angular step size per tick reveals the clock quality:

  Correct clock  →  hand sweeps equal angles every tick  (steady)
  Wrong clock    →  hand crawls then lurches             (erratic)

After N_SNAPS ticks the animation holds briefly with all past positions
visible (faint trail), then loops.  Cached after first render.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from interactive.theme import LML_BLUE, LML_GREY, FERMAT, BERNOULLI, render_slide_header

# ── Parameters ────────────────────────────────────────────────────────────────
T_MAX, T_START, N_PTS = 7.0, 2.0, 500
T_DISP = np.linspace(T_START, T_MAX, N_PTS)

ADD_ALPHA, MUL_G    = 1.5, 0.40
PL_ALPHA, PL_LN_X0  = 1.20, 1.0

N_SNAPS     = 18     # equal-Δt ticks per loop
HOLD_FRAMES = 6      # frames at end showing full trail before reset
INTERVAL_MS = 350    # milliseconds per frame

CLOCK_COLORS = {"additive": LML_BLUE, "multiplicative": FERMAT, "powerlaw": BERNOULLI}

DYNAMICS = [
    ("additive",       "Additive\nx → x+α"),
    ("multiplicative", "Multiplicative\nx → ηx"),
    ("powerlaw",       "Power-law\nx → xᵅ"),
]
CLOCKS = [
    ("additive",       "Additive clock\nφ = x"),
    ("multiplicative", "Mult. clock\nφ = ln x"),
    ("powerlaw",       "Power clock\nφ = ln ln x"),
]


# ── Helpers ───────────────────────────────────────────────────────────────────
def _safe_lnln(arr: np.ndarray) -> np.ndarray:
    return np.log(np.maximum(np.log(np.maximum(arr, 1.0 + 1e-9)), 1e-9))


def _paths(dyn: str):
    x = {
        "additive":       1.0 + ADD_ALPHA * T_DISP,
        "multiplicative": np.exp(MUL_G * T_DISP),
        "powerlaw":       np.exp(PL_LN_X0 * PL_ALPHA ** T_DISP),
    }[dyn]
    return x.copy(), np.log(x), _safe_lnln(x)


def _hand_angles(path: np.ndarray, col_scale: float) -> np.ndarray:
    """N_SNAPS hand angles using the correct clock's revolution as the scale.

    col_scale = total Δφ of the *correct* dynamic for this column.
    Correct clocks → exactly one steady revolution (0 → 2π).
    Wrong clocks   → over- or under-shoot, always unevenly.
    """
    phi_0  = path[0]
    snaps  = np.interp(np.linspace(T_DISP[0], T_DISP[-1], N_SNAPS), T_DISP, path)
    return 2.0 * np.pi * (snaps - phi_0) / col_scale


def _hand_xy(angle: float, r: float = 0.72):
    return np.sin(angle) * r, np.cos(angle) * r


def _draw_static_face(ax, color: str, correct: bool) -> None:
    """Background, rim, hour marks, centre dot — drawn once per axis."""
    face = "#EEF9EE" if correct else "white"
    rim  = color    if correct else "#CCCCCC"

    t = np.linspace(0, 2 * np.pi, 300)
    ax.fill(np.cos(t), np.sin(t), color=face,  zorder=0)
    ax.plot(np.cos(t), np.sin(t), color=rim, lw=2.2, zorder=5)

    for k in range(12):
        a  = 2 * np.pi * k / 12
        r0 = 0.78 if k % 3 == 0 else 0.87
        lw = 1.8  if k % 3 == 0 else 0.9
        ax.plot([np.sin(a) * r0, np.sin(a) * 0.97],
                [np.cos(a) * r0, np.cos(a) * 0.97],
                color="#BBBBBB", lw=lw, zorder=2)

    ax.plot(0, 0, "o", color=rim, ms=6, zorder=6)
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    ax.set_aspect("equal")
    ax.axis("off")


# ── GIF generator (cached) ────────────────────────────────────────────────────
@st.cache_data(show_spinner="Building clock animation…")
def _generate_gif() -> bytes:
    # Column scales: total Δφ of the *correct* (diagonal) dynamic per clock column.
    # This anchors one full revolution to what the right clock would do.
    col_scales = []
    for col, (dyn_key, _) in enumerate(DYNAMICS):
        ps = _paths(dyn_key)
        path = ps[col]
        col_scales.append(max(path[-1] - path[0], 1e-12))

    # Pre-compute hand angles for all 9 cells
    all_ang: dict = {}
    for row, (dyn_key, _) in enumerate(DYNAMICS):
        ps = _paths(dyn_key)
        for col in range(3):
            all_ang[(row, col)] = _hand_angles(ps[col], col_scales[col])

    N_FRAMES = N_SNAPS + HOLD_FRAMES

    fig, axes = plt.subplots(
        3, 3, figsize=(13.0, 9.0),
        gridspec_kw={"hspace": 0.15, "wspace": 0.15},
    )
    fig.patch.set_facecolor("white")

    # ── Static layout (drawn once) ────────────────────────────────────────────
    hand_store: dict = {}   # (row,col) → (curr_line, curr_dot, [(ghost_line, ghost_dot)…])

    for row, (_, dyn_label) in enumerate(DYNAMICS):
        for col, (clk_key, clk_label) in enumerate(CLOCKS):
            ax      = axes[row][col]
            correct = (row == col)
            color   = CLOCK_COLORS[clk_key]
            hcol    = color if correct else "#AAAAAA"

            _draw_static_face(ax, color, correct)

            if row == 0:
                ax.set_title(clk_label, fontsize=9, color=color,
                             fontweight="bold", pad=8)

            # Create ghost artists (one per past tick, initially invisible)
            ghosts = []
            for _ in range(N_SNAPS):
                gl, = ax.plot([], [], "-", color=hcol, lw=1.4, alpha=0, zorder=3)
                gd, = ax.plot([], [], "o", color=hcol, ms=3.5, alpha=0, zorder=3)
                ghosts.append((gl, gd))

            # Current hand artists
            cl, = ax.plot([], [], "-", color=hcol, lw=2.6, zorder=4)
            cd, = ax.plot([], [], "o", color=hcol, ms=5.0, zorder=4)
            hand_store[(row, col)] = (cl, cd, ghosts)

        # Row label (left of leftmost clock)
        axes[row][0].text(
            -0.28, 0.5, DYNAMICS[row][1],
            ha="right", va="center",
            transform=axes[row][0].transAxes,
            fontsize=9, color=LML_BLUE, fontweight="bold",
            clip_on=False,
        )

    fig.text(
        0.5, 0.01,
        "Each hand = one equal time step.   "
        "Evenly spread → stable clock.   Bunched together → wrong clock.",
        ha="center", va="bottom", fontsize=8, color=LML_GREY,
    )
    plt.tight_layout(pad=0.3, rect=[0.10, 0.04, 1.0, 1.0])

    # ── Collect all artists for blit ──────────────────────────────────────────
    all_artists = []
    for row in range(3):
        for col in range(3):
            cl, cd, ghosts = hand_store[(row, col)]
            all_artists += [cl, cd]
            for gl, gd in ghosts:
                all_artists += [gl, gd]

    # ── Animation update ──────────────────────────────────────────────────────
    def update(frame: int):
        is_hold = frame >= N_SNAPS
        tick    = min(frame, N_SNAPS - 1)

        for row in range(3):
            for col in range(3):
                cl, cd, ghosts = hand_store[(row, col)]
                ang = all_ang[(row, col)]

                if is_hold:
                    # Hide bright hand; show all positions equally
                    cl.set_data([], [])
                    cd.set_data([], [])
                    for k, (gl, gd) in enumerate(ghosts):
                        hx, hy = _hand_xy(ang[k])
                        gl.set_data([0, hx], [0, hy]); gl.set_alpha(0.65)
                        gd.set_data([hx], [hy]);        gd.set_alpha(0.65)
                else:
                    # Bright current hand
                    hx, hy = _hand_xy(ang[tick])
                    cl.set_data([0, hx], [0, hy])
                    cd.set_data([hx], [hy])

                    # Faint trail of past ticks
                    for k, (gl, gd) in enumerate(ghosts):
                        if k < tick:
                            hx2, hy2 = _hand_xy(ang[k])
                            gl.set_data([0, hx2], [0, hy2]); gl.set_alpha(0.20)
                            gd.set_data([hx2], [hy2]);        gd.set_alpha(0.20)
                        else:
                            gl.set_data([], []); gl.set_alpha(0)
                            gd.set_data([], []); gd.set_alpha(0)

        return all_artists

    anim = animation.FuncAnimation(
        fig, update,
        frames=N_FRAMES,
        interval=INTERVAL_MS,
        blit=True,
    )

    import tempfile, os
    tmp = tempfile.NamedTemporaryFile(suffix=".gif", delete=False)
    tmp.close()
    try:
        anim.save(tmp.name, writer="pillow", dpi=110,
                  savefig_kwargs={"facecolor": "white"})
        plt.close(fig)
        with open(tmp.name, "rb") as f:
            return f.read()
    finally:
        os.unlink(tmp.name)


# ── Slide entry point ─────────────────────────────────────────────────────────
def three_clocks_slide() -> None:
    render_slide_header("Three dynamics — three clocks: only one ticks steadily")
    gif = _generate_gif()
    _, img_col, _ = st.columns([0.15, 9.7, 0.15])
    with img_col:
        st.image(gif, use_container_width=True)
