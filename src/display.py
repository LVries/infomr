from vedo import load, show, interactor_modes

def display_model_from_file(file_path, cell_edge_width = .1):
    mesh = load(file_path)
    mesh.linewidth(cell_edge_width).flat()

    # print(mesh)
    show(mesh)
