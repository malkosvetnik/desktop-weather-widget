"""
Kreira weather.ico fajl za Weather Widget
"""
from PIL import Image, ImageDraw, ImageFont
import os

print("🎨 Kreiram weather.ico...")

# Kreiraj sliku 256x256 (za Windows ikonu)
size = 256
img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Nacrtaj gradient pozadinu (plavo-teget)
for y in range(size):
    color = (30 + int(y * 0.2), 60 + int(y * 0.2), 114 + int(y * 0.1), 255)
    draw.line([(0, y), (size, y)], fill=color)

# Nacrtaj krug
circle_margin = 20
draw.ellipse([circle_margin, circle_margin, size - circle_margin, size - circle_margin], 
             fill=(30, 60, 114, 255), 
             outline=(70, 130, 180, 255), 
             width=4)

# Pokušaj da dodaš emoji ili tekst
try:
    # Probaj da koristiš Segoe UI Emoji font (Windows)
    font_size = 120
    font = ImageFont.truetype("seguiemj.ttf", font_size)
    emoji = "☀️"
except:
    # Ako emoji ne radi, koristi tekst
    try:
        font = ImageFont.truetype("arial.ttf", 80)
        emoji = "W"
    except:
        font = ImageFont.load_default()
        emoji = "W"

# Centriraj emoji/tekst
bbox = draw.textbbox((0, 0), emoji, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x = (size - text_width) // 2
y = (size - text_height) // 2 - 10

# Nacrtaj tekst/emoji
draw.text((x, y), emoji, fill=(255, 255, 255, 255), font=font)

# Sačuvaj kao .ico sa više rezolucija (multi-size icon)
icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
img.save('weather.ico', format='ICO', sizes=icon_sizes)

print("✅ weather.ico kreiran!")
print("📁 Lokacija:", os.path.abspath('weather.ico'))
print("\nMožeš sada pokrenuti build_exe.bat")
