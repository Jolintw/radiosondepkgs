import numpy as np
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
from metpy.plots import SkewT
from metpy.units import units

def getCAPEprofile(var, z_tropopause):
    var = var.copy()
    var['p'] = var['p']*units.hPa
    var['T'] = var['T']*units.degC
    if "Td" in var:
        var['Td'] = var['Td']*units.degC
    else:
        var['Td'] = mpcalc.dewpoint_from_relative_humidity(var['T'], var['rh'] * units.percent)
    # var['ws'] = var['ws']*units.meter/units.seconds
    # var['wd'] = var['wd']*units.degree
    # var['u'], var['v'] = mpcalc.wind_components(var['ws'], var['wd'])
    zlen = np.sum(var["z"] < z_tropopause)
    CAPElist = []
    for i in range(zlen):
        prof = mpcalc.parcel_profile(var['p'], var['T'][i], var['Td'][i]).to('degC')
        CAPE, CIN = mpcalc.cape_cin(var['p'], var['T'], var['Td'], prof)
        print(CAPE)
        CAPElist.append(CAPE.magnitude)
    CAPEarray = np.zeros_like(var["z"])
    CAPEarray[:zlen] = np.array(CAPElist)
    return CAPEarray