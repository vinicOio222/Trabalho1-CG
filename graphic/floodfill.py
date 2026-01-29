from graphic.shapes import set_pixel 
def flood_fill(surface, xc, yc, fill_color, border_color):
    width = surface.get_width()
    height = surface.get_height()

    stack = [(xc, yc)]
    while stack:
        x, y = stack.pop()

        if not (0 <= x < width and 0 <= y < height):
            continue

        current_color = surface.get_at((x, y))[:3]

        if current_color == border_color or current_color == fill_color:
            continue

        set_pixel(surface, x, y, fill_color)

        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))