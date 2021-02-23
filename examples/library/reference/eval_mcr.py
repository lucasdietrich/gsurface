from gsurface.advanced.complexity.mcr import ModelComplexityRepresentation


mcrs = [
    'iM62-S62T62R62-F12I324-T10000',
    'M-F12-T100',
    'iM2-I-T100',
    'M-T1000',
    'M-S3T3R2-T1000',
    'M-S3T3R2'
]

for mcr in mcrs:
    MCR = ModelComplexityRepresentation.from_mcr(mcr)
    print(mcr, MCR.mcr(True), MCR.complexity(), MCR.mcr_number())
