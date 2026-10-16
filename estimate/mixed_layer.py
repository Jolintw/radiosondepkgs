import numpy as np
import metpy.calc as mpcalc
from metpy.units import units
from mypkgs.processor.numericalmethod import RightAngleInterpolater
from atmospkg.calculation import saturation_vapor_pressure, mixingratio_from_pressure, potential_temperature, vapor_pressure_from_mixingratio
from atmospkg.unit import Tunitconversion, Punitconversion

# problem not solved
def mixed_layer_CAPE_CIN(P, T, RH, mixed_layer_depth = 10000, Punit = "Pa", Tunit = "K", RHunit = "", mixed_layer_depth_unit = "Pa"):
    T = Tunitconversion(T, Tunit, aimunit = "K")
    P = Punitconversion(P, Punit, aimunit="Pa")
    if not (RHunit == "%" or RHunit == "percent"):
        RH = RH * 100

    mixed_layer_depth = Punitconversion(mixed_layer_depth, mixed_layer_depth_unit, aimunit="Pa")
    mlq, mlpt = mixed_layer_q_pt_depthinp(P, T, RH, mixed_layer_depth, RHunit="%")
    print(mlq, mlpt)
    P_mltop = P[0] - mixed_layer_depth
    T_mltop = potential_temperature(mlpt, P=100000, P_ref=P_mltop)
    es_mltop = saturation_vapor_pressure(T_mltop) * 100
    e_mltop = vapor_pressure_from_mixingratio(mlq, P_mltop)
    RH_mltop = e_mltop / es_mltop * 100
    mask_above_mltop = P < P_mltop
    P_above_mltop = np.append([P_mltop], P[mask_above_mltop]) * units.Pa
    T_above_mltop = np.append([T_mltop], T[mask_above_mltop]) * units.K
    RH_above_mltop = np.append([RH_mltop], RH[mask_above_mltop]) * units.percent
    Td_above_mltop = mpcalc.dewpoint_from_relative_humidity(T_above_mltop, RH_above_mltop)
    print(RH_above_mltop[0], P_above_mltop[0], T_above_mltop[0], Td_above_mltop[0])
    prof = mpcalc.parcel_profile(P_above_mltop, T_above_mltop[0], Td_above_mltop[0]).to('degC')
    CAPE, CIN = mpcalc.cape_cin(P_above_mltop, T_above_mltop, Td_above_mltop, prof)
    return CAPE, CIN

def mixed_layer_q_pt_depthinp(P, T, RH, mixed_layer_depth = 10000, Punit = "Pa", Tunit = "K", RHunit = "", mixed_layer_depth_unit = "Pa"):
    """mixed layer mixing ratio and potential temperature
    return: mixed layer q (mixing ratio) in kg/kg, mixed layer potential temperature in K
    """
    T = Tunitconversion(T, Tunit, aimunit = "K")
    P = Punitconversion(P, Punit, aimunit="Pa")
    mixed_layer_depth = Punitconversion(mixed_layer_depth, mixed_layer_depth_unit, aimunit="Pa")
    es = saturation_vapor_pressure(T) * 100 # Pa
    if RHunit == "%" or RHunit == "percent":
        e = es * RH / 100
    else: 
        e = es * RH
    q = mixingratio_from_pressure(e, P)
    pt = potential_temperature(T, P)
    P0 = P[0]
    inter_p = np.linspace(P0, P0-mixed_layer_depth, 101)
    RAI = RightAngleInterpolater(P, inter_p, equidistance=False)
    inter_q = RAI.interpolate(q)
    inter_pt = RAI.interpolate(pt)
    mlq = np.nanmean(inter_q)
    mlpt = np.nanmean(inter_pt)
    return mlq, mlpt

