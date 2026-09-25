import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

os.makedirs('textures_3d', exist_ok=True)

W_FLAP, H_CARD = 1024, 2867
W_CTR = 2048
W_FRONT = 2048

# Fonts
font_hand_xl = ImageFont.truetype('fonts/Caveat.ttf', 64)
font_hand_lg = ImageFont.truetype('fonts/Caveat.ttf', 52)
font_hand_md = ImageFont.truetype('fonts/Caveat.ttf', 40)
font_hand_sm = ImageFont.truetype('fonts/Caveat.ttf', 35)
font_hand_msg = ImageFont.truetype('fonts/Caveat.ttf', 38)
font_pennant = ImageFont.truetype('fonts/Poppins-Bold.ttf', 42)
font_pennant_sid = ImageFont.truetype('fonts/Poppins-Bold.ttf', 48)

# Deep Luxury Charcoal/Black Cardstock (clean, natural, not washed out)
def make_dark_paper(w, h, base_rgb=(13, 13, 16), noise_std=2.0, vignette_strength=0.18):
    arr = np.tile(np.array(base_rgb, dtype=np.float32), (h, w, 1))
    noise = np.random.normal(0, noise_std, (h, w, 1)).astype(np.float32)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    y, x = np.ogrid[:h, :w]
    cx, cy = w / 2, h / 2
    dist = np.sqrt((x - cx)**2 + (y - cy)**2)
    max_dist = np.sqrt(cx**2 + cy**2)
    vignette = 1.0 - vignette_strength * (dist / max_dist)**1.4
    arr = (arr * vignette[:, :, np.newaxis]).astype(np.uint8)
    return Image.fromarray(arr)

def paste_with_shadow(base, img, px, py, offset=(4, 8), blur=12, opacity=170):
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

def make_polaroid(img_path, target_photo_w=390, target_photo_h=390, pad_top=22, pad_sides=22, pad_bot=60, rot=0, centering=(0.5, 0.35)):
    im = Image.open(img_path).convert('RGB')
    fitted = ImageOps.fit(im, (target_photo_w, target_photo_h), method=Image.LANCZOS, centering=centering)
    
    fw = target_photo_w + pad_sides * 2
    fh = target_photo_h + pad_top + pad_bot
    frame = Image.new('RGBA', (fw, fh), (248, 246, 242, 255))
    draw = ImageDraw.Draw(frame)
    draw.rectangle([pad_sides-1, pad_top-1, pad_sides + target_photo_w, pad_top + target_photo_h], outline=(210, 205, 195, 255), width=1)
    frame.paste(fitted, (pad_sides, pad_top))
    
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

def make_heart_photo(img_path, pw=310, ph=360, border=10, rot=0, centering=(0.5, 0.35)):
    im = Image.open(img_path).convert('RGB')
    fitted = ImageOps.fit(im, (pw, ph), method=Image.LANCZOS, centering=centering)
    fw = pw + border * 2
    fh = ph + border * 2
    frame = Image.new('RGBA', (fw, fh), (255, 255, 255, 255))
    frame.paste(fitted, (border, border))
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

def make_glossy_heart_sticker(size=40, color=(255, 95, 135)):
    s4 = size * 4
    canvas = Image.new('RGBA', (s4 * 2, s4 * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    c_x, c_y = s4, s4
    t = np.linspace(0, 2*np.pi, 200)
    xs = 16 * (np.sin(t)**3)
    ys = -(13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t))
    scale = (s4 * 0.8) / 16.0
    poly = [(c_x + x * scale, c_y + y * scale) for x, y in zip(xs, ys)]
    d.polygon(poly, fill=(color[0], color[1], color[2], 255))
    d.line(poly + [poly[0]], fill=(255, 220, 235, 180), width=4)
    d.ellipse([c_x - s4*0.48, c_y - s4*0.55, c_x - s4*0.18, c_y - s4*0.25], fill=(255, 255, 255, 180))
    return canvas.resize((size * 2, size * 2), Image.LANCZOS)

def draw_sparkle(draw, sx, sy, size=8, color=(255, 255, 255, 220)):
    draw.line([(sx-size, sy), (sx+size, sy)], fill=color, width=2)
    draw.line([(sx, sy-size), (sx, sy+size)], fill=color, width=2)
    s_sub = int(size * 0.6)
    c_sub = (color[0], color[1], color[2], int(color[3]*0.6))
    draw.line([(sx-s_sub, sy-s_sub), (sx+s_sub, sy+s_sub)], fill=c_sub, width=1)
    draw.line([(sx-s_sub, sy+s_sub), (sx+s_sub, sy-s_sub)], fill=c_sub, width=1)

def paste_letter(base, name, cx, cy, target_h=280, rot=0):
    im = Image.open(f'cutout_letters/{name}.png').convert('RGBA')
    scale = target_h / im.height
    w_new = int(im.width * scale)
    im = im.resize((w_new, target_h), Image.LANCZOS)
    if rot != 0:
        im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    px = cx - im.width // 2
    py = cy - im.height // 2
    paste_with_shadow(base, im, px, py, offset=(4, 9), blur=12, opacity=170)

def get_clean_balloon_rgba(path, target_h):
    im = Image.open(path).convert('RGBA')
    arr = np.array(im)
    rgb = arr[:, :, :3]
    white_mask = (rgb[:, :, 0] > 240) & (rgb[:, :, 1] > 240) & (rgb[:, :, 2] > 240)
    arr[:, :, 3] = np.where(white_mask, 0, 255)
    non_zero = np.where(arr[:, :, 3] > 0)
    ymin, ymax = np.min(non_zero[0]), np.max(non_zero[0])
    xmin, xmax = np.min(non_zero[1]), np.max(non_zero[1])
    crp = Image.fromarray(arr).crop((xmin, ymin, xmax, ymax))
    tw = int(crp.width * target_h / crp.height)
    return crp.resize((tw, target_h), Image.LANCZOS)

# Red paper swallowtail pennant with cut in half triangle from down
def make_red_swallowtail(char, font, w=72, h=92, notch=24, rot=0):
    p = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(p)
    # Swallowtail: cut in half triangle from down
    pts = [(0, 0), (w, 0), (w, h), (w//2, h - notch), (0, h)]
    
    # Red paper texture with subtle noise
    tile_arr = np.tile(np.array([215, 30, 52], dtype=np.float32), (h, w, 1))
    noise = np.random.normal(0, 3.5, (h, w, 1)).astype(np.float32)
    tile_arr = np.clip(tile_arr + noise, 0, 255).astype(np.uint8)
    tile_tex = Image.fromarray(tile_arr).convert('RGBA')
    
    mask = Image.new('L', (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.polygon(pts, fill=255)
    p.paste(tile_tex, (0, 0), mask)
    
    # Fine inner edge outline
    d.polygon(pts, outline=(245, 120, 140, 200), width=1)
    
    # Crisp white bold typography
    bbox = font.getbbox(char)
    cw = bbox[2] - bbox[0]
    ch = bbox[3] - bbox[1]
    d.text(((w - cw)//2 - bbox[0], (h - notch - ch)//2 - bbox[1] + 3), char, font=font, fill=(255, 255, 255, 255))
    
    if rot != 0:
        p = p.rotate(rot, expand=True, resample=Image.BICUBIC)
    return p

def draw_curved_pennant_line(base, word, font, cx, cy, w_total, dip=22, w_p=72, h_p=92, notch=24):
    d = ImageDraw.Draw(base)
    n = len(word)
    xs = np.linspace(cx - w_total//2, cx + w_total//2, n)
    ys = cy + dip * (1 - ((xs - cx) / (w_total/2))**2)
    
    # Twine rope curve
    rope_pts = [(xs[0] - 40, cy - 8)] + list(zip(xs, ys)) + [(xs[-1] + 40, cy - 8)]
    d.line(rope_pts, fill=(210, 180, 140, 230), width=3)
    
    for char, px, py in zip(word, xs, ys):
        angle = (px - cx) / (w_total/2) * 12
        tile = make_red_swallowtail(char, font, w=w_p, h=h_p, notch=notch, rot=-angle)
        paste_with_shadow(base, tile, int(px - tile.width//2), int(py), offset=(3, 6), blur=8, opacity=145)

# =========================================================================
# 1. FRONT COVER (HAPPY BIRTHDAY + '20' ROSE GOLD FOIL BALLOONS)
# =========================================================================
print('1. Generating Front Cover with 20 Balloon...')
front = make_dark_paper(W_FRONT, H_CARD, (13, 13, 16), 2.5, 0.18)
fdraw = ImageDraw.Draw(front)

# Big Pink Ribbon Bow at top center
bow = Image.open('stickers_extracted/sticker_25.png').convert('RGBA')
bow = bow.resize((300, int(bow.height * 300 / bow.width)), Image.LANCZOS)
paste_with_shadow(front, bow, 1024 - 150, 480, offset=(0, 6), blur=12, opacity=150)

h_hap = 300
h_bday = 270
y_happy = 850
y_bday = 1200

# HAPPY (Ransom cutout letters)
paste_letter(front, 'clean_H', 440, y_happy - 10, target_h=h_hap, rot=-3)
paste_letter(front, 'clean_A', 680, y_happy + 8, target_h=int(h_hap*0.95), rot=2)
paste_letter(front, 'clean_P1', 900, y_happy - 4, target_h=int(h_hap*0.98), rot=-2)
paste_letter(front, 'clean_P2', 1148, y_happy + 6, target_h=h_hap, rot=3)
paste_letter(front, 'clean_Y', 1390, y_happy - 8, target_h=int(h_hap*0.96), rot=-2)

# BIRTHDAY (Ransom cutout letters)
paste_letter(front, 'clean_b_B', 310, y_bday - 6, target_h=h_bday, rot=-2)
paste_letter(front, 'clean_b_I', 510, y_bday + 6, target_h=int(h_bday*0.94), rot=1)
paste_letter(front, 'clean_b_R', 705, y_bday - 4, target_h=int(h_bday*0.98), rot=-3)
paste_letter(front, 'clean_b_T', 905, y_bday + 6, target_h=h_bday, rot=2)
paste_letter(front, 'clean_b_H', 1140, y_bday - 6, target_h=h_bday, rot=-2)
paste_letter(front, 'clean_b_D', 1335, y_bday + 6, target_h=int(h_bday*0.96), rot=2)
paste_letter(front, 'clean_b_A', 1535, y_bday - 4, target_h=int(h_bday*0.95), rot=-2)
paste_letter(front, 'clean_b_Y', 1725, y_bday + 6, target_h=int(h_bday*0.92), rot=3)

# '20' ROSE GOLD FOIL BALLOONS
b_2 = Image.open('stickers_extracted/sticker_17.png').convert('RGBA')
b_0 = Image.open('stickers_extracted/sticker_18.png').convert('RGBA')
h_balloon = 470
w_2 = int(b_2.width * h_balloon / b_2.height)
w_0 = int(b_0.width * h_balloon / b_0.height)
b_2_res = b_2.resize((w_2, h_balloon), Image.LANCZOS)
b_0_res = b_0.resize((w_0, h_balloon), Image.LANCZOS)

y_balloon = 1580
paste_with_shadow(front, b_2_res, 1024 - 22 - w_2, y_balloon, offset=(5, 10), blur=14, opacity=170)
paste_with_shadow(front, b_0_res, 1024 + 22, y_balloon, offset=(5, 10), blur=14, opacity=170)

# Bottom stickers
st_stamp = Image.open('stickers_extracted/sticker_02.png').convert('RGBA').rotate(-8, expand=True)
st_stamp = st_stamp.resize((230, int(st_stamp.height * 230 / st_stamp.width)), Image.LANCZOS)
paste_with_shadow(front, st_stamp, 120, H_CARD - 390)

fl_bouquet = Image.open('stickers_extracted/sticker_01.png').convert('RGBA').rotate(15, expand=True)
fl_bouquet = fl_bouquet.resize((250, int(fl_bouquet.height * 250 / fl_bouquet.width)), Image.LANCZOS)
paste_with_shadow(front, fl_bouquet, W_FRONT - 340, H_CARD - 410)

# Glossy heart stickers & sparkles on front
for hx, hy, sz in [(520, 480, 26), (1500, 490, 22), (460, 2260, 26), (1560, 2260, 24), (920, 720, 20), (1130, 720, 20)]:
    h_s = make_glossy_heart_sticker(sz, (255, 95, 135))
    paste_with_shadow(front, h_s, hx, hy, blur=8, opacity=140)

for sx, sy in [(280, 360), (1740, 380), (180, 1080), (1860, 1080), (320, 2100), (1720, 2100)]:
    draw_sparkle(fdraw, sx, sy, size=9)

card_front_left = front.crop((0, 0, 1024, H_CARD))
card_front_right = front.crop((1024, 0, W_FRONT, H_CARD))
card_front_left.save('textures_3d/card_front_left.png')
card_front_right.save('textures_3d/card_front_right.png')
print('Saved card_front_left.png and card_front_right.png')

# =========================================================================
# 2. INSIDE LEFT FLAP (ZIGZAG CASCADE LAYOUT)
# =========================================================================
print('2. Inside Left Flap (Zigzag)...')
in_left = make_dark_paper(W_FLAP, H_CARD, (13, 13, 16), 2.5, 0.16)
ldraw = ImageDraw.Draw(in_left)

# Row 1: LEFT Photo (Smiling selfie with flower)
p1 = make_polaroid('photos_perfect/photo_02.jpg', target_photo_w=390, target_photo_h=390, rot=-3)
paste_with_shadow(in_left, p1, 45, 110, offset=(4, 8), blur=12, opacity=150)

# Row 1: RIGHT space -> Note + pink bow + glossy hearts
note_special = Image.open('stickers_extracted/sticker_00.png').convert('RGBA').rotate(3, expand=True)
note_special = note_special.resize((350, int(note_special.height * 350 / note_special.width)), Image.LANCZOS)
paste_with_shadow(in_left, note_special, 550, 140, offset=(3, 7), blur=10, opacity=140)

mini_bow = Image.open('stickers_extracted/sticker_05.png').convert('RGBA').rotate(-6, expand=True)
mini_bow = mini_bow.resize((170, int(mini_bow.height * 170 / mini_bow.width)), Image.LANCZOS)
paste_with_shadow(in_left, mini_bow, 640, 420, offset=(2, 5), blur=8, opacity=130)

paste_with_shadow(in_left, make_glossy_heart_sticker(26, (255, 95, 135)), 910, 110, blur=6, opacity=140)
paste_with_shadow(in_left, make_glossy_heart_sticker(20, (255, 130, 170)), 540, 430, blur=6, opacity=130)

# Row 2: LEFT space -> Personalized birthday letter from user + sweet stamp + glossy heart
lines_l = [
    "Happy birthday, babyyyy!",
    "Thank you so much for",
    "always being there for me.",
    "You don't know how much I love you.",
    "I really wish I could be there",
    "with you so we could celebrate",
    "your birthday together!"
]
y_tl = 810
for l in lines_l:
    ldraw.text((55, y_tl), l, font=font_hand_msg, fill=(255, 245, 240, 235))
    y_tl += 48

stamp_sweet = Image.open('stickers_extracted/sticker_23.png').convert('RGBA').rotate(4, expand=True)
stamp_sweet = stamp_sweet.resize((200, int(stamp_sweet.height * 200 / stamp_sweet.width)), Image.LANCZOS)
paste_with_shadow(in_left, stamp_sweet, 150, 1170, offset=(3, 6), blur=9, opacity=140)
paste_with_shadow(in_left, make_glossy_heart_sticker(24, (255, 95, 135)), 350, y_tl - 35, blur=6, opacity=140)

# Row 2: RIGHT Photo (Cute smiling face)
p2 = make_polaroid('photos_perfect/photo_03.jpg', target_photo_w=390, target_photo_h=390, rot=3)
paste_with_shadow(in_left, p2, 535, 780, offset=(4, 8), blur=12, opacity=150)

# Row 3: LEFT Photo (Blue ethnic dress)
p3 = make_polaroid('photos_perfect/photo_06.jpg', target_photo_w=390, target_photo_h=390, rot=2)
paste_with_shadow(in_left, p3, 45, 1450, offset=(4, 8), blur=12, opacity=150)

# Row 3: RIGHT space -> Teddy bear with red heart + Forever & Always note + hearts
teddy = Image.open('stickers_extracted/sticker_16.png').convert('RGBA').rotate(-3, expand=True)
teddy = teddy.resize((330, int(teddy.height * 330 / teddy.width)), Image.LANCZOS)
paste_with_shadow(in_left, teddy, 580, 1460, offset=(4, 8), blur=12, opacity=150)

note_fa = Image.open('stickers_extracted/sticker_04.png').convert('RGBA').rotate(2, expand=True)
note_fa = note_fa.resize((360, int(note_fa.height * 360 / note_fa.width)), Image.LANCZOS)
paste_with_shadow(in_left, note_fa, 560, 1850, offset=(3, 6), blur=10, opacity=140)
paste_with_shadow(in_left, make_glossy_heart_sticker(22, (255, 105, 145)), 920, 1880, blur=6, opacity=140)

# Row 4: LEFT space -> Reasons I love you note + memories quote
note_reasons = Image.open('stickers_extracted/sticker_20.png').convert('RGBA').rotate(-2, expand=True)
note_reasons = note_reasons.resize((410, int(note_reasons.height * 410 / note_reasons.width)), Image.LANCZOS)
paste_with_shadow(in_left, note_reasons, 55, 2130, offset=(4, 8), blur=12, opacity=140)

ldraw.text((55, 2580), 'you became a part of my heart forever!', font=font_hand_sm, fill=(255, 240, 245, 210))
paste_with_shadow(in_left, make_glossy_heart_sticker(24, (255, 95, 135)), 460, 2565, blur=6, opacity=140)

# Row 4: RIGHT Photo (Lab coat smiling)
p4 = make_polaroid('photos_perfect/photo_09.jpg', target_photo_w=390, target_photo_h=390, rot=-3)
paste_with_shadow(in_left, p4, 535, 2120, offset=(4, 8), blur=12, opacity=150)

# Sparkles & extra hearts on left flap
for sx, sy in [(500, 130), (100, 750), (920, 1400), (100, 2040), (920, 2690), (480, 800), (510, 2070)]:
    draw_sparkle(ldraw, sx, sy, size=7)
for hx, hy, sz in [(800, 530, 22), (460, 1380, 20), (460, 2050, 22), (100, 1380, 20), (900, 740, 22)]:
    paste_with_shadow(in_left, make_glossy_heart_sticker(sz, (255, 105, 145)), hx, hy, blur=6, opacity=140)

in_left.save('textures_3d/card_inside_left.png')
print('Saved card_inside_left.png')

# =========================================================================
# 3. INSIDE CENTER PANEL:
#    Top Lines: HAPPY / BIRTHDAY / SIDDHI on RED PAPER in CURVES
#               with cut in half triangle from down (swallowtail)
#    Then: 'I' Balloon
#    Then: 8-Photo Stepped Pixel Heart
#    Then: 'U' Balloon
#    Bottom: Friendship Quotes
# =========================================================================
print('3. Inside Center Panel (Red Curved Banners: Happy / Birthday / SIDDHI -> I -> Heart -> U)...')
ctr = make_dark_paper(W_CTR, H_CARD, (13, 13, 16), 2.5, 0.16)
cdraw = ImageDraw.Draw(ctr)

cx = W_CTR // 2

# 1. HAPPY (Curved Red Paper Swallowtail Bunting)
draw_curved_pennant_line(ctr, 'HAPPY', font_pennant, cx, 55, 480, dip=20, w_p=72, h_p=92, notch=24)

# 2. BIRTHDAY (Curved Red Paper Swallowtail Bunting)
draw_curved_pennant_line(ctr, 'BIRTHDAY', font_pennant, cx, 180, 750, dip=26, w_p=70, h_p=90, notch=22)

# 3. SIDDHI (Curved Red Paper Swallowtail Bunting - Bold)
draw_curved_pennant_line(ctr, 'SIDDHI', font_pennant_sid, cx, 310, 600, dip=24, w_p=80, h_p=102, notch=26)

# Hearts flanking SIDDHI banner
paste_with_shadow(ctr, make_glossy_heart_sticker(30, (255, 95, 135)), cx - 350, 315, blur=8, opacity=150)
paste_with_shadow(ctr, make_glossy_heart_sticker(30, (255, 95, 135)), cx + 320, 315, blur=8, opacity=150)

# 4. 'I' BALLOON
path_bi = r'C:\Users\akash\.gemini\antigravity-ide\brain\1e210473-9769-43a8-bd7d-63974ca30498\balloon_letter_i_isolated_1790324621149.jpg'
b_i_top = get_clean_balloon_rgba(path_bi, 240)
y_i = 445
paste_with_shadow(ctr, b_i_top, (W_CTR - b_i_top.width)//2, y_i, offset=(4, 9), blur=14, opacity=175)

# Hearts flanking balloon 'I'
paste_with_shadow(ctr, make_glossy_heart_sticker(26, (255, 95, 135)), (W_CTR - b_i_top.width)//2 - 110, y_i + 80, blur=8, opacity=150)
paste_with_shadow(ctr, make_glossy_heart_sticker(26, (255, 95, 135)), (W_CTR + b_i_top.width)//2 + 50, y_i + 80, blur=8, opacity=150)

# 5. 8-PHOTO STEPPED PIXEL HEART IN CENTER
pw_h, ph_h = 310, 360
gap_x, gap_y = 20, 20
border = 10
fw, fh = pw_h + border*2, ph_h + border*2

y_start = 710

heart_photos = [
    'photos_perfect/photo_16.jpg', # Row 1, left
    'photos_perfect/photo_07.jpg', # Row 1, right
    'photos_perfect/photo_15.jpg', # Row 2, left
    'photos_uploaded/turn3_img2_raw.png', # Row 2, center (Hello Kitty)
    'photos_uploaded/turn3_img3_raw.png', # Row 2, right (Pink kurta)
    'photos_perfect/photo_10.jpg', # Row 3, left
    'photos_uploaded/photo_upload_2_upright.png', # Row 3, right (B&W dress)
    'photos_perfect/photo_05.jpg'  # Row 4, bottom center
]

# Row 1: 2 photos
y1 = y_start
x1_l = cx - fw - gap_x // 2
x1_r = cx + gap_x // 2
paste_with_shadow(ctr, make_heart_photo(heart_photos[0], pw_h, ph_h, border, centering=(0.5, 0.25)), x1_l, y1)
paste_with_shadow(ctr, make_heart_photo(heart_photos[1], pw_h, ph_h, border, centering=(0.5, 0.35)), x1_r, y1)

# Row 2: 3 photos
y2 = y1 + fh + gap_y
x2_l = cx - fw - fw//2 - gap_x
x2_c = cx - fw//2
x2_r = cx + fw//2 + gap_x
paste_with_shadow(ctr, make_heart_photo(heart_photos[2], pw_h, ph_h, border, centering=(0.5, 0.3)), x2_l, y2)
paste_with_shadow(ctr, make_heart_photo(heart_photos[3], pw_h, ph_h, border, centering=(0.5, 0.35)), x2_c, y2)
paste_with_shadow(ctr, make_heart_photo(heart_photos[4], pw_h, ph_h, border, centering=(0.5, 0.35)), x2_r, y2)

# Row 3: 2 photos
y3 = y2 + fh + gap_y
x3_l = cx - fw - gap_x // 2
x3_r = cx + gap_x // 2
paste_with_shadow(ctr, make_heart_photo(heart_photos[5], pw_h, ph_h, border, centering=(0.5, 0.5)), x3_l, y3)
paste_with_shadow(ctr, make_heart_photo(heart_photos[6], pw_h, ph_h, border, centering=(0.5, 0.35)), x3_r, y3)

# Row 4: 1 photo
y4 = y3 + fh + gap_y
x4_c = cx - fw//2
paste_with_shadow(ctr, make_heart_photo(heart_photos[7], pw_h, ph_h, border, centering=(0.5, 0.45)), x4_c, y4)

# 6. STICKERS & HEARTS FLANKING THE SIDES OF THE HEART
# Left side of Row 2:
note_ilove = Image.open('stickers_extracted/sticker_19.png').convert('RGBA').rotate(-4, expand=True)
note_ilove = note_ilove.resize((360, int(note_ilove.height * 360 / note_ilove.width)), Image.LANCZOS)
paste_with_shadow(ctr, note_ilove, x2_l - 420, y2 + 20, offset=(3, 7), blur=10, opacity=140)

cdraw.text((x2_l - 420, y2 + 420), 'you mean the\nworld to me', font=font_hand_md, fill=(255, 240, 245, 220))
paste_with_shadow(ctr, make_glossy_heart_sticker(30, (255, 95, 135)), x2_l - 180, y2 + 450, blur=8, opacity=150)

# Left side of Row 1 & 3:
paste_with_shadow(ctr, mini_bow.rotate(12, expand=True), x2_l - 360, y1 + 50, blur=8, opacity=130)
paste_with_shadow(ctr, make_glossy_heart_sticker(26, (255, 120, 160)), x2_l - 160, y3 + 60, blur=8, opacity=140)

# Right side of Row 2:
note_smile2 = Image.open('stickers_extracted/sticker_03.png').convert('RGBA').rotate(3, expand=True)
note_smile2 = note_smile2.resize((370, int(note_smile2.height * 370 / note_smile2.width)), Image.LANCZOS)
paste_with_shadow(ctr, note_smile2, x2_r + fw + 60, y2 + 20, offset=(3, 7), blur=10, opacity=140)

cdraw.text((x2_r + fw + 70, y2 + 420), 'my favorite\nperson', font=font_hand_md, fill=(255, 240, 245, 220))
paste_with_shadow(ctr, make_glossy_heart_sticker(30, (255, 95, 135)), x2_r + fw + 280, y2 + 450, blur=8, opacity=150)

# Right side of Row 1 & 3:
stamp_rose_c = Image.open('stickers_extracted/sticker_02.png').convert('RGBA').rotate(8, expand=True)
stamp_rose_c = stamp_rose_c.resize((190, int(stamp_rose_c.height * 190 / stamp_rose_c.width)), Image.LANCZOS)
paste_with_shadow(ctr, stamp_rose_c, x2_r + fw + 160, y1 + 30, blur=8, opacity=140)
paste_with_shadow(ctr, make_glossy_heart_sticker(26, (255, 120, 160)), x2_r + fw + 200, y3 + 60, blur=8, opacity=140)

# 7. 'U' BALLOON BELOW HEART
path_bu = r'C:\Users\akash\.gemini\antigravity-ide\brain\1e210473-9769-43a8-bd7d-63974ca30498\balloon_letter_u_isolated_1790324657951.jpg'
b_u_bot = get_clean_balloon_rgba(path_bu, 270)
y_u = y4 + fh + 45
paste_with_shadow(ctr, b_u_bot, (W_CTR - b_u_bot.width)//2, y_u, offset=(4, 9), blur=14, opacity=175)

# Hearts flanking balloon 'U'
paste_with_shadow(ctr, make_glossy_heart_sticker(28, (255, 95, 135)), (W_CTR - b_u_bot.width)//2 - 120, y_u + 90, blur=8, opacity=150)
paste_with_shadow(ctr, make_glossy_heart_sticker(28, (255, 95, 135)), (W_CTR + b_u_bot.width)//2 + 50, y_u + 90, blur=8, opacity=150)

# Extra sparkles across center panel
sparkles_ctr = [
    (250, 150), (1800, 150), (x2_l - 120, y1 + 80), (x2_r + fw + 140, y1 + 80),
    (x2_l - 140, y3 + 160), (x2_r + fw + 150, y3 + 160),
    (220, y_u + 120), (1820, y_u + 120), (cx - 280, y_u + 260), (cx + 280, y_u + 260)
]
for sx, sy in sparkles_ctr:
    draw_sparkle(cdraw, sx, sy, size=8)

ctr.save('textures_3d/card_inside_center.png')
print('Saved card_inside_center.png')

# =========================================================================
# 4. INSIDE RIGHT FLAP (ZIGZAG CASCADE LAYOUT)
# =========================================================================
print('4. Inside Right Flap (Zigzag)...')
in_right = make_dark_paper(W_FLAP, H_CARD, (13, 13, 16), 2.5, 0.16)
rdraw = ImageDraw.Draw(in_right)

# Row 1: LEFT space -> Personalized blessing letter from user & rose stamp + hearts
lines_r = [
    "I really hope you get",
    "everything you want in life,",
    "always stay happy & healthy,",
    "and achieve everything",
    "you've ever dreamed of.",
    "You deserve all the love,",
    "happiness, and beautiful",
    "things life has to offer!"
]
y_tr = 135
for l in lines_r:
    rdraw.text((55, y_tr), l, font=font_hand_msg, fill=(255, 245, 240, 235))
    y_tr += 46

stamp_rose = Image.open('stickers_extracted/sticker_02.png').convert('RGBA').rotate(-6, expand=True)
stamp_rose = stamp_rose.resize((200, int(stamp_rose.height * 200 / stamp_rose.width)), Image.LANCZOS)
paste_with_shadow(in_right, stamp_rose, 150, 520, offset=(3, 6), blur=9, opacity=140)
paste_with_shadow(in_right, make_glossy_heart_sticker(24, (255, 95, 135)), 380, 520, blur=6, opacity=140)

# Row 1: RIGHT Photo (Whiskers & pink bow, full framing without white bars)
p5 = make_polaroid('photos_perfect/photo_11.jpg', target_photo_w=390, target_photo_h=390, rot=3, centering=(0.5, 0.15))
paste_with_shadow(in_right, p5, 535, 110, offset=(4, 8), blur=12, opacity=150)

# Row 2: LEFT Photo (Upright curly hair selfie)
p6 = make_polaroid('photos_uploaded/turn3_img1_rot_ccw.jpg', target_photo_w=390, target_photo_h=390, rot=-2)
paste_with_shadow(in_right, p6, 45, 780, offset=(4, 8), blur=12, opacity=150)

# Row 2: RIGHT space -> Tulips bouquet + Tomorrows note + hearts
tulips = Image.open('stickers_extracted/sticker_21.png').convert('RGBA').rotate(5, expand=True)
tulips = tulips.resize((290, int(tulips.height * 290 / tulips.width)), Image.LANCZOS)
paste_with_shadow(in_right, tulips, 590, 780, offset=(4, 8), blur=12, opacity=140)

note_today = Image.open('stickers_extracted/sticker_22.png').convert('RGBA').rotate(-3, expand=True)
note_today = note_today.resize((380, int(note_today.height * 380 / note_today.width)), Image.LANCZOS)
paste_with_shadow(in_right, note_today, 550, 1140, offset=(4, 8), blur=12, opacity=140)
paste_with_shadow(in_right, make_glossy_heart_sticker(22, (255, 110, 150)), 920, 1140, blur=6, opacity=140)

# Row 3: LEFT space -> Darling note + You make my heart smile + hearts
note_darling = Image.open('stickers_extracted/sticker_24.png').convert('RGBA').rotate(3, expand=True)
note_darling = note_darling.resize((350, int(note_darling.height * 350 / note_darling.width)), Image.LANCZOS)
paste_with_shadow(in_right, note_darling, 60, 1460, offset=(4, 8), blur=12, opacity=140)

note_smile = Image.open('stickers_extracted/sticker_03.png').convert('RGBA').rotate(-2, expand=True)
note_smile = note_smile.resize((350, int(note_smile.height * 350 / note_smile.width)), Image.LANCZOS)
paste_with_shadow(in_right, note_smile, 60, 1770, offset=(3, 6), blur=10, opacity=140)
paste_with_shadow(in_right, make_glossy_heart_sticker(26, (255, 95, 135)), 430, 1760, blur=6, opacity=140)

# Row 3: RIGHT Photo (Star glasses selfie)
p7 = make_polaroid('photos_uploaded/photo_upload_1_upright.png', target_photo_w=390, target_photo_h=390, rot=-3)
paste_with_shadow(in_right, p7, 535, 1450, offset=(4, 8), blur=12, opacity=150)

# Row 4: LEFT Photo (B&W heart crown selfie)
p8 = make_polaroid('photos_perfect/photo_13.jpg', target_photo_w=390, target_photo_h=390, rot=2)
paste_with_shadow(in_right, p8, 45, 2120, offset=(4, 8), blur=12, opacity=150)

# Row 4: RIGHT space -> I still fall for you note + sweet quote + hearts
note_fall = Image.open('stickers_extracted/sticker_26.png').convert('RGBA').rotate(-2, expand=True)
note_fall = note_fall.resize((370, int(note_fall.height * 370 / note_fall.width)), Image.LANCZOS)
paste_with_shadow(in_right, note_fall, 540, 2140, offset=(4, 8), blur=12, opacity=140)

rdraw.text((540, 2480), 'you make my heart smile and life beautiful,', font=font_hand_sm, fill=(255, 240, 245, 210))
rdraw.text((540, 2530), 'forever and always, no matter what!', font=font_hand_sm, fill=(255, 240, 245, 210))
paste_with_shadow(in_right, make_glossy_heart_sticker(24, (255, 95, 135)), 920, 2515, blur=6, opacity=140)

# Sparkles & extra hearts on right flap
for sx, sy in [(920, 130), (100, 750), (500, 1400), (100, 2040), (920, 2690), (480, 800), (510, 2070)]:
    draw_sparkle(rdraw, sx, sy, size=7)
for hx, hy, sz in [(480, 530, 22), (800, 1380, 20), (480, 2050, 22), (100, 1380, 20), (900, 740, 22)]:
    paste_with_shadow(in_right, make_glossy_heart_sticker(sz, (255, 105, 145)), hx, hy, blur=6, opacity=140)

in_right.save('textures_3d/card_inside_right.png')
print('Saved card_inside_right.png')

# Composite spread preview
full_inside = Image.new('RGB', (W_FLAP + W_CTR + W_FLAP, H_CARD))
full_inside.paste(in_left, (0, 0))
full_inside.paste(ctr, (W_FLAP, 0))
full_inside.paste(in_right, (W_FLAP + W_CTR, 0))
full_inside_small = full_inside.resize((1500, int(H_CARD * 1500 / full_inside.width)), Image.LANCZOS)
full_inside_small.save('inside_spread_preview.jpg')

front_small = front.resize((750, int(H_CARD * 750 / front.width)), Image.LANCZOS)
front_small.save('front_cover_preview.jpg')

print('ALL UPDATED TEXTURES CREATED SUCCESSFULLY!')
