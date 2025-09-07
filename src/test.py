import vedo
from vedo import load, show, interactor_modes

cell_edge_width = .1

mesh = load('./data/shape-database/Fish/D00012.obj')
mesh.linewidth(cell_edge_width).flat()

print(mesh)
show(mesh)