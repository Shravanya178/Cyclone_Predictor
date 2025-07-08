from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from backend.utils.predict_mask import load_model, predict_mask
from backend.utils.generate_overlay import create_overlay
from backend.utils.risk_score import calculate_risk
from backend.utils.metrics import (
    compute_area,
    compute_temperature,
    generate_explanation,
)
import os
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "backend/static"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = load_model("model/unet_insat.pt")

@app.route("/predict", methods=["POST"])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    filename = f"{uuid.uuid4().hex}.png"
    img_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(img_path)

    # Predict segmentation mask
    mask_img = predict_mask(model, img_path)
    mask_path = os.path.join(UPLOAD_FOLDER, f"mask_{filename}")
    mask_img.save(mask_path)

    # Generate overlay
    overlay_path = os.path.join(UPLOAD_FOLDER, f"overlay_{filename}")
    create_overlay(img_path, mask_path, overlay_path)

    # Risk Level and Coverage (% of image masked)
    risk_level, coverage = calculate_risk(mask_path)

    # Advanced Metrics
    temperature = float(round(compute_temperature(img_path), 1))      # °C (approx)
    area_km2 = float(round(compute_area(mask_path), 2))               # Area in km²
    confidence = min(100, round(float(coverage) * 2.5))               # Scaled confidence
    explanation = generate_explanation(risk_level, coverage, temperature)

    return jsonify({
        "risk": str(risk_level),
        "coverage": float(round(coverage, 2)),
        "temperature": temperature,
        "cluster_area": area_km2,
        "confidence": int(confidence),
        "explanation": explanation,
        "overlay_url": f"/static/overlay_{filename}",
        "input_url": f"/static/{filename}"
    })

@app.route("/static/<path:filename>")
def serve_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename))

if __name__ == "__main__":
    app.run(debug=True)
