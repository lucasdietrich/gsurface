ui, vi = 0, 1

xyz = 0, 1, 2

# flat SJH
(
    xi, yi, zi,
    duxi, dvxi, duyi, dvyi, duzi, dvzi,
    duuxi, duvxi, dvvxi, duuyi, duvyi, dvvyi, duuzi, duvzi, dvvzi
) = list(range(18))

# SJH indexes
Si = 0
Ji = 1
Hi = 2

# solutions return
Tyi = slice(0, None), slice(0, 3)  # trajectory : differents positions in time
Pi = slice(0, 3)  # position
Vi = slice(3, 6)  # speed
Fi = slice(6, 9)  # force

(
    txi, tyi, tzi,
    vxi, vyi, vzi,
    fxi, fyi, fzi,
    nVi, nFi,
    Eki, Epi, Emi
) = list(range(14))
