import numpy as np
from PIL import Image, ImageDraw, ImageFont

W_CTR, H_CARD = 2048, 2867
arr = np.tile(np.array((14, 14, 17), dtype=np.float32), (H_CARD, W_CTR, 1))
noise = np.random.normal(0, 2.0, (H_CARD, W_CTR, 1)).astype(np.float32)
arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
back = Image.fromarray(arr)
d = ImageDraw.Draw(back)

font_logo = ImageFont.truetype('fonts/Poppins-Bold.ttf', 38)
font_sub = ImageFont.truetype('fonts/Caveat.ttf', 44)

# Center hallmark
cx, cy = W_CTR // 2, H_CARD // 2
logo_text = 'MADE WITH LOVE FOR SIDDHI'
sub_text = '20th Birthday Edition  •  Forever Always'

bbox1 = d.textbbox((0, 0), logo_text, font=font_logo)
w1 = bbox1[2] - bbox1[0]
d.text((cx - w1//2, cy - 30), logo_text, font=font_logo, fill=(210, 180, 140, 180))

bbox2 = d.textbbox((0, 0), sub_text, font=font_sub)
w2 = bbox2[2] - bbox2[0]
d.text((cx - w2//2, cy + 30), sub_text, font=font_sub, fill=(240, 210, 220, 170))

# Gold border outline
d.rectangle([100, 100, W_CTR - 100, H_CARD - 100], outline=(210, 180, 140, 90), width=3)
d.rectangle([120, 120, W_CTR - 120, H_CARD - 120], outline=(210, 180, 140, 50), width=1)

back.save('textures_3d/card_back.png')
print('textures_3d/card_back.png saved!')
