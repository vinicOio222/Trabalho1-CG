"""Cohen-Sutherland line clipping algorithm implementation."""

# Region codes for Cohen-Sutherland algorithm
INSIDE = 0  # 0000 - Point is inside the clipping window
LEFT   = 1  # 0001 - Point is to the left of the clipping window
RIGHT  = 2  # 0010 - Point is to the right of the clipping window
BOTTOM = 4  # 0100 - Point is below the clipping window
TOP    = 8  # 1000 - Point is above the clipping window

def space_code(x, y, xmin, ymin, xmax, ymax):
    """
    Calculate the region code for a point relative to a clipping window.

    Args:
        x (float): x-coordinate of the point.
        y (float): y-coordinate of the point.
        xmin (float): Minimum x-coordinate of the clipping window.
        ymin (float): Minimum y-coordinate of the clipping window.
        xmax (float): Maximum x-coordinate of the clipping window.
        ymax (float): Maximum y-coordinate of the clipping window.

    Returns:
        int: Region code representing the position of the point relative to the window.
    """
    code = INSIDE
    if x < xmin: code |= LEFT
    elif x > xmax: code |= RIGHT
    if y < ymin: code |= TOP      
    elif y > ymax: code |= BOTTOM
    return code

def cohen_sutherland(x0, y0, x1, y1, xmin, ymin, xmax, ymax):
    """
    Clip a line segment to fit within a rectangular clipping window using Cohen-Sutherland algorithm.

    Args:
        x0 (float): x-coordinate of the first endpoint of the line.
        y0 (float): y-coordinate of the first endpoint of the line.
        x1 (float): x-coordinate of the second endpoint of the line.
        y1 (float): y-coordinate of the second endpoint of the line.
        xmin (float): Minimum x-coordinate of the clipping window.
        ymin (float): Minimum y-coordinate of the clipping window.
        xmax (float): Maximum x-coordinate of the clipping window.
        ymax (float): Maximum y-coordinate of the clipping window.

    Returns:
        tuple: (accept, x0, y0, x1, y1) where accept is True if the line is visible
               (even if clipped), and x0, y0, x1, y1 are the clipped coordinates.
               If the line is completely outside, returns (False, None, None, None, None).
    """
    # Calculate region codes for both endpoints
    c0 = space_code(x0, y0, xmin, ymin, xmax, ymax)
    c1 = space_code(x1, y1, xmin, ymin, xmax, ymax)

    while True:
        # Both endpoints inside window - trivially accept
        if not (c0 | c1):
            return True, x0, y0, x1, y1

        # Both endpoints share an outside region - trivially reject
        if c0 & c1:
            return False, None, None, None, None
        
        # Pick an endpoint that is outside the window
        c_out = c0 if c0 else c1

        # Calculate intersection point with clipping boundary
        if c_out & TOP:
            x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
            y = ymin
        elif c_out & BOTTOM:
            x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)
            y = ymax
        elif c_out & RIGHT:
            y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
            x = xmax
        elif c_out & LEFT:
            y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
            x = xmin

        # Replace the outside point with the intersection point
        if c_out == c0:
            x0, y0 = x, y
            c0 = space_code(x0, y0, xmin, ymin, xmax, ymax)
        else:
            x1, y1 = x, y
            c1 = space_code(x1, y1, xmin, ymin, xmax, ymax)