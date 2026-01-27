def indentity():
    return [
        [1, 0 ,0],
        [0, 1 ,0],
        [0, 0 ,1],
    ]

def translation(tx, ty):
    return [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1],
    ]

def scaling(sx, sy):
    return [
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1],
    ]

def rotation(angle_degrees):
    import math
    angle_radians = math.radians(angle_degrees)
    cos_a = math.cos(angle_radians)
    sin_a = math.sin(angle_radians)
    return [
        [cos_a, -sin_a, 0],
        [sin_a, cos_a, 0],
        [0, 0, 1],
    ]

def create_transformation():
    return indentity()

def multiply_matrices(a, b):
    result = [[0 for _ in range(len(b[0]))] for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                result[i][j] += a[i][k] * b[k][j]
    return result

def apply_transformation(points:list[list[int]], matrix:list[list[int]]):
    new_points = list()
    for x, y in points:
        transformed = multiply_matrices(matrix, [[x], [y], [1]])
        new_points.append((transformed[0][0], transformed[1][0]))
    return new_points