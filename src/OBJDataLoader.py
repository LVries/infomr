class OBJDataloader:
    file_path: str
    vertices: list
    faces: list
    
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        vertices = []
        faces = []
        with open(self.file_path, 'r') as file:
            for line in file:
                if line.startswith('v '):
                    parts = line.strip().split()
                    vertex = list(map(float, parts[1:4]))
                    vertices.append(vertex)
                elif line.startswith('f '):
                    parts = line.strip().split()
                    face = [int(part.split('/')[0]) - 1 for part in parts[1:]]
                    faces.append(face)
        self.vertices = vertices
        self.faces = faces

    def get_vertices(self):
        return self.vertices
    def get_faces(self):
        return self.faces
    
    def get_vertices_for_face(self):
        verticesForFace = []
        for face in self.faces:
            faceVertices = [self.vertices[idx] for idx in face]
            verticesForFace.append(faceVertices)
        return verticesForFace
    
        