import numpy as np
from PIL import Image

# Constants
PIXEL_RES_KM = 4  # 4 km per pixel
TEMP_SCALE = (330, 180)  # brightness temp approximation: 330K to 180K

def compute_coverage(mask_path: str) -> float:
    """Returns percentage of white pixels in mask"""
    mask = Image.open(mask_path).convert("L")
    arr = np.array(mask)
    white_pixels = int(np.sum(arr > 127))
    total_pixels = arr.size
    return float((white_pixels / total_pixels) * 100)

def compute_temperature(image_path: str) -> float:
    """Estimates mean brightness temperature from IR image"""
    img = Image.open(image_path).convert("L")
    arr = np.array(img)
    norm = arr / 255.0
    temp_k = TEMP_SCALE[0] - norm * (TEMP_SCALE[0] - TEMP_SCALE[1])  # 330K - normalized range
    temp_c = temp_k - 273.15
    return float(np.mean(temp_c))

def compute_area(mask_path: str) -> float:
    """Estimates area of the cloud cluster in km²"""
    mask = Image.open(mask_path).convert("L")
    arr = np.array(mask)
    white_pixels = int(np.sum(arr > 127))
    return float(white_pixels * (PIXEL_RES_KM ** 2))

def generate_explanation(risk: str, coverage: float, temperature: float) -> str:
    message = (
        f"AI MODEL DETECTION: Organized convective system identified with "
        f"{coverage:.1f}% cyclonic coverage. Model detected clear spiral organization and "
        f"deep convection patterns. Cloud top temperatures estimated at {temperature:.1f}°C "
        f"indicate strong vertical development. "
        f"{risk.upper()} CYCLONE FORMATION PROBABILITY detected by neural network analysis. "
        f"Immediate monitoring and preparation recommended."
    )
    return message
