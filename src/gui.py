import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget,
    QSizePolicy, QPushButton, QStackedWidget, QHBoxLayout, QFormLayout
)
from MeshViewer import MeshViewer
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class MainWindow(QMainWindow):
    def __init__(self, data_dir="./data/shape-database"):
        super().__init__()
        self.setWindowTitle("Mesh Viewer App")
        self.data_dir = data_dir

        # --- Stacked widget for multiple screens ---
        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)

        # --- Page 1: Main Menu ---
        self.menu_page = QWidget()
        menu_layout = QVBoxLayout()

        # Dropdowns in form layout
        form_layout = QFormLayout()
        self.folder_combo = QComboBox()
        self.folder_combo.addItems(sorted(os.listdir(self.data_dir)))
        self.folder_combo.currentTextChanged.connect(self.update_files)
        form_layout.addRow("Select Shape Folder:", self.folder_combo)

        self.file_combo = QComboBox()
        form_layout.addRow("Select OBJ File:", self.file_combo)

        menu_layout.addLayout(form_layout)

        # Buttons (Select + placeholder for future)
        button_row = QHBoxLayout()
        self.select_button = QPushButton("Open Mesh Viewer")
        self.select_button.clicked.connect(self.open_mesh_viewer)
        button_row.addWidget(self.select_button)
        menu_layout.addLayout(button_row)

        self.menu_page.setLayout(menu_layout)
        self.stacked.addWidget(self.menu_page)

        # --- Page 2: Mesh Viewer ---
        self.viewer_page = QWidget()
        viewer_layout = QVBoxLayout()

        # VTK widget
        self.vtk_widget = QVTKRenderWindowInteractor()
        self.vtk_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        viewer_layout.addWidget(self.vtk_widget, stretch=1)

        # Back button
        self.back_button = QPushButton("Back to Menu")
        self.back_button.clicked.connect(self.go_back_to_menu)
        viewer_layout.addWidget(self.back_button)
        
        self.toggle_lines_button = QPushButton("Toggle Mesh Lines")
        self.toggle_lines_button.clicked.connect(self.show_lines)
        viewer_layout.addWidget(self.toggle_lines_button)


        self.viewer_page.setLayout(viewer_layout)
        self.stacked.addWidget(self.viewer_page)

        # MeshViewer will be created later when needed
        self.viewer = None

        # Initialize file list
        self.update_files(self.folder_combo.currentText())

        # Start with menu page
        self.stacked.setCurrentWidget(self.menu_page)

    def show_lines(self):
        if self.viewer:
            current_text = self.toggle_lines_button.text()
            if current_text == "Show Mesh Lines":
                self.viewer.show_lines(True)
                self.toggle_lines_button.setText("Hide Mesh Lines")
            else:
                self.viewer.show_lines(False)
                self.toggle_lines_button.setText("Show Mesh Lines")

    def update_files(self, folder_name):
        folder_path = os.path.join(self.data_dir, folder_name)
        obj_files = [f for f in os.listdir(folder_path) if f.endswith(".obj")]

        self.file_combo.blockSignals(True)
        self.file_combo.clear()
        self.file_combo.addItems(sorted(obj_files))
        self.file_combo.blockSignals(False)

    def open_mesh_viewer(self):
        file_name = self.file_combo.currentText()
        if not file_name:
            return
        folder_name = self.folder_combo.currentText()
        file_path = os.path.join(self.data_dir, folder_name, file_name)

        if self.viewer is None:
            self.viewer = MeshViewer(self.vtk_widget)

        self.viewer.display_mesh(file_path)
        self.vtk_widget.resizeEvent = self.on_vtk_resize

        self.stacked.setCurrentWidget(self.viewer_page)

        self.viewer.plotter.interactor.Initialize()
        self.viewer.plotter.interactor.Start()

    def go_back_to_menu(self):
        self.stacked.setCurrentWidget(self.menu_page)

    def on_vtk_resize(self, event):
        if self.viewer:
            self.viewer.plotter.render()
        super(QVTKRenderWindowInteractor, self.vtk_widget).resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1000, 600)
    window.show()
    sys.exit(app.exec())
