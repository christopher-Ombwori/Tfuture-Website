import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image

def convert_svg_to_png(svg_path, png_path, scale=2):
    # Convert SVG to ReportLab Drawing
    drawing = svg2rlg(svg_path)
    
    # Scale the drawing
    drawing.width *= scale
    drawing.height *= scale
    drawing.scale(scale, scale)
    
    # Render as PNG
    renderPM.drawToFile(drawing, png_path, fmt="PNG")
    
    # Optimize the PNG
    img = Image.open(png_path)
    img.save(png_path, optimize=True)

def main():
    # Directory containing SVG files
    svg_dir = 'static/images/email-icons'
    
    # Create output directory if it doesn't exist
    os.makedirs(svg_dir, exist_ok=True)
    
    # Get all SVG files
    svg_files = [f for f in os.listdir(svg_dir) if f.endswith('.svg')]
    
    # Convert each SVG to PNG
    for svg_file in svg_files:
        svg_path = os.path.join(svg_dir, svg_file)
        png_file = svg_file.replace('.svg', '.png')
        png_path = os.path.join(svg_dir, png_file)
        
        print(f"Converting {svg_file} to {png_file}...")
        convert_svg_to_png(svg_path, png_path)
    
    print("Conversion complete!")

if __name__ == "__main__":
    main()