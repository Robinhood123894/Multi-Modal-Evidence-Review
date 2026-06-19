import pandas as pd
import os
import logging

from claim_parser import parse_claim
from vision import analyze_images
from evidence_checker import check_evidence
from risk_engine import get_risk_flags
from decision_engine import decide_claim
# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("Main module loaded")

def process_claim(row, user_history_df, evidence_df):
    user_id = row["user_id"]
    image_paths = row["image_paths"]
    user_claim = row["user_claim"]
    claim_object = row["claim_object"]

    # Extract claim details
    claim_info = parse_claim(user_claim)

    # If object_part is still unknown, use claim_object as fallback
    if claim_info["object_part"] == "unknown" and claim_object:
        claim_info["object_part"] = claim_object

    # Analyze images (use first image)
    if image_paths and isinstance(image_paths, str):
        first_image = image_paths.split(";")[0].strip() if ";" in image_paths else image_paths.strip()
    else:
        first_image = ""

    vision_result = {
        "issue_type": "unknown",
        "object_part": "unknown",
        "severity": "unknown",
        "valid_image": False,
        "supporting_image_ids": []
    }
    
    if first_image and os.path.exists(first_image):
        try:
            vision_result = analyze_images(first_image, claim_object)
            logger.info(f"Analyzed image: {first_image}")
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
    else:
        # If no image exists, use claim_info as fallback
        vision_result = {
            "issue_type": claim_info["issue_type"],
            "object_part": claim_info["object_part"],
            "severity": "medium",
            "valid_image": False,
            "supporting_image_ids": []
        }
        logger.warning(f"No valid image found for {user_id}")

    # Check evidence requirements
    evidence_result = check_evidence(
        claim_object,
        claim_info,
        vision_result,
        evidence_df
    )

    # Get user history
    if not user_history_df.empty:
        user_history = user_history_df[user_history_df["user_id"] == user_id]
    else:
        user_history = pd.DataFrame()

    # Generate risk flags
    risk_flags = get_risk_flags(vision_result, user_history)

    # Final decision
    decision = decide_claim(
        claim_info,
        vision_result,
        evidence_result
    )

    return {
        "user_id": user_id,
        "image_paths": image_paths,
        "user_claim": user_claim,
        "claim_object": claim_object,
        "evidence_standard_met": evidence_result["evidence_standard_met"],
        "evidence_standard_met_reason": evidence_result["reason"],
        "risk_flags": ";".join(risk_flags) if risk_flags else "none",
        "issue_type": vision_result["issue_type"],
        "object_part": vision_result["object_part"],
        "claim_status": decision["claim_status"],
        "claim_status_justification": decision["justification"],
        "supporting_image_ids": ";".join(vision_result.get("supporting_image_ids", [])) if vision_result.get("supporting_image_ids") else "none",
        "valid_image": vision_result.get("valid_image", False),
        "severity": vision_result.get("severity", "unknown")
    }


def main():
    print("\n" + "="*60)
    print("🚀 Starting Claim Processing System")
    print("="*60 + "\n")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"📁 Current directory: {current_dir}")
    
    # Check what files exist
    print("\n📄 Files in current directory:")
    for file in os.listdir(current_dir):
        if file.endswith('.csv'):
            print(f"   - {file}")
    print()
    
    # Read CSV files from current directory (not dataset folder)
    try:
        claims_df = pd.read_csv("claims.csv")
        print(f"✅ Loaded {len(claims_df)} claims from claims.csv")
    except FileNotFoundError:
        print("❌ claims.csv not found in current directory!")
        print(f"   Looking for: {os.path.join(current_dir, 'claims.csv')}")
        return
    except Exception as e:
        print(f"❌ Error reading claims.csv: {e}")
        return

    try:
        user_history_df = pd.read_csv("user_history.csv")
        print(f"✅ Loaded {len(user_history_df)} user history records")
    except FileNotFoundError:
        print("⚠️  user_history.csv not found, using empty history")
        user_history_df = pd.DataFrame()
    except Exception as e:
        print(f"⚠️  Error reading user_history.csv: {e}")
        user_history_df = pd.DataFrame()

    try:
        evidence_df = pd.read_csv("evidence_requirements.csv")
        print(f"✅ Loaded {len(evidence_df)} evidence requirements")
    except FileNotFoundError:
        print("⚠️  evidence_requirements.csv not found")
        evidence_df = pd.DataFrame()
    except Exception as e:
        print(f"⚠️  Error reading evidence_requirements.csv: {e}")
        evidence_df = pd.DataFrame()

    print("\n" + "-"*60)
    print("Processing claims...")
    print("-"*60 + "\n")

    results = []
    errors = 0
    successful = 0

    for index, row in claims_df.iterrows():
        try:
            result = process_claim(row, user_history_df, evidence_df)
            results.append(result)
            successful += 1
            
            # Print progress
            if (index + 1) % 10 == 0 or (index + 1) == len(claims_df):
                print(f"📊 Processed {index + 1}/{len(claims_df)} claims...")
                
        except Exception as e:
            errors += 1
            print(f"❌ Error processing claim {index} (User: {row.get('user_id', 'unknown')}): {e}")
            # Add error row
            results.append({
                "user_id": row.get("user_id", "unknown"),
                "image_paths": row.get("image_paths", ""),
                "user_claim": row.get("user_claim", ""),
                "claim_object": row.get("claim_object", "unknown"),
                "evidence_standard_met": False,
                "evidence_standard_met_reason": f"Error: {str(e)}",
                "risk_flags": "error",
                "issue_type": "unknown",
                "object_part": "unknown",
                "claim_status": "error",
                "claim_status_justification": f"Processing error: {str(e)}",
                "supporting_image_ids": "none",
                "valid_image": False,
                "severity": "unknown"
            })

    # Save results to CSV
    print("\n" + "-"*60)
    print("Saving results...")
    print("-"*60 + "\n")
    
    output_df = pd.DataFrame(results)
    
    # Ensure all required columns are present
    required_columns = [
        "user_id", "image_paths", "user_claim", "claim_object",
        "evidence_standard_met", "evidence_standard_met_reason",
        "risk_flags", "issue_type", "object_part",
        "claim_status", "claim_status_justification",
        "supporting_image_ids", "valid_image", "severity"
    ]
    
    # Add missing columns with default values
    for col in required_columns:
        if col not in output_df.columns:
            output_df[col] = "unknown"
    
    # Reorder columns to match expected schema
    output_df = output_df[required_columns]
    
    # Save to CSV
    output_df.to_csv("output.csv", index=False)
    
    # Print summary
    print("\n" + "="*60)
    print("📊 PROCESSING COMPLETE")
    print("="*60)
    print(f"✅ Total claims processed: {len(results)}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Errors: {errors}")
    print(f"📁 Output saved to: output.csv")
    print("="*60 + "\n")
    
    # Show first few rows of output
    print("Sample output (first 3 rows):")
    print("-"*60)
    print(output_df.head(3).to_string())
    print("-"*60 + "\n")
    # After saving output.csv
print("\n📊 Output CSV Summary:")
print("-"*60)
output_df = pd.read_csv("output.csv")
print(f"Total rows: {len(output_df)}")
print(f"Columns: {list(output_df.columns)}")
print("\nClaim Status Distribution:")
print(output_df['claim_status'].value_counts())
print("\nRisk Flags Distribution:")
print(output_df['risk_flags'].value_counts())
print("\nSample Data:")
print(output_df.head(5).to_string())


if __name__ == "__main__":
    main()