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

def windown_viewport(janela, viewport):
    """
    Cria matriz de transformação de janela (mundo) para viewport (tela).
    
    Args:
        janela: (xmin, ymin, xmax, ymax) - coordenadas do mundo
        viewport: (xmin, ymin, xmax, ymax) - coordenadas da viewport na tela
        invert_y: Se True, inverte o eixo Y (necessário para Pygame)
    
    Returns:
        Matriz de transformação 3x3
    """
    
    # 1. Translada janela para origem
    Wxmin, Wymin, _, _ = janela
    Vxmin, Vymin, _, _ = viewport

    m = indentity()
    
    sx, sy = get_scale_factors(janela, viewport) 

    m = multiply_matrices(translation(-Wxmin, -Wymin), m)

    # 2. Escala para dimensões da viewport
    m = multiply_matrices(scaling(sx, sy), m)

    # 3. Translada para posição da viewport
    
    m = multiply_matrices(translation(Vxmin, Vymin), m)

    return m

def transform_point(x, y, matrix):
    """
    Aplica transformação em um único ponto.
    
    Args:
        x, y: coordenadas do ponto
        matrix: matriz de transformação 3x3
    
    Returns:
        Tupla (x', y') com coordenadas transformadas
    """
    result = multiply_matrices(matrix, [[x], [y], [1]])
    return result[0][0], result[1][0]

def get_scale_factors(janela, viewport):
    """
    Calcula os fatores de escala de uma transformação janela-viewport.
    
    Args:
        janela: (xmin, ymin, xmax, ymax) - coordenadas do mundo
        viewport: (xmin, ymin, xmax, ymax) - coordenadas da viewport
    
    Returns:
        Tupla (sx, sy) com fatores de escala
    """
    Wxmin, Wymin, Wxmax, Wymax = janela
    Vxmin, Vymin, Vxmax, Vymax = viewport
    
    sx = (Vxmax - Vxmin) / (Wxmax - Wxmin)
    sy = (Vymax - Vymin) / (Wymax - Wymin)
    
    return sx, sy

def transform_dimension(width, height, sx, sy):
    """
    Transforma dimensões (largura, altura) aplicando apenas escala.
    Use esta função para transformar tamanhos, raios, larguras, etc.
    NÃO use para coordenadas de pontos!
    
    Args:
        width: largura/dimensão em x
        height: altura/dimensão em y
        sx, sy: fatores de escala
    
    Returns:
        Tupla (width', height') com dimensões transformadas
    """
    return abs(width * sx), abs(height * sy)