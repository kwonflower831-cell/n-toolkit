import struct
import zlib

def make_png(width, height, path):
    raw = bytearray()
    r_bg, g_bg, b_bg = 234, 88, 12 # #ea580c (Warm Store Orange)
    
    for y in range(height):
        row = bytearray([0])
        for x in range(width):
            corner_radius = width // 5
            in_shape = True
            
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
                
            # Storefront shape (roof & pillars)
            # Roof: triangle/trapezoid from y: 0.22 to 0.42
            roof_top = height * 0.22
            roof_bottom = height * 0.42
            is_roof = False
            if roof_top <= y <= roof_bottom:
                progress = (y - roof_top) / (roof_bottom - roof_top)
                left_edge = width * (0.40 - progress * 0.18)
                right_edge = width * (0.60 + progress * 0.18)
                if left_edge <= x <= right_edge:
                    is_roof = True
                    
            # Pillars & Base: y: 0.42 to 0.76
            body_top = height * 0.42
            body_bottom = height * 0.76
            body_left = width * 0.26
            body_right = width * 0.74
            is_body = False
            if body_top <= y <= body_bottom and body_left <= x <= body_right:
                # Door cut in middle
                door_left = width * 0.42
                door_right = width * 0.58
                door_top = height * 0.52
                if door_left <= x <= door_right and y >= door_top:
                    is_body = False
                else:
                    is_body = True
                    
            # Star/Sparkle accent on top right (x: 0.72-0.85, y: 0.20-0.35)
            cx, cy = width * 0.76, height * 0.26
            dist_sq = (x - cx)**2 + (y - cy)**2
            is_sparkle = (abs(x - cx) <= width*0.03 and abs(y - cy) <= height*0.09) or (abs(x - cx) <= width*0.09 and abs(y - cy) <= height*0.03)
            
            if is_roof or is_body or is_sparkle:
                row.extend([255, 255, 255, 255])
            else:
                row.extend([r_bg, g_bg, b_bg, 255])
                
        raw.extend(row)
        
    compressed = zlib.compress(bytes(raw), 9)
    png = bytearray(b'\x89PNG\r\n\x1a\n')
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    png.extend(struct.pack('>I', 13))
    png.extend(b'IHDR')
    png.extend(ihdr_data)
    png.extend(struct.pack('>I', zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff))
    png.extend(struct.pack('>I', len(compressed)))
    png.extend(b'IDAT')
    png.extend(compressed)
    png.extend(struct.pack('>I', zlib.crc32(b'IDAT' + compressed) & 0xffffffff))
    png.extend(struct.pack('>I', 0))
    png.extend(b'IEND')
    png.extend(struct.pack('>I', zlib.crc32(b'IEND') & 0xffffffff))
    
    with open(path, 'wb') as f:
        f.write(png)

make_png(192, 192, r'C:\Users\kwonf\.gemini\antigravity\scratch\boss-ai\icon-192.png')
make_png(512, 512, r'C:\Users\kwonf\.gemini\antigravity\scratch\boss-ai\icon-512.png')
print('BossAI icons created successfully!')
