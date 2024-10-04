import trimesh
import numpy as np
from numpy import float64, ndarray

from .assets import loadObj as loadObj


class DebugMesh:

    verticies: ndarray
    walkable: bytes

    def __init__(self, verticies: ndarray, walkable: bytes) -> None:
        self.verticies = verticies
        self.walkable = walkable


class Generator:
    coss: float64

    def _is_walkable(self, faces, vertices) -> np.ndarray:
        v0 = vertices[faces[:, 0]]
        v1 = vertices[faces[:, 1]]
        v2 = vertices[faces[:, 2]]

        normals = np.cross(v1 - v0, v2 - v0)
        norms = np.linalg.norm(normals, axis=1)
        normals = normals / norms[:, np.newaxis]
        walkable = np.abs(normals[:, 1]) > self.coss

        return walkable

    def _simplify(self, vertices, faces, reduction: float):
        mesh = trimesh.Trimesh(vertices, faces)
        simplified_mesh = mesh.simplify_quadric_decimation(percent=reduction)

        return (
            np.ascontiguousarray(simplified_mesh.vertices),
            np.ascontiguousarray(simplified_mesh.faces),
        )

    def _create(self, faces, verticies):
        return self._is_walkable(faces, verticies)

    def _to_bytes(self, bools) -> bytes:
        packed = np.packbits(bools.astype(np.uint8))
        return packed.tobytes()

    def createNavMesh(self, fileName: str, reduction: float, maxSlope: int) -> bytes:
        objVertices, objFaces = loadObj(fileName)
        verticies, faces = self._simplify(objVertices, objFaces, reduction)
        self.coss = np.cos(np.radians(maxSlope))

        return self._to_bytes(self._create(faces, verticies))

    def debug(self, fileName: str, reduction: float, maxSlope: int):
        objVertices, objFaces = loadObj(fileName)
        verticies, faces = self._simplify(objVertices, objFaces, reduction)
        self.coss = np.cos(np.radians(maxSlope))

        return DebugMesh(verticies, self._to_bytes(self._create(faces, verticies)))
