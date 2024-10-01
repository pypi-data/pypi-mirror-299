import numpy as np
from HUST_PPS import HornerNhanDaThuc, HornerChiaDaThuc

def LapBangTichLagrange(a: np.ndarray):
    list_of_arrays = []
    b = [1]
    for i in range(0,len(a)):
        b1 = HornerNhanDaThuc(b,a[i])
        list_of_arrays.append(b1)
        b = b1.copy()
    
    return list_of_arrays,list_of_arrays[-1]

def LapBangThuongLagrange(a: np.ndarray):
    list_of_c = []
    _ , b = LapBangTichLagrange(a)
    for i in range(0,len(a)):
        c, _ = HornerChiaDaThuc(b,a[i])
        list_of_c.append(c)
    return np.array(list_of_c)
    
def CalculateCy(a: np.ndarray, y: np.ndarray):
    c = [0] * len(a)
    for i in range(0,len(y)):
        res = 1
        for j in range(0,len(a)):
            if i != j:
                res *= (a[i] - a[j])
        if res != 0:
            c[i] = y[i] / res
        else:
            c[i] = y[i]
    return np.array(c)

def DaThucLagrange(a: np.ndarray, y: np.ndarray):
    m = LapBangThuongLagrange(a)[:, :-1]
    Cy = CalculateCy(a,y)
    return Cy @ m