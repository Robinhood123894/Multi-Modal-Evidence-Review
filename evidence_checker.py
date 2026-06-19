print("evidence_checker loaded")

def check_evidence(claim_object, claim_info, vision_result, evidence_df):
    """
    Check if evidence meets minimum requirements
    """
    # Check if we have a valid image
    if not vision_result.get("valid_image", False):
        return {
            "evidence_standard_met": False,
            "reason": "No valid image available for review"
        }
    
    claim_issue = claim_info.get("issue_type", "unknown")
    claim_part = claim_info.get("object_part", "unknown")
    vision_issue = vision_result.get("issue_type", "unknown")
    vision_part = vision_result.get("object_part", "unknown")
    
    # If vision detected something
    if vision_issue != "unknown" or vision_part != "unknown":
        # Check if claim matches vision (at least partially)
        if claim_issue == vision_issue or claim_part == vision_part:
            return {
                "evidence_standard_met": True,
                "reason": f"Evidence supports claim: {vision_issue} on {vision_part}"
            }
        else:
            return {
                "evidence_standard_met": False,
                "reason": f"Claimed {claim_issue} on {claim_part}, evidence shows {vision_issue} on {vision_part}"
            }
    else:
        return {
            "evidence_standard_met": False,
            "reason": "Could not identify damage in images"
        }