from . import __surfaces__


def check_library_surfaces():
    print("Check library surfaces")
    for SurfaceClass in __surfaces__:
        surface = SurfaceClass()
        print("\t", surface, surface.check(20, 20, 1e-7))
