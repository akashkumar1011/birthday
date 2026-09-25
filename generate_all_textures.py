import os
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

os.makedirs('textures_3d', exist_ok=True)

# Canvas dimensions
W_FLAP, H_CARD = 1024, 2867
W_CTR = 2048
W_FRONT = 2048

# Load fonts
font_hand_xl = ImageFont.truetype('fonts/Caveat.ttf', 62)
font_hand_lg = ImageFont.truetype('fonts/Caveat.ttf', 52)
font_hand_md = ImageFont.truetype('fonts/Caveat.ttf', 44)
font_hand_sm = ImageFont.truetype('fonts/Caveat.ttf', 38)
font_callig_xl = ImageFont.truetype('fonts/Caveat.ttf', 300)

# Helper: realistic paper background
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
def paste_with_shadow(base, img, px, py, offset=(4, 8), blur=10, opacity=160):
    sw, sh = img.size
    shadow = Image.new('RGBA', (sw + 50, sh + 50), (0, 0, 0, 0))
    alpha = img.split()[3] if img.mode == 'RGBA' else Image.new('L', (sw, sh), 255)
    black = Image.new('RGBA', (sw, sh), (0, 0, 0, 0))
    black.putalpha(alpha.point(lambda p: int(p * (opacity / 255.0))))
    shadow.paste(black, (25 + offset[0], 25 + offset[1]), black)
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    base.paste(shadow, (px - 25, py - 25), shadow)
    if img.mode == 'RGBA':
        base.paste(img, (px, py), img)
    else:
        base.paste(img, (px, py))

# Helper: make polaroid photo frame with tape
def make_polaroid(img_path, target_photo_w=380, target_photo_h=380, pad_top=22, pad_sides=22, pad_bot=60, rot=0):
    im = Image.open(img_path).convert('RGB')
    im = ImageOps.fit(im, (target_photo_w, target_photo_h), method=Image.LANCZOS)
    
    fw = target_photo_w + pad_sides * 2
    fh = target_photo_h + pad_top + pad_bot
    frame = Image.new('RGBA', (fw, fh), (248, 246, 242, 255))
    draw = ImageDraw.Draw(frame)
    draw.rectangle([pad_sides-1, pad_top-1, pad_sides + target_photo_w, pad_top + target_photo_h], outline=(210, 205, 195, 255), width=1)
    frame.paste(im, (pad_sides, pad_top))
    
    tape_w, tape_h = 110, 30
    tape = Image.new('RGBA', (tape_w, tape_h), (255, 240, 215, 190))
    tdraw = ImageDraw.Draw(tape)
    tdraw.line([(0, 0), (tape_w, 0)], fill=(255, 255, 255, 140), width=1)
    
    full_card = Image.new('RGBA', (fw, fh + 20), (0, 0, 0, 0))
    full_card.paste(frame, (0, 15))
    full_card.paste(tape, ((fw - tape_w)//2, 0), tape)
    
    if rot != 0:
        full_card = full_card.rotate(rot, expand=True, resample=Image.BICUBIC)
    return full_card

# Helper: framed mini photo for the stepped heart
def make_heart_photo(img_path, pw=330, ph=390, border=12, rot=0):
    im = Image.open(img_path).convert('RGB')
    im = ImageOps.fit(im, (pw, ph), method=Image.LANCZOS)
    fw = pw + border * 2
    fh = ph + border * 2
    frame = Image.new('RGBA', (fw, fh), (255, 255, 255, 255))
    frame.paste(im, (border, border))
    draw = ImageDraw.Draw(frame)
    dash_len = 8
    for x in range(2, fw-2, dash_len*2):
        draw.line([(x, 2), (min(x+dash_len, fw-2), 2)], fill=(195, 195, 195, 255), width=1)
        draw.line([(x, fh-3), (min(x+dash_len, fw-2), fh-3)], fill=(195, 195, 195, 255), width=1)
    for y in range(2, fh-2, dash_len*2):
        draw.line([(2, y), (2, min(y+dash_len, fh-2))], fill=(195, 195, 195, 255), width=1)
        draw.line([(fw-3, y), (fw-3, min(y+dash_len, fh-2))], fill=(195, 195, 195, 255), width=1)
        
    if rot != 0:
        frame = frame.rotate(rot, expand=True, resample=Image.BICUBIC)
    return frame

# Helper: draw sparkles and stars
def draw_sparkle(draw, sx, sy, size=8, color=(255, 255, 255, 200)):
    draw.line([(sx-size, sy), (sx+size, sy)], fill=color, width=2)
    draw.line([(sx, sy-size), (sx, sy+size)], fill=color, width=2)
    s_sub = int(size * 0.6)
    c_sub = (color[0], color[1], color[2], int(color[3]*0.6))
    draw.line([(sx-s_sub, sy-s_sub), (sx+s_sub, sy+s_sub)], fill=c_sub, width=1)
    draw.line([(sx-s_sub, sy+s_sub), (sx+s_sub, sy-s_sub)], fill=c_sub, width=1)

def draw_heart(draw, hx, hy, size=9, color=(255, 185, 210, 220), fill_color=None):
    pts = [
        (hx, hy + size),
        (hx - size, hy),
        (hx - size//2, hy - size),
        (hx, hy - size//2),
        (hx + size//2, hy - size),
        (hx + size, hy),
        (hx, hy + size)
    ]
    if fill_color:
        draw.polygon(pts, fill=fill_color)
    draw.line(pts, fill=color, width=2)

def paste_letter(base, name, cx, cy, target_h=300, rot=0):
    im = Image.open(f'cutout_letters/{name}.png').convert('RGBA')
    scale = target_h / im.height
    w_new = int(im.width * scale)
    im = im.resize((w_new, target_h), Image.LANCZOS)
    if rot != 0:
        im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    px = cx - im.width // 2
    py = cy - im.height // 2
    paste_with_shadow(base, im, px, py, offset=(4, 9), blur=12, opacity=170)

# =========================================================================
# 1. FRONT COVER (2048 x 2867) -> Left Flap & Right Flap
# =========================================================================
print('1. Generating Front Cover...')
front = make_paper(W_FRONT, H_CARD, (18, 18, 22), 3.2, 0.16)
fdraw = ImageDraw.Draw(front)

h_hap = 330
h_bday = 300
y_happy = 1120
y_bday = 1530

# HAPPY: Left flap (H, A, P1), Right flap (P2, Y)
paste_letter(front, 'clean_H', 440, y_happy - 10, target_h=h_hap, rot=-3)
paste_letter(front, 'clean_A', 680, y_happy + 8, target_h=int(h_hap*0.95), rot=2)
paste_letter(front, 'clean_P1', 900, y_happy - 4, target_h=int(h_hap*0.98), rot=-2)

paste_letter(front, 'clean_P2', 1148, y_happy + 6, target_h=h_hap, rot=3)
paste_letter(front, 'clean_Y', 1390, y_happy - 8, target_h=int(h_hap*0.96), rot=-2)

# BIRTHDAY: Left flap (B, I, R, T), Right flap (H, D, A, Y)
paste_letter(front, 'clean_b_B', 310, y_bday - 6, target_h=h_bday, rot=-2)
paste_letter(front, 'clean_b_I', 510, y_bday + 6, target_h=int(h_bday*0.94), rot=1)
paste_letter(front, 'clean_b_R', 705, y_bday - 4, target_h=int(h_bday*0.98), rot=-3)
paste_letter(front, 'clean_b_T', 905, y_bday + 6, target_h=h_bday, rot=2)

paste_letter(front, 'clean_b_H', 1140, y_bday - 6, target_h=h_bday, rot=-2)
paste_letter(front, 'clean_b_D', 1335, y_bday + 6, target_h=int(h_bday*0.96), rot=2)
paste_letter(front, 'clean_b_A', 1535, y_bday - 4, target_h=int(h_bday*0.95), rot=-2)
paste_letter(front, 'clean_b_Y', 1725, y_bday + 6, target_h=int(h_bday*0.92), rot=3)

# Big Pink Ribbon Bow placed at the top center seam (splits with the flaps)
bow = Image.open('stickers_extracted/sticker_25.png').convert('RGBA')
bow = bow.resize((320, int(bow.height * 320 / bow.width)), Image.LANCZOS)
paste_with_shadow(front, bow, 1024 - 160, 720, offset=(0, 6), blur=12, opacity=140)

# Sweet Corner Stamps & Bouquets
fl = Image.open('stickers_extracted/sticker_01.png').convert('RGBA').rotate(15, expand=True)
fl = fl.resize((240, int(fl.height * 240 / fl.width)), Image.LANCZOS)
paste_with_shadow(front, fl, W_FRONT - 320, H_CARD - 380)

st = Image.open('stickers_extracted/sticker_02.png').convert('RGBA').rotate(-8, expand=True)
st = st.resize((220, int(st.height * 220 / st.width)), Image.LANCZOS)
paste_with_shadow(front, st, 100, H_CARD - 360)

# Cute mini pink ribbon bows on flaps
mini_bow_l = bow.resize((150, int(bow.height * 150 / bow.width)), Image.LANCZOS).rotate(-8, expand=True)
paste_with_shadow(front, mini_bow_l, 240, 720, offset=(2, 4), blur=8, opacity=130)

mini_bow_r = bow.resize((150, int(bow.height * 150 / bow.width)), Image.LANCZOS).rotate(10, expand=True)
paste_with_shadow(front, mini_bow_r, 1630, 720, offset=(2, 4), blur=8, opacity=130)

# Sparkles and stars across the front
sparkle_positions = [
    (180, 450), (280, 580), (820, 520), (1240, 500), (1750, 460), (1850, 620),
    (150, 1000), (950, 980), (1100, 990), (1900, 1010),
    (180, 1650), (320, 2050), (980, 1600), (1080, 1600), (1700, 1650), (1880, 2000),
    (300, 2450), (600, 2650), (1450, 2650), (1750, 2450)
]
for sx, sy in sparkle_positions:
    draw_sparkle(fdraw, sx, sy, size=8)

heart_pts = [
    (450, 650), (1600, 680), (220, 1280), (1820, 1280), 
    (550, 1920), (1500, 1920), (380, 2350), (1660, 2350)
]
for hx, hy in heart_pts:
    draw_heart(fdraw, hx, hy, size=10, fill_color=(255, 175, 195, 70))

# Split into left and right flaps
card_front_left = front.crop((0, 0, 1024, H_CARD))
card_front_right = front.crop((1024, 0, W_FRONT, H_CARD))
card_front_left.save('textures_3d/card_front_left.png')
card_front_right.save('textures_3d/card_front_right.png')
print('Saved card_front_left.png and card_front_right.png')

# =========================================================================
# 2. INSIDE LEFT FLAP (1024 x 2867): 2 photos top, notes/stickers mid, 2 photos bottom
# =========================================================================
print('2. Generating Inside Left Flap...')
in_left = make_paper(W_FLAP, H_CARD, (18, 18, 22), 3.0, 0.12)
ldraw = ImageDraw.Draw(in_left)

# TOP ROW: 2 photos side by side (upright from photos_perfect!)
p_top_l = make_polaroid('photos_perfect/photo_02.jpg', target_photo_w=380, target_photo_h=380, rot=-2)
paste_with_shadow(in_left, p_top_l, 40, 90, offset=(3, 7), blur=10, opacity=140)

p_top_r = make_polaroid('photos_perfect/photo_03.jpg', target_photo_w=380, target_photo_h=380, rot=2)
paste_with_shadow(in_left, p_top_r, 520, 95, offset=(3, 7), blur=10, opacity=140)

# MIDDLE SECTION: Teddy bear, cute notes, white gel pen message
lines_left = [
    "Birthday meri Rasmalai,",
    "Blessed to have you in my life.",
    "Tu meri life ka wo hissa hai jisko",
    "mein kabhi bhi apne se alag",
    "nahi kar sakti... Tu hai toh mein hu!"
]
y_text = 750
for line in lines_left:
    ldraw.text((100, y_text), line, font=font_hand_md, fill=(255, 245, 240, 230))
    y_text += 60
draw_heart(ldraw, 680, y_text - 50, size=9, fill_color=(255, 175, 195, 90))

# Cute stickers in middle
teddy = Image.open('stickers_extracted/sticker_16.png').convert('RGBA').rotate(-4, expand=True)
teddy = teddy.resize((360, int(teddy.height * 360 / teddy.width)), Image.LANCZOS)
paste_with_shadow(in_left, teddy, 550, 1080, offset=(4, 8), blur=12, opacity=150)

note_special = Image.open('stickers_extracted/sticker_00.png').convert('RGBA').rotate(3, expand=True)
note_special = note_special.resize((340, int(note_special.height * 340 / note_special.width)), Image.LANCZOS)
paste_with_shadow(in_left, note_special, 80, 1100, offset=(3, 6), blur=10, opacity=140)

note_reasons = Image.open('stickers_extracted/sticker_20.png').convert('RGBA').rotate(-2, expand=True)
note_reasons = note_reasons.resize((440, int(note_reasons.height * 440 / note_reasons.width)), Image.LANCZOS)
paste_with_shadow(in_left, note_reasons, 280, 1530, offset=(4, 8), blur=12, opacity=140)

# Sweet love note below reasons
ldraw.text((100, 2050), "some people just come into our life and", font=font_hand_sm, fill=(255, 240, 245, 200))
ldraw.text((100, 2100), "leave memories, but you became a part of my heart.", font=font_hand_sm, fill=(255, 240, 245, 200))
draw_heart(ldraw, 760, 2110, size=8, fill_color=(255, 175, 195, 90))

# BOTTOM ROW: 2 photos side by side (upright from photos_perfect!)
p_bot_l = make_polaroid('photos_perfect/photo_04.jpg', target_photo_w=380, target_photo_h=380, rot=2)
paste_with_shadow(in_left, p_bot_l, 40, 2190, offset=(3, 7), blur=10, opacity=140)

p_bot_r = make_polaroid('photos_perfect/photo_09.jpg', target_photo_w=380, target_photo_h=380, rot=-2)
paste_with_shadow(in_left, p_bot_r, 520, 2185, offset=(3, 7), blur=10, opacity=140)

# Sparkles and hearts
for sx, sy in [(120, 700), (900, 710), (500, 1020), (920, 1450), (100, 1500), (880, 2080)]:
    draw_sparkle(ldraw, sx, sy, size=6)
for hx, hy in [(480, 720), (850, 1000), (120, 1980), (480, 2150)]:
    draw_heart(ldraw, hx, hy, size=8)

in_left.save('textures_3d/card_inside_left.png')
print('Saved card_inside_left.png')

# =========================================================================
# 3. INSIDE CENTER PANEL (2048 x 2867): 'I [HEART] U'
# =========================================================================
print('3. Generating Inside Center Panel...')
ctr = make_paper(W_CTR, H_CARD, (18, 18, 22), 3.0, 0.12)
cdraw = ImageDraw.Draw(ctr)

# Top Quote
top_quote = "you are my only sunshine"
bbox_tq = cdraw.textbbox((0, 0), top_quote, font=font_hand_xl)
tq_w = bbox_tq[2] - bbox_tq[0]
cdraw.text(((W_CTR - tq_w)//2 - 20, 230), top_quote, font=font_hand_xl, fill=(255, 245, 240, 230))
draw_heart(cdraw, (W_CTR - tq_w)//2 + tq_w + 10, 255, size=11, fill_color=(255, 175, 195, 100))

# Mini Bunting Banner for "SIDDHI"
banner_text = "SIDDHI"
b_x = (W_CTR - len(banner_text) * 80) // 2
b_y = 325
twine_pts = [(b_x - 40, b_y + 10)]
for i in range(len(banner_text) + 1):
    twine_pts.append((b_x + i * 80, b_y + 20 + int(np.sin(i / len(banner_text) * np.pi) * 25)))
twine_pts.append((b_x + len(banner_text) * 80 + 40, b_y + 10))
cdraw.line(twine_pts, fill=(210, 180, 140, 230), width=3)

font_pennant = ImageFont.truetype('fonts/Poppins-Bold.ttf', 38)
for i, char in enumerate(banner_text):
    px = b_x + i * 80 + 10
    py = b_y + 18 + int(np.sin(i / len(banner_text) * np.pi) * 25)
    pw, ph = 60, 75
    p_pts = [(px, py), (px + pw, py), (px + pw, py + ph), (px + pw//2, py + ph - 18), (px, py + ph)]
    cdraw.polygon(p_pts, fill=(255, 182, 193, 245), outline=(255, 150, 170, 255))
    bbox_c = cdraw.textbbox((0, 0), char, font=font_pennant)
    cw = bbox_c[2] - bbox_c[0]
    cdraw.text((px + (pw - cw)//2, py + 12), char, font=font_pennant, fill=(255, 255, 255, 255))

# Build Stepped Pixel Heart with the 8 approved photos
pw, ph = 310, 360
gap_x, gap_y = 20, 20
border = 10
fw, fh = pw + border*2, ph + border*2

cx = W_CTR // 2
y_start = 540

heart_photos = [
    'heart_user_approved/h1_photo06.jpg', # Row 1, left
    'heart_user_approved/h2_photo07.jpg', # Row 1, right
    'heart_user_approved/h3_photo15.jpg', # Row 2, left
    'heart_user_approved/h4_photo08.jpg', # Row 2, center
    'heart_user_approved/h5_photo17.jpg', # Row 2, right
    'heart_user_approved/h6_photo10.jpg', # Row 3, left
    'heart_user_approved/h7_photo01.jpg', # Row 3, right
    'heart_user_approved/h8_photo05.jpg'  # Row 4, bottom center
]

# Row 1: 2 photos
y1 = y_start
x1_l = cx - fw - gap_x // 2
x1_r = cx + gap_x // 2
paste_with_shadow(ctr, make_heart_photo(heart_photos[0], pw, ph, border), x1_l, y1)
paste_with_shadow(ctr, make_heart_photo(heart_photos[1], pw, ph, border), x1_r, y1)

# Row 2: 3 photos
y2 = y1 + fh + gap_y
x2_l = cx - fw - fw//2 - gap_x
x2_c = cx - fw//2
x2_r = cx + fw//2 + gap_x
paste_with_shadow(ctr, make_heart_photo(heart_photos[2], pw, ph, border), x2_l, y2)
paste_with_shadow(ctr, make_heart_photo(heart_photos[3], pw, ph, border), x2_c, y2)
paste_with_shadow(ctr, make_heart_photo(heart_photos[4], pw, ph, border), x2_r, y2)

# Row 3: 2 photos
y3 = y2 + fh + gap_y
x3_l = cx - fw - gap_x // 2
x3_r = cx + gap_x // 2
paste_with_shadow(ctr, make_heart_photo(heart_photos[5], pw, ph, border), x3_l, y3)
paste_with_shadow(ctr, make_heart_photo(heart_photos[6], pw, ph, border), x3_r, y3)

# Row 4: 1 photo
y4 = y3 + fh + gap_y
x4_c = cx - fw//2
paste_with_shadow(ctr, make_heart_photo(heart_photos[7], pw, ph, border), x4_c, y4)

# Left of Heart: 'I' and quote
cdraw.text((x2_l - 220, y2 + 40), "I", font=font_callig_xl, fill=(255, 180, 205, 120))
cdraw.text((x2_l - 222, y2 + 38), "I", font=font_callig_xl, fill=(255, 235, 245, 255))
cdraw.text((x2_l - 250, y2 + 340), "you mean the\nworld to me", font=font_hand_md, fill=(255, 240, 245, 220))
draw_heart(cdraw, x2_l - 70, y2 + 400, size=9, fill_color=(255, 175, 195, 90))

# Right of Heart: 'U' and quote
cdraw.text((x2_r + fw + 70, y2 + 40), "U", font=font_callig_xl, fill=(255, 180, 205, 120))
cdraw.text((x2_r + fw + 68, y2 + 38), "U", font=font_callig_xl, fill=(255, 235, 245, 255))
cdraw.text((x2_r + fw + 60, y2 + 340), "my favorite\nperson", font=font_hand_md, fill=(255, 240, 245, 220))
draw_heart(cdraw, x2_r + fw + 200, y2 + 400, size=9, fill_color=(255, 175, 195, 90))

# Bottom Quotes
b_quote1 = "words will never be enough to express how grateful I am to have you as my best friend"
bbox_bq1 = cdraw.textbbox((0, 0), b_quote1, font=font_hand_md)
bq1_w = bbox_bq1[2] - bbox_bq1[0]
cdraw.text(((W_CTR - bq1_w)//2 - 15, y4 + fh + 65), b_quote1, font=font_hand_md, fill=(255, 245, 240, 220))
draw_heart(cdraw, (W_CTR - bq1_w)//2 + bq1_w + 10, y4 + fh + 85, size=9, fill_color=(255, 175, 195, 90))

b_quote2 = "A friend like you is just rare to find"
bbox_bq2 = cdraw.textbbox((0, 0), b_quote2, font=font_hand_md)
bq2_w = bbox_bq2[2] - bbox_bq2[0]
cdraw.text(((W_CTR - bq2_w)//2 - 15, y4 + fh + 135), b_quote2, font=font_hand_md, fill=(255, 230, 240, 210))
draw_heart(cdraw, (W_CTR - bq2_w)//2 + bq2_w + 10, y4 + fh + 155, size=9, fill_color=(255, 175, 195, 90))

# Sparkles and hearts around center
sparkles_ctr = [
    (250, 260), (1800, 260), (x2_l - 120, y1 + 100), (x2_r + fw + 140, y1 + 100),
    (x2_l - 140, y3 + 200), (x2_r + fw + 150, y3 + 200),
    (400, y4 + fh + 210), (1650, y4 + fh + 210)
]
for sx, sy in sparkles_ctr:
    draw_sparkle(cdraw, sx, sy, size=8)

ctr.save('textures_3d/card_inside_center.png')
print('Saved card_inside_center.png')

# =========================================================================
# 4. INSIDE RIGHT FLAP (1024 x 2867): 2 photos top, notes/stickers mid, 2 photos bottom
# =========================================================================
print('4. Generating Inside Right Flap...')
in_right = make_paper(W_FLAP, H_CARD, (18, 18, 22), 3.0, 0.12)
rdraw = ImageDraw.Draw(in_right)

# TOP ROW: 2 photos side by side (upright from photos_perfect!)
p_rtop_l = make_polaroid('photos_perfect/photo_11.jpg', target_photo_w=380, target_photo_h=380, rot=-2)
paste_with_shadow(in_right, p_rtop_l, 40, 90, offset=(3, 7), blur=10, opacity=140)

p_rtop_r = make_polaroid('photos_perfect/photo_12.jpg', target_photo_w=380, target_photo_h=380, rot=2)
paste_with_shadow(in_right, p_rtop_r, 520, 95, offset=(3, 7), blur=10, opacity=140)

# MIDDLE SECTION: Handwritten message and stickers
lines_right = [
    "Thank you for every late night laugh,",
    "every conversation, every memory.",
    "You've always been my biggest cheerleader,",
    "my safe place, my partner in crime.",
    "Happy 20th Birthday, my love!"
]
y_rtext = 750
for line in lines_right:
    rdraw.text((100, y_rtext), line, font=font_hand_md, fill=(255, 245, 240, 230))
    y_rtext += 60
draw_heart(rdraw, 640, y_rtext - 50, size=9, fill_color=(255, 175, 195, 90))

# Stickers in middle
note_today = Image.open('stickers_extracted/sticker_22.png').convert('RGBA').rotate(-3, expand=True)
note_today = note_today.resize((420, int(note_today.height * 420 / note_today.width)), Image.LANCZOS)
paste_with_shadow(in_right, note_today, 80, 1100, offset=(4, 8), blur=12, opacity=140)

tulips = Image.open('stickers_extracted/sticker_21.png').convert('RGBA').rotate(5, expand=True)
tulips = tulips.resize((360, int(tulips.height * 360 / tulips.width)), Image.LANCZOS)
paste_with_shadow(in_right, tulips, 570, 1080, offset=(4, 8), blur=12, opacity=140)

note_darling = Image.open('stickers_extracted/sticker_24.png').convert('RGBA').rotate(3, expand=True)
note_darling = note_darling.resize((380, int(note_darling.height * 380 / note_darling.width)), Image.LANCZOS)
paste_with_shadow(in_right, note_darling, 100, 1550, offset=(4, 8), blur=12, opacity=140)

note_fall = Image.open('stickers_extracted/sticker_26.png').convert('RGBA').rotate(-2, expand=True)
note_fall = note_fall.resize((380, int(note_fall.height * 380 / note_fall.width)), Image.LANCZOS)
paste_with_shadow(in_right, note_fall, 530, 1560, offset=(4, 8), blur=12, opacity=140)

# Sweet love note below stickers
rdraw.text((100, 2050), "you make my heart smile and life beautiful,", font=font_hand_sm, fill=(255, 240, 245, 200))
rdraw.text((100, 2100), "forever and always, no matter what!", font=font_hand_sm, fill=(255, 240, 245, 200))
draw_heart(rdraw, 640, 2110, size=8, fill_color=(255, 175, 195, 90))

# BOTTOM ROW: 2 photos side by side (upright from photos_perfect!)
p_rbot_l = make_polaroid('photos_perfect/photo_13.jpg', target_photo_w=380, target_photo_h=380, rot=2)
paste_with_shadow(in_right, p_rbot_l, 40, 2190, offset=(3, 7), blur=10, opacity=140)

p_rbot_r = make_polaroid('photos_perfect/photo_16.jpg', target_photo_w=380, target_photo_h=380, rot=-2)
paste_with_shadow(in_right, p_rbot_r, 520, 2185, offset=(3, 7), blur=10, opacity=140)

# Sparkles and hearts
for sx, sy in [(120, 700), (900, 710), (500, 1020), (920, 1450), (100, 1500), (880, 2080)]:
    draw_sparkle(rdraw, sx, sy, size=6)
for hx, hy in [(480, 720), (850, 1000), (120, 1980), (480, 2150)]:
    draw_heart(rdraw, hx, hy, size=8)

in_right.save('textures_3d/card_inside_right.png')
print('Saved card_inside_right.png')

# =========================================================================
# 5. CREATE FULL INSIDE SPREAD PREVIEW (Left Flap + Center + Right Flap)
# =========================================================================
print('5. Creating composite showcase preview...')
full_inside = Image.new('RGB', (W_FLAP + W_CTR + W_FLAP, H_CARD))
full_inside.paste(in_left, (0, 0))
full_inside.paste(ctr, (W_FLAP, 0))
full_inside.paste(in_right, (W_FLAP + W_CTR, 0))

full_inside_small = full_inside.resize((1500, int(H_CARD * 1500 / full_inside.width)), Image.LANCZOS)
full_inside_small.save('inside_spread_preview.jpg')

front_small = front.resize((750, int(H_CARD * 750 / front.width)), Image.LANCZOS)
front_small.save('front_cover_preview.jpg')

# Master showcase image (Front + Inside)
showcase_w = 1600
showcase_h = 1000
showcase = Image.new('RGB', (showcase_w, showcase_h), (12, 12, 15))

fc_h = 880
fc_w = int(front.width * fc_h / front.height)
fc_render = front.resize((fc_w, fc_h), Image.LANCZOS)
showcase.paste(fc_render, (60, 60))

ins_w = 940
ins_h = int(full_inside.height * ins_w / full_inside.width)
ins_render = full_inside.resize((ins_w, ins_h), Image.LANCZOS)
showcase.paste(ins_render, (600, (showcase_h - ins_h)//2))

showcase.save('card_3d_showcase.jpg')
artifact_dir = 'C:/Users/akash/.gemini/antigravity-ide/brain/1e210473-9769-43a8-bd7d-63974ca30498'
showcase.save(f'{artifact_dir}/card_3d_showcase.jpg')

print('ALL 3D TEXTURES & SHOWCASE GENERATED SUCCESSFULLY!')
