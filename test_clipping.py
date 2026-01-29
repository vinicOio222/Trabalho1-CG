# Test script to verify clipping bounds
minimap_bounds = (10, 10, 160, 120)
xmin, ymin, xmax, ymax = minimap_bounds[0], minimap_bounds[1], minimap_bounds[0] + minimap_bounds[2], minimap_bounds[1] + minimap_bounds[3]

print(f"Minimap bounds: {minimap_bounds}")
print(f"xmin={xmin}, ymin={ymin}, xmax={xmax}, ymax={ymax}")
