from gsurface.examples import tore_sim
from gsurface.serialize import save, load
from gsurface.serialize.encoder import ExplicitEncoder, ExplicitDecoder, ImplicitDecoder, ImplicitEncoder, AutoDecoder

expl_filename = __file__ + ".expl.json"
impl_filename = __file__ + ".impl.json"

save(expl_filename, tore_sim, indent=4, encoder=ExplicitEncoder)
save(impl_filename, tore_sim, indent=4, encoder=ImplicitEncoder)

oe = load(expl_filename, encoder=ExplicitDecoder)
oi = load(impl_filename, encoder=ImplicitDecoder)

oea = load(expl_filename, encoder=AutoDecoder)
oia = load(impl_filename, encoder=AutoDecoder)

print(oe)
print(oi)
print(oea)
print(oia)