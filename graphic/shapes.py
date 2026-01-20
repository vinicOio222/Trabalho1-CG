"""Function for drawing graphic on a surface."""

def set_pixel(surface, x, y, color):
    """Set the pixel at (x, y) on the given surface to the specified color."""
    if 0 <= x < surface.get_width() and 0 <= y < surface.get_height():
        surface.set_at((int(x), int(y)), color)


def draw_line(surface, x0, y0, x1, y1, color):
    """
    Draw a line from (x1, y1) to (x2, y2)
    on the given surface using Bresenham's algorithm.
    """
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        set_pixel(surface, x0, y0, color)
        if x0 == x1 and y0 == y1:
            break
        err2 = err * 2
        if err2 > -dy:
            err -= dy
            x0 += sx
        if err2 < dx:
            err += dx
            y0 += sy


def draw_circle(surface, xc, yc, r, color):
    """
    Draw a circle centered at (xc, yc) with radius r
    on the given surface using the Midpoint Circle algorithm.
    """
    # Initial points
    x = 0
    y = r
    d = 1 - r

    # Draw the initial points in all octant's
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


def draw_arc(surface, cx, cy, r_arc, ball_cx, ball_cy, ball_r, color):
    """
    Draw an arc centered at (cx, cy) with radius r_arc
    on the given surface. Only draw pixels that lie within
    the circle defined by (ball_cx, ball_cy, ball_r).
    Used on the basketball to draw the arcs.
    """
    x = 0
    y = r_arc
    d = 1 - r_arc

    # Draw the arc points conditionally
    while x <= y:
        points = [
            ( x,  y), ( y,  x), (-x,  y), (-y,  x),
            ( x, -y), ( y, -x), (-x, -y), (-y, -x)
        ]
        # Check each point if it lies within the ball's circle
        for px, py in points:
            sx = cx + px
            sy = cy + py

            if (sx - ball_cx)**2 + (sy - ball_cy)**2 <= ball_r**2:
                set_pixel(surface, sx, sy, color)

        # Update decision parameter and coordinates
        if d < 0:
            d += 2*x + 3
        else:
            d += 2*(x - y) + 5
            y -= 1
        x += 1


def _plot_ellipse_points(surface, xc, yc, x, y, color):
    """Helper function to plot the four symmetrical points of an ellipse."""
    points = [
        (x, y), (-x, y),
        (x, -y), (-x, -y)
    ]

    # Plot the points
    for px, py in points:
        set_pixel(surface, xc + px, yc + py, color)


def draw_ellipse(surface, xc, yc, a, b, color):
    """Draw an ellipse centered at (xc, yc) with semi-major axis a and semi-minor axis b
    on the given surface using the Midpoint Ellipse algorithm. Used on the basketball hoop.
    """
    # Starting point at the top of the ellipse
    x = 0
    y = b

    # Precompute squared axis lengths to avoid repeated multiplications
    a2 = a * a
    b2 = b * b

    # Initial derivatives of the ellipse equation
    # dx and dy are used to determine the slope transition
    dx = 2 * b2 * x
    dy = 2 * a2 * y

    # Decision parameter for Region 1 (slope > -1)
    d1 = b2 - a2 * b + 0.25 * a2

    # Region 1
    # In this region, the ellipse slope magnitude is less than 1
    while dx < dy:
        _plot_ellipse_points(surface, xc, yc, x, y, color)

        if d1 < 0:
            # Choose the pixel directly to the right (E)
            x += 1
            dx += 2 * b2
            d1 += dx + b2
        else:
            # Choose the pixel diagonally down-right (SE)
            x += 1
            y -= 1
            dx += 2 * b2
            dy -= 2 * a2
            d1 += dx - dy + b2

    # Decision parameter for Region 2 (slope <= -1)
    # Transition occurs when dx >= dy
    d2 = (
        b2 * (x + 0.5) ** 2
        + a2 * (y - 1) ** 2
        - a2 * b2
    )

    # Region 2
    # In this region, the ellipse slope magnitude is greater than or equal to 1
    while y >= 0:
        # Plot the four symmetric points of the ellipse
        _plot_ellipse_points(surface, xc, yc, x, y, color)

        if d2 > 0:
            # Choose the pixel directly below (S)
            y -= 1
            dy -= 2 * a2
            d2 += a2 - dy
        else:
            # Choose the pixel diagonally down-right (SE)
            y -= 1
            x += 1
            dx += 2 * b2
            dy -= 2 * a2
            d2 += dx - dy + a2