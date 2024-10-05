from PIL import Image, ImageDraw, ImageStat

def average_color_stat(area):
    stat = ImageStat.Stat(area)
    return tuple(int(c) for c in stat.mean)

def create_triangular_mask(size, vertices):
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.polygon(vertices, fill=255)
    return mask

def pixelate_image_with_right_triangles(image, triangle_size):
    width, height = image.size

    # Create a new blank image
    pixelated_img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(pixelated_img)
    
    # Loop through the image in blocks of triangle_size
    for y in range(0, height, triangle_size):
        for x in range(0, width, triangle_size):
            # Get the block
            block = image.crop((x, y, x + triangle_size, y + triangle_size))
            
            # Define vertices for the top-left triangle
            top_left_vertices = [(0, 0), (triangle_size, 0), (0, triangle_size)]
            top_left_mask = create_triangular_mask(block.size, top_left_vertices)
            top_left_triangle = Image.composite(block, Image.new('RGB', block.size), top_left_mask)
            avg_color_top_left = average_color_stat(top_left_triangle)
            
            # Define vertices for the bottom-right triangle
            bottom_right_vertices = [(triangle_size, triangle_size), (0, triangle_size), (triangle_size, 0)]
            bottom_right_mask = create_triangular_mask(block.size, bottom_right_vertices)
            bottom_right_triangle = Image.composite(block, Image.new('RGB', block.size), bottom_right_mask)
            avg_color_bottom_right = average_color_stat(bottom_right_triangle)

            # Draw the top-left triangle
            draw.polygon([(x, y), (x + triangle_size, y), (x, y + triangle_size)], fill=avg_color_top_left)
            
            # Draw the bottom-right triangle
            draw.polygon([(x + triangle_size, y + triangle_size), (x, y + triangle_size), (x + triangle_size, y)], fill=avg_color_bottom_right)
    
    return pixelated_img