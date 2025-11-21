"""
Generate favicon files for Dubai Smart Investment website
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Colors from the website
GOLD = '#d4af37'
DARK = '#1a1a1a'
WHITE = '#ffffff'

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_favicon_image(size):
    """Create a favicon image with DSI branding"""
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw gold circle background
    margin = size // 10
    draw.ellipse([margin, margin, size - margin, size - margin], 
                 fill=hex_to_rgb(GOLD))
    
    # Draw "D" for Dubai in dark color
    try:
        # Try to use a nice font
        font_size = int(size * 0.6)
        font = ImageFont.truetype("arialbd.ttf", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Draw the letter "D" centered
    text = "D"
    
    # Get text bounding box for centering
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2 - bbox[0]
    y = (size - text_height) // 2 - bbox[1]
    
    draw.text((x, y), text, fill=hex_to_rgb(DARK), font=font)
    
    return img

def main():
    print("Generating favicon files for Dubai Smart Investment...")
    
    # Generate different sizes
    sizes = {
        'favicon-16x16.png': 16,
        'favicon-32x32.png': 32,
        'apple-touch-icon.png': 180,
        'android-chrome-192x192.png': 192,
        'android-chrome-512x512.png': 512,
    }
    
    for filename, size in sizes.items():
        print(f"Creating {filename} ({size}x{size})...")
        img = create_favicon_image(size)
        img.save(filename, 'PNG')
    
    # Create ICO file (multi-resolution)
    print("Creating favicon.ico...")
    img_16 = create_favicon_image(16)
    img_32 = create_favicon_image(32)
    img_48 = create_favicon_image(48)
    
    # Save as ICO with multiple sizes
    img_16.save('favicon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
    
    print("✅ All favicon files generated successfully!")
    print("\nGenerated files:")
    for filename in sizes.keys():
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            print(f"  ✓ {filename} ({file_size:,} bytes)")
    if os.path.exists('favicon.ico'):
        file_size = os.path.getsize('favicon.ico')
        print(f"  ✓ favicon.ico ({file_size:,} bytes)")

if __name__ == '__main__':
    main()
