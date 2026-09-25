import os
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

os.makedirs('textures_3d', exist_ok=True)

# ---------------------------------------------------------
# Helper: realistic paper background
# ---------------------------------------------------------
def make_paper(w, h, base_rgb=(18, 18, 22), noise_std=3.0, vignette_strength=0.14):
    arr = np.tile(np.array(base_rgb, dtype=np.float32), (h, w, 1))
    noise = np.random.normal(0, noise_std, (h, w, 1)).astype(np.float32)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    y, x = np.ogrid[:h, :w]
    cx, cy = w / 2, h / 2
    dist = np.sqrt((x - cx)**2 + (y - cy)**2)
    max_dist = np.sqrt(cx**2 + cy**2)
    vignette = 1.0 - vignette_strength * (dist / max_dist)**1.5
    arr = (arr * vignette[:, :, np.newaxis]).astype(np.uint8)
    return Image.fromarray(arr)

# Helper: paste with drop shadow
def paste_with_shadow(base, img, px, py, offset=(4, 8), blur=10, opacity=150):
    sw, sh = img.size
    shadow = Image.new('RGBA', (sw + 50, sh + 50), (0, 0, 0, 0))
    alpha = img.split()[3] if img.mode == 'RGBA' else Image.new('L', (sw, sh), 255)
    black = Image.new('RGBA', (sw, sh), (0, 0, 0, 0))
    black.putalpha(alpha.point(lambda p: int(p * (opacity / 255.0))))
    shadow.paste(black, (25 + offset[0], 25 + offset[1]), black)
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    base.paste(shadow, (px - 25, py - 25), shadow)
    base.paste(img, (px, py), img)

# Helper: make polaroid photo frame with tape
def make_polaroid(img_path, target_photo_w=360, target_photo_h=360, pad_top=25, pad_sides=25, pad_bot=65, rot=0):
    im = Image.open(img_path).convert('RGB')
    im = ImageOps.fit(im, (target_photo_w, target_photo_h), method=Image.LANCZOS)
    
    fw = target_photo_w + pad_sides * 2
    fh = target_photo_h + pad_top + pad_bot
    frame = Image.new('RGBA', (fw, fh), (248, 246, 242, 255))
    draw = ImageDraw.Draw(frame)
    # Subtle inner photo border
    draw.rectangle([pad_sides-1, pad_top-1, pad_sides + target_photo_w, pad_top + target_photo_h], outline=(210, 205, 195, 255), width=1)
    frame.paste(im, (pad_sides, pad_top))
    
    # Add tape at top center
    tape_w, tape_h = 110, 32
    tape = Image.new('RGBA', (tape_w, tape_h), (255, 240, 215, 180))
    tdraw = ImageDraw.Draw(tape)
    tdraw.line([(0, 0), (tape_w, 0)], fill=(255, 255, 255, 140), width=1)
    
    # Composite frame with tape
    full_card = Image.new('RGBA', (fw, fh + 20), (0, 0, 0, 0))
    full_card.paste(frame, (0, 15))
    full_card.paste(tape, ((fw - tape_w)//2, 0), tape)
    
    if rot != 0:
        full_card = full_card.rotate(rot, expand=True, resample=Image.BICUBIC)
    return full_card

# Helper: draw sparkles and stars
def draw_sparkle(draw, sx, sy, size=8, color=(255, 255, 255, 200)):
    draw.line([(sx-size, sy), (sx+size, sy)], fill=color, width=2)
    draw.line([(sx, sy-size), (sx, sy+size)], fill=color, width=2)
    s_sub = int(size * 0.6)
    c_sub = (color[0], color[1], color[2], int(color[3]*0.6))
    draw.line([(sx-s_sub, sy-s_sub), (sx+s_sub, sy+s_sub)], fill=c_sub, width=1)
    draw.line([(sx-s_sub, sy+s_sub), (sx+s_sub, sy-s_sub)], fill=c_sub, width=1)

def draw_heart(draw, hx, hy, size=7, color=(255, 200, 215, 220)):
    pts = [
        (hx, hy + size),
        (hx - size, hy),
        (hx - size//2, hy - size),
        (hx, hy - size//2),
        (hx + size//2, hy - size),
        (hx + size, hy),
        (hx, hy + size)
    ]
    draw.line(pts, fill=color, width=2)

print('Base helpers defined.')
