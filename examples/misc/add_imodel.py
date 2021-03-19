from gsurface.examples import model_structure, tore_sim

m1 = model_structure + model_structure

print("m1 = model_structure + model_structure\n", m1)

m2 = model_structure + tore_sim

print("m2 = model_structure + tore_sim\n", m2)

m3 = tore_sim + model_structure

print("m3 = tore_sim + model_structure\n", m3)
