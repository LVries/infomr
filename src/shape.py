class Shape:
    def __init__(self, shape_class, vertices, faces):
        self.shape_class = shape_class
        self.vertices = vertices 
        self.faces = faces  

    def nr_vertices(self):
        return len(self.vertices)

    def nr_faces(self):
        return len(self.faces)