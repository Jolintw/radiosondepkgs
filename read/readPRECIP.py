import numpy as np

def read_sounding_L2(filepath):
    var = {}
    var['time_offset'], var['p'], var['T'], var['rh'], var['ws'], var['wd'], var['z'], var['Td'], var['u'], var['v'] = np.loadtxt(filepath, delimiter=',', skiprows=47, unpack=True, usecols=(1,2,3,4,5,6,9,11,12,13))
    dp = var["p"][1:] - var["p"][:-1]
    while np.any(dp>=0):
        ind = np.arange(dp.shape[0], dtype=int)
        saveind = np.append([0], ind[dp<0] + 1)
        for v in var:
            var[v] = var[v][saveind]
        dp = var["p"][1:] - var["p"][:-1]
    return var