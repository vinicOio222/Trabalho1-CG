from graphic.shapes import set_pixel


def circle_scanline(surface, xc, yc, r, fill_color, border_color):
    """Scan-line fill a circle centered at (xc, yc) with radius r"""

    # Iterate over each y-coordinate within the circle's bounding box
    for y in range(yc - r + 1, yc + r):
        inside = False
        x_start = None
        x_end = None

        # Find the start and end x-coordinates for the current y
        for x in range(xc - r, xc + r + 1):
            if (x - xc)**2 + (y - yc)**2 <= r*r:
                if not inside:
                    x_start = x
                    inside = True
                x_end = x

        if x_start is None:
            continue

        for x in range(x_start, x_end + 1):
            if surface.get_at((x, y)) != border_color:
                set_pixel(surface,x, y, fill_color)


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
