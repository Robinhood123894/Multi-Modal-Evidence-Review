from google import genai
from PIL import Image
import json
import os
import random

print("vision loaded")

# ============================================================
# ⚠️  IMPORTANT: Insert your Gemini API key below
# ============================================================
# Get your API key from: https://aistudio.google.com/
# ============================================================

API_KEY = "YOUR_GEMINI_API_KEY_HERE"  # Replace with your actual API key

# Check if API key is set
if API_KEY == "YOUR_GEMINI_API_KEY_HERE":
    print("\n" + "="*70)
    print("⚠️  WARNING: Using simulated image analysis")
    print("   Insert your Gemini API key in vision.py for real analysis")
    print("   Get it from: https://aistudio.google.com/")
    print("="*70 + "\n")
    client = None
else:
    try:
        client = genai.Client(api_key=API_KEY)
        print("✅ Gemini client initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize Gemini: {e}")
        client = None

def analyze_images(image_path, claim_object):
    """
    Analyze image using Gemini Vision API or fallback to simulation
    """
    # Check if client is available
    if client is None:
        print(f"⚠️  Using simulated analysis for: {image_path}")
        return simulate_analysis(claim_object)
    
    try:
        # Check if image exists
        if not os.path.exists(image_path):
            print(f"ERROR: Image not found: {image_path}")
            return simulate_analysis(claim_object)
        
        img = Image.open(image_path)
        
        prompt = f"""
Analyze this {claim_object} damage image.

Return ONLY valid JSON.

{{
"issue_type": "unknown",
"object_part": "unknown",
"severity": "unknown",
"valid_image": true
}}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, img]
        )
        print("RAW RESPONSE:")
        print(response.text)

        text = response.text.strip()
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        data = json.loads(text)

        return {
            "issue_type": data.get("issue_type", "unknown"),
            "object_part": data.get("object_part", "unknown"),
            "severity": data.get("severity", "unknown"),
            "valid_image": data.get("valid_image", True),
            "supporting_image_ids": ["img_1"]
        }
    except Exception as e:
        print(f"ERROR analyzing image: {e}")
        return simulate_analysis(claim_object)

def simulate_analysis(claim_object):
    """
    Simulate image analysis when no real images or API key are available
    """
    # Generate realistic results based on claim_object
    if claim_object == "car":
        issues = ["scratch", "dent", "crack", "broken_part", "missing_part"]
        parts = ["front_bumper", "rear_bumper", "door", "hood", "windshield", 
                "side_mirror", "headlight", "taillight"]
        severities = ["low", "medium", "high"]
    elif claim_object == "laptop":
        issues = ["scratch", "dent", "crack", "broken_part", "missing_part", 
                 "water_damage", "stain"]
        parts = ["screen", "keyboard", "trackpad", "hinge", "lid", "body"]
        severities = ["low", "medium", "high"]
    else:  # package
        issues = ["crushed", "torn", "water_damage", "stain", "missing_part"]
        parts = ["box", "seal", "label", "package"]
        severities = ["low", "medium", "high"]
    
    # Generate random but realistic results
    issue_type = random.choice(issues)
    object_part = random.choice(parts)
    severity = random.choice(severities)
    
    print(f"🔍 Simulated: {issue_type} on {object_part} (severity: {severity})")
    
    return {
        "issue_type": issue_type,
        "object_part": object_part,
        "severity": severity,
        "valid_image": True,
        "supporting_image_ids": ["simulated_1"]
    }