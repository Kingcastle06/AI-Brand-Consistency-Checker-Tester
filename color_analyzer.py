import math
from typing import List, Tuple, Dict
from PIL import Image
import numpy as np

def hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_xyz(r: int, g: int, b: int) -> Tuple[float, float, float]:
    s_r, s_g, s_b = r / 255.0, g / 255.0, b / 255.0
    s_r = math.pow((s_r + 0.055) / 1.055, 2.4) if s_r > 0.04045 else s_r / 12.92
    s_g = math.pow((s_g + 0.055) / 1.055, 2.4) if s_g > 0.04045 else s_g / 12.92
    s_b = math.pow((s_b + 0.055) / 1.055, 2.4) if s_b > 0.04045 else s_b / 12.92
    s_r, s_g, s_b = s_r * 100, s_g * 100, s_b * 100
    x = s_r * 0.4124 + s_g * 0.3576 + s_b * 0.1805
    y = s_r * 0.2126 + s_g * 0.7152 + s_b * 0.0722
    z = s_r * 0.0193 + s_g * 0.1192 + s_b * 0.9505
    return x, y, z

def xyz_to_lab(x: float, y: float, z: float) -> Tuple[float, float, float]:
    ref_x, ref_y, ref_z = 95.047, 100.000, 108.883
    x_ratio, y_ratio, z_ratio = x / ref_x, y / ref_y, z / ref_z
    f_x = math.pow(x_ratio, 1/3) if x_ratio > 0.008856 else (7.787 * x_ratio) + (16 / 116)
    f_y = math.pow(y_ratio, 1/3) if y_ratio > 0.008856 else (7.787 * y_ratio) + (16 / 116)
    f_z = math.pow(z_ratio, 1/3) if z_ratio > 0.008856 else (7.787 * z_ratio) + (16 / 116)
    l = (116 * f_y) - 16
    a = 500 * (f_x - f_y)
    b = 200 * (f_y - f_z)
    return l, a, b

def rgb_to_lab(r: int, g: int, b: int) -> Tuple[float, float, float]:
    x, y, z = rgb_to_xyz(r, g, b)
    return xyz_to_lab(x, y, z)

def calculate_delta_e(lab1: Tuple[float, float, float], lab2: Tuple[float, float, float]) -> float:
    return math.sqrt(math.pow(lab1[0] - lab2[0], 2) + math.pow(lab1[1] - lab2[1], 2) + math.pow(lab1[2] - lab2[2], 2))

def extract_dominant_colors(image_path: str, max_colors: int = 5) -> List[Tuple[int, int, int]]:
    with Image.open(image_path) as img:
        img = img.convert("RGB").resize((100, 100))
        pixels = np.array(img.getdata())
        unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
        sorted_indices = np.argsort(-counts)
        dominant_rgbs = unique_colors[sorted_indices][:max_colors]
        return [tuple(map(int, color)) for color in dominant_rgbs]

# 🔍 Ensure this exact function matches your main.py import statement!
def audit_image_colors(image_path: str, brand_hex_palette: List[str], threshold: float = 10.0) -> List[Dict]:
    detected_rgbs = extract_dominant_colors(image_path)
    brand_labs = [rgb_to_lab(*hex_to_rgb(hx)) for hx in brand_hex_palette]
    violations = []
    
    for rgb in detected_rgbs:
        detected_lab = rgb_to_lab(*rgb)
        detected_hex = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        distances = [calculate_delta_e(detected_lab, brand_lab) for brand_lab in brand_labs]
        min_distance = min(distances) if distances else 999.0
        
        if min_distance > threshold:
            violations.append({
                "detected_hex": detected_hex,
                "detected_rgb": rgb,
                "perceptual_distance_delta": round(min_distance, 2),
                "status": "Violated",
                "summary": f"Color center {detected_hex} is visibly off-brand by a perceptual margin of {round(min_distance, 2)}."
            })
    return violations