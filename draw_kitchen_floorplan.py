
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc, Polygon

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
CABINET_FILL = "0.88"


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


def poly(points_in, lw=1.0, fill="white"):
    """Polygon whose vertices are given in physical inches."""
    ax.add_patch(
        Polygon(
            [(X(x), Y(y)) for x, y in points_in],
            closed=True,
            linewidth=lw,
            edgecolor=INK,
            facecolor=fill,
        )
    )


def label(x_in, y_in, s, size=9, ha="center", weight="normal", color=INK):
    ax.text(
        X(x_in),
        Y(y_in),
        s,
        fontsize=size,
        family="DejaVu Sans",
        ha=ha,
        va="center",
        color=color,
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
line(0,   210, 0,   0,   lw=6)
line(0,   0,   226, 0,   lw=6)
line(226, 190, 226, 0,   lw=6)
line(251, 312, 251, 190, lw=6)
line(226, 190, 251, 190, lw=6)
line(226, 312, 251, 312, lw=6)

# Backyard door
# 32" opening, with the lower edge/hinge still 70" from the bottom wall.
BACKYARD_DOOR_W = 32.0
BACKYARD_DOOR_Y = 242.0  # 312" - 70"

line(0, BACKYARD_DOOR_Y, BACKYARD_DOOR_W, BACKYARD_DOOR_Y, lw=1.6)
ax.add_patch(
    Arc(
        (X(0), Y(BACKYARD_DOOR_Y)),
        U(BACKYARD_DOOR_W * 2),
        U(BACKYARD_DOOR_W * 2),
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
label(126, 301, "FRIDGE", size=9, weight="bold")

rect(144, 287, 30, 25, lw=1.1, fill=CABINET_FILL)
label(159, 301, "BASE", size=9)

# Stove as its own polygon
poly(
    [
        (174, 287),
        (204, 287),
        (204, 312),
        (174, 312),
    ],
    lw=1.1,
    fill="black",
)
label(189, 301, "STOVE", size=9, weight="bold", color="white")

# L-shaped base cabinet: one continuous polygon
# Vertices trace the combined 22" bottom leg + 25" right leg.
poly(
    [
        (204, 287),
        (226, 287),
        (226, 247),
        (251, 247),
        (251, 312),
        (204, 312),
    ],
    lw=1.1,
    fill=CABINET_FILL,
)

# Keep labels in each functional leg
label(215, 301, "BASE", size=9)
label(238.5, 281, "BASE", size=9)

# Pantry
rect(226, 190, 25, 57, lw=1.1)
label(238.5, 220, "PANTRY", size=9, weight="bold")
line(226, 247, 251, 247, lw=6)

# Pantry door — 30", centered within the same 36" opening
PANTRY_DOOR_W = 30.0
PANTRY_OPENING_W = 36.0
PANTRY_DOOR_OFFSET = (PANTRY_OPENING_W - PANTRY_DOOR_W) / 2.0  # 3" each side

PANTRY_DOOR_HINGE_X = 226.0
PANTRY_DOOR_Y = 200.5 + PANTRY_DOOR_OFFSET

line(
    PANTRY_DOOR_HINGE_X,
    PANTRY_DOOR_Y,
    PANTRY_DOOR_HINGE_X - PANTRY_DOOR_W,
    PANTRY_DOOR_Y,
    lw=1.6,
)

ax.add_patch(
    Arc(
        (X(PANTRY_DOOR_HINGE_X), Y(PANTRY_DOOR_Y)),
        U(PANTRY_DOOR_W * 2),
        U(PANTRY_DOOR_W * 2),
        angle=0,
        theta1=90,
        theta2=180,
        linewidth=1,
        edgecolor=INK,
    )
)

label(
    PANTRY_DOOR_HINGE_X - PANTRY_DOOR_W / 2,
    PANTRY_DOOR_Y - 3.5,
    '2\'-6" PANTRY DOOR',
    size=8,
)

# Island plumbing location
PLUMB_X = 148.0
PLUMB_Y = 197.0

# Plumbing data callout — Excel/scatter-plot style
# Compact upper-right label connected to the plumbing point by an elbow leader.
CALLOUT_X = PLUMB_X + 16.0
CALLOUT_Y = PLUMB_Y - 14.0

# Leader: point -> angled segment -> short horizontal segment
LEADER_KNEE_X = PLUMB_X + 9.0
LEADER_KNEE_Y = PLUMB_Y - 11.0
LEADER_END_X = CALLOUT_X - 2.0

line(PLUMB_X, PLUMB_Y, LEADER_KNEE_X, LEADER_KNEE_Y, lw=0.8)
line(LEADER_KNEE_X, LEADER_KNEE_Y, LEADER_END_X, LEADER_KNEE_Y, lw=0.8)

label(
    CALLOUT_X,
    CALLOUT_Y,
    '78" from pantry\n115" from north wall',
    size=8,
    ha="left",
)

# Sectional, exact overall footprint 125" x 99"
rect(12, 114, 125, 38, lw=0.9, fill="navy")
rect(12, 53, 38, 61, lw=0.9, fill="navy")
label(74.5, 135, "SECTIONAL", size=9, color="white")
label(74.5, 142, '125" × 99"', size=8, color="white")
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

# Left-side 32" backyard door opening segment
door_dim_x = X(-12)
raw_line(X(0), Y(242), door_dim_x - 4, Y(242), lw=0.7)
raw_line(X(0), Y(210), door_dim_x - 4, Y(210), lw=0.7)
raw_line(door_dim_x, Y(242), door_dim_x, Y(210), lw=0.8)
raw_text(door_dim_x - 12, (Y(242) + Y(210)) / 2, '2\'-8" (32")', size=9, ha="right")

# Moved left of the fridge for readability.
COUCH_CLEAR_X = 88.0
COUCH_BOTTOM_Y = 152.0
SOUTH_WALL_Y = 312.0

line(COUCH_CLEAR_X, COUCH_BOTTOM_Y, COUCH_CLEAR_X, SOUTH_WALL_Y, lw=0.8)
raw_line(
    X(COUCH_CLEAR_X - 2),
    Y(COUCH_BOTTOM_Y),
    X(COUCH_CLEAR_X + 2),
    Y(COUCH_BOTTOM_Y),
    lw=0.8,
)
raw_line(
    X(COUCH_CLEAR_X - 2),
    Y(SOUTH_WALL_Y),
    X(COUCH_CLEAR_X + 2),
    Y(SOUTH_WALL_Y),
    lw=0.8,
)
label(
    COUCH_CLEAR_X - 3,
    (COUCH_BOTTOM_Y + SOUTH_WALL_Y) / 2,
    '13\'-4" (160")',
    size=9,
    ha="right",
)

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


# Island
# 7'-0" wide x 3'-6" deep
# 52" clearance from the range run
# 36" clearance from the pantry face
ISLAND_W = 84.0
ISLAND_H = 42.0
CLEAR_TO_RANGE = 52.0
CLEAR_TO_PANTRY = 36.0

# Reference faces in inches
RANGE_RUN_TOP_Y = 287.0     # top face of the bottom cabinet/range run
PANTRY_LEFT_X = 226.0       # left face of pantry wall/cabinet run

# Place island so the bottom edge is 52" from the range run
# and the right edge is 36" from the pantry.
ISLAND_RIGHT_X = PANTRY_LEFT_X - CLEAR_TO_PANTRY
ISLAND_LEFT_X = ISLAND_RIGHT_X - ISLAND_W
ISLAND_BOTTOM_Y = RANGE_RUN_TOP_Y - CLEAR_TO_RANGE
ISLAND_TOP_Y = ISLAND_BOTTOM_Y - ISLAND_H

# Island shown as two stacked rectangles to display the overhang
ISLAND_OVERHANG_H = 12.0
ISLAND_BASE_H = 30.0

# Top 12" overhang band
rect(
    ISLAND_LEFT_X,
    ISLAND_TOP_Y,
    ISLAND_W,
    ISLAND_OVERHANG_H,
    lw=1.4,
    fill=CABINET_FILL,
)

# Lower 2'-6" body band
rect(
    ISLAND_LEFT_X,
    ISLAND_TOP_Y + ISLAND_OVERHANG_H,
    ISLAND_W,
    ISLAND_BASE_H,
    lw=1.4,
    fill=CABINET_FILL,
)


# Optional dimension callouts for the island placement
# 52" vertical clearance to range run
dim_x = ISLAND_LEFT_X - 8
line(dim_x, ISLAND_BOTTOM_Y, dim_x, RANGE_RUN_TOP_Y, lw=0.8)
raw_line(X(dim_x - 2), Y(ISLAND_BOTTOM_Y), X(dim_x + 2), Y(ISLAND_BOTTOM_Y), lw=0.8)
raw_line(X(dim_x - 2), Y(RANGE_RUN_TOP_Y), X(dim_x + 2), Y(RANGE_RUN_TOP_Y), lw=0.8)
raw_line(X(dim_x), Y(ISLAND_BOTTOM_Y), X(ISLAND_LEFT_X), Y(ISLAND_BOTTOM_Y), lw=0.6)
raw_line(X(dim_x), Y(RANGE_RUN_TOP_Y), X(174), Y(RANGE_RUN_TOP_Y), lw=0.6)
raw_text(X(dim_x - 3), (Y(ISLAND_BOTTOM_Y) + Y(RANGE_RUN_TOP_Y)) / 2, '52"', size=9, ha="right")

# Island depth breakdown aligned with the 52" dimension
island_dim_x = dim_x

# 12" overhang band
line(island_dim_x, ISLAND_TOP_Y, island_dim_x, ISLAND_TOP_Y + ISLAND_OVERHANG_H, lw=0.8)
raw_line(X(island_dim_x - 2), Y(ISLAND_TOP_Y), X(island_dim_x + 2), Y(ISLAND_TOP_Y), lw=0.8)
raw_line(
    X(island_dim_x - 2),
    Y(ISLAND_TOP_Y + ISLAND_OVERHANG_H),
    X(island_dim_x + 2),
    Y(ISLAND_TOP_Y + ISLAND_OVERHANG_H),
    lw=0.8,
)
raw_text(
    X(island_dim_x - 3),
    (Y(ISLAND_TOP_Y) + Y(ISLAND_TOP_Y + ISLAND_OVERHANG_H)) / 2,
    '12"',
    size=9,
    ha="right",
)

# 30" base/body band
line(
    island_dim_x,
    ISLAND_TOP_Y + ISLAND_OVERHANG_H,
    island_dim_x,
    ISLAND_BOTTOM_Y,
    lw=0.8,
)
raw_line(
    X(island_dim_x - 2),
    Y(ISLAND_TOP_Y + ISLAND_OVERHANG_H),
    X(island_dim_x + 2),
    Y(ISLAND_TOP_Y + ISLAND_OVERHANG_H),
    lw=0.8,
)
raw_line(
    X(island_dim_x - 2),
    Y(ISLAND_BOTTOM_Y),
    X(island_dim_x + 2),
    Y(ISLAND_BOTTOM_Y),
    lw=0.8,
)
raw_text(
    X(island_dim_x - 3),
    (Y(ISLAND_TOP_Y + ISLAND_OVERHANG_H) + Y(ISLAND_BOTTOM_Y)) / 2,
    '30"',
    size=9,
    ha="right",
)

# 36" horizontal clearance to pantry
dim_y = ISLAND_BOTTOM_Y + 16
line(ISLAND_RIGHT_X, dim_y, PANTRY_LEFT_X, dim_y, lw=0.8)
raw_line(X(ISLAND_RIGHT_X), Y(dim_y - 2), X(ISLAND_RIGHT_X), Y(dim_y + 2), lw=0.8)
raw_line(X(PANTRY_LEFT_X), Y(dim_y - 2), X(PANTRY_LEFT_X), Y(dim_y + 2), lw=0.8)
raw_line(X(ISLAND_RIGHT_X), Y(dim_y), X(ISLAND_RIGHT_X), Y(ISLAND_BOTTOM_Y), lw=0.6)
raw_line(X(PANTRY_LEFT_X), Y(dim_y), X(PANTRY_LEFT_X), Y(190), lw=0.6)
raw_text((X(ISLAND_RIGHT_X) + X(PANTRY_LEFT_X)) / 2, Y(dim_y - 4), '36"', size=9)

# Island width dimension aligned with the 36" dimension
island_width_dim_y = dim_y
line(ISLAND_LEFT_X, island_width_dim_y, ISLAND_RIGHT_X, island_width_dim_y, lw=0.8)
raw_line(
    X(ISLAND_LEFT_X),
    Y(island_width_dim_y - 2),
    X(ISLAND_LEFT_X),
    Y(island_width_dim_y + 2),
    lw=0.8,
)
raw_line(
    X(ISLAND_RIGHT_X),
    Y(island_width_dim_y - 2),
    X(ISLAND_RIGHT_X),
    Y(island_width_dim_y + 2),
    lw=0.8,
)
raw_text(
    (X(ISLAND_LEFT_X) + X(ISLAND_RIGHT_X)) / 2,
    Y(island_width_dim_y - 4),
    '84"',
    size=9,
)

# Re-draw plumbing marker in the foreground as a compact bullseye
ax.add_patch(
    Circle(
        (X(PLUMB_X), Y(PLUMB_Y)),
        U(1.25),
        facecolor="white",
        edgecolor=INK,
        linewidth=1.2,
        zorder=10,
    )
)
ax.plot(
    [X(PLUMB_X - 1.5), X(PLUMB_X + 1.5)],
    [Y(PLUMB_Y), Y(PLUMB_Y)],
    color=INK,
    linewidth=0.8,
    solid_capstyle="butt",
    zorder=11,
)
ax.plot(
    [X(PLUMB_X), X(PLUMB_X)],
    [Y(PLUMB_Y - 1.5), Y(PLUMB_Y + 1.5)],
    color=INK,
    linewidth=0.8,
    solid_capstyle="butt",
    zorder=11,
)

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
