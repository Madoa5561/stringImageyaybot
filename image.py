import os
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 800, 450
TEXT_COLOR = "black"
TIMESTAMP_COLOR = "white"
FONT_PATH = "Fudeekimeigyo1.2.ttf"
FONT_SIZE = int(HEIGHT * 0.3)
SAVE_DIR = "images"
TIMESTAMP_RATIO = 0.12

HIRAGANA = list("あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん")

os.makedirs(SAVE_DIR, exist_ok=True)

def random_hiragana(n=3):
    return "".join(random.choices(HIRAGANA, k=n))

def find_system_font():
    candidates = [
        "YuGoth", "YuGothR", "YuGothB", "Yu Gothic", "Meiryo", "meiryo", "msgothic",
        "NotoSansCJK", "NotoSansJP", "ipa", "IPAMin", "TakaoPGothic"
    ]
    windir = os.environ.get("WINDIR", "C:\\Windows")
    win_fonts = os.path.join(windir, "Fonts")
    if os.path.isdir(win_fonts):
        for fname in os.listdir(win_fonts):
            fn_lower = fname.lower()
            for key in candidates:
                if key.lower() in fn_lower and (fn_lower.endswith(".ttf") or fn_lower.endswith(".ttc") or fn_lower.endswith(".otf")):
                    return os.path.join(win_fonts, fname)
    for root in ("/usr/share/fonts", "/usr/local/share/fonts", os.path.expanduser("~/.local/share/fonts")):
        if not os.path.isdir(root):
            continue
        for dirpath, _, files in os.walk(root):
            for fname in files:
                fn_lower = fname.lower()
                for key in candidates:
                    if key.lower() in fn_lower and (fn_lower.endswith(".ttf") or fn_lower.endswith(".ttc") or fn_lower.endswith(".otf")):
                        return os.path.join(dirpath, fname)
    for root in ("/Library/Fonts", os.path.expanduser("~/Library/Fonts")):
        if not os.path.isdir(root):
            continue
        for fname in os.listdir(root):
            fn_lower = fname.lower()
            for key in candidates:
                if key.lower() in fn_lower and (fn_lower.endswith(".ttf") or fn_lower.endswith(".ttc") or fn_lower.endswith(".otf")):
                    return os.path.join(root, fname)
    return None

def load_font(path, size):
    try:
        if path and os.path.exists(path):
            return ImageFont.truetype(path, size)
    except Exception:
        pass
    found = find_system_font()
    if found:
        try:
            return ImageFont.truetype(found, size)
        except Exception:
            pass
    return ImageFont.load_default()

def hsv_to_rgb(h, s, v):
    c = v * s
    x = c * (1 - abs((h / 60.0) % 2 - 1))
    m = v - c
    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))

def make_blue_rainbow_background(width, height):
    img = Image.new("RGB", (width, height))
    px = img.load()
    for y in range(height):
        t = y / (height - 1) if height > 1 else 0
        hue = 200 + t * 80
        color = hsv_to_rgb(hue, 0.9, 0.95)
        for x in range(width):
            px[x, y] = color
    return img

def get_text_size(draw, text, font):
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]
    except Exception:
        try:
            return draw.textsize(text, font=font)
        except Exception:
            try:
                return font.getsize(text)
            except Exception:
                mask = font.getmask(text)
                return mask.size

def make_image(text, width=WIDTH, height=HEIGHT, color=TEXT_COLOR, font=None):
    bg = make_blue_rainbow_background(width, height)
    draw = ImageDraw.Draw(bg)
    w, h = get_text_size(draw, text, font)
    x = (width - w) // 2
    y = (height - h) // 2
    draw.text((x, y), text, fill=color, font=font)
    ts_font = load_font(FONT_PATH, max(10, int(height * TIMESTAMP_RATIO)))
    ts = datetime.now().strftime("%Y年%m月%d日 %H時%M分")
    tw, th = get_text_size(draw, ts, ts_font)
    padding = int(height * 0.03)
    tx = width - tw - padding
    ty = height - th - padding
    draw.text((tx, ty), ts, fill=TIMESTAMP_COLOR, font=ts_font)

    return bg

def generate_image():
    font = load_font(FONT_PATH, FONT_SIZE)
    try:
        txt = random_hiragana(3)
        img = make_image(txt, font=font)
        fname = "result.png"
        path = os.path.join(SAVE_DIR, fname)
        img.save(path)
        print(f"Saved: {path}  -> text: {txt}")
    except KeyboardInterrupt:
        print("Stopped by user.")

if __name__ == "__main__":
    generate_image()
