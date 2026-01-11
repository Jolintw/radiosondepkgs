import numpy as np
def lapserate_tropopause(T, z, zstart=1e4):
    """
    Docstring for lapserate_tropopause
    The tropical tropopause (Highwood and Hoskins 1998)
    """
    izstart = np.min(np.arange(len(z), dtype=int)[z > zstart])
    for iz in range(izstart, len(z)):
        znow = z[iz]
        izplus2km = np.min(np.arange(len(z), dtype=int)[z > znow+2e3])
        Lhere = (T[iz+1] - T[iz])/([iz+1] - z[iz])
        L2km = (T[izplus2km] - T[iz])/(z[izplus2km] - z[iz])
        if Lhere > -2e-3 and L2km > -2e-3:
            return z[iz], iz