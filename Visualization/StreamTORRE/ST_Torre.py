import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.colors as mcolors
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Turning Torso · 3D Visualizer",
    page_icon="🏛️",
    layout="wide",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=DM+Mono:wght@300;400&display=swap');

  html, body, [class*="css"] {
    font-family: 'Cormorant Garamond', serif;
    background-color: #0d0d0f;
    color: #e8e4dc;
  }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background-color: #111114;
    border-right: 1px solid #2a2a30;
  }
  [data-testid="stSidebar"] * {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    color: #9a9590 !important;
  }
  [data-testid="stSidebar"] .stSlider label,
  [data-testid="stSidebar"] .stSelectbox label {
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #5a5a60 !important;
    font-size: 0.68rem !important;
  }

  /* Title block */
  .title-block {
    padding: 2.5rem 0 1rem 0;
    border-bottom: 1px solid #2a2a30;
    margin-bottom: 2rem;
  }
  .title-block h1 {
    font-family: 'Cormorant Garamond', serif;
    font-weight: 300;
    font-size: 3.2rem;
    letter-spacing: 0.04em;
    color: #e8e4dc;
    margin: 0;
    line-height: 1;
  }
  .title-block .subtitle {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    color: #4a4a52;
    text-transform: uppercase;
    margin-top: 0.5rem;
  }

  /* Stats row */
  .stat-card {
    background: #14141a;
    border: 1px solid #22222a;
    border-radius: 2px;
    padding: 1rem 1.2rem;
    font-family: 'DM Mono', monospace;
  }
  .stat-label {
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4a4a52;
    margin-bottom: 0.25rem;
  }
  .stat-value {
    font-size: 1.6rem;
    font-weight: 300;
    color: #c8c0b0;
  }
  .stat-unit {
    font-size: 0.65rem;
    color: #4a4a52;
    margin-left: 0.2rem;
  }

  /* Metric highlight */
  [data-testid="metric-container"] {
    background: #14141a;
    border: 1px solid #22222a;
    padding: 1rem;
    border-radius: 2px;
  }
</style>
""", unsafe_allow_html=True)


# ─── Sidebar controls ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### TURNING TORSO")
    st.markdown("---")

    floors = st.slider("Floors", min_value=1, max_value= 15, value= 7)
    rotation_per_floor = st.slider("Rotation per floor (°)", 0.0, 30.0, 10.0, step=0.1)
    sides = st.selectbox("Floor shape", options=[3, 4, 5, 6, 8],
                         format_func=lambda x: {3:"Triangle",4:"Square",5:"Pentagon",6:"Hexagon",8:"Octagon"}[x],
                         index=1)
    height_per_floor = st.slider("Floor height (m)", 2, 8, 4)
    radius = st.slider("Building radius (m)", 5, 15, 10)

    st.markdown("---")
    st.markdown("**Color scheme**")
    palette = st.selectbox("Color scheme", ["Ice · Blue–White", "Ember · Red–Gold", "Forest · Green–Teal", "Mono · Grey"])

    st.markdown("---")
    show_verticals = st.checkbox("Show vertical edges", value=True)
    show_floor_fill = st.checkbox("Show floor fill", value=False)

# ─── Color palettes ─────────────────────────────────────────────────────────
PALETTES = {
    "Ice · Blue–White":   ("#3a7bd5", "#d0e8ff"),
    "Ember · Red–Gold":   ("#c0392b", "#f9ca24"),
    "Forest · Green–Teal":("#27ae60", "#81ecec"),
    "Mono · Grey":        ("#555560", "#dcdce0"),
}
color_start, color_end = PALETTES[palette]

def lerp_color(c1, c2, t):
    r1, g1, b1 = mcolors.to_rgb(c1)
    r2, g2, b2 = mcolors.to_rgb(c2)
    return (r1+(r2-r1)*t, g1+(g2-g1)*t, b1+(b2-b1)*t)

# ─── Page header ────────────────────────────────────────────────────────────
st.markdown("""
<div class="title-block">
  <h1>Turning Torso</h1>
  <div class="subtitle">Parametric 3D Tower · Interactive Visualizer</div>
</div>
""", unsafe_allow_html=True)

# ─── Stats row ──────────────────────────────────────────────────────────────
total_height = floors * height_per_floor
total_rotation = floors * rotation_per_floor
col1, col2, col3, col4 = st.columns(4)

for col, label, value, unit in [
    (col1, "Total Height",    f"{total_height}", "m"),
    (col2, "Total Rotation",  f"{total_rotation:.1f}", "°"),
    (col3, "Floors",          f"{floors}", ""),
    (col4, "Shape",           {3:"Triangle",4:"Square",5:"Pentagon",6:"Hexagon",8:"Octagon"}[sides], ""),
]:
    with col:
        st.markdown(f"""
        <div class="stat-card">
          <div class="stat-label">{label}</div>
          <div class="stat-value">{value}<span class="stat-unit">{unit}</span></div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── 3D Figure ──────────────────────────────────────────────────────────────

# Base Polygon 
fig = plt.figure(figsize=(9, 13), facecolor="#0d0d0f")
ax = fig.add_subplot(111, projection="3d", facecolor="#0d0d0f")

angles = np.linspace(0, 2 * np.pi, sides, endpoint=False)
x_base = radius * np.cos(angles)
y_base = radius * np.sin(angles)

x_base = np.append(x_base, x_base[0])
y_base = np.append(y_base, y_base[0])

# assign height
# Build polygons for each floor
floor_polys = []
for floor in range(floors):
    z = floor * height_per_floor
    theta = np.deg2rad(floor * rotation_per_floor)
    x_rot = x_base * np.cos(theta) - y_base * np.sin(theta)
    y_rot = x_base * np.sin(theta) + y_base * np.cos(theta)
    polygon = list(zip(x_rot, y_rot, np.full_like(x_rot, z)))
    floor_polys.append(polygon)

# Loop over each floor polygon and add walls
for i in range(floors):
    polygon = floor_polys[i]

    # Gradient color based on floor index
    t = i / max(floors - 1, 1)
    color = lerp_color(color_start, color_end, t)
    alpha = 0.3 + 0.4 * t

    # --- Draw the floor itself ---
    poly_floor = Poly3DCollection([polygon], facecolor=color, alpha=alpha, edgecolor='none')
    ax.add_collection3d(poly_floor)

    # --- Draw the outline (optional) ---
    xs, ys, zs = zip(*polygon)
    ax.plot(xs, ys, zs, color=color, linewidth=0.8, alpha=alpha)

    # --- Draw the walls (if not the last floor) ---
    if i < floors - 1:
        polygon_lower = polygon
        polygon_upper = floor_polys[i + 1]

        walls = []
        for v in range(sides):
            (x1, y1, z1) = polygon_lower[v]
            (x2, y2, z1) = polygon_lower[v+1]
            (x1u, y1u, z2) = polygon_upper[v]
            (x2u, y2u, z2) = polygon_upper[v+1]

            wall = [(x1, y1, z1), (x2, y2, z1),
                    (x2u, y2u, z2), (x1u, y1u, z2)]
            walls.append(wall)

        poly_walls = Poly3DCollection(walls, facecolor=color, alpha=alpha, edgecolor='none')
        ax.add_collection3d(poly_walls)

# Axis styling
for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
    pane.fill = False
    pane.set_edgecolor("#1e1e26")

ax.tick_params(colors="#333340", labelsize=7)
for spine in ax.spines.values():
    spine.set_color("#1e1e26")

ax.set_xlabel("X", color="#333340", fontsize=8, labelpad=8)
ax.set_ylabel("Y", color="#333340", fontsize=8, labelpad=8)
ax.set_zlabel("Z (m)", color="#333340", fontsize=8, labelpad=8)
ax.xaxis.label.set_color("#333340")
ax.yaxis.label.set_color("#333340")
ax.zaxis.label.set_color("#333340")
ax.tick_params(axis='x', colors="#333340")
ax.tick_params(axis='y', colors="#333340")
ax.tick_params(axis='z', colors="#333340")

ax.set_title("", pad=0)
fig.tight_layout(pad=0)

st.pyplot(fig, use_container_width=True)


# ─── Footer note ────────────────────────────────────────────────────────────
st.markdown("""
<div style="font-family:'DM Mono',monospace; font-size:0.65rem; color:#2e2e38;
            text-align:center; margin-top:2rem; letter-spacing:0.15em;">
  PARAMETRIC ARCHITECTURE VISUALIZER · BUILT WITH STREAMLIT + MATPLOTLIB
</div>
""", unsafe_allow_html=True)

