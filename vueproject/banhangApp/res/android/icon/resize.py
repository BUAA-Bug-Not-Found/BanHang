from PIL import Image

def resize_image(input_path, output_path, size):
    image = Image.open(input_path)
    image = image.resize((size, size))
    image.save(output_path)

input_file = "微信图片_20240509160011.png"
sizes = [36, 48, 72, 96, 144, 192]

for size in sizes:
    output_file = f"icon{size}.png"
    resize_image(input_file, output_file, size)