"""Function for drawing graphic on a surface."""

def set_pixel(surface, x, y, color):
    """Set the pixel at (x, y) on the given surface to the specified color."""
    if 0 <= x < surface.get_width() and 0 <= y < surface.get_height():
        surface.set_at((int(x), int(y)), color)


def line_dda(surface, x1, y1, x2, y2, color):
    """Draw a line from (x1, y1) to (x2, y2) on the given surface using the DDA algorithm."""
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))

    if steps == 0:
        set_pixel(surface, x1, y1, color)
        return

    x_inc = dx / steps
    y_inc = dy / steps

    x = x1
    y = y1
    for _ in range(steps + 1):
        set_pixel(surface, round(x), round(y), color)
        x += x_inc
        y += y_inc