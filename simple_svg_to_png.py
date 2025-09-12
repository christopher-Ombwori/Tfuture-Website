import os
import cairosvg
from PIL import Image

def convert_svg_to_png(svg_path, png_path, scale=2):
    # Convert SVG to PNG using cairosvg
    cairosvg.svg2png(url=svg_path, write_to=png_path, scale=scale)
    
    # Optimize the PNG
    img = Image.open(png_path)
    img.save(png_path, optimize=True)

def main():
    # Directory containing SVG files
    svg_dir = 'static/images/email-icons'
    
    # Get all SVG files
    svg_files = [f for f in os.listdir(svg_dir) if f.endswith('.svg')]
    
    # Convert each SVG to PNG
    for svg_file in svg_files:
        svg_path = os.path.join(svg_dir, svg_file)
        png_file = svg_file.replace('.svg', '.png')
        png_path = os.path.join(svg_dir, png_file)
        
        print(f"Converting {svg_file} to {png_file}...")
        try:
            convert_svg_to_png(svg_path, png_path)
            print(f"Successfully converted {svg_file} to {png_file}")
        except Exception as e:
            print(f"Error converting {svg_file}: {str(e)}")
    
    print("Conversion complete!")

if __name__ == "__main__":
    main()