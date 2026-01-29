from graphic.shapes import set_pixel
from graphic.clipping import space_code, INSIDE


def circle_scanline(surface, xc, yc, r, fill_color, border_color):
    """Scan-line fill a circle centered at (xc, yc) with radius r"""
    
    # Get surface dimensions
    width, height = surface.get_size()

    # Iterate over each y-coordinate within the circle's bounding box
    for y in range(max(0, yc - r + 1), min(height, yc + r)):
        inside = False
        x_start = None
        x_end = None

        # Find the start and end x-coordinates for the current y
        for x in range(max(0, xc - r), min(width, xc + r + 1)):
            if (x - xc)**2 + (y - yc)**2 <= r*r:
                if not inside:
                    x_start = x
                    inside = True
                x_end = x

        if x_start is None:
            continue

        for x in range(x_start, x_end + 1):
            if 0 <= x < width and 0 <= y < height:
                if surface.get_at((x, y)) != border_color:
                    set_pixel(surface, x, y, fill_color)


def hoop_scanline(
    surface,
    xc, yc,
    a_outer, b_outer,
    a_inner, b_inner,
    fill_color,
    border_color
):
    """Scan-line fill a basketball hoop shape defined by two ellipses."""

    # Iterate over each y-coordinate within the outer ellipse's bounding box
    for y in range(yc - b_outer, yc + b_outer + 1):
        outer_x = []
        inner_x = []

        # Find intersection x-coordinates for the current y
        for x in range(xc - a_outer, xc + a_outer + 1):
            dx = x - xc
            dy = y - yc

            # Ellipse equations
            outer_eq = (dx*dx)/(a_outer*a_outer) + (dy*dy)/(b_outer*b_outer)
            inner_eq = (dx*dx)/(a_inner*a_inner) + (dy*dy)/(b_inner*b_inner)

            if outer_eq <= 1:
                outer_x.append(x)

            if inner_eq <= 1:
                inner_x.append(x)

        if not outer_x:
            continue

        left_outer  = min(outer_x)
        right_outer = max(outer_x)

        # Fill between outer and inner ellipses
        if inner_x:
            left_inner  = min(inner_x)
            right_inner = max(inner_x)

            for x in range(left_outer, left_inner):
                if surface.get_at((x, y)) != border_color:
                    set_pixel(surface, x, y, fill_color)

            for x in range(right_inner + 1, right_outer + 1):
                if surface.get_at((x, y)) != border_color:
                    set_pixel(surface, x, y, fill_color)
        else:
            for x in range(left_outer, right_outer + 1):
                if surface.get_at((x, y)) != border_color:
                    set_pixel(surface, x, y, fill_color)


def color_interpolate(color1, color2, t):
    """Interpolate between two colors."""
    r = int(color1[0] + (color2[0] - color1[0]) * t)
    g = int(color1[1] + (color2[1] - color1[1]) * t)
    b = int(color1[2] + (color2[2] - color1[2]) * t)

    # Clamp values to valid range
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    
    return r, g, b


def scanline_gradient_sky(surface, top_color, bottom_color):
    """
    Render a full-screen sky background using a polygon-based
    scanline gradient fill.

    Args:
        surface (pygame.Surface): Target surface.
        top_color (tuple): RGB color at the top of the screen.
        bottom_color (tuple): RGB color at the bottom of the screen.
    """
    width, height = surface.get_size()

    # Screen rectangle as a polygon
    points = [
        (0, 0),              # top-left
        (width, 0),          # top-right
        (width, height),     # bottom-right
        (0, height)          # bottom-left
    ]

    # Colors associated with each vertex
    colors = [
        top_color,     # top-left
        top_color,     # top-right
        bottom_color,  # bottom-right
        bottom_color   # bottom-left
    ]

    ys = [p[1] for p in points]
    y_min = int(min(ys))
    y_max = int(max(ys))

    n = len(points)

    for y in range(y_min, y_max):
        intersections = []

        for i in range(n):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % n]

            c0 = colors[i]
            c1 = colors[(i + 1) % n]

            # Ignore horizontal edges
            if y0 == y1:
                continue

            # Ensure y0 < y1
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
                c0, c1 = c1, c0

            # Scanline inclusion rule
            if y < y0 or y >= y1:
                continue

            # Edge interpolation
            t = (y - y0) / (y1 - y0)
            x = x0 + t * (x1 - x0)
            color_y = color_interpolate(c0, c1, t)

            intersections.append((x, color_y))

        # Sort intersections by x
        intersections.sort(key=lambda item: item[0])

        # Fill spans
        for i in range(0, len(intersections), 2):
            if i + 1 < len(intersections):
                x_start, color_start = intersections[i]
                x_end, color_end = intersections[i + 1]

                if x_end == x_start:
                    continue

                for x in range(int(x_start), int(x_end) + 1):
                    t = (x - x_start) / (x_end - x_start)
                    color = color_interpolate(color_start, color_end, t)
                    set_pixel(surface, x, y, color)


def scanline_polygon(surface, points, fill_color):
    """
    Scan-line fill a polygon defined by a list of points
    on the given surface.
    """
    ys = [p[1] for p in points]
    y_min = int(min(ys))
    y_max = int(max(ys))

    n = len(points)

    for y in range(y_min, y_max):
        intersections = []

        for i in range(n):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % n]

            # Ignore horizontal edges
            if y0 == y1:
                continue

            # Ensure y0 < y1
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0

            # Scanline inclusion rule
            if y < y0 or y >= y1:
                continue

            # Edge interpolation
            t = (y - y0) / (y1 - y0)
            x = x0 + t * (x1 - x0)

            intersections.append(x)

        # Sort intersections by x
        intersections.sort()

        # Fill spans
        for i in range(0, len(intersections), 2):
            if i + 1 < len(intersections):
                x_start = int(intersections[i])
                x_end = int(intersections[i + 1])

                for x in range(x_start, x_end + 1):
                    set_pixel(surface, x, y, fill_color)


def scanline_polygon_clipping(surface, points, fill_color, xmin, ymin, xmax, ymax):
    """
    Scan-line fill a polygon defined by a list of points
    on the given surface with clipping to a rectangular window.
    
    Args:
        surface: The surface to draw on.
        points: List of (x, y) points defining the polygon.
        fill_color: Color to fill the polygon.
        xmin (float): Minimum x-coordinate of the clipping window.
        ymin (float): Minimum y-coordinate of the clipping window.
        xmax (float): Maximum x-coordinate of the clipping window.
        ymax (float): Maximum y-coordinate of the clipping window.
    """
    ys = [p[1] for p in points]
    y_min = int(min(ys))
    y_max = int(max(ys))

    # Clip y range to window - ensure we don't go beyond ymax
    y_min = max(y_min, int(ymin))
    y_max = min(y_max, int(ymax))

    n = len(points)

    for y in range(y_min, y_max):
        intersections = []

        for i in range(n):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % n]

            # Ignore horizontal edges
            if y0 == y1:
                continue

            # Ensure y0 < y1
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0

            # Scanline inclusion rule
            if y < y0 or y >= y1:
                continue

            # Edge interpolation
            t = (y - y0) / (y1 - y0)
            x = x0 + t * (x1 - x0)

            intersections.append(x)

        # Sort intersections by x
        intersections.sort()

        # Fill spans with clipping
        for i in range(0, len(intersections), 2):
            if i + 1 < len(intersections):
                x_start = int(intersections[i])
                x_end = int(intersections[i + 1])

                # Clip x range to window
                x_start = max(x_start, int(xmin))
                x_end = min(x_end, int(xmax))

                for x in range(x_start, x_end + 1):
                    # Double check if pixel is inside clipping window
                    if space_code(x, y, xmin, ymin, xmax, ymax) == INSIDE:
                        set_pixel(surface, x, y, fill_color)


def scanline_texture(surface, points, uvs, texture, tex_w, tex_h):
    """
    Scan-line fill a polygon with texture mapping.
    """
    n = len(points)

    ys = [p[1] for p in points]
    y_min = int(min(ys))
    y_max = int(max(ys))

    for y in range(y_min, y_max):
        inter = []

        for i in range(n):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % n]

            u0, v0 = uvs[i]
            u1, v1 = uvs[(i + 1) % n]

            if y0 == y1:
                continue

            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
                u0, v0, u1, v1 = u1, v1, u0, v0

            if y < y0 or y >= y1:
                continue

            t = (y - y0) / (y1 - y0)

            x = x0 + t * (x1 - x0)
            u = u0 + t * (u1 - u0)
            v = v0 + t * (v1 - v0)

            inter.append((x, u, v))

        inter.sort(key=lambda i: i[0])

        for i in range(0, len(inter), 2):
            if i + 1 >= len(inter):
                continue

            x_start, u_start, v_start = inter[i]
            x_end,   u_end,   v_end   = inter[i + 1]

            if x_start == x_end:
                continue

            for x in range(int(x_start), int(x_end) + 1):
                t = (x - x_start) / (x_end - x_start)

                u = u_start + t * (u_end - u_start)
                v = v_start + t * (v_end - v_start)

                tx = int((u % 1.0) * tex_w)
                ty = int((v % 1.0) * tex_h)

                if 0 <= tx < tex_w and 0 <= ty < tex_h:
                    cor = texture.get_at((tx, ty))
                    set_pixel(surface, x, y, cor)