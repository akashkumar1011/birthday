import os, fitz, shutil
from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageDraw, ImageFont
import numpy as np

# Scale 1.5x -> 3720 x 5262 (450 DPI Ultra-HD A4 format)
scale = 1.5
W_PAGE = int(2480 * scale) # 3720
H_PAGE = int(3508 * scale) # 5262

page = Image.new('RGB', (W_PAGE, H_PAGE), (255, 255, 255))
pdraw = ImageDraw.Draw(page)

# Heart Card Dimensions
cw = int(440 * scale) # 660
ch = int(510 * scale) # 765
pad = int(18 * scale) # 27
g = int(22 * scale)   # 33

step_x = cw + g
step_y = ch + g

heart_w = 3 * cw + 2 * g
start_x = (W_PAGE - heart_w) // 2
start_y = int(90 * scale) # 135

def enhance_photo(im):
    im = ImageEnhance.Color(im).enhance(1.06)
    im = ImageEnhance.Contrast(im).enhance(1.05)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=110, threshold=2))
    return im

def create_card_with_shadow(img_path, rot=0, box=None, centering=(0.5, 0.35)):
    im = Image.open(img_path)
    if rot != 0:
        im = im.rotate(rot, expand=True)
    if box:
        im = im.crop(box)
    
    pw, ph = cw - 2*pad, ch - 2*pad
    fitted = ImageOps.fit(im, (pw, ph), method=Image.LANCZOS, centering=centering)
    fitted = enhance_photo(fitted)
    
    card = Image.new('RGB', (cw, ch), (255, 255, 255))
    card.paste(fitted, (pad, pad))
    
    cdraw = ImageDraw.Draw(card)
    cdraw.rectangle([0, 0, cw-1, ch-1], outline=(200, 200, 200), width=int(1.5 * scale))
    dash = int(6 * scale)
    for x in range(0, cw, dash*2):
        cdraw.line([(x, 0), (min(x+dash, cw), 0)], fill=(150, 150, 150), width=int(1.5 * scale))
        cdraw.line([(x, ch-1), (min(x+dash, cw), ch-1)], fill=(150, 150, 150), width=int(1.5 * scale))
    for y in range(0, ch, dash*2):
        cdraw.line([(0, y), (0, min(y+dash, ch))], fill=(150, 150, 150), width=int(1.5 * scale))
        cdraw.line([(cw-1, y), (cw-1, min(y+dash, ch))], fill=(150, 150, 150), width=int(1.5 * scale))
    cdraw.rectangle([pad-1, pad-1, cw-pad, ch-pad], outline=(230, 230, 230), width=1)
    
    shadow_margin = int(24 * scale)
    sw, sh = cw + 2*shadow_margin, ch + 2*shadow_margin
    shadow = Image.new('RGBA', (sw, sh), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle(
        [shadow_margin - 3, shadow_margin + 5, shadow_margin + cw + 3, shadow_margin + ch + 12],
        radius=int(6 * scale),
        fill=(0, 0, 0, 35)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(int(9 * scale)))
    
    card_rgba = card.convert('RGBA')
    shadow.paste(card_rgba, (shadow_margin, shadow_margin), card_rgba)
    return shadow, shadow_margin

# 8 Photos of Stepped Heart
heart_specs = [
    # Row 1: 2 photos
    (int(0.5 * step_x), 0, 'photos_perfect/photo_16.jpg', 0, None, (0.5, 0.25)),
    (int(1.5 * step_x), 0, 'photos_perfect/photo_07.jpg', 0, None, (0.5, 0.35)),
    # Row 2: 3 photos (middle: Hello Kitty clips, right: pink kurta)
    (0, step_y, 'photos_perfect/photo_15.jpg', 0, None, (0.5, 0.3)),
    (step_x, step_y, 'photos_uploaded/turn3_img2_raw.png', 0, None, (0.5, 0.35)),
    (2 * step_x, step_y, 'photos_uploaded/turn3_img3_raw.png', 0, None, (0.5, 0.35)),
    # Row 3: 2 photos (left: phone mirror, right: B&W dress mirror selfie)
    (int(0.5 * step_x), 2 * step_y, 'photos_perfect/photo_10.jpg', 0, (0, 420, 1080, 1920), (0.5, 0.5)),
    (int(1.5 * step_x), 2 * step_y, 'photos_uploaded/photo_upload_2_upright.png', 0, None, (0.5, 0.35)),
    # Row 4: 1 photo (tip)
    (step_x, 3 * step_y, 'photos_perfect/photo_05.jpg', 0, None, (0.5, 0.45))
]

for lx, ty, path, rot, box, centering in heart_specs:
    shadow_card, sm = create_card_with_shadow(path, rot, box, centering)
    page.paste(shadow_card, (start_x + lx - sm, start_y + ty - sm), shadow_card)

# Helper: Cut isolated balloon letter and build clean card
def make_clean_balloon_card(img_path, letter_name):
    im = Image.open(img_path).convert('RGBA')
    arr = np.array(im)
    rgb = arr[:, :, :3]
    white_mask = (rgb[:, :, 0] > 240) & (rgb[:, :, 1] > 240) & (rgb[:, :, 2] > 240)
    arr[:, :, 3] = np.where(white_mask, 0, 255)
    non_zero = np.where(arr[:, :, 3] > 0)
    ymin, ymax = np.min(non_zero[0]), np.max(non_zero[0])
    xmin, xmax = np.min(non_zero[1]), np.max(non_zero[1])
    letter_cropped = Image.fromarray(arr).crop((xmin, ymin, xmax, ymax))
    
    target_h = int(470 * scale)
    target_w = int(letter_cropped.width * target_h / letter_cropped.height)
    letter_resized = letter_cropped.resize((target_w, target_h), Image.LANCZOS)
    
    b_cw = target_w + int(80 * scale)
    b_ch = target_h + int(85 * scale)
    
    card = Image.new('RGB', (b_cw, b_ch), (255, 255, 255))
    cdraw = ImageDraw.Draw(card)
    
    dash = int(6 * scale)
    for x in range(0, b_cw, dash*2):
        cdraw.line([(x, 0), (min(x+dash, b_cw), 0)], fill=(160, 160, 160), width=int(1.5 * scale))
        cdraw.line([(x, b_ch-1), (min(x+dash, b_cw), b_ch-1)], fill=(160, 160, 160), width=int(1.5 * scale))
    for y in range(0, b_ch, dash*2):
        cdraw.line([(0, y), (0, min(y+dash, b_ch))], fill=(160, 160, 160), width=int(1.5 * scale))
        cdraw.line([(b_cw-1, y), (b_cw-1, min(y+dash, b_ch))], fill=(160, 160, 160), width=int(1.5 * scale))
    
    bx = (b_cw - target_w) // 2
    by = int(18 * scale)
    card.paste(letter_resized, (bx, by), letter_resized)
    
    font_bl = ImageFont.truetype('fonts/Outfit.ttf', int(13 * scale))
    sub_text = f'✂ CUT OUT: {letter_name}'
    sbbox = cdraw.textbbox((0, 0), sub_text, font=font_bl)
    sw = sbbox[2] - sbbox[0]
    cdraw.text(((b_cw - sw)//2, b_ch - int(28 * scale)), sub_text, font=font_bl, fill=(150, 150, 150))
    
    shadow_margin = int(24 * scale)
    sw_full, sh_full = b_cw + 2*shadow_margin, b_ch + 2*shadow_margin
    shadow = Image.new('RGBA', (sw_full, sh_full), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle(
        [shadow_margin - 3, shadow_margin + 5, shadow_margin + b_cw + 3, shadow_margin + b_ch + 12],
        radius=int(6 * scale),
        fill=(0, 0, 0, 30)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(int(8 * scale)))
    
    card_rgba = card.convert('RGBA')
    shadow.paste(card_rgba, (shadow_margin, shadow_margin), card_rgba)
    return shadow, shadow_margin, b_cw, b_ch

path_i = r'C:\Users\akash\.gemini\antigravity-ide\brain\1e210473-9769-43a8-bd7d-63974ca30498\balloon_letter_i_isolated_1790324621149.jpg'
path_u = r'C:\Users\akash\.gemini\antigravity-ide\brain\1e210473-9769-43a8-bd7d-63974ca30498\balloon_letter_u_isolated_1790324657951.jpg'

card_i, sm_i, bi_w, bi_h = make_clean_balloon_card(path_i, 'I')
card_u, sm_u, bu_w, bu_h = make_clean_balloon_card(path_u, 'U')

tip_x = start_x + step_x # 1530
tip_y = start_y + 3 * step_y
card_y = tip_y + (ch - bi_h) // 2

# Generous wide spacing from the tip photo
pos_i_x = (tip_x - bi_w) // 2
page.paste(card_i, (pos_i_x - sm_i, card_y - sm_i), card_i)

pos_u_x = (tip_x + cw) + (W_PAGE - (tip_x + cw) - bu_w) // 2
page.paste(card_u, (pos_u_x - sm_u, card_y - sm_u), card_u)

# Add Cute Pinterest Aesthetic Stickers in the Upper Corners
p_stickers = Image.open(r'C:\Users\akash\.gemini\antigravity-ide\brain\1e210473-9769-43a8-bd7d-63974ca30498\pinterest_aesthetic_stickers_1790324892308.jpg')

bow1 = p_stickers.crop((420, 120, 580, 270))
bow2 = p_stickers.crop((590, 120, 750, 270))
bday_badge = p_stickers.crop((600, 280, 810, 480))
cake_sticker = p_stickers.crop((415, 280, 585, 500))
bouquet_sticker = p_stickers.crop((690, 480, 920, 750))
stamps_sticker = p_stickers.crop((80, 520, 550, 710))
hearts_sticker = p_stickers.crop((80, 250, 380, 510))

def add_sticker_card(stk_img, dest_x, dest_y, target_max_dim, label='✂ CUT OUT'):
    w, h = stk_img.size
    ratio = min(target_max_dim / w, target_max_dim / h)
    nw, nh = int(w * ratio), int(h * ratio)
    stk_res = stk_img.resize((nw, nh), Image.LANCZOS)
    
    pad_s = int(12 * scale)
    scw = nw + 2*pad_s
    sch = nh + 2*pad_s + int(20 * scale)
    
    scard = Image.new('RGB', (scw, sch), (255, 255, 255))
    scdraw = ImageDraw.Draw(scard)
    scard.paste(stk_res, (pad_s, pad_s))
    
    dash = int(5 * scale)
    for x in range(0, scw, dash*2):
        scdraw.line([(x, 0), (min(x+dash, scw), 0)], fill=(180, 180, 180), width=int(1.5 * scale))
        scdraw.line([(x, sch-1), (min(x+dash, scw), sch-1)], fill=(180, 180, 180), width=int(1.5 * scale))
    for y in range(0, sch, dash*2):
        scdraw.line([(0, y), (0, min(y+dash, sch))], fill=(180, 180, 180), width=int(1.5 * scale))
        scdraw.line([(scw-1, y), (scw-1, min(y+dash, sch))], fill=(180, 180, 180), width=int(1.5 * scale))
        
    font_s = ImageFont.truetype('fonts/Outfit.ttf', int(11 * scale))
    sbbox = scdraw.textbbox((0, 0), label, font=font_s)
    sw = sbbox[2] - sbbox[0]
    scdraw.text(((scw - sw)//2, sch - int(20 * scale)), label, font=font_s, fill=(160, 160, 160))
    
    sm = int(16 * scale)
    sw_full, sh_full = scw + 2*sm, sch + 2*sm
    shadow = Image.new('RGBA', (sw_full, sh_full), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle(
        [sm - 2, sm + 3, sm + scw + 2, sm + sch + 6],
        radius=int(5 * scale),
        fill=(0, 0, 0, 25)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(int(6 * scale)))
    scard_rgba = scard.convert('RGBA')
    shadow.paste(scard_rgba, (sm, sm), scard_rgba)
    page.paste(shadow, (dest_x - sm, dest_y - sm), shadow)

# Place stickers in the upper-left open area
add_sticker_card(bday_badge, int(80 * scale), int(60 * scale), int(260 * scale), '✂ BDAY BADGE')
add_sticker_card(bow1, int(80 * scale), int(360 * scale), int(260 * scale), '✂ PINK BOW')
add_sticker_card(hearts_sticker, int(80 * scale), int(580 * scale), int(260 * scale), '✂ CUTE HEARTS')

# Place stickers in the upper-right open area
add_sticker_card(bouquet_sticker, W_PAGE - int(340 * scale), int(60 * scale), int(260 * scale), '✂ ROSE BOUQUET')
add_sticker_card(bow2, W_PAGE - int(340 * scale), int(360 * scale), int(260 * scale), '✂ CUTE BOW')
add_sticker_card(stamps_sticker, W_PAGE - int(340 * scale), int(580 * scale), int(260 * scale), '✂ LOVE STAMPS')

# Down Part: INCREASED SIZE to fill the empty space!
flap_cw = int(580 * scale) # 870 px
flap_ch = int(470 * scale) # 705 px
flap_pad = int(15 * scale) # 22 px
flap_gap_x = int(35 * scale) # 52 px
start_flap_x = (W_PAGE - (4 * flap_cw + 3 * flap_gap_x)) // 2

flap_row1_y = int(2320 * scale) # 3480
flap_row2_y = int(2850 * scale) # 4275

flap_photos_row1 = [
    ('photos_perfect/photo_02.jpg', 'Flap Photo 1', (0.5, 0.35), False),
    ('photos_perfect/photo_03.jpg', 'Flap Photo 2', (0.5, 0.35), False),
    ('photos_perfect/photo_06.jpg', 'Flap Photo 3 (Blue Dress)', (0.5, 0.35), False),
    ('photos_perfect/photo_09.jpg', 'Flap Photo 4', (0.5, 0.35), False)
]

flap_photos_row2 = [
    ('photos_perfect/photo_11.jpg', 'Flap Photo 5 (Whiskers & Bow)', (0.5, 0.0), True),
    ('photos_uploaded/turn3_img1_rot_ccw.jpg', 'Flap Photo 6 (Selfie Upright)', (0.5, 0.35), False),
    ('photos_uploaded/photo_upload_1_upright.png', 'Flap Photo 7', (0.5, 0.35), False),
    ('photos_perfect/photo_13.jpg', 'Flap Photo 8', (0.5, 0.35), False)
]

font_label = ImageFont.truetype('fonts/Outfit.ttf', int(13 * scale))

for idx, (path, label, centering, keep_orig) in enumerate(flap_photos_row1):
    im = Image.open(path)
    card = Image.new('RGB', (flap_cw, flap_ch), (255, 255, 255))
    pw, ph = flap_cw - 2*flap_pad, flap_ch - 2*flap_pad - int(25 * scale)
    fitted = ImageOps.fit(im, (pw, ph), method=Image.LANCZOS, centering=centering)
    fitted = enhance_photo(fitted)
    card.paste(fitted, (flap_pad, flap_pad))
    cdraw = ImageDraw.Draw(card)
    dash = int(6 * scale)
    for x in range(0, flap_cw, dash*2):
        cdraw.line([(x, 0), (min(x+dash, flap_cw), 0)], fill=(160, 160, 160), width=int(1.5 * scale))
        cdraw.line([(x, flap_ch-1), (min(x+dash, flap_cw), flap_ch-1)], fill=(160, 160, 160), width=int(1.5 * scale))
    for y in range(0, flap_ch, dash*2):
        cdraw.line([(0, y), (0, min(y+dash, flap_ch))], fill=(160, 160, 160), width=int(1.5 * scale))
        cdraw.line([(flap_cw-1, y), (flap_cw-1, min(y+dash, flap_ch))], fill=(160, 160, 160), width=int(1.5 * scale))
    cdraw.rectangle([flap_pad-1, flap_pad-1, flap_cw-flap_pad, flap_pad+ph], outline=(225, 225, 225), width=1)
    cdraw.text((flap_pad + 6, flap_ch - int(28 * scale)), label, font=font_label, fill=(150, 150, 150))
    bx = start_flap_x + idx * (flap_cw + flap_gap_x)
    page.paste(card, (bx, flap_row1_y))

for idx, (path, label, centering, keep_orig) in enumerate(flap_photos_row2):
    im = Image.open(path)
    card = Image.new('RGB', (flap_cw, flap_ch), (255, 255, 255))
    pw, ph = flap_cw - 2*flap_pad, flap_ch - 2*flap_pad - int(25 * scale)
    if keep_orig:
        contained = ImageOps.contain(im, (pw, ph), method=Image.LANCZOS)
        contained = enhance_photo(contained)
        cx = flap_pad + (pw - contained.width) // 2
        cy = flap_pad + (ph - contained.height) // 2
        card.paste(contained, (cx, cy))
    else:
        fitted = ImageOps.fit(im, (pw, ph), method=Image.LANCZOS, centering=centering)
        fitted = enhance_photo(fitted)
        card.paste(fitted, (flap_pad, flap_pad))
        
    cdraw = ImageDraw.Draw(card)
    dash = int(6 * scale)
    for x in range(0, flap_cw, dash*2):
        cdraw.line([(x, 0), (min(x+dash, flap_cw), 0)], fill=(160, 160, 160), width=int(1.5 * scale))
        cdraw.line([(x, flap_ch-1), (min(x+dash, flap_cw), flap_ch-1)], fill=(160, 160, 160), width=int(1.5 * scale))
    for y in range(0, flap_ch, dash*2):
        cdraw.line([(0, y), (0, min(y+dash, flap_ch))], fill=(160, 160, 160), width=int(1.5 * scale))
        cdraw.line([(flap_cw-1, y), (flap_cw-1, min(y+dash, flap_ch))], fill=(160, 160, 160), width=int(1.5 * scale))
    cdraw.rectangle([flap_pad-1, flap_pad-1, flap_cw-flap_pad, flap_pad+ph], outline=(225, 225, 225), width=1)
    cdraw.text((flap_pad + 6, flap_ch - int(28 * scale)), label, font=font_label, fill=(150, 150, 150))
    bx = start_flap_x + idx * (flap_cw + flap_gap_x)
    page.paste(card, (bx, flap_row2_y))

# Footer
font_foot = ImageFont.truetype('fonts/Outfit.ttf', int(22 * scale))
foot_text = '✂ SIDDHI 20TH BIRTHDAY CARD — MASTER A4 DIY PRINT SHEET (450 DPI ULTRA-HD) — CUT ALONG DASHED LINES'
f_bbox = pdraw.textbbox((0, 0), foot_text, font=font_foot)
fw_txt = f_bbox[2] - f_bbox[0]
pdraw.text(((W_PAGE - fw_txt)//2, H_PAGE - int(60 * scale)), foot_text, font=font_foot, fill=(170, 170, 170))

# Save master files
png_path = 'Siddhi_Photos_A4_Print_Sheet.png'
page.save(png_path, format='PNG', optimize=True)

jpg_path = 'Siddhi_Photos_A4_Print_Sheet.jpg'
page.save(jpg_path, format='JPEG', quality=98, subsampling=0)

pdf_path = 'Siddhi_Photos_A4_Print_Sheet.pdf'
doc = fitz.open()
rect = fitz.Rect(0, 0, 595.276, 841.890)
pdf_page = doc.new_page(width=595.276, height=841.890)
pdf_page.insert_image(rect, filename=png_path)
doc.save(pdf_path, deflate=True)

# Copy to user's Downloads folder
user_downloads = r'C:\Users\akash\Downloads'
shutil.copy2(png_path, os.path.join(user_downloads, 'Siddhi_Photos_A4_Print_Sheet.png'))
shutil.copy2(jpg_path, os.path.join(user_downloads, 'Siddhi_Photos_A4_Print_Sheet.jpg'))
shutil.copy2(pdf_path, os.path.join(user_downloads, 'Siddhi_Photos_A4_Print_Sheet.pdf'))

# Save preview
preview_small = page.resize((1080, int(H_PAGE * 1080 / W_PAGE)), Image.LANCZOS)
preview_small.save('print_sheet_final_preview.jpg')
preview_small.save(r'C:\Users\akash\.gemini\antigravity-ide\brain\1e210473-9769-43a8-bd7d-63974ca30498\print_sheet_final_preview.jpg')
print('SUCCESS! Master Print Sheet fully generated and copied to Downloads!')
