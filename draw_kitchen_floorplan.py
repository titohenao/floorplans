import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc

# ============================================================
# GLOBAL SCALE
# ============================================================
# All architectural geometry below is specified in INCHES.
# Changing SCALE changes only the rendered drawing size.
# It does NOT change any physical dimension.
SCALE = 4.0  # drawing units per inch

# Canvas origin for the architectural plan.
ORIGIN_X = 123.0
ORIGIN_Y = 119.0

CANVAS_W = 1270
CANVAS_H = 1494
INK = "#111"


# ============================================================
# UNIT HELPERS
# ============================================================
def X(inches):
    """Physical x-coordinate in inches -> drawing x-coordinate."""
    return ORIGIN_X + inches * SCALE


def Y(inches):
    """Physical y-coordinate in inches -> drawing y-coordinate."""
    return ORIGIN_Y + inches * SCALE


def U(inches):
    """Physical length in inches -> drawing length."""
    return inches * SCALE


# ============================================================
# BASIC DRAWING HELPERS
# ============================================================
fig, ax = plt.subplots(figsize=(CANVAS_W / 100, CANVAS_H / 100), dpi=100)
ax.set_xlim(0, CANVAS_W)
ax.set_ylim(CANVAS_H, 0)  # SVG-style coordinates: y increases downward
ax.set_aspect("equal")
ax.axis("off")

fig.patch.set_facecolor("white")
ax.set_facecolor("white")


def line(x1_in, y1_in, x2_in, y2_in, lw=1.0, dashed=False):
    ax.plot(
        [X(x1_in), X(x2_in)],
        [Y(y1_in), Y(y2_in)],
        color=INK,
        linewidth=lw,
        linestyle=(0, (5, 4)) if dashed else "-",
        solid_capstyle="butt",
    )


def rect(x_in, y_in, w_in, h_in, lw=1.0, fill="white", dashed=False):
    ax.add_patch(
        Rectangle(
            (X(x_in), Y(y_in)),
            U(w_in),
            U(h_in),
            linewidth=lw,
            edgecolor=INK,
            facecolor=fill,
            linestyle=(0, (5, 4)) if dashed else "-",
        )
    )


def label(x_in, y_in, s, size=9, ha="center", weight="normal"):
    ax.text(
        X(x_in),
        Y(y_in),
        s,
        fontsize=size,
        family="DejaVu Sans",
        ha=ha,
        va="center",
        color=INK,
        fontweight=weight,
    )


def raw_line(x1, y1, x2, y2, lw=1.0):
    """For page annotation geometry that is not part of the physical plan."""
    ax.plot([x1, x2], [y1, y2], color=INK, linewidth=lw, solid_capstyle="butt")


def raw_text(x, y, s, size=9, ha="center", weight="normal"):
    ax.text(
        x, y, s,
        fontsize=size,
        family="DejaVu Sans",
        ha=ha,
        va="center",
        color=INK,
        fontweight=weight,
    )


# ============================================================
# PHYSICAL PLAN GEOMETRY — ALL DIMENSIONS IN INCHES
# ============================================================

# Main walls
# Overall vertical length = 26'-0" = 312"
# Main horizontal width to pantry wall = 18'-10" = 226"
# Right-side return extends 25" farther east.
line(0,   312, 226, 312, lw=6)
line(0,   312, 0,   242, lw=6)
line(0,   206, 0,   0,   lw=6)
line(0,   0,   226, 0,   lw=6)
line(226, 190, 226, 0,   lw=6)
line(251, 312, 251, 190, lw=6)

# Left door
# 36" opening
line(0, 242, 36, 242, lw=1.6)
ax.add_patch(
    Arc(
        # Original SVG:
        # M (36, 242) A 36 36 0 0 0 (0, 206)
        (X(0), Y(242)),
        U(72),
        U(72),
        angle=0,
        theta1=270,
        theta2=360,
        linewidth=1,
        edgecolor=INK,
    )
)

# Kitchen cabinetry
# Bottom run
rect(108, 287, 36, 25, lw=1.1)
label(126, 301, "REF.", size=9, weight="bold")

rect(144, 287, 30, 25, lw=1.1)
label(159, 301, "BASE", size=9)

rect(174, 287, 30, 25, lw=1.1)
label(189, 301, "RANGE", size=9, weight="bold")

rect(204, 287, 22, 25, lw=1.1)
label(215, 301, "BASE", size=9)

# Right run
rect(226, 247, 25, 65, lw=1.1)
label(238.5, 281, "BASE", size=9)

# Pantry
rect(226, 190, 25, 57, lw=1.1)
label(238.5, 220, "PANTRY", size=9, weight="bold")

# Pantry door — 36"
line(226, 200.5, 190, 200.5, lw=1.6)
ax.add_patch(
    Arc(
        # Original SVG:
        # M (226, 236.5) A 36 36 0 0 1 (190, 200.5)
        # Hinge/center is at the pantry wall: (226, 200.5)
        (X(226), Y(200.5)),
        U(72),
        U(72),
        angle=0,
        theta1=90,
        theta2=180,
        linewidth=1,
        edgecolor=INK,
    )
)
label(207, 197, '3\'-0" PANTRY DOOR', size=8)

# Island plumbing center
PLUMB_X = 148.0
PLUMB_Y = 197.0
ax.add_patch(
    Circle(
        (X(PLUMB_X), Y(PLUMB_Y)),
        U(1.25),
        facecolor="white",
        edgecolor=INK,
        linewidth=1.2,
    )
)
line(145, 197, 151, 197, lw=0.8)
line(148, 200, 148, 194, lw=0.8)
label(148, 190, "ISLAND PLUMBING", size=9)

# Plumbing reference dimensions
line(148, 312, 148, 197, lw=0.7, dashed=True)
label(151, 257, '9\'-7"', size=9, ha="left")

line(148, 197, 226, 197, lw=0.7, dashed=True)
label(187, 194, '6\'-6"', size=9)

# Sectional, exact overall footprint 125" x 99"
rect(12, 114, 125, 38, lw=0.9)
rect(12, 53, 38, 61, lw=0.9)
label(74.5, 135, "SECTIONAL", size=9)
label(74.5, 142, '125" × 99"', size=8)
line(15, 121, 134, 121, lw=0.6)
line(43, 111, 43, 56, lw=0.6)

# 12" offset from left wall to sectional
line(0, 159, 12, 159, lw=0.8)
line(0, 161, 0, 157, lw=0.8)
line(12, 161, 12, 157, lw=0.8)
label(6, 155, '1\'-0"', size=8)

# TV
rect(73, 3, 28, 5, lw=0.8)
label(87, 12, "TV", size=9)

# ============================================================
# DIMENSION ANNOTATIONS
# These dimensions are also defined from physical-inch anchors.
# ============================================================

# 13'-4" = 160"
line(148, 312, 148, 152, lw=0.8)
raw_line(X(146), Y(312), X(150), Y(312), lw=0.8)
raw_line(X(146), Y(152), X(150), Y(152), lw=0.8)
label(151, 232, '13\'-4" (160")', size=9, ha="left")

# 4'-5" = 53"
line(56, 53, 56, 0, lw=0.8)
raw_line(X(54), Y(53), X(58), Y(53), lw=0.8)
raw_line(X(54), Y(0), X(58), Y(0), lw=0.8)
label(53, 26.5, '4\'-5" (53")', size=9, ha="right")

# Overall 26'-0" dimension at right
overall_dim_x = X(262)
raw_line(X(226), Y(312), overall_dim_x + 8, Y(312), lw=0.7)
raw_line(X(226), Y(0), overall_dim_x + 8, Y(0), lw=0.7)
raw_line(overall_dim_x, Y(312), overall_dim_x, Y(0), lw=0.8)
raw_line(overall_dim_x - 8, Y(312) + 8, overall_dim_x + 8, Y(312) - 8, lw=0.8)
raw_line(overall_dim_x - 8, Y(0) + 8, overall_dim_x + 8, Y(0) - 8, lw=0.8)
raw_text(overall_dim_x - 12, (Y(312) + Y(0)) / 2, '26\'-0" OVERALL', size=9, ha="right")

# Left-side 70" segment
left_dim_x = X(-9)
raw_line(X(0), Y(312), left_dim_x, Y(312), lw=0.7)
raw_line(X(0), Y(242), left_dim_x, Y(242), lw=0.7)
raw_line(left_dim_x, Y(312), left_dim_x, Y(242), lw=0.8)
raw_text(left_dim_x - 12, (Y(312) + Y(242)) / 2, '5\'-10" (70")', size=9, ha="right")

# Left-side 36" door opening segment
door_dim_x = X(-12)
raw_line(X(0), Y(242), door_dim_x - 4, Y(242), lw=0.7)
raw_line(X(0), Y(206), door_dim_x - 4, Y(206), lw=0.7)
raw_line(door_dim_x, Y(242), door_dim_x, Y(206), lw=0.8)
raw_text(door_dim_x - 12, (Y(242) + Y(206)) / 2, '3\'-0"', size=9, ha="right")

# Bottom segmented dimensions
bottom_y = Y(322)
for xi in [0, 108, 144, 174, 204, 226, 251]:
    raw_line(X(xi), Y(312), X(xi), Y(324), lw=0.6)

raw_line(X(0), bottom_y, X(251), bottom_y, lw=0.8)

for xi in [0, 108, 144, 174, 204, 226, 251]:
    x = X(xi)
    raw_line(x - 6, bottom_y + 6, x + 6, bottom_y - 6, lw=0.8)

raw_text(X(54),  Y(319), '9\'-0"',  size=8)
raw_text(X(126), Y(319), '3\'-0"',  size=8)
raw_text(X(159), Y(319), '2\'-6"',  size=8)
raw_text(X(189), Y(319), '2\'-6"',  size=8)
raw_text(X(215), Y(319), '1\'-10"', size=8)
raw_text(X(238.5), Y(319), '2\'-1"', size=8)

# Room labels
label(108, 27, "LIVING", size=12, weight="bold")
label(163, 272, "KITCHEN", size=11, weight="bold")

# Page title intentionally positioned in page space, not floor-plan space
raw_text(123, 79, "SCHEMATIC FLOOR PLAN", size=11, ha="left", weight="bold")

plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

OUT_SVG = "/mnt/data/kitchen_floorplan_from_inches.svg"
OUT_PNG = "/mnt/data/kitchen_floorplan_from_inches.png"

fig.savefig(OUT_SVG, format="svg", bbox_inches="tight", pad_inches=0)
fig.savefig(OUT_PNG, format="png", dpi=150, bbox_inches="tight", pad_inches=0)
plt.close(fig)

print(f"SCALE = {SCALE} drawing units / inch")
print(f"SVG: {OUT_SVG}")
print(f"PNG: {OUT_PNG}")
