def identity():
    """
    Create a 3x3 identity matrix.

    Returns:
        list[list[int]]: A 3x3 identity matrix.
    """
    return [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ]


def translation(tx, ty):
    """
    Create a 3x3 translation matrix.

    Args:
        tx (float): Translation in x-direction.
        ty (float): Translation in y-direction.

    Returns:
        list[list[float]]: A 3x3 translation matrix.
    """
    return [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1],
    ]


def scaling(sx, sy):
    """
    Create a 3x3 scaling matrix.

    Args:
        sx (float): Scale factor in x-direction.
        sy (float): Scale factor in y-direction.

    Returns:
        list[list[float]]: A 3x3 scaling matrix.
    """
    return [
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1],
    ]


def rotation(angle_degrees):
    """
    Create a 3x3 rotation matrix.

    Args:
        angle_degrees (float): Rotation angle in degrees.

    Returns:
        list[list[float]]: A 3x3 rotation matrix.
    """
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
    """
    Create an identity transformation matrix.

    Returns:
        list[list[int]]: A 3x3 identity matrix.
    """
    return identity()


def multiply_matrices(a, b):
    """
    Multiply two matrices.

    Args:
        a (list[list[float]]): First matrix (m x n).
        b (list[list[float]]): Second matrix (n x p).

    Returns:
        list[list[float]]: Result matrix (m x p).
    """
    result = [[0 for _ in range(len(b[0]))] for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                result[i][j] += a[i][k] * b[k][j]
    return result


def apply_transformation(points: list[list[int]], matrix: list[list[int]]):
    """
    Apply transformation matrix to a list of points.

    Args:
        points (list[tuple[int, int]]): List of (x, y) points.
        matrix (list[list[int]]): 3x3 transformation matrix.

    Returns:
        list[tuple[float, float]]: List of transformed points.
    """
    new_points = list()
    for x, y in points:
        transformed = multiply_matrices(matrix, [[x], [y], [1]])
        new_points.append((transformed[0][0], transformed[1][0]))
    return new_points


def window_viewport(window, viewport):
    """
    Create a transformation matrix from window (world) to viewport (screen).

    Steps:
    1. Translate window to origin
    2. Scale to viewport dimensions
    3. Translate to viewport position

    Args:
        window (tuple): (xmin, ymin, xmax, ymax) - world coordinates
        viewport (tuple): (xmin, ymin, xmax, ymax) - viewport coordinates on screen

    Returns:
        list[list[float]]: 3x3 transformation matrix
    """
    # Extract coordinates
    w_xmin, w_ymin, _, _ = window
    v_xmin, v_ymin, _, _ = viewport

    # Get scale factors
    sx, sy = get_scale_factors(window, viewport)

    # Create transformation matrix
    m = identity()

    # 1. Translate window to origin
    m = multiply_matrices(translation(-w_xmin, -w_ymin), m)

    # 2. Scale to viewport dimensions
    m = multiply_matrices(scaling(sx, sy), m)

    # 3. Translate to viewport position
    m = multiply_matrices(translation(v_xmin, v_ymin), m)

    return m


def transform_point(x, y, matrix):
    """
    Apply transformation to a single point.

    Args:
        x (float): x-coordinate of the point.
        y (float): y-coordinate of the point.
        matrix (list[list[float]]): 3x3 transformation matrix.

    Returns:
        tuple[float, float]: (x', y') transformed coordinates.
    """
    result = multiply_matrices(matrix, [[x], [y], [1]])
    return result[0][0], result[1][0]


def get_scale_factors(window, viewport):
    """
    Calculate scale factors for window-to-viewport transformation.

    Args:
        window (tuple): (xmin, ymin, xmax, ymax) - world coordinates
        viewport (tuple): (xmin, ymin, xmax, ymax) - viewport coordinates

    Returns:
        tuple[float, float]: (sx, sy) scale factors
    """
    w_xmin, w_ymin, w_xmax, w_ymax = window
    v_xmin, v_ymin, v_xmax, v_ymax = viewport

    sx = (v_xmax - v_xmin) / (w_xmax - w_xmin)
    sy = (v_ymax - v_ymin) / (w_ymax - w_ymin)

    return sx, sy


def transform_dimension(width, height, sx, sy):
    """
    Transform dimensions (width, height) by applying scale only.
    Use this function for transforming sizes, radii, widths, etc.
    DO NOT use for point coordinates!

    Args:
        width (float): Width/dimension in x-direction.
        height (float): Height/dimension in y-direction.
        sx (float): Scale factor in x-direction.
        sy (float): Scale factor in y-direction.

    Returns:
        tuple[float, float]: (width', height') transformed dimensions.
    """
    return abs(width * sx), abs(height * sy)