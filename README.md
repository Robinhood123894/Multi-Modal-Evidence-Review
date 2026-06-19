# Multi-Modal-Evidence-Review
Multi-Modal Evidence Review System for processing damage claims using text parsing, image analysis (Google Gemini), and risk assessment. Handles car, laptop, and package claims.


# Multi-Modal Evidence Review System

## 📋 Overview

A claim processing system that verifies damage claims using multi-modal evidence analysis. The system processes claims for **cars**, **laptops**, and **packages** using text parsing, image analysis, user history, and evidence requirements.

## 🎯 Features

- **Text Claim Parsing**: Extracts damage type and affected part from conversation
- **Image Analysis**: Google Gemini Vision API (with simulation fallback)
- **Evidence Verification**: Checks if evidence meets minimum requirements
- **Risk Assessment**: Identifies risk flags from user history
- **Decision Making**: Supported/Contradicted/Insufficient
- **Structured Output**: CSV format

## 🏗️ Architecture
Input CSV Files → main.py →
├── claim_parser.py (Text parsing)
├── vision.py (Image analysis)
├── evidence_checker.py (Evidence verification)
├── risk_engine.py (Risk assessment)
└── decision_engine.py (Decision making)
→ output.csv (Final results)


## 📁 Project Structure
project/
├── main.py # Main orchestrator
├── claim_parser.py # Text claim parsing
├── vision.py # Image analysis (Gemini API)
├── evidence_checker.py # Evidence verification
├── risk_engine.py # Risk assessment
├── decision_engine.py # Decision making
├── README.md # This file
│
├── dataset/
│ ├── claims.csv # Input claims
│ ├── user_history.csv # User history
│ └── evidence_requirements.csv # Evidence rules
│
└── images/ # Claim images (optional)


## 🔧 Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Install Dependencies
```bash
pip install pandas pillow google-generativeai


API Key Setup (Optional)
To use real image analysis with Google Gemini:

Get API key from Google AI Studio

Add to vision.py:

python
API_KEY = "YOUR_GEMINI_API_KEY_HERE"
Note: System works without API key using simulated analysis.

🚀 Usage
Quick Start
bash
# Run the system
python main.py

# Check output
cat output.csv

Input Files Required
File	Description
claims.csv	Claim data with user_id, image_paths, user_claim, claim_object
user_history.csv	User history with risk flags
evidence_requirements.csv	Evidence rules per object type

Output Format
output.csv contains:

user_id: User identifier

issue_type: Damage type (scratch, dent, crack, etc.)

object_part: Affected part (front_bumper, door, screen, etc.)

claim_status: supported/contradicted/not_enough_information

risk_flags: Risk indicators from history

severity: low/medium/high

evidence_standard_met: True/False

claim_status_justification: Decision reason

🔄 Processing Workflow
Parse Claim: Extract issue_type and object_part from text

Analyze Images: Process using Gemini Vision or simulation

Check Evidence: Verify against evidence requirements

Assess Risk: Flag based on user history

Make Decision: Supported/Contradicted/Insufficient

Generate Output: Create structured CSV

Supported Object Parts
Cars
front_bumper, rear_bumper, door, hood, windshield

side_mirror, headlight, taillight

Laptops
screen, keyboard, trackpad, hinge, lid, body

Packages
box, seal, label, package

🧪 Testing

# test_system.py
import pandas as pd
from main import process_claim

# Test single claim
row = {
    "user_id": "test_user",
    "image_paths": "test.jpg",
    "user_claim": "Front bumper has a scratch",
    "claim_object": "car"
}
result = process_claim(row, pd.DataFrame(), pd.DataFrame())
print(result)

**Example Output***

user_id | issue_type | object_part | claim_status | severity
--------|------------|-------------|--------------|----------
user_002| dent       | front_bumper| supported    | medium
user_005| scratch    | door        | contradicted | low
user_004| crack      | windshield  | supported    | high
