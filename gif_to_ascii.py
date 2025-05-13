from PIL import Image, ImageDraw, ImageFont
import argparse

def extract_frames(gif_path):
    img = Image.open(gif_path)
    frames = []
    durations = []

    try:
        while True:
            frame = img.convert("RGB")
            frames.append(frame.copy())
            durations.append(img.info.get('duration', 100))
            img.seek(img.tell() + 1)
    except EOFError:
        pass

    return frames, durations

def image_to_ascii_image(img, cols=100, scale=1, font_path=None, font_size=10):
    ascii_chars = "@%#*+=-:. "
    width, height = img.size
    aspect_ratio = height / width
    new_width = cols
    new_height = int(aspect_ratio * cols * scale)
    img = img.resize((new_width, new_height)).convert("L")
    pixels = img.getdata()
    ascii_str = ''.join([ascii_chars[pixel * len(ascii_chars) // 256] for pixel in pixels])

    if font_path is None:
        font = ImageFont.load_default()
    else:
        font = ImageFont.truetype(font_path, font_size)

    char_width, char_height = font.getsize("A")
    output_img = Image.new("RGB", (char_width * new_width, char_height * new_height), color=(0, 0, 0))
    draw = ImageDraw.Draw(output_img)

    for i in range(new_height):
        line = ascii_str[i * new_width:(i + 1) * new_width]
        draw.text((0, i * char_height), line, font=font, fill=(255, 255, 255))

    return output_img

def make_ascii_gif(input_gif, output_gif, cols=1, scale=0.2, font_path=None, font_size=10):
    frames, durations = extract_frames(input_gif)
    ascii_frames = []

    for i, frame in enumerate(frames):
        print(f"Processing frame {i+1}/{len(frames)}")
        ascii_img = image_to_ascii_image(frame, cols=cols, scale=scale, font_path=font_path, font_size=font_size)
        ascii_frames.append(ascii_img)

    ascii_frames[0].save(
        output_gif,
        save_all=True,
        append_images=ascii_frames[1:],
        duration=durations,
        loop=0
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a GIF to ASCII GIF.')
    parser.add_argument('--input', type=str, default='input.gif', help='Path to input GIF')
    parser.add_argument('--output', type=str, default='ascii_output.gif', help='Path to save output GIF')
    parser.add_argument('--cols', type=int, default=100, help='Number of ASCII columns (horizontal resolution)')
    parser.add_argument('--scale', type=float, default=1, help='Vertical scale (character height ratio)')
    parser.add_argument('--font_path', type=str, default=None, help='Path to TTF font file')
    parser.add_argument('--font_size', type=int, default=10, help='Font size for ASCII characters')

    args = parser.parse_args()

    make_ascii_gif(
        input_gif=args.input,
        output_gif=args.output,
        cols=args.cols,
        scale=args.scale,
        font_path=args.font_path,
        font_size=args.font_size
    )

