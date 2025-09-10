from vedo import load, Plotter
from PyQt6.QtCore import QTimer


CELL_EDGE_WIDTH = 0.1

class MeshViewer:
    def __init__(self, parent_widget):
        self.plotter = Plotter(bg="white", axes=1, qt_widget=parent_widget)
        self.mesh = None
        self.camera_initialized = False

    def load_mesh(self, file_path):
        mesh = load(file_path)
        mesh.linewidth(CELL_EDGE_WIDTH).flat()
        return mesh

    def display_mesh(self, file_path):
        if self.mesh:
            self.plotter.remove(self.mesh)
        self.mesh = self.load_mesh(file_path)
        self.plotter.add(self.mesh)
        # Only reset camera once after initial widget sizing
        if not self.camera_initialized:
            # Use a timer to ensure the widget has a valid size
            QTimer.singleShot(50, self._reset_camera)
            self.camera_initialized = True
        self.plotter.show()
    
    def _reset_camera(self):
        self.plotter.reset_camera()
        self.plotter.show()