from gsurface.surface import __surfaces__


def check_library_surfaces(nu: int = 20, nv: int = 20, tolerance: float = 1e-7):
    print("Check library surfaces")
    for SurfaceClass in __surfaces__:
        surface = SurfaceClass()

        valid = surface.check(nu, nv, tolerance)

        print("\t", surface, valid)

        if not valid:
            surface.check_verbose(nu, nv, tolerance)
    print("Done")
