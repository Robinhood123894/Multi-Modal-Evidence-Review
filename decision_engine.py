print("decision_engine loaded")

def decide_claim(claim_info, vision_result, evidence_result):
    """
    Make final claim decision
    """
    claim_issue = claim_info.get("issue_type", "unknown")
    claim_part = claim_info.get("object_part", "unknown")
    
    vision_issue = vision_result.get("issue_type", "unknown")
    vision_part = vision_result.get("object_part", "unknown")
    valid_image = vision_result.get("valid_image", False)
    severity = vision_result.get("severity", "unknown")
    
    # Check if evidence standard is met
    if not evidence_result.get("evidence_standard_met", False):
        return {
            "claim_status": "not_enough_information",
            "justification": evidence_result.get("reason", "Insufficient evidence")
        }
    
    # If no valid image
    if not valid_image:
        return {
            "claim_status": "not_enough_information",
            "justification": "No valid image available"
        }
    
    # If vision couldn't detect anything
    if vision_issue == "unknown" and vision_part == "unknown":
        return {
            "claim_status": "not_enough_information",
            "justification": "Could not determine damage from images"
        }
    
    # Check if claim matches vision
    issue_match = (claim_issue == vision_issue or claim_issue == "unknown" or vision_issue == "unknown")
    part_match = (claim_part == vision_part or claim_part == "unknown" or vision_part == "unknown")
    
    if issue_match and part_match:
        return {
            "claim_status": "supported",
            "justification": f"Image evidence matches claim: {vision_issue} on {vision_part}"
        }
    elif issue_match and not part_match:
        return {
            "claim_status": "contradicted",
            "justification": f"Part mismatch: claimed {claim_part}, image shows {vision_part}"
        }
    elif not issue_match and part_match:
        return {
            "claim_status": "contradicted",
            "justification": f"Issue mismatch: claimed {claim_issue}, image shows {vision_issue}"
        }
    else:
        return {
            "claim_status": "contradicted",
            "justification": f"Evidence contradicts claim: image shows {vision_issue} on {vision_part}"
        }