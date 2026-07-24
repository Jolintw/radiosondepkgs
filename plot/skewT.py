import numpy as np
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
from metpy.plots import SkewT
from metpy.units import units
from mypkgs.processor.numericalmethod import RightAngleInterpolater

def skewTlogP(var):
    var = var.copy()
    var['p'] = var['p']*units.hPa
    var['T'] = var['T']*units.degC
    if "Td" in var:
        var['Td'] = var['Td']*units.degC
    else:
        var['Td'] = mpcalc.dewpoint_from_relative_humidity(var['T'], var['rh'] * units.percent)
    var['ws'] = var['ws']*units.meter/units.seconds
    var['wd'] = var['wd']*units.degree
    var['u'], var['v'] = mpcalc.wind_components(var['ws'], var['wd'])
    ds = mpcalc.parcel_profile_with_lcl_as_dataset(var['p'], var['T'], var['Td'])
    prof = mpcalc.parcel_profile(var['p'], var['T'][0], var['Td'][0]).to('degC')
    lcl = mpcalc.lcl(var['p'][0], var['T'][0], var['Td'][0])
    CAPE, CIN = mpcalc.cape_cin(var['p'], var['T'], var['Td'], prof)
    info = ""
    info = "$P_0=${:.1f} hPa\n$T_0=${:.1f} $^o$C\n$Td_0=${:.1f} $^o$C\n".format(var['p'][0].magnitude, var['T'][0].magnitude, var['Td'][0].magnitude)
    info = info + "CAPE={:.0f} $J/kg$\n".format(CAPE.magnitude)
    info = info + "CIN={:.0f} $J/kg$".format(CIN.magnitude)
    # print(list(ds.variables))

    ft =  20
    fig = plt.figure(figsize=(8, 7), dpi=300)
    skew = SkewT(fig, rotation=45)

    plt.tick_params(labelsize=ft-2)
    skew.plot(ds.isobaric, ds.ambient_temperature, 'r')
    skew.plot(ds.isobaric, ds.ambient_dew_point, 'g')
    skew.plot(ds.isobaric, ds.parcel_temperature.metpy.convert_units('degC'), 'black')
    z_p100 = var["z"][np.argmin(np.abs(var['p'].magnitude - 100))]
    barb_z_intv = 500 # meter
    RAI = RightAngleInterpolater(X=var["z"], newX=np.arange(1, int(z_p100)//barb_z_intv+1) * barb_z_intv, equidistance=False)
    p_barb = np.append([var["p"][0]], RAI.interpolate(var["p"]))
    u_barb = np.append([var["u"][0]], RAI.interpolate(var["u"]))
    v_barb = np.append([var["v"][0]], RAI.interpolate(var["v"]))
    # nbarb = 2
    # skew.plot_barbs(var['p'][::nbarb], var['u'][::nbarb], var['v'][::nbarb], xloc=1.07, plot_units=units.knots)
    skew.plot_barbs(p_barb, u_barb, v_barb, xloc=1.11, plot_units=units.knots)
    # Add the relevant special lines
    pressure = np.arange(1000, 499, -50) * units('hPa')
    mixing_ratio = np.array([0.1, 0.2, 0.4, 0.6, 1, 1.5, 2, 3, 4,
                            6, 8, 10, 13, 16, 20, 25, 30, 36, 42]).reshape(-1, 1) * units('g/kg')

    skew.plot_dry_adiabats(t0=np.arange(233, 533, 10) * units.K, alpha=0.25,
                            colors='orangered', linewidths=1)
    skew.plot_moist_adiabats(t0=np.arange(233, 400, 5) * units.K, alpha=0.25,
                                colors='tab:green', linewidths=1)
    skew.plot_mixing_lines(pressure=pressure, mixing_ratio=mixing_ratio, linestyles='dotted',
                            colors='dodgerblue', linewidths=1)
    skew.ax.set_ylabel("Pressure (hPa)", fontsize=ft-2)
    skew.ax.set_xlabel("Temperature (\u00B0C)", fontsize=ft-2)
    skew.ax.set_ylim(1000, 100)
    skew.ax.set_xlim(-20, 40)
    skew.ax.text(-69, 102,info, verticalalignment="top", fontsize=ft-4)
    return fig, skew