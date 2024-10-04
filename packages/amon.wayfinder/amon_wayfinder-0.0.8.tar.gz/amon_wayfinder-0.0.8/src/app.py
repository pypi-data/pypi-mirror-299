from wayfinder import MeshGenerator


if __name__ == "__main__":

    gen = MeshGenerator()
    mesh = gen.debug("test", 0.3, 30)

    print(mesh)
