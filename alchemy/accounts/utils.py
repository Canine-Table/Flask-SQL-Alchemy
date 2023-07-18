def crop_to_square(image):
    width, height = image.size
    if width == height:
        return image
    elif width > height:
        offset = int(abs(height - width) / 2)
        return image.crop((offset, 0, width - offset, height))
    else:
        offset = int(abs(width - height) / 2)
        return image.crop((0, offset, width, height - offset))
