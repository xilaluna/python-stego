"""
[Day 7] Assignment: Steganography
    - Turn in on Gradescope (https://make.sc/bew2.3-gradescope)
    - Lesson Plan: https://tech-at-du.github.io/ACS-3230-Web-Security/#/Lessons/Steganography

Deliverables:
    1. All TODOs in this file.
    2. Decoded sample image with secret text revealed
    3. Your own image encoded with hidden secret text!
"""
# TODO: Run `pip3 install Pillow` before running the code.
from PIL import Image, ImageDraw


def decode_image(path_to_png):
    """
    Decode image by checking the LSB of the red channel then changing the red value based on LSB
    """
    # Open the image using PIL:
    encoded_image = Image.open(path_to_png)

    # Separate the red channel from the rest of the image:
    red_channel = encoded_image.split()[0]

    # Create a new PIL image with the same size as the encoded image:
    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()
    x_size, y_size = encoded_image.size

    for i in range(x_size):
        for j in range(y_size):
            redchannel_bin_num = bin(red_channel.getpixel((i, j)))
            last_int = int(str(redchannel_bin_num)[-1:])
            if last_int == 0:
                pixels[i, j] = (255, 0, 0)
            elif last_int == 1:
                pixels[i, j] = (0, 0, 0)

    # Save the decoded image to disk:
    decoded_image.save("decoded_image.png")


def write_text(text_to_write, size):
    """
    Create black and white image with text.
    """
    text_decoded_image = Image.new("RGB", size)

    ImageDraw.Draw(text_decoded_image).text(
        (0, 0), text_to_write, (255, 255, 255)
    )
    text_decoded_image.save("message_image.png")


def encode_image(path_to_png, message):
    """
    TODO: Add docstring and complete implementation.
    """
    # Open decoded image
    decoded_image = Image.open(path_to_png)
    decoded_red = decoded_image.split()[0]
    green = decoded_image.split()[1]
    blue = decoded_image.split()[2]

    # Create secret message image, open & load red channel
    write_text(message, decoded_image.size)
    secret_message_img = Image.open('./message_image.png')
    secret_message_red_channel = secret_message_img.split()[0]

    # Create new Image and load pixels
    new_encoded_image = Image.new("RGB", decoded_image.size)
    pixels = new_encoded_image.load()

    # Load decoded pixels & loop through the image
    x_size, y_size = decoded_image.size
    for i in range(x_size):
        for j in range(y_size):
            if secret_message_red_channel.getpixel((i, j)) == 255:
              # Change the LSB of red channel of decoded image to 1
                decoded_red_bin = decoded_red.getpixel((i, j)) | 1
                pixels[i, j] = (
                    decoded_red_bin,
                    green.getpixel((i, j)),
                    blue.getpixel((i, j))
                )
            elif secret_message_red_channel.getpixel((i, j)) == 0:
                decoded_red_bin = decoded_red.getpixel((i, j)) & ~1
                pixels[i, j] = (
                    decoded_red_bin,
                    green.getpixel((i, j)),
                    blue.getpixel((i, j))
                )

    new_encoded_image.save("new_encoded_image.png")


decode_image("./encoded_sample.png")
# encode_image('./my_decoded.png', 'Hello World')
