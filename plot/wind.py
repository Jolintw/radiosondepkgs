
import numpy as np
from atmospkg.calculation import wswd_to_uv
from mypkgs.plotter.plotter import Plotter

def radial_wind(u, v, angle, angle_unit = "radius"):
    if angle_unit == "degree":
        angle = angle / 180 * np.pi
    return u * np.cos(angle) + v * np.sin(angle)

figsize = [7, 8]
def uvplot_z(var, ylim = [0, 5000], xlim = [-5, 30], figsize = figsize):
    Pt = Plotter(figsize = figsize)#figsize = [6, 8])
    # Pt.title(site + time.strftime(' %Y-%m-%d %H UTC') + "\n", loc = "left")
    plotwindline_1(Pt, var, yname="z")
    Pt.set_ylabel("height (m)")
    setting(Pt, xlim, ylim)
    return Pt

def uvplot_p(var, ylim = [1000, 600], xlim = [-5, 30], figsize = figsize):
    Pt = Plotter(figsize = figsize)#figsize = [6, 8])
    # Pt.title(site + time.strftime(' %Y-%m-%d %H UTC') + "\n", loc = "left")
    plotwindline(Pt, var, yname="p")
    Pt.ax.invert_yaxis()
    Pt.set_ylabel("pressure (hPa)")
    setting(Pt, xlim, ylim)
    
    return Pt

def plotwindline(Pt, var, yname, uvline = True, wsline = True):
    y = var[yname]
    u, v = wswd_to_uv(var['ws'], var['wd'], wdunit="deg")
    if uvline:
        Pt.ax.plot(u, y, "r", label = "u")
        Pt.ax.plot(v, y, "b", label = "v")
    if wsline:
        Pt.ax.plot(np.sqrt(u**2+v**2), y, "k", label = "ws")

def plotwindline_1(Pt, var, yname, uvline = True, wsline = True):
    y = var[yname]
    u, v = wswd_to_uv(var['ws'], var['wd'], wdunit="deg")
    if uvline:
        Pt.ax.plot(u, y, "r", label = "u")
        Pt.ax.plot(v, y, "b", label = "v")
    if wsline:
        Pt.ax.plot(np.sqrt(u**2+v**2), y, "k", label = "ws")
        Pt.ax.plot(radial_wind(u, v, angle=60/180*np.pi), y, "green", label = "60\u00B0")

def setting(Pt, xlim, ylim):
    Pt.set_ylim(ylim)
    Pt.set_xlim(xlim)
    Pt.ax.grid()
    Pt.set_xlabel("m/s")
    Pt.legend()
    Pt.fig.tight_layout()

