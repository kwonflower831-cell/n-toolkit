import struct
import zlib

def make_png(width, height, path):
    # Generates a clean blue square with rounded corners and white inner symbol
    raw = bytearray()
    
    # Pre-render pixels (RGBA)
    r_bg, g_bg, b_bg = 37, 99, 235 # #2563eb (Modern Blue)
    
    for y in range(height):
        row = bytearray([0]) # Filter type 0 (None)
        for x in range(width):
            # Check if within rounded rectangle
            corner_radius = width // 5
            # distance from corner centers
            in_shape = True
            
            # Corner tests
            if x < corner_radius and y < corner_radius:
                if (x - corner_radius)**2 + (y - corner_radius)**2 > corner_radius**2:
                    in_shape = False
            elif x >= width - corner_radius and y < corner_radius:
                if (x - (width - corner_radius))**2 + (y - corner_radius)**2 > corner_radius**2:
                    in_shape = False
            elif x < corner_radius and y >= height - corner_radius:
                if (x - corner_radius)**2 + (y - (height - corner_radius))**2 > corner_radius**2:
                    in_shape = False
            elif x >= width - corner_radius and y >= height - corner_radius:
                if (x - (width - corner_radius))**2 + (y - (height - corner_radius))**2 > corner_radius**2:
                    in_shape = False
                    
            if not in_shape:
                row.extend([0, 0, 0, 0])
                continue
                
            # Inner white document symbol
            doc_left = width * 0.28
            doc_right = width * 0.72
            doc_top = height * 0.22
            doc_bottom = height * 0.78
            
            is_doc = (doc_left <= x <= doc_right) and (doc_top <= y <= doc_bottom)
            
            # Lines inside document
            is_line1 = is_doc and (width * 0.38 <= x <= width * 0.62) and (height * 0.40 <= y <= height * 0.45)
            is_line2 = is_doc and (width * 0.38 <= x <= width * 0.62) and (height * 0.50 <= y <= height * 0.55)
            is_line3 = is_doc and (width * 0.38 <= x <= width * 0.54) and (height * 0.60 <= y <= height * 0.65)
            
            if is_line1 or is_line2 or is_line3:
                # Blue line on document
                row.extend([37, 99, 235, 255])
            elif is_doc:
                # White document paper
                row.extend([255, 255, 255, 255])
            else:
                # Blue background
                row.extend([r_bg, g_bg, b_bg, 255])
                
        raw.extend(row)
        
    compressed = zlib.compress(bytes(raw), 9)
    
    png = bytearray(b'\x89PNG\r\n\x1a\n')
    
    # IHDR
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    png.extend(struct.pack('>I', 13))
    png.extend(b'IHDR')
    png.extend(ihdr_data)
    png.extend(struct.pack('>I', zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff))
    
    # IDAT
    png.extend(struct.pack('>I', len(compressed)))
    png.extend(b'IDAT')
    png.extend(compressed)
    png.extend(struct.pack('>I', zlib.crc32(b'IDAT' + compressed) & 0xffffffff))
    
    # IEND
    png.extend(struct.pack('>I', 0))
    png.extend(b'IEND')
    png.extend(struct.pack('>I', zlib.crc32(b'IEND') & 0xffffffff))
    
    with open(path, 'wb') as f:
        f.write(png)

make_png(192, 192, r'C:\Users\kwonf\.gemini\antigravity\scratch\quick-quote\icon-192.png')
make_png(512, 512, r'C:\Users\kwonf\.gemini\antigravity\scratch\quick-quote\icon-512.png')
print('Icons generated successfully!')
