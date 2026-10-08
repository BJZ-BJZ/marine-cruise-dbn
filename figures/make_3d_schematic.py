"""3D schematic illustration for this project.
Rendered in Python (matplotlib) - not ANSYS/Fluent/STAR-CCM+ output.
Run: python make_3d_schematic.py  (needs matplotlib, numpy)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def hull_mesh(L=100.0, B=20.0, T=8.0, D=6.0, p=1.0, q=0.8, nx=61, ny=31):
    xs = np.linspace(-L/2, L/2, nx)
    a = np.linspace(0, np.pi, ny)
    X, A = np.meshgrid(xs, a)
    xn = 2*X/L
    hb = (B/2.0)*np.maximum(0.0, 1-xn**2)**p
    Y = hb*np.cos(A)
    Z = D - (D+T)*np.sin(A)**q
    return X, Y, Z

def draw_hull(ax, L, B, T, D, p=1.0, q=0.8, color='#b8c4cc', alpha=0.95):
    X, Y, Z = hull_mesh(L, B, T, D, p, q)
    ax.plot_surface(X, Y, Z, color=color, alpha=alpha, shade=True,
                    rstride=2, cstride=2, linewidth=0, antialiased=True)

def box(ax, x0,x1, y0,y1, z0,z1, color='lightgray', alpha=1.0):
    v = np.array([[x0,y0,z0],[x1,y0,z0],[x1,y1,z0],[x0,y1,z0],
                  [x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]])
    faces = [[v[0],v[1],v[2],v[3]],[v[4],v[5],v[6],v[7]],
             [v[0],v[1],v[5],v[4]],[v[2],v[3],v[7],v[6]],
             [v[1],v[2],v[6],v[5]],[v[4],v[7],v[3],v[0]]]
    ax.add_collection3d(Poly3DCollection(faces, facecolor=color, alpha=alpha,
                                        edgecolor='#333333', linewidths=0.4))

def plane(ax, x0,x1, y0,y1, z, color, alpha):
    X, Y = np.meshgrid([x0,x1],[y0,y1])
    ax.plot_surface(X, Y, np.full_like(X,float(z)), color=color, alpha=alpha, shade=False)

def water(ax, x0,x1, y0,y1, z=0):
    plane(ax, x0,x1, y0,y1, z, '#7fb3d5', 0.16)

def seabed(ax, x0,x1, y0,y1, z, color='#d9c9a8'):
    plane(ax, x0,x1, y0,y1, z, color, 0.5)
    for gx in np.linspace(x0,x1,9):
        ax.plot([gx,gx],[y0,y1],[z,z], color='#b09a72', lw=0.4, alpha=0.6)
    for gy in np.linspace(y0,y1,7):
        ax.plot([x0,x1],[gy,gy],[z,z], color='#b09a72', lw=0.4, alpha=0.6)

def mooring_line(ax, p0, p1, n=60, **kw):
    s = np.linspace(0,1,n)
    x = p0[0]+(p1[0]-p0[0])*s
    y = p0[1]+(p1[1]-p0[1])*s
    z = p0[2]+(p1[2]-p0[2])*(s**1.6)
    ax.plot(x, y, z, **kw)

def finish(ax, fname, title, elev=18, azim=-58):
    ax.set_title(title, fontsize=12, pad=10)
    ax.set_xlabel('x (m)'); ax.set_ylabel('y (m)')
    ax.set_zlabel('z (m)')
    ax.view_init(elev=elev, azim=azim)
    plt.tight_layout()
    plt.savefig(fname, dpi=150, bbox_inches='tight')
    plt.close()
    print('saved', fname)

from pathlib import Path
import numpy as np

L, B, T, D = 300.0, 38.0, 9.0, 11.0
fig = plt.figure(figsize=(11, 7.5))
ax = fig.add_subplot(111, projection='3d')

draw_hull(ax, L, B, T, D, p=0.75, q=0.9, color='#dde3e8')
box(ax, -L/2, L/2, -B/2*0.92, B/2*0.92, D-0.5, D+0.5, color='#9aa5ad', alpha=0.9)
# cruise superstructure: stacked tapering decks
y = B/2*0.80
for k, (x0, x1, h) in enumerate([(-120, 110, 12), (-105, 95, 12), (-90, 80, 11), (-75, 60, 10)]):
    box(ax, x0, x1, -y, y, D+k*11.5, D+k*11.5+h, color='#f2f4f5', alpha=0.95)
    y *= 0.94
# funnel
box(ax, -30, -14, -6, 6, D+46, D+58, color='#c0392b', alpha=0.95)
# bridge
box(ax, 108, 122, -14, 14, D, D+14, color='#b9c6ce', alpha=0.95)
water(ax, -320, 320, -220, 220)
# heading arrow
ax.quiver(150, 0, 6, 60, 0, 0, color='#1f4e79', lw=2.2, arrow_length_ratio=0.12)
ax.text(215, 8, 8, 'speed / heading', fontsize=10, color='#1f4e79')
ax.text(-140, -70, D+55, 'cruise ship', fontsize=10, ha='center')
ax.set_zlim(-12, 78)
ax.set_xlim(-330, 330)
finish(ax, str(Path(__file__).parent / 'fig2_cruise_3d.png'),
       'Cruise ship 3D schematic', elev=13, azim=-63)
