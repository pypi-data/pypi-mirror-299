import numpy as np
from .utils import timer


@timer
def loadObj(fileName):
    vertices = []
    faces = []

    with open(f"data/maps/{fileName}.obj", "r") as f:
        for line in f:
            if line.startswith("v "):
                parts = line.split()
                v = [float(parts[1]), float(parts[2]), float(parts[3])]
                vertices.append(v)

            elif line.startswith("f "):
                parts = line.split()
                face = [int(p.split("/")[0]) - 1 for p in parts[1:]]
                faces.append(face)

    vertices = np.array(vertices, dtype="f4")
    return vertices, faces
