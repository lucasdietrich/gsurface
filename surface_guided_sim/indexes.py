ui, vi = 0, 1

xyz = 0, 1, 2

(
    xi, yi, zi,
    duxi, dvxi, duyi, dvyi, duzi, dvzi,
    duuxi, duvxi, dvvxi, duuyi, duvyi, dvvyi, duuzi, duvzi, dvvzi
) = list(range(18))

Si = slice(0, 3)
Vi = slice(3, 6)
Fi = slice(6, 9)

(
    vxi, vyi, vzi,
    fxi, fyi, fzi,
    nVi, nFi,
    Eki, Epi, Emi
) = list(range(3, 14))
