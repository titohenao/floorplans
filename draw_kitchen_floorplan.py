import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc

W, H = 1270, 1494
INK = "#111"

fig, ax = plt.subplots(figsize=(W/100, H/100), dpi=100)
ax.set_xlim(0, W)
ax.set_ylim(H, 0)  # match SVG coordinates: origin at top-left
ax.set_aspect("equal")
ax.axis("off")
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

def line(x1, y1, x2, y2, lw=1, dashed=False):
    ax.plot([x1, x2], [y1, y2], color=INK, linewidth=lw,
            linestyle=(0, (5, 4)) if dashed else "-",
            solid_capstyle="butt")

def rect(x, y, w, h, lw=1, fill="white"):
    ax.add_patch(Rectangle((x, y), w, h, linewidth=lw,
                           edgecolor=INK, facecolor=fill))

def text(x, y, s, size=9, ha="center", weight="normal"):
    ax.text(x, y, s, fontsize=size, family="Arial",
            ha=ha, va="center", color=INK, fontweight=weight)

# --- Main room walls ---
line(123,1367,1027,1367,6)
line(123,1367,123,1087,6)
line(123,943,123,119,6)
line(123,119,1027,119,6)
line(1027,879,1027,119,6)
line(1127,1367,1127,879,6)

# --- Left door ---
line(123,1087,267,1087,1.6)
ax.add_patch(Arc((123,1087), 288, 288, angle=0, theta1=270, theta2=360,
                 linewidth=1, edgecolor=INK))

# --- Kitchen cabinetry ---
rect(555,1267,144,100,1.1)
text(627,1323,"REF.",9,weight="bold")

rect(699,1267,120,100,1.1)
text(759,1323,"BASE",9)

rect(819,1267,120,100,1.1)
text(879,1323,"RANGE",9,weight="bold")

rect(939,1267,88,100,1.1)
text(983,1323,"BASE",9)

rect(1027,1107,100,260,1.1)
text(1077,1243,"BASE",9)

rect(1027,879,100,228,1.1)
text(1077,999,"PANTRY",9,weight="bold")

# --- Pantry door ---
line(1027,921,883,921,1.6)
ax.add_patch(Arc((1027,921), 288, 288, angle=0, theta1=90, theta2=180,
                 linewidth=1, edgecolor=INK))
text(951,907,'3\'-0" PANTRY DOOR',8)

# --- Island plumbing point + dimensions ---
ax.add_patch(Circle((715,907),5,facecolor="white",edgecolor=INK,linewidth=1.2))
line(703,907,727,907,0.8)
line(715,919,715,895,0.8)
text(715,879,"ISLAND PLUMBING",9)
line(715,1367,715,907,0.7,True)
text(727,1147,'9\'-7"',9,ha="left")
line(715,907,1027,907,0.7,True)
text(871,895,'6\'-6"',9)

# --- Sectional ---
rect(171,575,500,152,0.9)
rect(171,331,152,244,0.9)
text(421,659,"SECTIONAL",9)
text(421,687,'125" × 99"',8)
line(183,603,659,603,0.6)
line(295,563,295,343,0.6)

# --- 1'-0" wall offset ---
line(123,755,171,755,0.8)
line(123,763,123,747,0.8)
line(171,763,171,747,0.8)
text(147,739,'1\'-0"',8)

# --- 13'-4" vertical dimension ---
line(715,1367,715,727,0.8)
line(707,1367,723,1367,0.8)
line(707,727,723,727,0.8)
text(727,1047,'13\'-4" (160")',9,ha="left")

# --- TV ---
rect(415,131,112,20,0.8)
text(471,167,"TV",9)

# --- 4'-5" dimension ---
line(347,331,347,119,0.8)
line(339,331,355,331,0.8)
line(339,119,355,119,0.8)
text(335,225,'4\'-5" (53")',9,ha="right")

# --- Overall right dimension ---
line(1027,1367,1179,1367,0.7)
line(1027,119,1179,119,0.7)
line(1171,1367,1171,119,0.8)
line(1163,1375,1179,1359,0.8)
line(1163,127,1179,111,0.8)
text(1159,743,'26\'-0" OVERALL',9,ha="right")

# --- Left vertical dimensions ---
line(123,1367,87,1367,0.7)
line(123,1087,87,1087,0.7)
line(87,1367,87,1087,0.8)
text(75,1227,'5\'-10" (70")',9,ha="right")

line(123,1087,71,1087,0.7)
line(123,943,71,943,0.7)
line(75,1087,75,943,0.8)
text(63,1015,'3\'-0"',9,ha="right")

# --- Bottom segmented dimensions ---
for x in [123,555,699,819,939,1027,1127]:
    line(x,1367,x,1415,0.6)

line(123,1407,1127,1407,0.8)
for x in [123,555,699,819,939,1027,1127]:
    line(x-6,1413,x+6,1401,0.8)

text(339,1395,'9\'-0"',8)
text(627,1395,'3\'-0"',8)
text(759,1395,'2\'-6"',8)
text(879,1395,'2\'-6"',8)
text(983,1395,'1\'-10"',8)
text(1077,1395,'2\'-1"',8)

# --- Labels ---
text(555,227,"LIVING",12,weight="bold")
text(775,1207,"KITCHEN",11,weight="bold")
text(123,79,"SCHEMATIC FLOOR PLAN",11,ha="left",weight="bold")

plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

out_svg = "kitchen_floorplan_python.svg"
out_png = "kitchen_floorplan_python.png"

fig.savefig(out_svg, format="svg", bbox_inches="tight", pad_inches=0)
fig.savefig(out_png, format="png", dpi=150, bbox_inches="tight", pad_inches=0)
plt.close(fig)

print(out_svg)
print(out_png)
