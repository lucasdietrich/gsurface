ui, vi = 0, 1

xyz = 0, 1, 2

(
    xi, yi, zi,
    duxi, dvxi, duyi, dvyi, duzi, dvzi,
    duuxi, duvxi, dvvxi, duuyi, duvyi, dvvyi, duuzi, duvzi, dvvzi
) = list(range(18))

Si = slice(0, 3)
Vi = slice(0, 3)
Fi = slice(0, 3)

(
    vxi, vyi, vzi,
    fxi, fyi, fzi,
    nVi, nFi, Eci
) = list(range(3, 12))
