"""Function for drawing graphic on a surface."""

def set_pixel(surface, x, y, color):
    """Set the pixel at (x, y) on the given surface to the specified color."""
    if 0 <= x < surface.get_width() and 0 <= y < surface.get_height():
        surface.set_at((int(x), int(y)), color)


def line_dda(surface, x1, y1, x2, y2, color):
    """
    Draw a line from (x1, y1) to (x2, y2)
    on the given surface using the DDA algorithm.
    """
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


def line_bresenham(surface, x1, y1, x2, y2, color):
    """
    Draw a line from (x1, y1) to (x2, y2)
    on the given surface using Bresenham's algorithm.
    """
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        set_pixel(surface, x1, y1, color)
        if x1 == x2 and y1 == y2:
            break
        err2 = err * 2
        if err2 > -dy:
            err -= dy
            x1 += sx
        if err2 < dx:
            err += dx
            y1 += sy


def draw_circle(surface, xc, yc, r, color):
    """
    Draw a circle centered at (xc, yc) with radius r
    on the given surface using the Midpoint Circle algorithm.
    """
    # Initial points
    x = 0
    y = r
    d = 1 - r

    # Draw the initial points in all octants
    while x<=y:
        for px, py in [
            (x, y), (y, x), (-x, y), (-y, x),
            (x, -y), (y, -x), (-x, -y), (-y, -x)
        ]:
            set_pixel(surface, xc + px, yc + py, color)
        # Update decision parameter and coordinates
        if d < 0:
            # if d is less than 0, choose East pixel
            d += 2 * x + 3
        else:
            # else choose South-East pixel
            d += 2 * (x - y) + 5
            y -= 1
        x += 1 # Move to the next pixel in x direction
