from gsurface.surface.plan import Plan, np
from gsurface.plotter.mayavi import mayavi_plot_surfaces, mlab, SurfacePlot

# definition
plan = Plan.from_rotations(-np.pi / 2, np.pi / 2, shift=1.0)
U, V = plan.mesh(50, 50)  # mesh
surface = plan.build_surface(U, V)  # surface mesh

# __repr__
print(plan)

# check
err = 0
U, V = plan.mesh(50, 50)
for u in U:
    for v in V:
        err += abs(plan.utest(u, v))
print("Ok ?", err == 0.0)

# plot
mayavi_plot_surfaces([
    SurfacePlot(surface, True, 0)
], show=False)
mlab.points3d(0, 0, 0, color=(1, 0, 0), scale_factor=0.05)
mlab.show()

