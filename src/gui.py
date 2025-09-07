import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget, QLabel, QSizePolicy
from MeshViewer import MeshViewer
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class MainWindow(QMainWindow):
    def __init__(self, data_dir="./data/shape-database"):
        super().__init__()
        self.setWindowTitle("Mesh Viewer")
        self.data_dir = data_dir

        layout = QVBoxLayout()

        # Folder dropdown
        self.folder_combo = QComboBox()
        self.folder_combo.addItems(sorted(os.listdir(self.data_dir)))
        self.folder_combo.currentTextChanged.connect(self.update_files)
        layout.addWidget(QLabel("Select Shape Folder:"))
        layout.addWidget(self.folder_combo)

        # File dropdown
        self.file_combo = QComboBox()
        layout.addWidget(QLabel("Select OBJ File:"))
        layout.addWidget(self.file_combo)

        # VTK render widget
        self.vtk_widget = QVTKRenderWindowInteractor()
        self.vtk_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.vtk_widget, stretch=1)

        # Detect resize events to keep the mesh centered
        self.vtk_widget.resizeEvent = self.on_vtk_resize

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Mesh viewer
        self.viewer = MeshViewer(self.vtk_widget)

        # Initialize file list and render first mesh safely
        self.update_files(self.folder_combo.currentText())

        # Render mesh only when OBJ file changes
        self.file_combo.currentTextChanged.connect(self.display_selected_mesh)

    def update_files(self, folder_name):
        folder_path = os.path.join(self.data_dir, folder_name)
        obj_files = [f for f in os.listdir(folder_path) if f.endswith(".obj")]

        self.file_combo.blockSignals(True)
        self.file_combo.clear()
        self.file_combo.addItems(sorted(obj_files))
        self.file_combo.blockSignals(False)

        # Safely select and render first file, if available
        if obj_files:
            first_file = sorted(obj_files)[0]
            self.file_combo.setCurrentText(first_file)  # triggers rendering via currentTextChanged

    def display_selected_mesh(self, file_name):
        if not file_name:
            return
        folder_name = self.folder_combo.currentText()
        file_path = os.path.join(self.data_dir, folder_name, file_name)
        self.viewer.display_mesh(file_path)

    def on_vtk_resize(self, event):
        """Keep the mesh centered when resizing the VTK widget."""
        self.viewer.plotter.render()
        super(QVTKRenderWindowInteractor, self.vtk_widget).resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1000, 700)
    window.show()
    window.viewer.plotter.interactor.Initialize()
    window.viewer.plotter.interactor.Start()
    sys.exit(app.exec())